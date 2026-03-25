# Supabase Setup Guide - Step by Step

## What is Supabase?
Supabase is an open-source Firebase alternative that provides:
- PostgreSQL database (free tier: 500MB storage, unlimited api requests)
- Built-in authentication
- Real-time subscriptions
- Instant APIs

## Prerequisites
- GitHub account (for deploying via Railway)
- Email for Supabase account
- This project repository

---

## Part 1: Create Supabase Account & Database

### Step 1: Sign Up
1. Go to [https://supabase.com/dashboard](https://supabase.com/dashboard)
2. Click **"Start your project"**
3. Sign up with your email or GitHub
4. Click **"I'll start with Supabase"**

### Step 2: Create Organization
1. Enter Organization name: `spm-estimation`
2. Click **"Create new organization"**

### Step 3: Create Project
1. Click **"New Project"** button
2. Fill in:
   - **Name**: `spm-estimation-prod`
   - **Database Password**: `SecurePassword123!` (save this!)
   - **Region**: Select closest to you
   - **Pricing Plan**: Free (sufficient for this project)
3. Click **"Create new project"** (wait 2-3 minutes for setup)

### Step 4: Get Connection String
1. After project is created, go to **Settings** (gear icon)
2. Navigate to **Database**
3. Under "Connection string", select **"PostgreSQL"**
4. Copy the connection string - it looks like:
   ```
   postgresql://postgres.xxxxx:PASSWORD@xxxxx.postgres.supabase.co:5432/postgres
   ```
5. **Replace PASSWORD with the password you set in Step 3**
6. Save this URL - you'll need it soon

### Step 5: Create Database Tables
1. In Supabase dashboard, go to **SQL Editor** (left sidebar)
2. Click **"New query"**
3. Paste this SQL script:

```sql
-- Create projects table
CREATE TABLE projects (
  id SERIAL PRIMARY KEY,
  project_name VARCHAR(255) NOT NULL,
  project_type VARCHAR(50) NOT NULL CHECK (project_type IN ('Organic', 'Semi-Detached', 'Embedded')),
  kloc FLOAT NOT NULL CHECK (kloc > 0),
  cost_per_person_month FLOAT NOT NULL CHECK (cost_per_person_month > 0),
  team_experience VARCHAR(50) NOT NULL CHECK (team_experience IN ('Junior', 'Intermediate', 'Senior')),
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
  selected_model VARCHAR(50) DEFAULT 'Basic' CHECK (selected_model IN ('Basic', 'Intermediate')),
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
  probability FLOAT CHECK (probability >= 0 AND probability <= 1),
  impact FLOAT CHECK (impact >= 0 AND impact <= 1),
  adjustment_factor FLOAT DEFAULT 1.0,
  description TEXT
);

-- Create evm_tracking table
CREATE TABLE evm_tracking (
  id SERIAL PRIMARY KEY,
  project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
  planned_value FLOAT DEFAULT 0,
  earned_value FLOAT DEFAULT 0,
  actual_cost FLOAT DEFAULT 0,
  cost_variance FLOAT,
  schedule_variance FLOAT,
  cost_performance_index FLOAT,
  schedule_performance_index FLOAT,
  project_status VARCHAR(20) DEFAULT 'Green' CHECK (project_status IN ('Green', 'Yellow', 'Red')),
  percentage_complete FLOAT DEFAULT 0.0 CHECK (percentage_complete >= 0 AND percentage_complete <= 100),
  tracking_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX idx_estimations_project ON estimations(project_id);
CREATE INDEX idx_risks_project ON risks(project_id);
CREATE INDEX idx_evm_project ON evm_tracking(project_id);
CREATE INDEX idx_projects_created ON projects(created_date DESC);

-- Enable Row Level Security (optional but recommended)
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;
ALTER TABLE estimations ENABLE ROW LEVEL SECURITY;
ALTER TABLE risks ENABLE ROW LEVEL SECURITY;
ALTER TABLE evm_tracking ENABLE ROW LEVEL SECURITY;

-- Create policies (allow all for now)
CREATE POLICY "allow_all_projects" ON projects FOR ALL USING (true);
CREATE POLICY "allow_all_estimations" ON estimations FOR ALL USING (true);
CREATE POLICY "allow_all_risks" ON risks FOR ALL USING (true);
CREATE POLICY "allow_all_evm" ON evm_tracking FOR ALL USING (true);
```

4. Click **"RUN"** button to execute
5. You should see a success message

### Step 6: Verify Tables Created
1. In left sidebar, click **"Table Editor"**
2. You should see:
   - `projects`
   - `estimations`  
   - `risks`
   - `evm_tracking`

---

## Part 2: Update Local Project Configuration

### Step 1: Update Environment File
1. Open `.env` file in your project root
2. Add this line (replace with your actual connection string):
```
DATABASE_URL=postgresql://postgres.xxxxx:PASSWORD@xxxxx.postgres.supabase.co:5432/postgres
```

### Step 2: Install PostgreSQL Driver
```bash
cd backend
pip install -r requirements-prod.txt
```

### Step 3: Test Local Connection
```bash
cd backend
python -c "from app import app; from models import db; 
with app.app_context(): db.create_all(); print('Database tables created!')"
```

---

## Part 3: Deploy to Railway

### Step 1: Push to GitHub
If not already done:
```bash
git add .
git commit -m "Setup for Supabase deployment"
git push origin main
```

### Step 2: Create Railway Account
1. Go to [https://railway.app](https://railway.app)
2. Sign up with GitHub
3. Authorize Railway to access your GitHub

### Step 3: Create New Project
1. In Railway dashboard, click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Select your repository
4. Select `main` branch

### Step 4: Configure Environment Variables
1. In Railway dashboard, click **"Variables"**
2. Add these variables:
   - `DATABASE_URL`: Your Supabase connection string
   - `FLASK_ENV`: `production`
   - `SECRET_KEY`: Generate a random string (use `python -c "import secrets; print(secrets.token_hex(32))"`)

3. Click **"Save"**

### Step 5: Configure Build Settings
1. Click **"Settings"** tab
2. Set:
   - **Build Command**: `pip install -r backend/requirements-prod.txt`
   - **Start Command**: `python run_waitress.py`
3. Click **"Save"**

### Step 6: Deploy
1. Click **"Deploy"** button
2. Railway will automatically build and deploy
3. After ~2 minutes, you'll see a public URL

### Step 7: Get Your Public URL
1. In Railway dashboard, look for **"Domains"** section
2. You'll see something like: `your-app.railway.app`
3. Visit `https://your-app.railway.app` to test

---

## Part 4: Update Frontend for Production

### Step 1: Update API Base URL
1. Open `frontend/js/app.js`
2. Replace this line (near the top):
```javascript
const API_BASE = 'http://localhost:5000/api';
```

With:
```javascript
const API_BASE = 'https://your-railway-url.railway.app/api';
```

### Step 2: Rebuild Frontend
1. Push changes to GitHub
2. Railway will automatically rebuild and deploy

### Step 3: Test
1. Visit your Railway URL
2. You should see the login page
3. Login with:
   - Username: `admin`  
   - Password: `password`
4. Create a test project to verify everything works

---

## Troubleshooting

### Issue: "Connection refused" when accessing app
**Solution:**
- Check Railway logs: Dashboard > Logs tab
- Verify DATABASE_URL is correct in variables
- Check if app crashed (red "×" icon)

### Issue: Database tables not found
**Solution:**
- Run SQL schema script again in Supabase
- Verify you're using the correct DATABASE_URL
- Check table names in Supabase Table Editor

### Issue: CORS errors in browser console
**Solution:**
- The Flask app has CORS enabled
- Check if API_BASE URL in app.js matches Railway URL
- Clear browser cache (Ctrl+Shift+Delete)

### Issue: Static files returning 404
**Solution:**
- Ensure `/assets` folder structure is correct
- Files should be at: `frontend/assets/css/style.css` and `frontend/assets/js/app.js`
- Check file paths in index.html for typos

### Issue: Login not working
**Solution:**
- Check DATABASE_URL is using PostgreSQL (starts with `postgresql://`)
- Verify users table exists in Supabase
- Check browser console for actual error message

---

## Monitoring & Maintenance

### View Logs
**Railway Logs:**
1. Dashboard > select project > Logs tab
2. Use search filter for errors

**Supabase Logs:**
1. Dashboard > Settings > Database > Logs
2. View query performance and errors

### Backup Database
**Supabase Backups:**
1. Go to Settings > Backups
2. Manual backups are available
3. Daily automatic backups included

### Monitor Usage
1. Supabase dashboard shows storage and API calls
2. Free tier: 500MB storage, unlimited API calls
3. Upgrade if needed from Settings

---

## Cost Breakdown (as of 2024)
- **Supabase (PostgreSQL)**: Free (up to 500MB)
- **Railway Backend**: Free tier available, ~$7/month for production
- **Total**: Free to ~$7/month

---

## Next Steps

✅ Supabase database ready  
✅ Flask backend deployed on Railway  
✅ Frontend also deployed  
✅ Monitoring in place  

You're all set for production use! 🎉

