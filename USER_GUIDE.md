# User Guide & Feature Checklist

## 🚀 Getting Started (First Time)

### 1. Initial Setup
- [ ] Install Python 3.8+ from python.org
- [ ] Navigate to project directory
- [ ] Run: `pip install -r backend/requirements.txt`
- [ ] Run: `python backend/app.py`
- [ ] Open: `http://localhost:5000` in browser

### 2. Verify Installation
- [ ] Main page loads with 7 module buttons
- [ ] Sidebar shows "Project Input" is selected
- [ ] No console errors (press F12)

---

## 📋 Module-by-Module Walkthrough

### Module 1: Project Input 📋

**Purpose:** Define the project baseline

**What to do:**
1. [ ] Enter Project Name (e.g., "Banking App")
2. [ ] Select Project Type:
   - [ ] Organic (small, well-understood)
   - [ ] Semi-Detached (medium complexity)
   - [ ] Embedded (complex, integrated)
3. [ ] Enter Size in KLOC (e.g., 50)
4. [ ] Enter Cost per Person-Month (e.g., 5000)
5. [ ] Select Team Experience:
   - [ ] Junior
   - [ ] Intermediate
   - [ ] Senior
6. [ ] Click "Create Project"
7. [ ] Project appears in list below

**Expected Results:**
- ✓ Project saved to database
- ✓ Project appears in project lists in other modules
- ✓ Can create multiple projects

**Viva Question:** "Why does project type matter?"
Answer: "Different types have different effort multipliers. Embedded projects are more complex (need more effort)."

---

### Module 2: Effort Estimation 📈

**Purpose:** Calculate how much effort is needed using COCOMO models

#### 2A: Basic COCOMO

**What to do:**
1. [ ] Select your project from dropdown
2. [ ] Click "Basic COCOMO" tab
3. [ ] Click "Calculate Basic COCOMO"

**What you'll see:**
- [ ] Effort (person-months)
- [ ] Duration (calendar months)
- [ ] Total Cost
- [ ] Phase-wise cost breakdown

**Interpretation Guide:**
```
Effort = 50 person-months
Duration = 10.5 months
Total Cost = $250,000

Meaning: 
- Need 50 person-months of work
- Can be done in ~10.5 calendar months (5 people team)
- Will cost $250,000
```

**Viva Question:** "What's the formula for Basic COCOMO?"
Answer: "Effort = a × (KLOC)^b, where a and b vary by project type."

#### 2B: Intermediate COCOMO

**What to do:**
1. [ ] Still in Effort Estimation module
2. [ ] Click "Intermediate COCOMO" tab
3. [ ] Select multiplier values:
   - [ ] Required Software Reliability (Very Low to Very High)
   - [ ] Product Complexity (Simple to Very High)
4. [ ] Click "Calculate Intermediate COCOMO"

**What you'll see:**
- [ ] Base Effort
- [ ] Multiplier Impact (>1.0 means increased effort)
- [ ] Adjusted Effort
- [ ] Duration
- [ ] Adjusted Total Cost

**Interpretation Guide:**
```
Base Effort: 50 person-months
Multipliers: Reliability (1.15) × Complexity (1.15) × Experience (0.85)
Multiplier Impact: 0.945x
Final Effort: 47.25 person-months

Meaning:
- The project is complex, so needs more testing
- But team is experienced, so a bit faster
- Net effect: slightly less effort than basic model
```

**Viva Question:** "Why use Intermediate instead of Basic?"
Answer: "Intermediate accounts for specific project characteristics, making estimates more accurate."

---

### Module 3: Schedule & Cost 📅

**Purpose:** View cost distribution and project timeline

**What to do:**
1. [ ] Click "Schedule & Cost" in sidebar
2. [ ] Select your project
3. [ ] View:
   - [ ] Cost distribution pie chart
   - [ ] Gantt chart with 4 phases

**What you'll see:**

**Cost Distribution:**
```
Design (40%):       $100,000
Coding (30%):       $75,000
Testing (20%):      $50,000
Integration (10%):  $25,000
Total:              $250,000
```

**Gantt Chart:**
```
Design Phase ████████████████ 30 days
Coding Phase ███████████████████████ 45 days
Testing Phase ████████████████ 30 days
Integration & Deploy ████████ 15 days
```

**Viva Question:** "Why break down cost by phases?"
Answer: "It helps resource planning. Different phases need different skills and budgets."

---

### Module 4: Risk Management ⚠️

**Purpose:** Identify risks and adjust estimates accordingly

**What to do:**
1. [ ] Click "Risk Management" in sidebar
2. [ ] Select your project
3. [ ] Add New Risk:
   - [ ] Risk Name (e.g., "Key person departure")
   - [ ] Risk Category:
     - [ ] Technical
     - [ ] Resource
     - [ ] Schedule
     - [ ] External
   - [ ] Probability (0 = unlikely, 1 = certain)
   - [ ] Impact (0 = no impact, 1 = catastrophic)
   - [ ] Adjustment Factor (1.0 = no change, 1.2 = 20% increase)
   - [ ] Description (optional)
4. [ ] Click "Add Risk"
5. [ ] Add multiple risks if needed
6. [ ] Click "Apply Risk Adjustments to Estimation"

**Example Risk:**
```
Risk Name: "Team members lack .NET experience"
Category: Resource
Probability: 0.4 (40% likely)
Impact: 0.7 (70% severity if happens)
Adjustment Factor: 1.25 (25% effort increase)

Effect: Original 50 PM → 62.5 PM (20% increase)
        Original $250K → $312.5K (20% increase)
```

**Viva Question:** "How do risks affect estimation?"
Answer: "Each risk with high probability × impact gets an adjustment factor (>1.0 increases effort/cost)."

---

### Module 5: EVM Tracking 📊

**Purpose:** Monitor project progress using Earned Value Management

**What to do:**
1. [ ] Click "EVM Tracking" in sidebar
2. [ ] Select your project
3. [ ] Record EVM Data:
   - [ ] Planned Value (PV): "What budget was scheduled for now?"
   - [ ] Earned Value (EV): "What is actual work value?"
   - [ ] Actual Cost (AC): "How much did we actually spend?"
   - [ ] % Complete: "What % of project is done?"
4. [ ] Click "Record EVM Data"

**Example EVM Data:**
```
As of end of Month 3:

Planned Value: $75,000 (was supposed to spend this by now)
Earned Value: $60,000 (the work completed is worth this)
Actual Cost:  $70,000 (we actually spent this)
% Complete:   35%

Calculated Metrics:
- Cost Variance (CV) = $60,000 - $70,000 = -$10,000 (OVER budget)
- Schedule Variance (SV) = $60,000 - $75,000 = -$15,000 (BEHIND schedule)
- CPI = $60,000 / $70,000 = 0.86 (Getting 86¢ value per $1 spent)
- SPI = $60,000 / $75,000 = 0.80 (At 80% of planned progress)

Project Status: RED (both CPI and SPI < 0.90)
Reason: Project significantly over budget and behind schedule
```

**What you'll see:**
- [ ] All calculated metrics
- [ ] Project status (Green/Yellow/Red)
- [ ] Status explanation
- [ ] Performance charts

**Status Interpretation:**
```
🟢 GREEN   CPI > 0.95 & SPI > 0.95    → Continue current approach
🟡 YELLOW  0.90 < CPI < 0.95         → Monitor carefully, prepare actions
🔴 RED     CPI < 0.90 or SPI < 0.90  → Take corrective actions now
```

**Viva Question:** "What does CPI = 0.85 mean?"
Answer: "For every dollar spent, we only got 85 cents of work value. We're operating at 85% efficiency."

---

### Module 6: Dashboard 🎯

**Purpose:** See complete project overview at a glance

**What to do:**
1. [ ] Click "Dashboard" in sidebar
2. [ ] Select your project
3. [ ] Review:
   - [ ] Project Information (name, type, size)
   - [ ] Estimation Summary (model, effort, cost)
   - [ ] EVM Status (if data recorded)

**What you'll see:**
- Complete project snapshot
- All key metrics in one place
- Quick reference for status

---

### Module 7: Reports 📄

**Purpose:** Generate professional project documentation

**What to do:**
1. [ ] Click "Reports" in sidebar
2. [ ] Select your project
3. [ ] Review report sections:
   - [ ] Project Information
   - [ ] Estimation Results
   - [ ] Project Risks
   - [ ] EVM Metrics (if recorded)
4. [ ] Click "Print Report"

**What you'll see:**
- Professional formatted report
- Print dialog opens
- Can save as PDF

**Report Contents:**
```
1. PROJECT INFORMATION
   - Name, Type, Size, Cost/Month, Team Experience

2. EFFORT ESTIMATION RESULTS
   - COCOMO Model Used
   - Effort (Person-Months)
   - Duration (Months)
   - Total Cost
   - Risk Adjustment Factor

3. PROJECT RISKS (if any)
   - Risk Name
   - Category
   - Probability & Impact
   - Adjustment Factor

4. EARNED VALUE MANAGEMENT (if tracked)
   - PV, EV, AC
   - Variance metrics
   - Performance indices
   - Project Status
```

---

## 🧪 Test Scenarios

### Scenario 1: Small Organic Project
**Inputs:**
- Name: "Desktop App"
- Type: Organic
- Size: 10 KLOC
- Cost/Month: 4000
- Experience: Senior

**Expected Results:**
- Low effort (~10 person-months)
- Short duration (~3 months)
- Lower cost (~$40,000)

---

### Scenario 2: Large Embedded System
**Inputs:**
- Name: "Avionics System"
- Type: Embedded
- Size: 200 KLOC
- Cost/Month: 7000
- Experience: Intermediate

**Expected Results:**
- High effort (~240+ person-months)
- Moderate duration (~20 months)
- Very high cost (~$1.7M)

---

### Scenario 3: Risk Impact Demo
**Steps:**
1. [ ] Create project
2. [ ] Calculate Basic COCOMO (note cost)
3. [ ] Add multiple risks (high probability/impact)
4. [ ] Apply adjustments
5. [ ] Compare final cost (should be 20-50% higher)

---

## ❓ FAQ

### Q: Why are effort and duration different?
**A:** Effort is total person-months (1 person × 50 months OR 5 people × 10 months). Duration is calendar months needed with a team.

### Q: How accurate is COCOMO?
**A:** Historical ±30% for similar projects. Intermediate model is more accurate than Basic due to multipliers.

### Q: When should I use Green vs Yellow status?
**A:** Green = continue as-is. Yellow = implement preventive actions. Red = implement corrective actions now.

### Q: Can I edit a project after creating it?
**A:** Current version doesn't support editing (by design for simplicity). You can create a new project instead.

### Q: How do I delete a project?
**A:** To delete: Stop Flask, delete database/spm_estimation.db, restart Flask (new empty database created).

### Q: Can multiple people use this simultaneously?
**A:** Current version supports single user. Flask dev server handles one user. For multi-user, need production deployment with authentication.

---

## 📊 Sample Values for Testing

### Small Project
```
Name: Web Form Processor
Type: Organic
KLOC: 8
Cost/PM: 3000
Experience: Senior
```

### Medium Project
```
Name: E-commerce Platform
Type: Semi-Detached
KLOC: 50
Cost/PM: 5000
Experience: Intermediate
```

### Large Project
```
Name: Hospital Management System
Type: Embedded
KLOC: 150
Cost/PM: 6500
Experience: Junior
```

---

## 🎓 Viva Preparation Checklist

### Concept Understanding
- [ ] Can explain COCOMO formula
- [ ] Understand why project type matters
- [ ] Can explain effort vs duration
- [ ] Know what CPI < 1.0 means
- [ ] Can interpret Green/Yellow/Red status
- [ ] Know how risks affect estimates
- [ ] Understand why three-tier architecture

### Demonstration Skills
- [ ] Can create a project in 30 seconds
- [ ] Can calculate both COCOMO models
- [ ] Can add and apply risks
- [ ] Can record and interpret EVM data
- [ ] Can generate and view reports
- [ ] Can explain metrics in layman's terms

### Technical Knowledge
- [ ] Know what Flask is
- [ ] Know what SQLite stores
- [ ] Can explain database schema
- [ ] Know API endpoint purpose
- [ ] Can explain why REST API design
- [ ] Know Bootstrap purpose

---

## 🔐 Data Management

### Backing Up Data
```bash
# Copy database to backup
copy database\spm_estimation.db database\spm_estimation_backup.db
```

### Restoring from Backup
```bash
# Restore from backup
copy database\spm_estimation_backup.db database\spm_estimation.db
```

### Clearing All Data (CAREFUL!)
```bash
# Delete database (creates empty one when Flask starts)
del database\spm_estimation.db
python app.py  # Creates fresh empty database
```

---

## 🚨 Troubleshooting During Use

| Issue | Solution |
|-------|----------|
| Module not responding | Refresh browser (F5) |
| Chart not showing | Close other tabs, refresh |
| Can't create project | Check all fields filled |
| API error in console | Make sure Flask is running |
| Database error | Stop Flask, delete DB, restart |
| Page very slow | Close other applications |

---

## 💡 Tips & Tricks

### For Better Estimates
1. Use Intermediate COCOMO (more accurate than Basic)
2. Be realistic about team experience
3. Add appropriate risks (don't skip this step)
4. Compare with historical similar projects

### For Better Monitoring
1. Record EVM data regularly (weekly or monthly)
2. Track trends, not just single data points
3. Take action when status turns Yellow
4. Update risks as project progresses

### For Better Demonstration
1. Create 2-3 sample projects beforehand
2. Take screenshots of results
3. Print a sample report
4. Document manual calculations for comparison

---

## 📞 Getting Help

### If Something Doesn't Work
1. Check browser console (F12 → Console tab)
2. Check Flask terminal for error messages
3. Read error message carefully
4. Check SETUP.md troubleshooting section
5. Verify database hasn't corrupted

### For Viva Help
1. Review SPM_CONCEPTS.md for theory
2. Practice explaining each metric
3. Have manual calculation examples ready
4. Be ready to discuss trade-offs

---

**Version:** 1.0
**Last Updated:** January 30, 2026
**Ready to Use:** Yes ✅
