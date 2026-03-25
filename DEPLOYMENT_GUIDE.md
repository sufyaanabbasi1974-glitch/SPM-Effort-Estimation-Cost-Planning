# Deployment Guide: Supabase + Railway

## Overview
This guide walks you through deploying the SPM Effort Estimation System to Supabase (PostgreSQL database) and Railway (Backend hosting).

## Step 1: Set Up Supabase

### 1.1 Create a Supabase Project
1. Go to [https://supabase.com](https://supabase.com)
2. Click "Start Your Project"
3. Sign up with your email
4. Create a new project:
   - **Project Name**: `spm-estimation-system`
   - **Database Password**: Save this securely
   - **Region**: Choose closest to your location

### 1.2 Get Your Connection Details
1. In Supabase dashboard, go to **Settings > Database**
2. Copy the connection string (PostgreSQL URL)
3. Format: `postgresql://username:password@host:port/database`

### 1.3 Create Database Schema
1. In Supabase, go to **SQL Editor**
2. Run the SQL initialization script (see below)

## Step 2: Configure Environment Variables

Create a `.env` file in the backend folder:

```
# Database Configuration
DATABASE_URL=postgresql://username:password@host:5432/postgres

# Flask Configuration
FLASK_ENV=production
SECRET_KEY=your-super-secret-key-change-this
DEBUG=False

# Server Configuration
PORT=5000
WORKERS=4
```

## Step 3: Update Flask Configuration

The `app.py` has been updated to:
- Use PostgreSQL for production
- Support both SQLite (dev) and PostgreSQL (prod)
- Automatically detect the environment

## Step 4: Install Dependencies

```bash
cd backend
pip install -r requirements-prod.txt
```

## Step 5: Deploy Backend to Railway

### 5.1 Create Railway Account
1. Go to [https://railway.app](https://railway.app)
2. Sign up with GitHub
3. Create a new project

### 5.2 Connect Repository
1. Click "New Project"
2. Select "Deploy from GitHub"
3. Select your repository
4. Select the branch to deploy

### 5.3 Add Environment Variables
1. In Railway dashboard, click "Variables"
2. Add all variables from `.env`:
   - `DATABASE_URL`
   - `FLASK_ENV=production`
   - `SECRET_KEY`

### 5.4 Configure Build
1. Set build command: `pip install -r backend/requirements-prod.txt`
2. Set start command: `cd backend && waitress-serve --port=$PORT app:app`

### 5.5 Deploy
Railway will automatically deploy when you push to GitHub.

## Step 6: Update Frontend

### 6.1 Update API Base URL
In `frontend/js/app.js`, update the API_BASE:

```javascript
// Change from:
const API_BASE = 'http://localhost:5000/api';

// To:
const API_BASE = 'https://your-railway-app-url.railway.app/api';
```

### 6.2 Deploy Frontend (Optional)

**Option A: Vercel (Recommended)**
```bash
npm install -g vercel
cd frontend
vercel
```

**Option B: Railway**
1. Create `frontend/index.js`:
```javascript
const express = require('express');
const app = express();
const path = require('path');

app.use(express.static(__dirname));
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

app.listen(process.env.PORT || 3000);
```

2. Create `package.json`:
```json
{
  "name": "spm-frontend",
  "version": "1.0.0",
  "scripts": {
    "start": "node index.js"
  }
}
```

## Step 7: Database Migration Script

Run this SQL in Supabase SQL Editor to create all tables:

```sql
-- Create projects table
CREATE TABLE projects (
  id SERIAL PRIMARY KEY,
  project_name VARCHAR(255) NOT NULL,
  project_type VARCHAR(50) NOT NULL,
  kloc FLOAT NOT NULL,
  cost_per_person_month FLOAT NOT NULL,
  team_experience VARCHAR(50) NOT NULL,
  created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
  created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
  tracking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX idx_estimations_project ON estimations(project_id);
CREATE INDEX idx_risks_project ON risks(project_id);
CREATE INDEX idx_evm_project ON evm_tracking(project_id);
```

## Step 8: Verify Deployment

1. Visit your Railway app URL
2. You should see the login page
3. Login with:
   - Username: `admin`
   - Password: `password`
4. Create a test project to verify database connection

## Troubleshooting

**Database Connection Error**
- Check `DATABASE_URL` format in environment variables
- Verify Supabase project is active
- Check firewall/IP restrictions in Supabase settings

**Frontend API Errors**
- Ensure API_BASE URL is correct in `app.js`
- Check CORS settings in `app.py`
- Verify Railway backend is running

**Static Files Not Loading**
- Clear browser cache (Ctrl+Shift+Delete)
- Ensure `/assets` folder exists in frontend
- Check CSS/JS file paths in HTML

## Production Checklist

- [ ] Database backup enabled in Supabase
- [ ] Environment variables configured in Railway
- [ ] CORS properly configured for your domain
- [ ] Static files serving correctly
- [ ] Authentication working
- [ ] HTTPS enabled
- [ ] Error logging configured
- [ ] Database indexes created

## Support

For issues, check:
1. Railway logs: Dashboard > Logs
2. Supabase logs: Database > Logs
3. Browser console (F12)
4. Network tab for API requests

---

**Deployment URL**: Will be assigned by Railway  
**Database**: Supabase PostgreSQL  
**Frontend**: Same Railway instance or Vercel
