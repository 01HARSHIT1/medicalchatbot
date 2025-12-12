# 🚀 Deploy Backend to Railway - 5 Minutes

## ⚡ Quick Steps

### 1. Go to Railway
Visit: **https://railway.app/new**

### 2. Deploy from GitHub
- Click **"Deploy from GitHub repo"**
- Sign in with GitHub
- Select repository: **`01HARSHIT1/medicalchatbot`**

### 3. Configure
- Railway will auto-detect Python ✅
- Go to **Settings** → **Root Directory**
- Set to: **`backend-api`**
- Save

### 4. Get URL
- Go to **Settings** → **Networking**
- Click **"Generate Domain"**
- Copy the URL (e.g., `https://your-app.railway.app`)

### 5. Configure Vercel
- Go to Vercel Dashboard → Your Project
- **Settings** → **Environment Variables**
- Add: `VITE_API_URL` = `https://your-app.railway.app`
- **Save**

### 6. Redeploy Vercel
- **Deployments** tab → Click **⋯** → **Redeploy**

### 7. Done! ✅
Your backend is now live and connected!

## 🧪 Test It

Visit your Railway URL in browser - you should see the Flask app running!

Then test from your Vercel frontend - medical prediction should work!
