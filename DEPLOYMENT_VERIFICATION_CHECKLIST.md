# ✅ DEPLOYMENT CHECKLIST

Use this before and after deployment to verify everything.

---

## PRE-DEPLOYMENT

### Code Ready
- [ ] All changes committed locally
- [ ] Code pushed to GitHub (`git push origin main`)
- [ ] Verify: Visit GitHub repo to confirm files are there

### Accounts Created
- [ ] GitHub account with repo
- [ ] Railway account (https://railway.app)
- [ ] Vercel account (https://vercel.com)

### Configuration Files Ready
- [ ] `vercel.json` exists (Vercel config)
- [ ] `.vercelignore` exists (Files to ignore)
- [ ] `Procfile` exists (Railway backend config)
- [ ] `requirements.txt` complete (Python dependencies)

---

## RAILWAY BACKEND DEPLOYMENT

### During Deployment
- [ ] Selected GitHub repository
- [ ] Railway detected Python/Flask app
- [ ] Build started
- [ ] Build logs scrolling past
- [ ] No red errors in logs

### After Deployment
- [ ] Deployment shows "Success" ✅
- [ ] Can see "Public URL" or "Domain"
- [ ] Backend URL copied and saved

### Test Backend
- [ ] Open: `https://your-railway-url/api/projects` in browser
- [ ] Returns JSON (empty array or data) ✅
- [ ] No 500 errors

---

## VERCEL FRONTEND DEPLOYMENT

### During Setup
- [ ] Selected GitHub repository
- [ ] **Root Directory set to `frontend/`** (CRITICAL!)
- [ ] Build Command: empty
- [ ] Output Directory: empty
- [ ] Environment Variable `API_BASE` added with Railway URL

### During Deployment
- [ ] "Building..." shows progress
- [ ] Build completes without errors
- [ ] "Deployments" shows green checkmark

### After Deployment
- [ ] Deployment successful page shows
- [ ] Can click preview URL
- [ ] Vercel gives you: `https://your-project.vercel.app`
- [ ] Frontend URL copied and saved

---

## CORS CONFIGURATION

### Update Backend for Vercel
- [ ] Go to Railway backend service
- [ ] Go to "Variables"
- [ ] Add or update `CORS_ORIGINS`
- [ ] Set value: `https://your-project.vercel.app`
- [ ] Railway shows it's redeploying ✅

---

## POST-DEPLOYMENT TESTING

### Frontend Tests
- [ ] Visit `https://your-project.vercel.app`
- [ ] Page loads (no 404)
- [ ] Styling displays correctly
- [ ] All images load
- [ ] Responsive design works on mobile
- [ ] No red errors in browser console (F12)

### API Connectivity
- [ ] Open browser console (F12)
- [ ] Run test (copy-paste this):
  ```javascript
  fetch('https://your-railway-url/api/projects')
    .then(r => r.json())
    .then(data => console.log('✅ API Works:', data))
    .catch(e => console.error('❌ Error:', e))
  ```
- [ ] See `✅ API Works:` message (not an error)

### Application Features
- [ ] Login page displays
- [ ] Can see navigation
- [ ] Project input form works
- [ ] Can create a project (if database working)
- [ ] Effort estimation calculates
- [ ] Results display
- [ ] No API errors in console

---

## LIVE VERIFICATION

### URLs Working
- [ ] Frontend: `https://your-project.vercel.app` ✅
- [ ] Backend: `https://your-railway-url/api/projects` ✅
- [ ] Both accessible from anywhere

### Auto-Deploy Working
- [ ] Made small code change locally
- [ ] Pushed to GitHub (`git push origin main`)
- [ ] Vercel auto-deployed (1-2 minutes)
- [ ] Change visible on live site ✅

---

## TROUBLESHOOTING CHECKS

If something isn't working:

### Frontend 404 Error
- [ ] Vercel Root Directory is `frontend/` (not `.`)
- [ ] Go to Vercel Deployments
- [ ] Click "Redeploy"

### API Connection Failed
- [ ] Railway backend is running
- [ ] Test URL directly in browser
- [ ] Check `API_BASE` environment variable in Vercel
- [ ] Verify it matches your Railway URL exactly

### CORS Errors
- [ ] Railway `CORS_ORIGINS` includes Vercel domain
- [ ] Changed value 2+ minutes ago
- [ ] Railway shows redeployment complete

### Styling/CSS Issues
- [ ] Hard refresh: Ctrl+F5
- [ ] Clear cache: Ctrl+Shift+Del
- [ ] Check paths: `/assets/css/style.css`

### Database Issues
- [ ] Railway shows PostgreSQL service is running
- [ ] Error logs in Railway don't show SQL errors
- [ ] LOCAL test works to verify app logic

---

## SUCCESS CHECKLIST ✅

If all of these are checked:
- ✅ Frontend deploys to Vercel
- ✅ Backend deploys to Railway  
- ✅ Both services auto-deploy on GitHub push
- ✅ Frontend loads without errors
- ✅ API connects and returns data
- ✅ All features work

**YOUR DEPLOYMENT IS COMPLETE AND WORKING!** 🎉

---

**Status: READY TO USE** 🚀
