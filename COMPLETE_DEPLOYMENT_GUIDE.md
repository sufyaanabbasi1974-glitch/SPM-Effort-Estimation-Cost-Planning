# 🚀 Complete Deployment Guide: Local + Live

## Quick Navigation
- **Local Deployment**: Development on your machine
- **Live Deployment**: Production on Supabase + Railway
- **Testing**: Both environments fully functional

---

## PART 1: LOCAL DEPLOYMENT ✅

### 1.1 Prerequisites
- Python 3.11+ installed
- Git installed
- Your project folder

### 1.2 Setup (5 minutes)

#### Step 1: Navigate to Backend
```bash
cd backend
```

#### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

#### Step 3: Run the Server
```bash
python app.py
```

**You should see:**
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
 * Debugger is active!
```

### 1.3 Access Your App

#### Login Page
```
http://127.0.0.1:5000/login
```

#### Home Dashboard
```
http://127.0.0.1:5000/home
```

#### Direct Access
```
http://127.0.0.1:5000
↓ (redirects to login if not logged in)
↓
http://127.0.0.1:5000/login
```

### 1.4 Default Credentials
```
Username: admin
Password: password
```

### 1.5 Local Database
- **Type**: SQLite
- **Location**: `database/spm_estimation.db`
- **Auto-created**: Yes, on first run
- **Reset**: Delete the `.db` file and restart

### 1.6 Local Features Available
✅ Project creation & management
✅ COCOMO effort estimation
✅ Risk management
✅ EVM tracking
✅ Report generation
✅ Activity history
✅ Data import/export
✅ Theme switching (dark/light)

### 1.7 Stop the Server
```
Press Ctrl+C in terminal
```

---

## PART 2: LIVE DEPLOYMENT (Supabase + Railway)

### Prerequisites
- GitHub account (for code repository)
- Supabase account (free at https://supabase.com)
- Railway account (free at https://railway.app)
- 30 minutes setup time

### 2.1 Step 1: Prepare GitHub Repository

#### Option A: Existing Repository
```bash
cd your-project-folder
git remote -v  # Check if remote exists
git add .
git commit -m "Prepare for live deployment"
git push origin main
```

#### Option B: New Repository
```bash
cd your-project-folder
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/spm-estimation.git
git push -u origin main
```

### 2.2 Step 2: Create Supabase Database (10 minutes)

#### 2.2.1 Sign Up
1. Go to https://supabase.com/dashboard
2. Click "Start Your Project"
3. Sign up with email or GitHub
4. Create organization: "spm-estimation"

#### 2.2.2 Create Project
1. Click "New Project"
2. Fill in:
   - **Name**: `spm-estimation-prod`
   - **Database Password**: `SecurePassword123!` (save this!)
   - **Region**: Choose closest to you
   - **Plan**: Free tier
3. Wait 2-3 minutes for setup

#### 2.2.3 Get Connection String
1. Go to **Settings** → **Database**
2. Under "Connection string", select **PostgreSQL**
3. Copy the string (looks like):
   ```
   postgresql://postgres.xxxxx:PASSWORD@xxxxx.postgres.supabase.co:5432/postgres
   ```
4. **Replace PASSWORD with your database password**
5. **Save this URL** - you'll need it soon

#### 2.2.4 Create Database Tables
1. Go to **SQL Editor** in Supabase
2. Click **"New query"**
3. Paste this SQL:

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

-- Create estimations table
CREATE TABLE estimations (
  id SERIAL PRIMARY KEY,
  project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
  basic_effort FLOAT,
  basic_duration FLOAT,
  basic_cost FLOAT,
  intermediate_effort FLOAT,
  intermediate_duration FLOAT,
  intermediate_cost FLOAT,
  selected_model VARCHAR(50) DEFAULT 'Basic',
  final_effort FLOAT,
  final_cost FLOAT,
  risk_adjustment_factor FLOAT DEFAULT 1.0,
  created_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create risks table
CREATE TABLE risks (
  id SERIAL PRIMARY KEY,
  project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
  risk_name VARCHAR(255) NOT NULL,
  risk_category VARCHAR(100) NOT NULL,
  probability FLOAT,
  impact FLOAT,
  adjustment_factor FLOAT DEFAULT 1.0,
  description TEXT
);

-- Create evm_tracking table
CREATE TABLE evm_tracking (
  id SERIAL PRIMARY KEY,
  project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
  planned_value FLOAT,
  earned_value FLOAT,
  actual_cost FLOAT,
  cost_variance FLOAT,
  schedule_variance FLOAT,
  cost_performance_index FLOAT,
  schedule_performance_index FLOAT,
  project_status VARCHAR(20) DEFAULT 'Green',
  percentage_complete FLOAT DEFAULT 0.0,
  tracking_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes
CREATE INDEX idx_estimations_project ON estimations(project_id);
CREATE INDEX idx_risks_project ON risks(project_id);
CREATE INDEX idx_evm_project ON evm_tracking(project_id);
```

4. Click **RUN**
5. You should see success message

#### 2.2.5 Verify Tables
1. Left sidebar → **Table Editor**
2. You should see:
   - `projects`
   - `estimations`
   - `risks`
   - `evm_tracking`

### 2.3 Step 3: Deploy to Railway (10 minutes)

#### 2.3.1 Sign Up
1. Go to https://railway.app
2. Sign up with GitHub
3. Authorize Railway

#### 2.3.2 Create Project
1. Dashboard → **New Project**
2. Select **"Deploy from GitHub repo"**
3. Select your repository
4. Select **main** branch

#### 2.3.3 Wait for Build
Railway will:
1. Install dependencies from `requirements-prod.txt`
2. Build the application
3. Deploy it
- This takes ~2-3 minutes

#### 2.3.4 Configure Environment Variables
1. Project → **Variables** tab
2. Add these environment variables:
   ```
   DATABASE_URL = postgresql://postgres.xxxxx:PASSWORD@xxxxx.postgres.supabase.co:5432/postgres
   FLASK_ENV = production
   SECRET_KEY = (run this in Python: import secrets; print(secrets.token_hex(32)))
   DEBUG = False
   ```

#### 2.3.5 Get Your Public URL
1. In Railway dashboard, look for **"Domains"**
2. You'll see something like: `your-project.railway.app`
3. **Save this URL**

### 2.4 Step 4: Update Frontend for Production

#### 2.4.1 Update API Base URL
1. Open `frontend/js/app.js`
2. Find this line (near top):
   ```javascript
   const API_BASE = 'http://localhost:5000/api';
   ```
3. Replace with:
   ```javascript
   const API_BASE = 'https://your-railway-url.railway.app/api';
   ```
   (Use your actual Railway URL)

4. Save the file

#### 2.4.2 Push Changes to GitHub
```bash
git add frontend/js/app.js
git commit -m "Update API base URL for production"
git push origin main
```

#### 2.4.3 Railway Auto-Deploys
- Railway automatically rebuilds when you push
- Check Railway dashboard for deployment status
- Should complete in ~1-2 minutes

### 2.5 Test Live Deployment

#### Access Your Live App
```
https://your-railway-url.railway.app
```

#### Login
```
Username: admin
Password: password
```

#### Create Test Project
1. Fill in:
   - Name: "Live Test Project"
   - Type: Semi-Detached
   - Size: 50 KLOC
   - Cost: $5000/month
   - Experience: Intermediate

2. Click "Create Project"
3. **If it creates successfully, everything is working!**

#### Verify Database
1. In Supabase, go to **Table Editor**
2. Open **projects** table
3. You should see your test project

---

## PART 3: WORKING WITH BOTH ENVIRONMENTS

### Switching Between Local and Live

#### Local Development
```bash
# No changes needed, always uses SQLite
cd backend
python app.py
# Access at http://127.0.0.1:5000
```

#### Live Production
```bash
# Leave DATABASE_URL in environment
# Railway will use PostgreSQL automatically
# Access at https://your-railway-url.railway.app
```

### Database Selection (Automatic)
The app automatically chooses database based on `DATABASE_URL` environment variable:
```
If DATABASE_URL exists → Use PostgreSQL (Supabase)
If DATABASE_URL missing → Use SQLite (local)
```

### Syncing Data Between Environments

#### Export from Local
1. Local app → Settings → **"Export Data"**
2. Save JSON file

#### Import to Live
1. Live app (same browser for auth) → Settings → **"Import Data"**
2. Upload JSON file

#### Or Use SQL Backups
1. Export from local database
2. Import to Supabase via SQL Editor

---

## PART 4: TROUBLESHOOTING

### Local Issues

**"Port 5000 already in use"**
```bash
# Change port in backend/app.py, last line:
app.run(debug=True, host='0.0.0.0', port=5001)  # Change 5000 to 5001
```

**"ModuleNotFoundError"**
```bash
cd backend
pip install -r requirements.txt
```

**"Database error"**
```bash
# Delete and recreate database
rm database/spm_estimation.db
python app.py
```

---

### Live Issues

**"Connection refused" or "500 error"**
1. Check Railway logs: Dashboard > Logs tab
2. Verify DATABASE_URL is correct
3. Ensure all environment variables are set
4. Check Supabase is online

**"Static files returning 404"**
1. Verify `/assets` folder structure
2. Check CSS/JS file paths in HTML
3. Clear browser cache (Ctrl+Shift+Delete)

**"Database tables not found"**
1. Go to Supabase SQL Editor
2. Run the table creation script again
3. Check Supabase connection string is correct

**"Login not working"**
1. Check SECRET_KEY is set in Railway
2. Verify DATABASE_URL
3. Check browser console (F12) for errors

---

## PART 5: SECURITY CHECKLIST

Before going fully live:

### Local
- [ ] `.env` file is in `.gitignore`
- [ ] No secrets in code
- [ ] Database is local only

### Live (Production)
- [ ] SECRET_KEY is cryptographically secure
- [ ] DATABASE_URL password is strong
- [ ] No hardcoded secrets in code
- [ ] FLASK_ENV = production
- [ ] DEBUG = False
- [ ] CORS configured for your domain
- [ ] HTTPS enabled (Railway provides this)
- [ ] SSL certificate valid

---

## PART 6: MONITORING & MAINTENANCE

### Check Live App Status
1. Railway dashboard → Your project
2. Look for ✅ (healthy) or ❌ (error)
3. Click "Logs" to see recent requests

### Database Backups
1. Supabase → Settings → Backups
2. Manual backups available free
3. Daily automatic backups included

### Monitor Usage
- Supabase: Shows storage usage (free: 500MB)
- Railway: Shows CPU/Memory usage
- Both have free generous tiers

---

## PART 7: COMPLETE SETUP SUMMARY

### What You Now Have:

✅ **Local Deployment**
- SQLite database
- Flask server on localhost:5000
- Full development environment  
- Instant restarts with debug mode

✅ **Live Deployment**
- PostgreSQL on Supabase
- Python server on Railway
- Auto-deploy from GitHub
- Production-ready

✅ **Both Synchronized**
- Same codebase
- Same features
- Data export/import between
- Easy troubleshooting

### Time Investment
- Local: Already done (0 min)
- Supabase: 10 minutes
- Railway: 10 minutes
- Setup API URL: 2 minutes
- Total: ~22 minutes for full setup

### Monthly Cost
- **Supabase**: Free (up to 500MB)
- **Railway**: Free tier includes $5 credit/month
- **Total**: ~$5-10/month if you exceed limits

---

## QUICK LINKS

| Resource | URL |
|----------|-----|
| Local App | http://127.0.0.1:5000 |
| Supabase | https://supabase.com/dashboard |
| Railway | https://railway.app/dashboard |
| GitHub | https://github.com/YOUR-USERNAME/repo |

---

## NEXT STEPS

1. ✅ Local deployment working (you're here!)
2. ⏭️  **Follow Part 2.1-2.5 for live deployment**
3. ⏭️  Test both environments
4. ⏭️  Monitor and maintain

**You now have a fully functional application locally AND ready for live deployment!** 🎉

---

**Last Updated**: March 24, 2026  
**Status**: Production Ready ✅  
**Both Environments**: Fully Functional ✅

