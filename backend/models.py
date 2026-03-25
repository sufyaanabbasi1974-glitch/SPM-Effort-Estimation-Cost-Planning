"""
Database models for SPM Effort Estimation System
Defines Project, Estimation, Risk, and EVM tracking entities
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Project(db.Model):
    """Project entity - stores basic project information"""
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(255), nullable=False)
    project_type = db.Column(db.String(50), nullable=False)  # Organic, Semi-Detached, Embedded
    kloc = db.Column(db.Float, nullable=False)  # Size in KLOC
    cost_per_person_month = db.Column(db.Float, nullable=False)
    team_experience = db.Column(db.String(50), nullable=False)  # Junior, Intermediate, Senior
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    estimations = db.relationship('Estimation', backref='project', lazy=True, cascade='all, delete-orphan')
    risks = db.relationship('Risk', backref='project', lazy=True, cascade='all, delete-orphan')
    evm_data = db.relationship('EVMTracking', backref='project', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Project {self.project_name}>'


class Estimation(db.Model):
    """Estimation entity - stores COCOMO effort and cost calculations"""
    __tablename__ = 'estimations'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    
    # Basic COCOMO results
    basic_effort = db.Column(db.Float)  # Person-months
    basic_duration = db.Column(db.Float)  # Months
    basic_cost = db.Column(db.Float)  # Total cost
    
    # Intermediate COCOMO results (with effort multipliers)
    intermediate_effort = db.Column(db.Float)
    intermediate_duration = db.Column(db.Float)
    intermediate_cost = db.Column(db.Float)
    
    # Selected model (Basic or Intermediate)
    selected_model = db.Column(db.String(50), default='Basic')
    
    # Final adjusted values after risk impact
    final_effort = db.Column(db.Float)
    final_cost = db.Column(db.Float)
    risk_adjustment_factor = db.Column(db.Float, default=1.0)
    
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Estimation Project_ID:{self.project_id}>'


class Risk(db.Model):
    """Risk entity - stores project risks and their adjustments"""
    __tablename__ = 'risks'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    
    risk_name = db.Column(db.String(255), nullable=False)
    risk_category = db.Column(db.String(100), nullable=False)  # Technical, Resource, Schedule, etc.
    probability = db.Column(db.Float)  # 0-1 scale
    impact = db.Column(db.Float)  # 0-1 scale
    adjustment_factor = db.Column(db.Float, default=1.0)  # 0.8 to 1.5 range
    description = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Risk {self.risk_name}>'


class EVMTracking(db.Model):
    """EVM (Earned Value Management) tracking entity"""
    __tablename__ = 'evm_tracking'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    
    # Planned Value (PV) - budgeted cost of work scheduled
    planned_value = db.Column(db.Float)
    
    # Earned Value (EV) - budgeted cost of work performed
    earned_value = db.Column(db.Float)
    
    # Actual Cost (AC) - real cost incurred
    actual_cost = db.Column(db.Float)
    
    # Calculated variance metrics
    cost_variance = db.Column(db.Float)  # CV = EV - AC
    schedule_variance = db.Column(db.Float)  # SV = EV - PV
    cost_performance_index = db.Column(db.Float)  # CPI = EV / AC
    schedule_performance_index = db.Column(db.Float)  # SPI = EV / PV
    
    # Project status: Green (on track), Yellow (warning), Red (critical)
    project_status = db.Column(db.String(20), default='Green')
    
    percentage_complete = db.Column(db.Float, default=0.0)
    tracking_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<EVMTracking Project_ID:{self.project_id} Status:{self.project_status}>'
