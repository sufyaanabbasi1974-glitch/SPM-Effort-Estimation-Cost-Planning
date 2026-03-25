"""
Flask application for SPM Effort Estimation System
Implements API endpoints for all modules
"""
import os
from functools import wraps
from flask import Flask, render_template, request, jsonify, send_from_directory, session, redirect, url_for
from flask_cors import CORS
from dotenv import load_dotenv
from models import db, Project, Estimation, Risk, EVMTracking
from cocomo_calculator import COCOMOCalculator
from evm_calculator import EVMCalculator
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Load environment variables
load_dotenv()

# Get project root directory
project_root = os.path.dirname(os.path.dirname(__file__))
frontend_dir = os.path.join(project_root, 'frontend')

# Initialize Flask app with custom template and static folders
app = Flask(__name__, 
            template_folder=frontend_dir,
            static_folder=frontend_dir,
            static_url_path='/assets')

# Database configuration - Support both SQLite (dev) and PostgreSQL (prod)
database_url = os.getenv('DATABASE_URL')
flask_env = os.getenv('FLASK_ENV', 'development')

# Enable CORS - Restrict in production
cors_origins = os.getenv('CORS_ORIGINS', 'http://localhost:5000').split(',')
if flask_env == 'production':
    CORS(app, resources={r"/api/*": {"origins": cors_origins}})
else:
    CORS(app)

if database_url:
    # Production: Use PostgreSQL from Supabase
    # Fix Supabase URL: postgres:// -> postgresql://
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'connect_args': {
            'sslmode': 'require'
        },
        'pool_size': 10,
        'pool_recycle': 3600,
        'pool_pre_ping': True
    }
else:
    # Development: Use SQLite
    db_dir = os.path.join(project_root, 'database')
    os.makedirs(db_dir, exist_ok=True)
    db_path = os.path.join(db_dir, 'spm_estimation.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'connect_args': {
            'timeout': 30
        }
    }

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Load secret key from environment or fail in production
secret_key = os.getenv('SECRET_KEY')
if not secret_key and flask_env == 'production':
    raise RuntimeError("CRITICAL: SECRET_KEY not set in production environment!")
app.config['SECRET_KEY'] = secret_key or 'dev-secret-key-spm-2024'

app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = 86400  # 24 hours

# Security Headers & Session Security
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
if flask_env == 'production':
    app.config['SESSION_COOKIE_SECURE'] = True  # Only send over HTTPS in production

# Add security headers to every response
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    # More strict CSP could be added here if needed
    return response

# Initialize database
db.init_app(app)

# Create database tables
with app.app_context():
    db.create_all()


# ==================== AUTHENTICATION ====================

# Demo users - Passwords are hashed for security
# admin: password
# user: user123
VALID_USERS_HASHED = {
    'admin': 'scrypt:32768:8:1$zyRdlDrqLcWh7Opl$fd972986a380f605d72e80048a9d87c3fa829527693bf9b10752187b70a1492342d1785b30b0125f4d81e7284e55fb20cea6949d5275f4d709717f849eb0ffaa',
    'user': 'scrypt:32768:8:1$k13AUBE65vSdgM7k$58e424f779e077e6b18fcf8df23d2a5356eac0a2dbf9067f1889e68b5b8e884c8a425ac4e4a546c314b2b4ac05ba93851136d2c0e0e44f90842b2349882bfece'
}

@app.route('/')
def index():
    """Root route - redirect to login or home"""
    if 'user_id' in session:
        return redirect('/home')
    return redirect('/login')

def login_required(f):
    """Decorator to require login for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login')
def login():
    """Serve login page"""
    if 'user_id' in session:
        return redirect('/home')
    return render_template('login.html')

@app.route('/api/login', methods=['POST'])
def api_login():
    """Handle login request"""
    try:
        data = request.json
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        # Validate credentials using hashed passwords
        user_hash = VALID_USERS_HASHED.get(username)
        if user_hash and check_password_hash(user_hash, password):
            session['user_id'] = username
            session['username'] = username
            session.permanent = True
            return jsonify({
                'success': True,
                'message': 'Login successful',
                'user': username
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Invalid username or password'
            }), 401
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/logout')
def logout():
    """Handle logout"""
    session.clear()
    return redirect('/login')

@app.route('/home')
@login_required
def home():
    """Serve home page (main dashboard)"""
    return render_template('index.html')

@app.route('/api/user')
def get_user():
    """Get current user info"""
    if 'user_id' not in session:
        return jsonify({'user': None}), 401
    return jsonify({
        'user': session.get('username'),
        'user_id': session.get('user_id')
    }), 200

@app.route('/api/clear-all-data', methods=['POST'])
def clear_all_data():
    """Clear all data from the database"""
    try:
        # Delete all records from all tables
        db.session.query(EVMTracking).delete()
        db.session.query(Risk).delete()
        db.session.query(Estimation).delete()
        db.session.query(Project).delete()
        
        # Commit changes
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'All data has been cleared successfully'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ==================== STATIC FILES ====================

@app.route('/css/<path:filename>')
def serve_css(filename):
    """Serve CSS files from frontend/css directory"""
    css_dir = os.path.join(frontend_dir, 'css')
    return send_from_directory(css_dir, filename)

@app.route('/js/<path:filename>')
def serve_js(filename):
    """Serve JavaScript files from frontend/js directory"""
    js_dir = os.path.join(frontend_dir, 'js')
    return send_from_directory(js_dir, filename)

@app.route('/assets/<path:filename>')
def serve_assets(filename):
    """Serve asset files from frontend/assets directory"""
    assets_dir = os.path.join(frontend_dir, 'assets')
    return send_from_directory(assets_dir, filename)


# ==================== PROJECT MODULE ENDPOINTS ====================

# ==================== PROJECT MODULE ENDPOINTS ====================

@app.route('/api/projects', methods=['POST'])
def create_project():
    """Create a new project"""
    try:
        data = request.json
        
        # Validate required fields
        required_fields = ['project_name', 'project_type', 'kloc', 'cost_per_person_month', 'team_experience']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            error_msg = f'Missing required fields: {", ".join(missing_fields)}'
            print(f"Validation error: {error_msg}")
            return jsonify({'error': error_msg}), 400
        
        print(f"Creating project with data: {data}")
        
        # Create project
        project = Project(
            project_name=data['project_name'],
            project_type=data['project_type'],
            kloc=float(data['kloc']),
            cost_per_person_month=float(data['cost_per_person_month']),
            team_experience=data['team_experience']
        )
        
        db.session.add(project)
        db.session.commit()
        
        print(f"Project created successfully with ID: {project.id}")
        return jsonify({
            'success': True,
            'project_id': project.id,
            'message': 'Project created successfully'
        }), 201
    
    except ValueError as ve:
        error_msg = f'Invalid value: {str(ve)}'
        print(f"ValueError creating project: {error_msg}")
        db.session.rollback()
        return jsonify({'error': error_msg}), 400
    except Exception as e:
        error_msg = f'Error creating project: {str(e)}'
        print(error_msg)
        import traceback
        traceback.print_exc()
        db.session.rollback()
        return jsonify({'error': error_msg}), 500


@app.route('/api/projects/<int:project_id>', methods=['GET'])
def get_project(project_id):
    """Retrieve project details"""
    try:
        project = Project.query.get(project_id)
        if not project:
            return jsonify({'error': 'Project not found'}), 404
        
        return jsonify({
            'id': project.id,
            'project_name': project.project_name,
            'project_type': project.project_type,
            'kloc': project.kloc,
            'cost_per_person_month': project.cost_per_person_month,
            'team_experience': project.team_experience
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/projects', methods=['GET'])
def list_projects():
    """List all projects"""
    try:
        projects = Project.query.all()
        return jsonify([{
            'id': p.id,
            'project_name': p.project_name,
            'project_type': p.project_type,
            'kloc': p.kloc,
            'created_date': p.created_date.isoformat()
        } for p in projects]), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== EFFORT ESTIMATION ENDPOINTS ====================

@app.route('/api/estimations/basic-cocomo/<int:project_id>', methods=['POST'])
def calculate_basic_cocomo(project_id):
    """Calculate Basic COCOMO estimation"""
    try:
        project = Project.query.get(project_id)
        if not project:
            return jsonify({'error': 'Project not found'}), 404
        
        # Calculate Basic COCOMO
        cocomo_result = COCOMOCalculator.calculate_basic_cocomo(project.kloc, project.project_type)
        
        # Calculate costs
        cost_result = COCOMOCalculator.calculate_costs(cocomo_result['effort'], project.cost_per_person_month)
        
        # Save or update estimation
        estimation = Estimation.query.filter_by(project_id=project_id).first()
        if not estimation:
            estimation = Estimation(project_id=project_id)
        
        estimation.basic_effort = cocomo_result['effort']
        estimation.basic_duration = cocomo_result['duration']
        estimation.basic_cost = cost_result['total_cost']
        estimation.selected_model = 'Basic'
        estimation.final_effort = cocomo_result['effort']
        estimation.final_cost = cost_result['total_cost']
        
        db.session.add(estimation)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'model': 'Basic COCOMO',
            'effort_person_months': cocomo_result['effort'],
            'duration_months': cocomo_result['duration'],
            'total_cost': cost_result['total_cost'],
            'cost_per_phase': cost_result['cost_per_phase'],
            'estimation_id': estimation.id
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/estimations/intermediate-cocomo/<int:project_id>', methods=['POST'])
def calculate_intermediate_cocomo(project_id):
    """Calculate Intermediate COCOMO estimation with effort multipliers"""
    try:
        project = Project.query.get(project_id)
        if not project:
            return jsonify({'error': 'Project not found'}), 404
        
        data = request.json or {}
        
        # Calculate Intermediate COCOMO
        cocomo_result = COCOMOCalculator.calculate_intermediate_cocomo(
            project.kloc,
            project.project_type,
            project.team_experience,
            data.get('multipliers')
        )
        
        # Calculate costs with adjusted effort
        cost_result = COCOMOCalculator.calculate_costs(cocomo_result['effort'], project.cost_per_person_month)
        
        # Save or update estimation
        estimation = Estimation.query.filter_by(project_id=project_id).first()
        if not estimation:
            estimation = Estimation(project_id=project_id)
        
        estimation.intermediate_effort = cocomo_result['effort']
        estimation.intermediate_duration = cocomo_result['duration']
        estimation.intermediate_cost = cost_result['total_cost']
        estimation.selected_model = 'Intermediate'
        estimation.final_effort = cocomo_result['effort']
        estimation.final_cost = cost_result['total_cost']
        
        db.session.add(estimation)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'model': 'Intermediate COCOMO',
            'base_effort': cocomo_result['base_effort'],
            'effort_person_months': cocomo_result['effort'],
            'multiplier_impact': cocomo_result['multiplier_impact'],
            'duration_months': cocomo_result['duration'],
            'total_cost': cost_result['total_cost'],
            'cost_per_phase': cost_result['cost_per_phase'],
            'estimation_id': estimation.id
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ==================== RISK MANAGEMENT ENDPOINTS ====================

@app.route('/api/risks/<int:project_id>', methods=['POST'])
def add_risk(project_id):
    """Add a risk to a project"""
    try:
        project = Project.query.get(project_id)
        if not project:
            return jsonify({'error': 'Project not found'}), 404
        
        data = request.json
        required_fields = ['risk_name', 'risk_category', 'probability', 'impact', 'adjustment_factor']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        risk = Risk(
            project_id=project_id,
            risk_name=data['risk_name'],
            risk_category=data['risk_category'],
            probability=float(data['probability']),
            impact=float(data['impact']),
            adjustment_factor=float(data['adjustment_factor']),
            description=data.get('description', '')
        )
        
        db.session.add(risk)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'risk_id': risk.id,
            'message': 'Risk added successfully'
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/risks/<int:project_id>', methods=['GET'])
def get_project_risks(project_id):
    """Get all risks for a project"""
    try:
        risks = Risk.query.filter_by(project_id=project_id).all()
        return jsonify([{
            'id': r.id,
            'risk_name': r.risk_name,
            'risk_category': r.risk_category,
            'probability': r.probability,
            'impact': r.impact,
            'adjustment_factor': r.adjustment_factor,
            'description': r.description
        } for r in risks]), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/risks/<int:project_id>/apply-adjustments', methods=['POST'])
def apply_risk_adjustments(project_id):
    """Apply aggregated risk adjustments to estimation"""
    try:
        project = Project.query.get(project_id)
        if not project:
            return jsonify({'error': 'Project not found'}), 404
        
        estimation = Estimation.query.filter_by(project_id=project_id).first()
        if not estimation:
            return jsonify({'error': 'No estimation found for this project'}), 404
        
        # Calculate aggregate risk adjustment factor
        risks = Risk.query.filter_by(project_id=project_id).all()
        if not risks:
            adjustment_factor = 1.0
        else:
            # Simple aggregation: multiply all factors (can be customized)
            adjustment_factor = 1.0
            for risk in risks:
                risk_effect = 1 + ((risk.probability * risk.impact) * (risk.adjustment_factor - 1))
                adjustment_factor *= risk_effect
        
        # Apply adjustment to estimation
        adjusted = COCOMOCalculator.apply_risk_adjustment(
            estimation.final_effort,
            estimation.final_cost,
            adjustment_factor
        )
        
        estimation.final_effort = adjusted['adjusted_effort']
        estimation.final_cost = adjusted['adjusted_cost']
        estimation.risk_adjustment_factor = adjusted['adjustment_factor']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'adjustment_factor': adjusted['adjustment_factor'],
            'adjusted_effort': adjusted['adjusted_effort'],
            'adjusted_cost': adjusted['adjusted_cost'],
            'message': 'Risk adjustments applied successfully'
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ==================== EVM ENDPOINTS ====================

@app.route('/api/evm/<int:project_id>', methods=['POST'])
def record_evm_data(project_id):
    """Record EVM tracking data"""
    try:
        project = Project.query.get(project_id)
        if not project:
            return jsonify({'error': 'Project not found'}), 404
        
        data = request.json
        required_fields = ['planned_value', 'earned_value', 'actual_cost', 'percentage_complete']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        pv = float(data['planned_value'])
        ev = float(data['earned_value'])
        ac = float(data['actual_cost'])
        
        # Calculate EVM metrics
        metrics = EVMCalculator.calculate_evm_metrics(pv, ev, ac)
        status = EVMCalculator.determine_project_status(
            metrics['cost_variance'],
            metrics['schedule_variance'],
            metrics['cost_performance_index'],
            metrics['schedule_performance_index']
        )
        
        # Get last estimation for budget reference
        estimation = Estimation.query.filter_by(project_id=project_id).first()
        bac = estimation.final_cost if estimation else 0
        
        eac = EVMCalculator.estimate_at_completion(bac, metrics['cost_performance_index'])
        etc = EVMCalculator.estimate_to_complete(bac, ev)
        
        # Save EVM data
        evm = EVMTracking(
            project_id=project_id,
            planned_value=pv,
            earned_value=ev,
            actual_cost=ac,
            cost_variance=metrics['cost_variance'],
            schedule_variance=metrics['schedule_variance'],
            cost_performance_index=metrics['cost_performance_index'],
            schedule_performance_index=metrics['schedule_performance_index'],
            project_status=status['status'],
            percentage_complete=float(data['percentage_complete'])
        )
        
        db.session.add(evm)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'evm_id': evm.id,
            'metrics': metrics,
            'project_status': status['status'],
            'status_reason': status['reason'],
            'estimate_at_completion': eac,
            'estimate_to_complete': etc,
            'message': 'EVM data recorded successfully'
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/evm/<int:project_id>', methods=['GET'])
def get_evm_data(project_id):
    """Get latest EVM tracking data for a project"""
    try:
        evm = EVMTracking.query.filter_by(project_id=project_id).order_by(
            EVMTracking.tracking_date.desc()
        ).first()
        
        if not evm:
            return jsonify({'error': 'No EVM data found'}), 404
        
        return jsonify({
            'id': evm.id,
            'planned_value': evm.planned_value,
            'earned_value': evm.earned_value,
            'actual_cost': evm.actual_cost,
            'cost_variance': evm.cost_variance,
            'schedule_variance': evm.schedule_variance,
            'cost_performance_index': evm.cost_performance_index,
            'schedule_performance_index': evm.schedule_performance_index,
            'project_status': evm.project_status,
            'percentage_complete': evm.percentage_complete,
            'tracking_date': evm.tracking_date.isoformat()
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== REPORT ENDPOINT ====================

@app.route('/api/reports/<int:project_id>', methods=['GET'])
def generate_report(project_id):
    """Generate comprehensive project estimation report"""
    try:
        project = Project.query.get(project_id)
        if not project:
            return jsonify({'error': 'Project not found'}), 404
        
        estimation = Estimation.query.filter_by(project_id=project_id).first()
        risks = Risk.query.filter_by(project_id=project_id).all()
        evm = EVMTracking.query.filter_by(project_id=project_id).order_by(
            EVMTracking.tracking_date.desc()
        ).first()
        
        report = {
            'project': {
                'name': project.project_name,
                'type': project.project_type,
                'size_kloc': project.kloc,
                'cost_per_person_month': project.cost_per_person_month,
                'team_experience': project.team_experience
            },
            'estimation': {
                'model_used': estimation.selected_model if estimation else 'None',
                'effort_person_months': estimation.final_effort if estimation else 0,
                'duration_months': estimation.basic_duration if estimation and estimation.selected_model == 'Basic' else estimation.intermediate_duration if estimation else 0,
                'total_cost': estimation.final_cost if estimation else 0,
                'risk_adjustment_factor': estimation.risk_adjustment_factor if estimation else 1.0,
                'cost_per_phase': estimation.estimated_cost_per_phase if hasattr(estimation, 'cost_per_phase') else {}
            },
            'risks': [{
                'name': r.risk_name,
                'category': r.risk_category,
                'probability': r.probability,
                'impact': r.impact,
                'adjustment_factor': r.adjustment_factor
            } for r in risks],
            'evm': {
                'planned_value': evm.planned_value if evm else 0,
                'earned_value': evm.earned_value if evm else 0,
                'actual_cost': evm.actual_cost if evm else 0,
                'cost_variance': evm.cost_variance if evm else 0,
                'schedule_variance': evm.schedule_variance if evm else 0,
                'cost_performance_index': evm.cost_performance_index if evm else 0,
                'schedule_performance_index': evm.schedule_performance_index if evm else 0,
                'project_status': evm.project_status if evm else 'Not Tracked',
                'percentage_complete': evm.percentage_complete if evm else 0
            }
        }
        
        return jsonify(report), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    is_dev = os.getenv('FLASK_ENV', 'development') == 'development'
    port = int(os.getenv('PORT', 5000))
    app.run(debug=is_dev, host='0.0.0.0', port=port)
