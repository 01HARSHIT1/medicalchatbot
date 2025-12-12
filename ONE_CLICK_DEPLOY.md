# 🚀 One-Click Railway Deployment

## The Fastest Way to Deploy (2 minutes)

### Step 1: Go to Railway
👉 **Click here**: https://railway.app/new

### Step 2: Deploy from GitHub
1. Click **"Deploy from GitHub repo"**
2. Sign in with GitHub
3. Select: **`01HARSHIT1/medicalchatbot`**
4. Click **"Deploy Now"**

### Step 3: Configure (30 seconds)
1. Click on the service that was created
2. **Settings** → **Root Directory**
3. Type: **`backend-api`**
4. Click **Save**

### Step 4: Get URL (30 seconds)
1. **Settings** → **Networking**
2. Click **"Generate Domain"**
3. **Copy the URL** (e.g., `https://your-app.railway.app`)

### Step 5: Configure Vercel (1 minute)
1. Go to: https://vercel.com/dashboard
2. Select your project
3. **Settings** → **Environment Variables**
4. Click **"Add New"**
5. **Name**: `VITE_API_URL`
6. **Value**: Paste your Railway URL
7. **Environments**: Check all ✅
8. **Save**
9. **Deployments** → **⋯** → **Redeploy**

## ✅ Done!

Your backend is now live and connected to your Vercel app! 🎉

Test it by using the medical prediction feature on your Vercel site.

