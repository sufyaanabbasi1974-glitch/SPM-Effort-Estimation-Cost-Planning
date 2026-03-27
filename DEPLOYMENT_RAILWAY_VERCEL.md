# 🚀 DEPLOYMENT SETUP: Railway Backend + Vercel Frontend

**Total Time: ~20 minutes**

This guide will deploy your SPM system:
- **Frontend**: Vercel (auto-deploy from GitHub)
- **Backend**: Railway (auto-deploy from GitHub)  
- **Database**: PostgreSQL on Railway

---

## Prerequisites

- ✅ GitHub account with code pushed
- ✅ Vercel account (free)
- ✅ Railway account (free)

---

## STEP 1: Get Code on GitHub (2 min)

```bash
cd "c:\Users\HP.DESKTOP-MNVUD8Q\Desktop\Web-based software effort estimation and cost planning system"

# Check status
git status

# Add all files
git add .

# Commit
git commit -m "Setup: Railway backend + Vercel frontend deployment"

# Push to GitHub
git push origin main
```

---

## STEP 2: Deploy Backend to Railway (7 min)

### 2.1: Go to Railway
- https://railway.app
- Click "Start a New Project"
- Sign in with GitHub

### 2.2: Deploy Backend
1. Click "+ New Project"
2. Select "Deploy from GitHub repo"
3. Find your repository
4. Select the main branch
5. Click "Deploy"

**Railway will auto-detect it's a Python app and deploy it!**

Wait 3-5 minutes for deployment to complete...

### 2.3: Railway Auto-Setup ✅
Railway automatically:
- ✅ Reads Procfile (gunicorn configuration)
- ✅ Installs requirements.txt
- ✅ Adds PostgreSQL database
- ✅ Sets DATABASE_URL environment variable
- ✅ Deploys your backend

### 2.4: Get Your Backend URL

In Railway dashboard:
1. Click your project
2. Click your backend service
3. Look for "Public URL" or "Domain"
4. **Copy it** (looks like: `https://spm-api-production.up.railway.app`)
5. **SAVE THIS - you'll need it for Vercel!**

### 2.5: Test Backend

Open in browser:
```
https://your-railway-url/api/projects
```

Should return: `[]` or `{"data": []}` ✅

---

## STEP 3: Deploy Frontend to Vercel (5 min)

### 3.1: Go to Vercel
- https://vercel.com/dashboard
- Sign in with GitHub (use same account)

### 3.2: Import Project
1. Click "+ Add New"
2. Click "Project"
3. Find your repository
4. Click "Import"

### 3.3: Configure Settings

**IMPORTANT: Set Root Directory!**

1. Find "Root Directory"
2. Click "Edit"
3. Type: `frontend`
4. Click "Save"

Leave Build Command and Output Directory empty.

### 3.4: Add Environment Variable

Before clicking "Deploy":

| Key | Value |
|-----|-------|
| `API_BASE` | `https://your-railway-url` |

Replace with actual URL from Railway dashboard.

Example:
```
API_BASE: https://spm-api-production.up.railway.app
```

### 3.5: Deploy!

Click "Deploy" button.

Wait 2-3 minutes...

### ✅ Success!
- You'll see "Congratulations! Your project has been deployed"
- Click the preview URL to see your live app
- Your app is at: `https://your-project.vercel.app`

---

## STEP 4: Configure CORS (2 min)

Your backend needs to allow requests from Vercel.

In Railway dashboard:
1. Go to backend service
2. Click "Variables" or "Environment"
3. Find `CORS_ORIGINS` variable (might not exist yet)
4. If it doesn't exist:
   - Click "+ Add Variable"
   - Name: `CORS_ORIGINS`
   - Value: `https://your-project.vercel.app`
5. Click "Save"

Railway will auto-redeploy with the new setting.

---

## STEP 5: Test Everything (3 min)

### Test 1: Frontend Loads
Visit `https://your-project.vercel.app`
- ✅ Page loads
- ✅ No 404 errors
- ✅ Styling looks good

### Test 2: API Works
Open browser console (F12) and run:
```javascript
fetch('https://your-railway-backend-url/api/projects')
  .then(r => r.json())
  .then(data => console.log('✅ Success:', data))
  .catch(e => console.error('❌ Error:', e))
```

Should show: `✅ Success: []`

### Test 3: Try Features
- Login with test credentials
- Create a project
- Run effort estimation
- Verify calculations work

---

## 🎉 DEPLOYMENT COMPLETE!

Your app is now LIVE:

| Component | URL |
|-----------|-----|
| **Frontend** | `https://your-project.vercel.app` |
| **Backend API** | `https://your-railway-backend-url` |
| **Database** | PostgreSQL (auto-created on Railway) |

---

## 📝 Your URLs (Save These)

```
Frontend: https://your-project.vercel.app
Backend: https://your-railway-url
```

---

## 🔄 Future Updates

When you make code changes:

```bash
# 1. Make changes locally
# 2. Commit and push
git add .
git commit -m "Your changes"
git push origin main

# 3. Both Vercel and Railway auto-deploy within 1-2 minutes!
```

---

## 🆘 Troubleshooting

### Frontend shows 404
- Check Root Directory is `frontend` in Vercel
- Go to Vercel Deployments and Redeploy

### API Connection Fails
- Verify `API_BASE` env variable in Vercel is correct
- Test Railway URL directly: `https://your-url/api/projects`
- Check Railway backend logs for errors

### CORS Errors in Console
- Verify `CORS_ORIGINS` in Railway includes your Vercel domain
- Wait 2 minutes for change to apply
- Try again

### Styling Broken
- Clear browser cache: Ctrl+Shift+Del
- Hard refresh: Ctrl+F5
- Check paths are `/assets/css/style.css`

### Backend Won't Deploy
- Check Railway deployment logs for errors
- Common issues:
  - `Procfile` missing or incorrect
  - `requirements.txt` incomplete
  - DATABASE_URL not set

---

## 📊 Dashboard Links

| Service | Link |
|---------|------|
| **Vercel Dashboard** | https://vercel.com/dashboard |
| **Railway Projects** | https://railway.app/dashboard |
| **Your GitHub Repo** | GitHub.com (your repo) |

---

**Status: ✅ READY TO DEPLOY**

Follow the steps above and you'll be live in 20 minutes! 🚀
