# 🔧 QUICK TROUBLESHOOTING GUIDE

## LOCAL ISSUES & FIXES

### ✗ Server won't start
```bash
# Check Python version
python --version
# Need: 3.11+

# If old version:
pip install --upgrade python
```

### ✗ Port 5000 already in use
```bash
# Windows - find what's using port 5000
netstat -ano | find "5000"

# Kill the process (replace PID)
taskkill /PID 12345 /F

# OR change port in app.py:
app.run(debug=True, host='0.0.0.0', port=5001)
```

### ✗ ModuleNotFoundError
```bash
# Install dependencies
cd backend
pip install -r requirements.txt
```

### ✗ Database error
```bash
# Delete and recreate database
cd project-root
rm database/spm_estimation.db
cd backend
python app.py  # Creates new DB
```

### ✗ Page shows blank/no output
```
Solution 1: Hard refresh browser
- Press: Ctrl+Shift+Delete (clear cache)
- Then: Ctrl+F5 (hard refresh)

Solution 2: Try incognito mode
- Ctrl+Shift+N (Chrome) or Ctrl+Shift+P (Firefox)
- Visit: http://127.0.0.1:5000

Solution 3: Check server logs
- Look at terminal running python app.py
- Should show GET /login if accessing page
```

### ✗ Login not working
```
Check:
1. Username field: admin
2. Password field: password
3. Browser console (F12): any errors?
4. Network tab (F12): failed requests?
```

### ✗ CSS/JS files not loading
```
Solution: Update paths in index.html and login.html
Change from: /css/style.css → /assets/css/style.css
Change from: /js/app.js → /assets/js/app.js

Already done! ✅
If still failing:
- Clear cache (Ctrl+Shift+Delete)
- Hard refresh (Ctrl+F5)
```

### ✗ Can't create project
```bash
Check browser console (F12):
- Tab: Console
- Look for red error messages
- Check exact error text

Check server terminal:
- Look for error logs
- Copy error message

Common causes:
1. Missing API_BASE (check app.js)
2. Invalid form input (blank fields?)
3. Server crashed (restart python app.py)
```

### ✗ Data not saving
```
Solution:
1. Refresh page (F5)
2. Check database exists: database/spm_estimation.db
3. Check server terminal for errors
4. Try creating again and watch console
```

---

## LIVE DEPLOYMENT ISSUES & FIXES

### ✗ Can't login to live app
```
Check:
1. Correct Railway URL entered?
2. DATABASE_URL set in Railway variables?
3. Supabase tables created?
4. Browser console (F12) for errors

Solution:
1. Check Railway dashboard > Variables
2. Verify: DATABASE_URL exists and is correct
3. Go to Supabase > Table Editor > check tables exist
4. Check Railway logs (Dashboard > Logs tab)
```

### ✗ 500 Internal Server Error
```
Solution:
1. Check Railway logs: Dashboard > Your Project > Logs
2. Look for Python error messages
3. Common causes:
   - DATABASE_URL missing
   - Database tables not created
   - Wrong connection string format
   - Supabase project offline

Fix:
1. Verify DATABASE_URL in Railway
2. Run SQL schema in Supabase
3. Check Supabase connection
4. Restart Railway deployment
```

### ✗ 404 Not Found errors
```
Solution:
1. Check if API_BASE URL is correct
2. File: frontend/js/app.js, line 4
3. Should be: https://YOUR-RAILWAY-URL.railway.app/api
4. NOT: http://localhost:5000/api

Fix:
1. Update API_BASE URL
2. Push to GitHub
3. Railways auto-deploys (wait 1-2 min)
4. Clear browser cache (Ctrl+Shift+Delete)
5. Hard refresh (Ctrl+F5)
```

### ✗ Static files not loading (404)
```
Solution:
1. Check /assets folder exists
2. Verify files: css/style.css, js/app.js exist
3. Clear browser cache (Ctrl+Shift+Delete)
4. Hard refresh (Ctrl+F5)

If still failing:
- Check Railway logs for errors
- Verify paths in HTML are correct
- Restart Railway deployment
```

### ✗ Database tables not found
```
Solution:
1. Go to Supabase > SQL Editor
2. Click "New query"
3. Paste the SQL schema (see LIVE_DEPLOYMENT_QUICK_START.md)
4. Click RUN
5. You should see 4 tables created

Verify:
1. Supabase > Table Editor
2. Check projects, estimations, risks, evm_tracking exist
```

### ✗ Can't connect to Supabase
```
Check connection string:
1. Should be: postgresql://postgres.xxxxx:PASSWORD@xxxxx.postgres.supabase.co:5432/postgres
2. Replace PASSWORD with actual password
3. Keep the format exact
4. No extra spaces

Test in Railway:
1. Set DATABASE_URL correctly
2. Check Supabase online (status.supabase.com)
3. Check your Supabase project hasn't hit limits
4. Try connecting from local first:
   - Add DATABASE_URL to local .env
   - python backend/app.py (should work if DB connection is valid)
```

### ✗ Railway deployment fails
```
Check:
1. Logs: Dashboard > Logs > Raw logs
2. Look for: "error", "failed", "exception"
3. Common issues:
   - Missing requirements.txt
   - Python syntax error
   - Failed to install dependencies

Solutions:
1. Check requirements-prod.txt exists
2. Verify Python code has no syntax errors
3. Ensure all imports can be found
4. Check file paths are correct

To debug:
1. Clone repo locally
2. Run: pip install -r requirements-prod.txt
3. Run: python backend/app.py
4. If it works locally, it will work on Railway
```

### ✗ Created project but can't see it
```
Check:
1. Did page say "Project created successfully"?
2. Check Supabase > Table Editor > projects table
3. See your project in database?

Solution:
1. Refresh page (F5)
2. Log out and back in
3. If still not visible:
   - Check browser console for errors
   - Check Railway logs
   - May need to restart Railway deployment
```

### ✗ App works locally but not live
```
Checklist:
1. API_BASE URL correct? (frontend/js/app.js line 4)
   ✓ LOCAL: http://localhost:5000/api
   ✓ LIVE: https://your-railway-url.railway.app/api

2. DATABASE_URL set in Railway?
   ✓ Visit Railway > Your Project > Variables
   ✓ Should be present and not empty

3. Supabase tables created?
   ✓ Supabase > Table Editor
   ✓ See projects, estimations, risks, evm_tracking?

4. Code pushed to GitHub?
   ✓ git push origin main
   ✓ Changes showing in GitHub repo?

5. Railway deployment complete?
   ✓ Dashboard > Logs
   ✓ See "Deployment completed successfully"?

After checking above:
- Clear cache (Ctrl+Shift+Delete)
- Hard refresh (Ctrl+F5)
- Test again
```

---

## DEBUGGING CHECKLIST

### When Something Breaks (Local)
```
1. Check server terminal
   Look for: error messages, invalid line numbers
   
2. Check browser console (F12)
   Tab: Console
   Look for: red error messages
   
3. Check Network tab (F12)
   Tab: Network
   Click request that failed
   See: response message details
   
4. Try: Ctrl+Shift+Delete (clear cache)
         Ctrl+F5 (hard refresh)
         
5. Restart server: Press Ctrl+C, then python app.py
```

### When Something Breaks (Live)
```
1. Check Railway logs
   Dashboard > Your Project > Logs
   Look for: error, failed, exception
   
2. Check Supabase logs
   Dashboard > Settings > Logs
   Look for: connection issues, failed queries
   
3. Check browser console (F12)
   Tab: Console
   Look for: error messages
   
4. Check browser Network tab (F12)
   Tab: Network  
   See which requests failed
   Click them for details
   
5. Try: Clear cache (Ctrl+Shift+Delete)
        Hard refresh (Ctrl+F5)
        Logout and back in
```

---

## FAST SOLUTIONS

| Issue | Fast Fix | Details |
|-------|----------|---------|
| Server won't start | `pip install -r requirements.txt` | Missing dependencies |
| Port in use | `netstat -ano \| find "5000"` | Find & kill process |
| Page blank | `Ctrl+Shift+Delete` + `Ctrl+F5` | Clear cache & refresh |
| 404 Not Found | Check API_BASE in app.js | Update with live URL |
| Database error | Delete `.db` file & restart | Recreate database |
| Login fails | Check username/password | Default: admin/password |
| CSS not loading | Check paths start with /assets | Already fixed! |
| 170 error | Check DATABASE_URL | Supabase connection string |
| Data not saving | Check server logs | Database connection issue |
| No requests showing | Hard refresh page | Browser cache issue |

---

## WHEN TO CONTACT SUPPORT

✅ **Can solve yourself:**
- Port already in use
- Missing modules
- Database errors
- Browser cache issues
- Static file paths
- Login credentials

❓ **Might need help:**
- Complex database issues
- Supabase quota limits
- Railway deployment failures
- Complex networking issues

📞 **Resources:**
- [Supabase Docs](https://supabase.com/docs)
- [Railway Docs](https://docs.railway.app)
- [Flask Docs](https://flask.palletsprojects.com)
- Project documentation files

---

## REMEMBER

- **First**: Check the documentation
- **Second**: Check the terminal logs
- **Third**: Check browser console
- **Fourth**: Google the error message
- **Last**: Restart everything (often works!)

**Most issues are:**
- ✓ Cache-related (= clear cache)
- ✓ Configuration (= check .env)
- ✓ Database (= check connection)
- ✓ Path issues (= check URLs)

---

**Good luck! You've got this!** 💪

