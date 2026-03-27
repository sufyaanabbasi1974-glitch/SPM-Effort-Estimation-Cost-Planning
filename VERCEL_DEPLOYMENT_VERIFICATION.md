# Vercel Deployment Verification Guide

## ✅ Backend Status (Railway)
- **URL**: `https://web-production-38264.up.railway.app`
- **Status**: ✅ Working
- **Test Endpoints**:
  - `GET https://web-production-38264.up.railway.app/api/projects` → Returns project list
  - `POST https://web-production-38264.up.railway.app/api/login` → Accepts credentials

---

## ✅ Frontend Configuration (Vercel)
Files are now properly configured:

- **`frontend/index.html`**:
  - ✅ `<meta name="api-base">` set to Railway URL
  - ✅ Dynamic API_BASE detection with fallback
  - ✅ `/home` redirect to `/` included
  - ✅ Enhanced console logging for diagnostics

- **`frontend/login.html`**:
  - ✅ `<meta name="api-base">` added
  - ✅ Same API_BASE detection as index
  - ✅ Login form sends POST to `${API_BASE}/api/login` with credentials

- **`frontend/js/app.js`**:
  - ✅ All API calls use `API_BASE` variable
  - ✅ All fetch requests include `credentials: 'include'` for CORS cookies
  - ✅ Auth check uses `${API_BASE}/api/user`

- **`backend/app.py`**:
  - ✅ CORS enabled with `supports_credentials=True`
  - ✅ Default CORS origins include Vercel domain
  - ✅ All `/api/*` endpoints accessible

---

## 🧪 How to Test on Vercel

### Step 1: Deploy to Vercel
```bash
git add .
git commit -m "Fix: Complete Vercel + Railway API integration"
git push
```

### Step 2: Open Vercel App
Visit: `https://spm-effort-estimation-cost-planning.vercel.app`

### Step 3: Check Browser Console
Press `F12` → Console tab. You should see:
```
=== Login Page Initialized ===
Meta API Base: https://web-production-38264.up.railway.app
Stored API Base: null (or stored value)
API_BASE final: https://web-production-38264.up.railway.app
Login will POST to: https://web-production-38264.up.railway.app/api/login
```

### Step 4: Attempt Login
- **Username**: `admin`
- **Password**: `password`

### Step 5: Check Network Tab
Press `F12` → Network tab. After login:
1. Request to `https://web-production-38264.up.railway.app/api/login`
   - Status should be `200` (success) or `401` (wrong credentials)
   - Response should include `Set-Cookie` for session
2. Request to `https://web-production-38264.up.railway.app/api/user`
   - Status should be `200`
   - Response includes username

### Step 6: Test Features
Click any feature button (Effort Estimation, Cost Planning, etc.):
- Should load projects from Railway backend
- Should calculate and display results
- Network requests should all go to `https://web-production-38264.up.railway.app/api/*`

---

## 🔍 Troubleshooting

### Issue: "API calls return 404"
**Solution**: Confirm Railway backend is running and accessible at `https://web-production-38264.up.railway.app/api/projects`

### Issue: "Login returns 401 (credentials rejected)"
**Possible causes**:
1. Demo credentials are incorrect (should be `admin` / `password`)
2. Backend authentication hash mismatch
3. Check Railway logs for auth errors

**Solution**:
- Verify `VALID_USERS_HASHED` in `backend/app.py`
- Re-hash password if needed using Flask werkzeug

### Issue: "Features load but return empty or error"
**Possible causes**:
1. Database not initialized on Railway
2. Project list is empty (need to create a project first)
3. CORS origin mismatch

**Solution**:
- Create a test project after logging in
- Check Railway PostgreSQL/SQLite connection string
- Verify `CORS_ORIGINS` environment variable includes Vercel domain

### Issue: "Console shows 'APIbase set to http://127.0.0.1:5000'"
**Cause**: Meta tag not loaded correctly

**Solution**:
- Hard refresh browser (Ctrl+Shift+R or Cmd+Shift+R)
- Clear browser cache: DevTools → Storage → Clear All

### Issue: "Cross-Origin Request Blocked (CORS error)"
**Cause**: CORS credentials not being sent or backend CORS config missing

**Solution**:
- Ensure all fetch calls include `credentials: 'include'`
- ✅ Already done in latest code
- Verify backend CORS header: `Access-Control-Allow-Credentials: true`

---

## 📋 Deployment Checklist

Before marking deployment complete:

- [ ] Vercel deployment successful (no build errors)
- [ ] Console shows correct `API_BASE` URL
- [ ] Login page loads and credentials accepted
- [ ] After login, can see feature cards
- [ ] Clicking "Effort Estimation" loads project dropdown
- [ ] Can create a new project
- [ ] Can select project and calculate estimation
- [ ] All network requests go to Railway backend
- [ ] No CORS or 401 errors in console
- [ ] `/home` URL works same as `/`

---

## 🚀 Full Feature Checklist

Once Vercel login works, test each module:

1. **Project Input**: ✓ Create a project
2. **Effort Estimation**: ✓ Select project, calculate COCOMO
3. **Schedule & Cost**: ✓ View Gantt chart and cost breakdown
4. **Risk Management**: ✓ Add risks, apply adjustments
5. **EVM Tracking**: ✓ Enter PV/EV/AC, see metrics
6. **Dashboard**: ✓ View project summary
7. **Reports**: ✓ Generate PDF/export report

---

## 📞 Next Steps

1. **Deploy to Vercel** with latest changes
2. **Test login flow** and check console output
3. **Report any errors** with screenshots
4. **Confirm all modules work** as they do locally

If you encounter issues, share:
- Browser console output (screenshot)
- Network tab request/response (screenshot)
- Step where it fails (e.g., "login succeeds but Effort Estimation returns 500")

---

**Status**: ✅ Ready for Vercel deployment
