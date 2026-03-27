# ✅ Vercel Deployment Checklist

Complete these steps in order to deploy your SPM system to Vercel.

## Pre-Deployment (Local)

### Code Preparation
- [ ] All code committed to GitHub
- [ ] No uncommitted changes (`git status` is clean)
- [ ] Branch is `main` or desired deployment branch
- [ ] Latest code pushed to GitHub

### Verify Configuration
- [ ] `vercel.json` exists in root directory
- [ ] `.vercelignore` exists in root directory
- [ ] `frontend/` folder structure is correct:
  - [ ] `frontend/index.html` exists
  - [ ] `frontend/login.html` exists
  - [ ] `frontend/assets/` folder exists with CSS and JS

### Backend Ready
- [ ] Backend deployed (Railway/Render/other)
  - [ ] Backend URL is accessible: `https://your-backend-url/api/projects`
  - [ ] CORS configured in backend to allow your domain
  - [ ] Database (Supabase) is connected and working

## Vercel Setup

### Create Vercel Project
- [ ] Signed up at https://vercel.com
- [ ] Connected GitHub account
- [ ] Imported repository

### Configure Vercel
- [ ] Set Root Directory to `frontend/`
- [ ] Build Command is empty (or auto)
- [ ] Output Directory is empty (or auto)
- [ ] Added Environment Variable `API_BASE=https://your-backend-url`

### Deploy
- [ ] Clicked "Deploy" or pushed to main branch
- [ ] Waited for deployment to complete
- [ ] Deployment shows success (green checkmark)

## Post-Deployment (Testing)

### Frontend Verification
- [ ] Visit `https://your-project.vercel.app`
- [ ] Page loads without errors
- [ ] All CSS and styling appears correct
- [ ] All images load properly
- [ ] Responsive design works on mobile

### API Connectivity
- [ ] Open browser console (F12)
- [ ] Run test:
  ```javascript
  fetch('https://your-backend-url/api/projects')
    .then(r => r.json())
    .then(data => console.log('Success:', data))
    .catch(e => console.error('Error:', e))
  ```
- [ ] No CORS errors in console
- [ ] Response shows data or empty array

### Feature Testing
- [ ] Login page loads
- [ ] Can enter credentials
- [ ] Project creation form displays
- [ ] Can create a new project
- [ ] API calls return data
- [ ] Calculations run without errors

### Browser Console Check
- [ ] No red errors in console
- [ ] No CORS warnings
- [ ] No 404 errors for assets
- [ ] No API timeout errors

## Update Backend (if needed)

### CORS Configuration
- [ ] Add Vercel domain to CORS allowed origins
  ```python
  'https://your-project.vercel.app'
  ```
- [ ] Redeploy backend
- [ ] Wait 5 minutes for changes to take effect

## Live & Monitoring

### Domain Setup (Optional)
- [ ] Added custom domain in Vercel
- [ ] DNS configured
- [ ] SSL certificate active

### Monitoring Active
- [ ] Check Vercel Analytics regularly
- [ ] Monitor error rates
- [ ] Check build times

## Troubleshooting Checklist

If something isn't working:

### 404 / Page Not Found
- [ ] Root Directory is set to `frontend/` (not root)
- [ ] `vercel.json` rewrites are correct
- [ ] Redeploy the project

### API Not Connecting
- [ ] Backend URL in Environment Variables is correct
- [ ] Backend is running and accessible
- [ ] CORS enabled in backend
- [ ] Added your Vercel domain to CORS
- [ ] Check browser console for specific errors
- [ ] Test `curl https://your-backend-url/api/projects`

### CSS/JS Not Loading
- [ ] Check paths in HTML are `/assets/css/style.css`
- [ ] Root Directory is `frontend/`
- [ ] Clear browser cache (Ctrl+Shift+Del)
- [ ] Hard refresh page (Ctrl+F5)

### Environment Variables Not Applied
- [ ] Redeploy after adding env vars
- [ ] Wait 2-3 minutes for propagation
- [ ] High restart on the deployment

---

## Quick Links

| Item | Link |
|------|------|
| Vercel Dashboard | https://vercel.com/dashboard |
| Your Project | https://your-project.vercel.app |
| Project Settings | https://vercel.com/dashboard/[project-name]/settings |
| Deployments | https://vercel.com/dashboard/[project-name]/deployments |
| Analytics | https://vercel.com/dashboard/[project-name]/analytics |

---

**Status:** Ready to deploy! 🚀

Follow the Vercel Deployment Guide for detailed instructions:
📖 `VERCEL_DEPLOYMENT_GUIDE.md`
