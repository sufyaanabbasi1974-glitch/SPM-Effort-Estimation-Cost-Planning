# Web-Based Software Effort Estimation and Cost Planning System

## Project Overview

This is a comprehensive **Software Project Management (SPM)** system designed for TYIT curriculum that helps project managers perform accurate early-stage estimation, cost planning, scheduling, risk analysis, and project monitoring using standard Software Project Management models.

**Project Title:** Design and Development of a Web-Based Software Effort Estimation and Cost Planning System Using Standard Software Project Management Models

## 🎯 System Purpose

The system assists project managers in:
- **Effort Estimation** using COCOMO (Basic & Intermediate) models
- **Cost Planning** and resource allocation
- **Schedule Generation** with phase-wise breakdown
- **Risk Analysis** with impact adjustment
- **Project Monitoring** using Earned Value Management (EVM)
- **Decision Making** based on accurate metrics and visualizations

## 📊 Core Modules

### 1. Project Input Module
- Captures project metadata
- Project name, type (Organic/Semi-Detached/Embedded), size (KLOC)
- Cost per person-month, team experience level
- Data validation and project persistence

### 2. Effort Estimation Module (COCOMO)
- **Basic COCOMO Model:** Effort = a × (KLOC)^b
  - Coefficients vary by project type
  - Calculates effort in person-months and duration
  
- **Intermediate COCOMO Model:** Applies effort multipliers
  - Reliability, Complexity, Experience adjustments
  - More accurate effort estimation

### 3. Cost & Schedule Estimation Module
- Total project cost = Effort × Cost per Person-Month
- Phase-wise distribution (Design 40%, Code 30%, Test 20%, Integration 10%)
- Gantt chart generation for project scheduling

### 4. Risk Impact Adjustment Module
- Predefined risk categories: Technical, Resource, Schedule, External
- Risk probability and impact assessment
- Effort and cost adjustment based on risk factors

### 5. Earned Value Management (EVM) Module
Tracks project performance metrics:
- **Planned Value (PV):** Budgeted cost of work scheduled
- **Earned Value (EV):** Budgeted cost of work performed
- **Actual Cost (AC):** Real cost incurred

**Calculated Metrics:**
- Cost Variance (CV) = EV - AC
- Schedule Variance (SV) = EV - PV
- Cost Performance Index (CPI) = EV / AC
- Schedule Performance Index (SPI) = EV / PV

**Project Status:**
- **Green:** Project on track (CPI > 0.95, SPI > 0.95)
- **Yellow:** Warning signs (0.90 < CPI < 0.95 or costs over budget)
- **Red:** Critical issues (CPI < 0.90 or behind schedule)

### 6. Visualization Dashboard
- Effort comparison charts (Basic vs Intermediate COCOMO)
- Cost distribution pie charts
- EVM performance tracking graphs
- Project status indicators

### 7. Report Generation Module
- Comprehensive project estimation summary
- Printable project report for documentation
- All calculated values and metrics
- Risk register and EVM tracking

## 🏗 System Architecture

### Three-Tier Architecture

#### **Presentation Layer (Frontend)**
- HTML5: Structure of web pages
- CSS3: Styling and responsive layout
- Bootstrap 5: Responsive UI framework
- JavaScript: Client-side validation and interaction
- Chart.js: Data visualization

#### **Application Layer (Backend)**
- Python with Flask framework
- RESTful API endpoints
- Business logic for COCOMO calculations
- EVM metric calculations
- Risk management logic

#### **Data Layer (Database)**
- SQLite database
- Tables: Projects, Estimations, Risks, EVM Tracking
- Persistent storage of project data

## 🛠 Technology Stack

| Layer | Technologies |
|-------|--------------|
| **Frontend** | HTML5, CSS3, Bootstrap 5, JavaScript, Chart.js |
| **Backend** | Python, Flask, SQLAlchemy ORM |
| **Database** | SQLite |
| **Web Server** | Flask Development Server |
| **IDE/Tools** | VS Code, Web Browser (Chrome/Firefox) |

## 📁 Project Structure

```
Web-based software effort estimation and cost planning system/
│
├── frontend/
│   ├── index.html              # Main application UI
│   ├── css/
│   │   └── style.css           # Custom styling
│   ├── js/
│   │   └── app.js              # Client-side logic
│   └── assets/                 # Images and resources
│
├── backend/
│   ├── app.py                  # Flask application entry point
│   ├── models.py               # Database models (SQLAlchemy)
│   ├── cocomo_calculator.py    # COCOMO estimation logic
│   ├── evm_calculator.py       # EVM calculations
│   └── requirements.txt        # Python dependencies
│
├── database/
│   └── spm_estimation.db       # SQLite database (auto-created)
│
├── README.md                   # Project documentation
├── SETUP.md                    # Installation and setup guide
└── .env                        # Environment configuration
```

## 🚀 Installation and Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Modern web browser (Chrome, Firefox, Safari)
- VS Code (recommended)

### Step 1: Install Python Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Step 2: Run Flask Application
```bash
cd backend
python app.py
```
The application will run on `http://localhost:5000`

### Step 3: Open in Web Browser
- Navigate to `http://localhost:5000` in your web browser
- The system will automatically create the SQLite database on first run

## 📖 How to Use the System

### 1. Create a Project
- Click "Project Input" in sidebar
- Enter project details (name, type, KLOC, cost per month, experience level)
- Click "Create Project"

### 2. Estimate Effort (COCOMO)
- Go to "Effort Estimation" module
- Select your project
- Click "Calculate Basic COCOMO" or "Calculate Intermediate COCOMO"
- Review effort estimates, duration, and costs

### 3. Plan Schedule & Costs
- Select "Schedule & Cost" module
- View phase-wise cost distribution
- Review Gantt chart for project timeline

### 4. Manage Risks
- Go to "Risk Management" module
- Add project risks with probability and impact
- Select adjustment factors
- Click "Apply Risk Adjustments" to adjust effort and cost

### 5. Track Project with EVM
- Navigate to "EVM Tracking" module
- Record Planned Value (PV), Earned Value (EV), Actual Cost (AC)
- View calculated performance metrics (CPI, SPI, CV, SV)
- Monitor project status (Green/Yellow/Red)

### 6. View Dashboard
- Use "Dashboard" to see project overview
- Review all estimations and EVM metrics at a glance

### 7. Generate Reports
- Click "Reports" module
- Select project
- Review comprehensive estimation report
- Click "Print Report" for documentation

## 📊 COCOMO Coefficients

### Basic COCOMO Coefficients

| Project Type | a | b |
|--------------|---|---|
| Organic | 2.4 | 1.05 |
| Semi-Detached | 3.0 | 1.12 |
| Embedded | 3.6 | 1.20 |

### Effort Multiplier Categories

- **Reliability:** Very Low (0.75) → Nominal (1.0) → Very High (1.40)
- **Complexity:** Simple (0.70) → Nominal (1.0) → Very High (1.30)
- **Database Size:** Low (0.93) → Nominal (1.0) → Very High (1.16)
- **Team Experience:** Junior (1.20) → Intermediate (1.0) → Senior (0.85)

## 🎓 SPM Concepts Mapping

| System Feature | SPM Concept |
|---|---|
| COCOMO Calculation | Effort & Cost Estimation |
| Phase-wise Breakdown | Work Breakdown Structure (WBS) |
| Gantt Chart | Schedule Management |
| Risk Management | Risk Analysis & Mitigation |
| EVM Metrics | Project Monitoring & Control |
| Reports | Project Documentation |

## 💾 Database Schema

### Projects Table
- id, project_name, project_type, kloc, cost_per_person_month, team_experience, created_date

### Estimations Table
- id, project_id, basic_effort, basic_duration, basic_cost, intermediate_effort, selected_model, final_effort, final_cost, risk_adjustment_factor

### Risks Table
- id, project_id, risk_name, risk_category, probability, impact, adjustment_factor, description

### EVM Tracking Table
- id, project_id, planned_value, earned_value, actual_cost, cost_variance, schedule_variance, CPI, SPI, project_status, percentage_complete

## 📝 API Endpoints

### Projects
- `POST /api/projects` - Create new project
- `GET /api/projects` - List all projects
- `GET /api/projects/<id>` - Get project details

### Estimations
- `POST /api/estimations/basic-cocomo/<project_id>` - Calculate Basic COCOMO
- `POST /api/estimations/intermediate-cocomo/<project_id>` - Calculate Intermediate COCOMO

### Risks
- `POST /api/risks/<project_id>` - Add risk
- `GET /api/risks/<project_id>` - Get project risks
- `POST /api/risks/<project_id>/apply-adjustments` - Apply risk adjustments

### EVM
- `POST /api/evm/<project_id>` - Record EVM data
- `GET /api/evm/<project_id>` - Get EVM data

### Reports
- `GET /api/reports/<project_id>` - Generate project report

## 🎯 Viva Preparation

### Key Concepts to Explain
1. **COCOMO Model:** Explain basic vs intermediate, coefficients, formula
2. **Effort vs Duration:** Person-months vs calendar months
3. **Risk Management:** How risks affect estimates, adjustment factors
4. **EVM Metrics:** What CV, SV, CPI, SPI mean and their interpretation
5. **Project Status:** How Green/Yellow/Red status is determined
6. **Three-Tier Architecture:** Why separation of concerns matters

### Demo Points
- Creating a sample project and showing all modules
- Comparing Basic and Intermediate COCOMO results
- Adding risks and seeing impact on estimates
- Tracking EVM metrics and interpreting project status
- Generating and printing reports

## 📝 System Limitations (by Design)

✓ No Machine Learning or AI complexity
✓ Simple, academic-focused calculations
✓ Single-user system (not multi-user)
✓ No external API integrations
✓ SQLite (suitable for small-scale projects)
✓ Clean, documentation-ready code

## 🔒 Future Enhancements (Beyond Current Scope)

- Multi-user support with authentication
- Historical project tracking and trends
- Advanced risk modeling (Monte Carlo simulation)
- Resource allocation and leveling
- Critical path analysis
- Integration with external tools

## 📞 Support & Documentation

For detailed setup instructions, see **SETUP.md**
For API documentation, see **API.md**
For SRS and WBS documentation, see **DOCUMENTATION/** folder

---

**Created:** January 2026
**Suitable for:** TYIT SPM Project Submission
**Approved for:** Academic documentation and viva presentation
