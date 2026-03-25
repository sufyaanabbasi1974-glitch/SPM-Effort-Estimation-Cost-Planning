# SPM Effort Estimation System - Production Deployment Guide

## 🎯 Overview
This guide covers deploying the SPM Effort Estimation System to production using:
- **Database**: Supabase (PostgreSQL)
- **Backend**: Railway.app (Python Flask)
- **Frontend**: Railway (same instance)

## 📋 What's Been Fixed

### Bug Fixes Completed
✅ Static file paths corrected (`/assets/` prefix)  
✅ Database configuration updated for PostgreSQL support  
✅ Error handling improved with detailed logging  
✅ Input validation enhanced for all endpoints  
✅ CORS properly configured  
✅ Environment variable support for production  

### Files Modified
- `frontend/index.html` - Fixed CSS/JS paths
- `backend/app.py` - Added PostgreSQL support
- `requirements-prod.txt` - Added PostgreSQL driver (psycopg2)
- `.env.example` - Created template for configuration

### New Files Created
- `SUPABASE_SETUP.md` - Detailed Supabase setup (FOLLOW THIS FIRST!)
- `DEPLOYMENT_GUIDE.md` - Complete deployment instructions
- `.env.example` - Environment configuration template
- `requirements-prod.txt` - Production dependencies
- `runtime.txt` - Python version specification

---

## ⚡ Quick Start (5 Minutes)

### Option 1: Full Local Development
```bash
# 1. Install dependencies
cd backend
pip install -r requirements.txt

# 2. Run locally
python app.py

# 3. Visit http://localhost:5000
```

### Option 2: Production Deployment with Supabase + Railway
**Follow these steps in order:**

1. **Read `SUPABASE_SETUP.md`** (10 minutes)
   - Create Supabase account
   - Set up PostgreSQL database
   - Create tables

2. **Read `DEPLOYMENT_GUIDE.md`** (15 minutes)
   - Deploy to Railway
   - Configure environment variables
   - Test remote deployment

3. **Update Frontend**
   - Update API_BASE in `frontend/js/app.js`
   - Push to GitHub
   - Railway auto-deploys

---

## 📚 File Guide

### Critical Files for Deployment

| File | Purpose | Action |
|------|---------|--------|
| `SUPABASE_SETUP.md` | Database setup | **READ FIRST** |
| `DEPLOYMENT_GUIDE.md` | Deployment steps | **READ SECOND** |
| `.env.example` | Config template | Copy to `.env` |
| `requirements-prod.txt` | Prod dependencies | Auto-installed by Railway |
| `Procfile` | Server startup | Already configured |
| `runtime.txt` | Python version | Already set |

### Application Files

| File | Purpose |
|------|---------|
| `backend/app.py` | Flask REST API |
| `backend/models.py` | Database models |
| `backend/cocomo_calculator.py` | COCOMO algorithm |
| `backend/evm_calculator.py` | EVM metrics |
| `frontend/index.html` | Main page |
| `frontend/js/app.js` | Frontend logic |
| `frontend/css/style.css` | Styling |

---

## 🔧 Key Features

### Supported Project Types
- **Organic**: Small, simple projects
- **Semi-Detached**: Medium, moderate complexity
- **Embedded**: Large, complex, highly coupled

### Calculation Models
- **Basic COCOMO**: Simple, 2-parameter model
- **Intermediate COCOMO**: Advanced, with effort multipliers

### Modules
1. **Project Input** - Create and manage projects
2. **Effort Estimation** - COCOMO calculations
3. **Schedule & Cost** - Phase-wise breakdown
4. **Risk Management** - Risk assessment and adjustment
5. **EVM Tracking** - Earned Value Management
6. **Reports** - Comprehensive printable reports

---

## 🚀 Deployment Checklist

Before deploying to production, ensure:

### Database (Supabase)
- [ ] Supabase account created
- [ ] PostgreSQL project created
- [ ] All tables created successfully
- [ ] Connection string copied and saved
- [ ] Row-level security policies in place

### Configuration
- [ ] `.env` file created with DATABASE_URL
- [ ] SECRET_KEY generated (use Python secrets module)
- [ ] FLASK_ENV set to "production"
- [ ] PORT configured (default: 5000)

### Code
- [ ] All files pushed to GitHub
- [ ] Branch main is clean
- [ ] No uncommitted changes
- [ ] .gitignore excludes sensitive files

### Railway Setup
- [ ] Railway account created
- [ ] Project connected to GitHub repo
- [ ] Environment variables configured
- [ ] Procfile in root directory
- [ ] runtime.txt specifying Python 3.11

### Frontend
- [ ] API_BASE URL updated to Railway domain
- [ ] Static file paths use `/assets/`
- [ ] CORS configured correctly

### Testing
- [ ] Local testing passed (dev mode)
- [ ] Remote testing passed (production mode)
- [ ] Login works
- [ ] Project creation works
- [ ] Estimations calculate correctly
- [ ] Database persist data

---

## 🔐 Security Checklist

Before going live:

- [ ] SECRET_KEY is cryptographically secure
- [ ] DATABASE_URL password is strong
- [ ] No secrets in GitHub (use .env)
- [ ] CORS restricted to known domains
- [ ] SSL/HTTPS enforced
- [ ] SQL injection protection (SQLAlchemy ORM)
- [ ] CSRF protection enabled (Flask-Session)
- [ ] Rate limiting implemented (optional)

---

## 📊 Expected Architecture

```
┌─────────────────────────────────────────────────────┐
│                  User Browser                       │
│        (http://your-app.railway.app)               │
└────────────────────┬────────────────────────────────┘
                     │
                     │ HTTP/REST API
                     ↓
┌─────────────────────────────────────────────────────┐
│             Railway.app (Backend)                   │
│  • Python Flask server                              │
│  • REST API endpoints                               │
│  • Business logic                                   │
│  • Static file serving (frontend)                   │
└────────────────────┬────────────────────────────────┘
                     │
                     │ PostgreSQL Driver (psycopg2)
                     ↓
┌─────────────────────────────────────────────────────┐
│        Supabase PostgreSQL Database                 │
│  • projects table                                   │
│  • estimations table                                │
│  • risks table                                      │
│  • evm_tracking table                               │
└─────────────────────────────────────────────────────┘
```

---

## 💰 Cost Estimate

**Monthly Cost (as of 2024)**:
- Supabase (free tier): $0
  - 500MB storage
  - Unlimited API calls
  - Up to 1GB auto-backup
- Railway (starter tier): $7 - $20
  - 500 hours/month free
  - Pay-as-you-go after
- **Total**: $7-20/month

**Free Alternative**:
- Supabase Free: $0
- Railway Free: $0 (limited hours)
- Total: $0 (with limitations)

---

## 📱 Accessing Your App

### After Deployment
1. Navigate to: `https://your-project.railway.app`
2. Login with:
   - Username: `admin`
   - Password: `password`
3. Create test project and verify functionality

### Getting Your URL
In Railway dashboard:
1. Select your project
2. Look for "Domains" section
3. You'll see: `your-project-name.railway.app`

---

## 🐛 Troubleshooting

### App won't start
- Check Railway logs
- Verify DATABASE_URL is correct
- Ensure requirements-prod.txt is installed

### Database connection ERROR
- Verify Supabase connection string
- Check password in DATABASE_URL
- Ensure psycopg2-binary is installed
- Check Supabase console for connection issues

### Frontend not loading
- Check API_BASE URL in app.js
- Clear browser cache
- Check /assets/ folder structure
- Verify CSS/JS files exist

### API returning 404
- Check route exists in app.py
- Verify request method (GET/POST)
- Check request body JSON format
- Look at server logs for details

---

## 📞 Support Resources

### Supabase Help
- [Supabase Docs](https://supabase.com/docs)
- [Supabase Discord](https://discord.supabase.com)
- [Status Page](https://status.supabase.com)

### Railway Help
- [Railway Docs](https://docs.railway.app)
- [Railway Discord](https://discord.gg/railway)

### Flask Help
- [Flask Documentation](https://flask.palletsprojects.com)
- [SQLAlchemy ORM](https://www.sqlalchemy.org/)

---

## 📝 Next Steps

1. **Read SUPABASE_SETUP.md** - Create your database
2. **Read DEPLOYMENT_GUIDE.md** - Deploy your app
3. **Monitor Logs** - Check Railway and Supabase logs
4. **Test Thoroughly** - Verify all features work
5. **Celebrate!** 🎉 - Your app is live!

---

## 📄 Documentation Files

| Document | Purpose | Read First? |
|----------|---------|------------|
| [SUPABASE_SETUP.md](./SUPABASE_SETUP.md) | Database setup | ✅ YES |
| [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) | Deployment guide | ✅ YES |
| [README.md](./README.md) | Architecture details | No (optional) |
| [QUICKSTART.md](./QUICKSTART.md) | Local development | No (optional) |
| [USER_GUIDE.md](./USER_GUIDE.md) | Using the app | No (optional) |

---

**Last Updated**: March 2024  
**Production Ready**: ✅ Yes  
**Status**: 🟢 Deployment Ready

