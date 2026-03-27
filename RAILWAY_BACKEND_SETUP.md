# 🚂 Deploy Backend to Railway (10 minutes)

## Why Railway?
- Free tier available
- PostgreSQL database included
- One-click deployment from GitHub
- Perfect for this project

---

## Step 1: Create Railway Account (2 min)

1. Go to https://railway.app
2. Click "Start Project"
3. Sign in with GitHub
4. Authorize Railway

---

## Step 2: Deploy Backend (5 min)

### Option A: Deploy from GitHub (Recommended)

1. In Railway dashboard, click "+ New Project"
2. Select "Deploy from GitHub repo"
3. Authenticate with GitHub
4. Select your repository
5. Select the branch (main)
6. Railway auto-detects it's a Python/Flask app
7. Click "Deploy"

**Wait 3-5 minutes...**

### Option B: Deploy from Git (if Option A doesn't work)

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Navigate to project
cd "path/to/your/project"

# Link to Railway
railway link

# Deploy
railway up
```

---

## Step 3: Get Your Backend URL (1 min)

In Railway dashboard:
1. Go to your project
2. Click "Deployments" tab
3. Find the successful deployment
4. Copy the "Public URL" (e.g., `https://spm-api.railway.app`)
5. **SAVE THIS URL** - you'll need it for Vercel!

---

## Step 4: Configure Database (1 min)

In Railway:
1. Click "+ Add Service"
2. Select "PostgreSQL"
3. Wait for it to start (~1 min)

### Connect Database to Backend

Railway auto-connects! But verify:
1. Go to your backend service
2. Click "Variables" tab
3. You should see `DATABASE_URL` set automatically
4. If not, copy PostgreSQL's URL to `DATABASE_URL`

---

## Step 5: Set Environment Variables (1 min)

In Railway dashboard, go to Variables tab on backend service:

| Key | Value |
|-----|-------|
| `FLASK_ENV` | `production` |
| `SECRET_KEY` | `your-secret-key-here` |
| `CORS_ORIGINS` | `https://your-project.vercel.app` |

**Note**: Update `CORS_ORIGINS` after you deploy to Vercel

---

## Step 6: Verify Backend Works (2 min)

Get your backend public URL and test:

```bash
# In terminal or browser:
curl https://your-backend-url/api/projects

# Should return: [] (empty array or data)
```

Or open in browser:
```
https://your-backend-url/api/projects
```

Should show JSON response ✅

---

## ✅ Backend Ready!

You now have:
- ✅ Backend URL: `https://your-backend-url.railway.app`
- ✅ Database connected
- ✅ Environment variables set
- ✅ API accessible and running

**Save this URL!** You'll need it for Vercel.

---

## 🐛 Troubleshooting

### Deployment Failed
- Check deployment logs in Railway
- Ensure `Procfile` exists in root
- Verify `requirements.txt` is complete

### Database Not Connected
- Check `DATABASE_URL` variable exists
- Verify PostgreSQL service is running
- Check backend app.py for database connection

### API Returns Error
- Check backend logs in Railway
- Verify CORS is configured
- Test locally first: `python backend/app.py`

---

## Next: Push to GitHub

Once backend is running on Railway:
1. Push code to GitHub
2. Deploy frontend to Vercel
3. Update CORS for Vercel domain

See: [BACKEND_DEPLOYMENT_GITHUB.md](./BACKEND_DEPLOYMENT_GITHUB.md)
