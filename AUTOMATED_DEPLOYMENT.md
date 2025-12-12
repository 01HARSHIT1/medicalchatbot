# 🤖 Automated Railway Deployment Guide

This guide will help you deploy the backend to Railway with minimal manual steps.

## ⚡ Quick Deploy (5 minutes)

### Option 1: Using Railway Web UI (Easiest - Recommended)

1. **Go to Railway**: https://railway.app/new
2. **Click "Deploy from GitHub repo"**
3. **Sign in** with GitHub (if not already)
4. **Select repository**: `01HARSHIT1/medicalchatbot`
5. **Click "Deploy Now"**
6. **Configure**:
   - Click on the service that was created
   - Go to **Settings** tab
   - Set **Root Directory**: `backend-api`
   - Railway will auto-detect Python ✅
7. **Get URL**:
   - Go to **Settings** → **Networking**
   - Click **"Generate Domain"**
   - Copy the URL (e.g., `https://your-app.railway.app`)

### Option 2: Using Railway CLI (Automated Script)

#### For Windows (PowerShell):
```powershell
cd ProjectAML
.\deploy-to-railway.ps1
```

#### For Mac/Linux:
```bash
cd ProjectAML
chmod +x deploy-to-railway.sh
./deploy-to-railway.sh
```

#### Manual CLI Steps:
```bash
# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Login to Railway
railway login

# 3. Navigate to backend
cd backend-api

# 4. Initialize project
railway init

# 5. Deploy
railway up

# 6. Get URL
railway domain
```

## ✅ After Deployment

1. **Copy your Railway URL** (from step 7 or CLI)
2. **Go to Vercel**: https://vercel.com/dashboard
3. **Select your project**: `medicalchatbot`
4. **Settings** → **Environment Variables**
5. **Add**:
   - **Name**: `VITE_API_URL`
   - **Value**: `https://your-app.railway.app` (your Railway URL)
   - **Environments**: ✅ Production, ✅ Preview, ✅ Development
6. **Save**
7. **Redeploy**: Go to **Deployments** → Click **⋯** → **Redeploy**

## 🧪 Test It

1. Visit your Railway URL in browser
2. You should see Flask app running (or a JSON response)
3. Test from your Vercel app - medical prediction should work!

## 🆘 Troubleshooting

**Deployment fails?**
- Check Railway logs for errors
- Verify Root Directory is set to `backend-api`
- Make sure all files are in the repository

**Can't connect from Vercel?**
- Verify Railway URL is correct
- Check that CORS is enabled (it is in the code)
- Make sure you redeployed Vercel after adding environment variable

## 📝 What Gets Deployed

- `backend-api/main.py` - Flask API
- `backend-api/requirements.txt` - Dependencies
- `backend-api/datasets/` - All CSV files
- `backend-api/models/` - ML models
- `backend-api/railway.json` - Railway config

Everything is ready! Just follow the steps above. 🚀

