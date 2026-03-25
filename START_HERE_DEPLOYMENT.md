# 🚀 Deployment Quick Reference

## In 3 Simple Steps:

### Step 1: Prepare Database (10 min)
```
1. Go to https://supabase.com/dashboard
2. Create new project
3. Copy connection string from Settings > Database
4. Run SQL schema from SUPABASE_SETUP.md in SQL Editor
```

### Step 2: Configure Environment (5 min)
```
1. Open .env file
2. Set: DATABASE_URL=your_supabase_connection_string
3. Set: FLASK_ENV=production
4. Generate SECRET_KEY: python -c "import secrets; print(secrets.token_hex(32))"
5. Set: SECRET_KEY=your_generated_key
```

### Step 3: Deploy (10 min)
```
1. Push to GitHub: git add . && git commit -m "Deploy" && git push
2. Go to https://railway.app
3. Create new project from your GitHub repo
4. Add environment variables (DATABASE_URL, FLASK_ENV, SECRET_KEY)
5. Railway auto-deploys! 
6. Get your URL from Railway dashboard
7. Update API_BASE in frontend/js/app.js
8. Done! Visit your-app.railway.app
```

---

## Files to Read (In Order)

1. **SUPABASE_SETUP.md** ← START HERE
   - Complete Supabase setup with screenshots
   - SQL schema to run
   - Connection string setup

2. **PRODUCTION_DEPLOYMENT.md** ← READ NEXT
   - Full deployment overview
   - Architecture diagram
   - Security checklist
   - Troubleshooting guide

3. **DEPLOYMENT_GUIDE.md** ← REFERENCE
   - Detailed step-by-step instructions
   - Cost breakdown
   - Additional deployment options

---

## Testing Your Deployment

After deployment:
```
1. Visit https://your-app.railway.app
2. Login: admin / password
3. Create a test project:
   - Name: Test
   - Type: Semi-Detached
   - Size: 50 KLOC
   - Cost: $5000/month
   - Experience: Intermediate
4. Click "Calculate Basic COCOMO"
5. Expected: ~24 months effort shown
6. If working: ✅ Deployment successful!
```

---

## What's Ready to Deploy

✅ Backend: Updated for PostgreSQL  
✅ Frontend: Static paths corrected  
✅ Database: Schema ready  
✅ Environment: Config template created  
✅ Documentation: Complete guides provided  

## Next Action

👉 **Open SUPABASE_SETUP.md and follow the steps!**

---

## Support

- Error with database? → Check SUPABASE_SETUP.md
- Error deploying? → Check DEPLOYMENT_GUIDE.md  
- Code not updating? → Check your git branches
- App won't start? → Check Railway logs

**You're all set! Deploy with confidence! 🎉**
