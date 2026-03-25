# Quick Start Guide

## 🚀 Get Running in 3 Minutes

### Step 1: Install Dependencies (1 minute)
```bash
cd backend
pip install -r requirements.txt
```

### Step 2: Start the Server (30 seconds)
```bash
python app.py
```

You should see:
```
Running on http://127.0.0.1:5000
```

### Step 3: Open in Browser (30 seconds)
Navigate to: **http://localhost:5000**

## ✅ Quick Verification

1. ✓ Page loads with navigation menu
2. ✓ Click "Project Input" button
3. ✓ Fill in sample project details:
   - Name: "Test Project"
   - Type: "Semi-Detached"
   - KLOC: 50
   - Cost/Month: 5000
   - Experience: "Intermediate"
4. ✓ Click "Create Project"
5. ✓ Project appears in project list

## 🎯 Try Each Module (5 minutes total)

### Module 1: Effort Estimation
- Select project in "Effort Estimation"
- Click "Calculate Basic COCOMO"
- See effort, duration, and cost estimates

### Module 2: Schedule & Cost
- View phase-wise cost distribution chart
- See Gantt chart with 4 phases

### Module 3: Risk Management
- Add a sample risk (e.g., "Team shortage")
- Set probability: 0.3, Impact: 0.5
- Click "Apply Risk Adjustments"

### Module 4: EVM Tracking
- Record sample values:
  - PV: 10000, EV: 8000, AC: 9000
- View metrics and project status

### Module 5: Reports
- View comprehensive project report
- Click "Print Report" to download

## 📊 Sample Project Values

```
Project Name:        "Mobile Banking App"
Project Type:        Semi-Detached
Size (KLOC):         75
Cost per Person-Month: 6000
Team Experience:     Intermediate
```

Expected Results:
- Effort: ~24 person-months
- Duration: ~7 months
- Total Cost: ~144,000

## 🔧 Troubleshooting Quick Fixes

| Problem | Solution |
|---------|----------|
| Port 5000 in use | Change port in `app.py`: `app.run(port=5001)` |
| ModuleNotFoundError | Run: `pip install -r requirements.txt` |
| Page won't load | Make sure Flask is running (check terminal) |
| Database error | Delete `database/spm_estimation.db` and restart |

## 📁 File Locations

- **Frontend UI:** `frontend/index.html`
- **Backend Logic:** `backend/app.py`
- **Database:** `database/spm_estimation.db` (auto-created)
- **Configuration:** `.env` (already configured)

## 🎓 Key Features to Demonstrate

1. **COCOMO Estimation** - Basic & Intermediate models
2. **Automatic Cost Calculation** - Phase-wise breakdown
3. **Risk Management** - Impact on estimates
4. **EVM Tracking** - Project status indicators (Green/Yellow/Red)
5. **Visualization** - Charts and Gantt diagrams
6. **Reporting** - Comprehensive printable reports

## 🧪 Test Scenarios

### Scenario 1: Small Organic Project
- Size: 10 KLOC, Type: Organic
- Low effort and short duration expected

### Scenario 2: Large Embedded Project
- Size: 100 KLOC, Type: Embedded
- High effort and long duration expected

### Scenario 3: Risk Impact Demo
- Create project → Apply high-risk adjustments
- See cost and effort increase proportionally

## 📝 Notes for Viva

- **Explain:** Why COCOMO models exist (historical context)
- **Show:** Difference between Basic and Intermediate models
- **Demonstrate:** How effort multipliers work
- **Discuss:** EVM as monitoring tool
- **Explain:** Why Green/Yellow/Red status helps decision-making

## 🛑 Stopping the Server

Press `CTRL+C` in the terminal running Flask

## 📚 Full Documentation

- **Setup Guide:** See `SETUP.md`
- **Architecture & Features:** See `README.md`

---

That's it! You're ready to use the SPM Estimation System. 🎉
