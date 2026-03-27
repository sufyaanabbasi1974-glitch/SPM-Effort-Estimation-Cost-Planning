# 🚀 Vercel Deployment Guide for SPM System

## Overview
This guide walks you through deploying your SPM Effort Estimation System on Vercel.

**Architecture:**
- **Frontend (Vercel)**: HTML, CSS, JavaScript - hosted on Vercel CDN
- **Backend (Railway/Render)**: Flask API - deployed separately
- **Database (Supabase)**: PostgreSQL - cloud-hosted

---

## Prerequisites

- [ ] GitHub account with your project pushed
- [ ] Vercel account (free at https://vercel.com)
- [ ] Backend deployed on Railway or Render (or any service)
- [ ] Supabase PostgreSQL database
- [ ] Backend API URL (e.g., `https://your-api.railway.app`)

---

## Step 1: Prepare Your Repository

### 1.1 Make sure all files are committed
```bash
git add .
git commit -m "Prepare for Vercel deployment"
git push origin main
```

### 1.2 Verify folder structure
Your repo should have:
```
your-repo/
├── frontend/
│   ├── index.html
│   ├── login.html
│   ├── assets/
│   │   ├── css/
│   │   └── js/
│   └── ...
├── backend/
│   ├── app.py
│   ├── models.py
│   ├── requirements.txt
│   └── ...
├── vercel.json          ✅ (created)
├── .vercelignore        ✅ (created)
├── package.json         (optional, for build)
└── ...
```

---

## Step 2: Connect to Vercel

### 2.1 Sign in to Vercel
1. Go to https://vercel.com
2. Click "Sign Up" or "Log In"
3. Sign in with GitHub

### 2.2 Import Your Repository
1. Click "+ New Project" ➔ "Import Git Repository"
2. Select your GitHub repository
3. Vercel will auto-detect it as a web project

### 2.3 Configure Build Settings

**Important: Change the root directory!**

In the Vercel dashboard:
1. Under "Root Directory", click "Edit"
2. Change from `.` to `frontend/`
3. Leave "Build Command" empty (clear if auto-filled)
4. Leave "Output Directory" empty
5. Click "Save"

---

## Step 3: Set Environment Variables

### 3.1 Add Environment Variables in Vercel

In Vercel Project Settings ➔ "Environment Variables":

**Add these variables:**

| Key | Value | When to use |
|-----|-------|-----------|
| `API_BASE` | `https://your-backend-url.railway.app` | Production API URL |
| `API_BASE_DEV` | `http://localhost:5000` | Local development |

**Example values:**
- `API_BASE`: `https://spm-api.railway.app`
- `API_BASE_DEV`: `http://localhost:5000`

### 3.2 Update frontend/js/app.js

Update the API base URL configuration:

```javascript
// In frontend/js/app.js
const API_BASE = process.env.API_BASE || 'https://your-backend-url.railway.app';

// Or use this pattern:
const API_BASE = window.location.hostname === 'localhost' 
  ? 'http://localhost:5000'
  : 'https://your-backend-url.railway.app';
```

---

## Step 4: Configure CORS on Backend

### 4.1 Update Backend CORS Settings

In your `backend/app.py`, update CORS to allow Vercel domain:

```python
from flask_cors import CORS

# For production with Vercel
cors_origins = [
    'http://localhost:5000',
    'http://localhost:3000',
    'https://your-project.vercel.app',  # Your Vercel domain
    'https://*.vercel.app'  # Allow all Vercel deployments
]

if os.getenv('FLASK_ENV') == 'production':
    CORS(app, resources={r"/api/*": {"origins": cors_origins}})
else:
    CORS(app)
```

### 4.2 Deploy Backend Changes

Deploy the updated backend to Railway/Render first before deploying frontend to Vercel.

---

## Step 5: Deploy to Vercel

### 5.1 Deploy Automatically

**Option A: Deploy from Vercel Dashboard**
1. Go to your Vercel project
2. Click "Deploy" button
3. Wait for build to complete (~2-3 minutes)

**Option B: Deploy from Git Push**
Every push to your main branch will auto-deploy:
```bash
git push origin main
```

### 5.2 Monitor Deployment

1. Go to Deployments tab in Vercel
2. Watch the build progress
3. Once successful, click the preview URL
4. Test your application

---

## Step 6: Test Your Deployment

### 6.1 Test Frontend
Visit `https://your-project.vercel.app`:
- [ ] Page loads without errors
- [ ] UI displays correctly
- [ ] CSS styling works
- [ ] JavaScript console clear (F12)

### 6.2 Test API Connectivity
In browser console (F12):
```javascript
// Test API connection
fetch('https://your-backend-url/api/projects')
  .then(r => r.json())
  .then(data => console.log('API connected:', data))
  .catch(e => console.error('API error:', e))
```

### 6.3 Test Features
- [ ] Login works
- [ ] Create project
- [ ] Run effort estimation
- [ ] View results

---

## Troubleshooting

### Issue: "API Connection Failed"

**Solution:**
1. Check Backend URL in Environment Variables
2. Verify backend is running (visit the backend URL directly)
3. Check CORS settings in backend
4. Clear browser cache (Ctrl+Shift+Del)

```bash
# Test backend connectivity
curl https://your-backend-url/api/projects
```

### Issue: "404 - Page Not Found"

**Solution:**
1. Verify Root Directory is set to `frontend/`
2. Check vercel.json rewrites configuration
3. Redeploy: Go to Deployments ➔ Redeploy

### Issue: "Environment Variables Not Applied"

**Solution:**
1. Redeploy after adding env vars (they're not retroactive)
2. Give it 2-3 minutes for changes to take effect
3. Check if hardcoded URLs override env vars in code

### Issue: "Static Files Not Loading (CSS/JS)"

**Solution:**
1. Verify files are in `frontend/assets/` folder
2. Check paths in HTML are correct:
   ```html
   <link rel="stylesheet" href="/assets/css/style.css">
   <script src="/assets/js/app.js"></script>
   ```
3. Ensure Root Directory is `frontend/`

### Issue: "CORS Errors in Console"

**Solution:**
1. Update CORS in backend (see Step 4)
2. Add your Vercel domain: `https://your-project.vercel.app`
3. Redeploy backend
4. Wait 5 minutes and test again

---

## Custom Domain (Optional)

### Add Custom Domain
1. Go to Vercel Project Settings ➔ "Domains"
2. Add your custom domain (e.g., `spm-tool.com`)
3. Follow DNS configuration instructions
4. Update Backend CORS to include new domain

---

## Monitoring & Maintenance

### View Logs
Vercel Dashboard ➔ Logs:
- **Deployment**: Build logs
- **Function**: Runtime errors
- **Edge**: CDN activities

### Check Performance
Vercel Dashboard ➔ Analytics:
- View response times
- Check error rates
- Monitor bandwidth usage

### Roll Back Deployment
1. Go to Deployments tab
2. Find previous working deployment
3. Click "..." ➔ "Redeploy"

---

## Environment Configuration Summary

### Production (Vercel)
```
API_BASE=https://your-backend-url.railway.app
```

### Development (Local)
```
API_BASE=http://localhost:5000
```

### Test Locally Before Deploying
```bash
# Terminal 1: Start backend
cd backend
python run_waitress.py

# Terminal 2: Open frontend
# Open frontend/index.html in browser or use Live Server
```

---

## Quick Reference

| Task | Command/Location |
|------|-----------------|
| **Deploy** | Push to main branch or click Deploy in Vercel |
| **Check Status** | Vercel Dashboard ➔ Deployments |
| **View Logs** | Vercel Dashboard ➔ Logs |
| **Add Env Vars** | Vercel Project Settings ➔ Environment Variables |
| **Change Domain** | Vercel Project Settings ➔ Domains |
| **Rollback** | Vercel Dashboard ➔ Deployments ➔ Redeploy |

---

## Support

If you encounter issues:
1. Check browser console (F12) for errors
2. Check Vercel deployment logs
3. Test backend connectivity separately
4. Verify environment variables are set
5. Check CORS configuration

---

**Deployment Time:** ~5-10 minutes

**Status:** After deployment, your app is live at `https://your-project.vercel.app` ✅

