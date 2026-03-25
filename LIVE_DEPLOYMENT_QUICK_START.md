# 🌐 LIVE DEPLOYMENT QUICK START

## What You'll Get
- ✅ Live app at: `https://your-app.railway.app`
- ✅ PostgreSQL database on Supabase
- ✅ Auto-deploy from GitHub
- ✅ Production-ready

## Time Required: 25 minutes

---

## QUICK CHECKLIST

### Prerequisites (2 min)
- [ ] GitHub account with pushed code
- [ ] Email for Supabase
- [ ] Email for Railway

### Supabase Setup (10 min)
- [ ] Sign up at https://supabase.com
- [ ] Create project (2-3 min wait)
- [ ] Copy connection string
- [ ] Run SQL schema
- [ ] Create 4 tables

### Railway Setup (10 min)
- [ ] Sign up at https://railway.app
- [ ] Deploy from GitHub
- [ ] Add environment variables
- [ ] Get public URL

### Frontend Update (3 min)
- [ ] Update API_BASE in app.js
- [ ] Push to GitHub
- [ ] Railway auto-deploys

### Testing (2 min)
- [ ] Visit https://your-app.railway.app
- [ ] Login and create project
- [ ] Success! 🎉

---

## COPY-PASTE GUIDE

### 1. Create Supabase Project
```
Visit: https://supabase.com/dashboard
Click: "Start Your Project" > "I'll start with Supabase"
Sign up with email
Name: spm-estimation-prod
Password: SecurePassword123!
Region: (choose closest)
Plan: Free
Wait 2-3 minutes...
```

### 2. Get Connection String
```
Settings > Database > PostgreSQL
Copy the string
Replace PASSWORD with your actual password
SAVE IT!
```

### 3. Create Tables in Supabase
```
SQL Editor > New Query > Paste the SQL below:
```

**Paste this SQL in Supabase:**
```sql
-- Create projects table
CREATE TABLE projects (
  id SERIAL PRIMARY KEY,
  project_name VARCHAR(255) NOT NULL,
  project_type VARCHAR(50) NOT NULL,
  kloc FLOAT NOT NULL,
  cost_per_person_month FLOAT NOT NULL,
  team_experience VARCHAR(50) NOT NULL,
  created_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE estimations (
  id SERIAL PRIMARY KEY,
  project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
  basic_effort FLOAT, basic_duration FLOAT, basic_cost FLOAT,
  intermediate_effort FLOAT, intermediate_duration FLOAT, intermediate_cost FLOAT,
  selected_model VARCHAR(50) DEFAULT 'Basic',
  final_effort FLOAT, final_cost FLOAT,
  risk_adjustment_factor FLOAT DEFAULT 1.0,
  created_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE risks (
  id SERIAL PRIMARY KEY,
  project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
  risk_name VARCHAR(255) NOT NULL,
  risk_category VARCHAR(100) NOT NULL,
  probability FLOAT, impact FLOAT,
  adjustment_factor FLOAT DEFAULT 1.0,
  description TEXT
);

CREATE TABLE evm_tracking (
  id SERIAL PRIMARY KEY,
  project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
  planned_value FLOAT, earned_value FLOAT, actual_cost FLOAT,
  cost_variance FLOAT, schedule_variance FLOAT,
  cost_performance_index FLOAT, schedule_performance_index FLOAT,
  project_status VARCHAR(20) DEFAULT 'Green',
  percentage_complete FLOAT DEFAULT 0.0,
  tracking_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_estimations_project ON estimations(project_id);
CREATE INDEX idx_risks_project ON risks(project_id);
CREATE INDEX idx_evm_project ON evm_tracking(project_id);
```

### 4. Deploy Railway
```
Visit: https://railway.app
Sign up with GitHub
New Project > Deploy from GitHub repo
Select your repository
Select main branch
```

### 5. Set Environment Variables in Railway
```
In Railway Dashboard:
- Variables tab
- Add: DATABASE_URL = (your Supabase connection string)
- Add: FLASK_ENV = production
- Add: SECRET_KEY = (generate with Python below)
- Add: DEBUG = False
- Click Save
```

**Generate SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 6. Update Frontend API URL
```
File: frontend/js/app.js
Find: const API_BASE = 'http://localhost:5000/api';
Replace with: const API_BASE = 'https://YOUR-RAILWAY-URL.railway.app/api';
```

**Get your Railway URL:**
```
Railway Dashboard > Your Project > Domains section
Should look like: your-project-name.railway.app
```

### 7. Push Changes
```bash
git add frontend/js/app.js
git commit -m "Update API URL for production"
git push origin main
```

Railway auto-deploys in 1-2 minutes.

### 8. Access Your App
```
https://your-railway-url.railway.app
Login: admin / password
```

---

## VERIFY IT WORKS

### Test Checklist
- [ ] Login page loads
- [ ] Can login with admin/password
- [ ] Dashboard displays
- [ ] Can create a project
- [ ] Project appears in list
- [ ] Can view project details
- [ ] Data persists (refresh page, data still there)

### If Something Doesn't Work

**Check Railway Logs:**
```
Dashboard > Your Project > Logs tab
Look for errors
```

**Check Supabase Connection:**
```
Supabase > Settings > Database
Verify connection string in Railway variables
```

**Check Frontend API URL:**
```
Open Browser DevTools (F12)
Console tab - look for API errors
Network tab - see which API calls are failing
```

---

## SUCCESS! 🎉

You now have:
- ✅ Local app at http://127.0.0.1:5000
- ✅ Live app at https://your-railway-url.railway.app
- ✅ Database backing both
- ✅ Full functionality

---

## MONITORING

### Railway
```
Dashboard > Your Project > Logs
Shows all requests and errors
```

### Supabase
```
Dashboard > Settings > Logs
Shows database queries
```

---

## TROUBLESHOOTING QUICK FIX

| Issue | Fix |
|-------|-----|
| 404 when accessing | Check API_BASE URL in app.js |
| Login not working | Check DATABASE_URL in Railway |
| No data after create | Refresh page, check browser console |
| Static files 404 | Clear cache (Ctrl+Shift+Delete) |
| Server won't start | Check Railway logs |

---

**TOTAL TIME: ~25 minutes**

**DIFFICULTY: Easy (just copy-paste!)**

**RESULT: Production-ready app! 🚀**

