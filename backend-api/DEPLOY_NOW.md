# 🚀 Deploy Backend Now - Step by Step

## ⚡ Quick Deploy to Railway (5 minutes)

### Step 1: Go to Railway
1. Visit: https://railway.app/new
2. Click **"Deploy from GitHub repo"**
3. Sign in with GitHub if needed

### Step 2: Select Your Repository
1. Find and select: **`01HARSHIT1/medicalchatbot`**
2. Click **"Deploy Now"**

### Step 3: Configure Railway
1. Railway will show "Detecting..."
2. Click on the service that was created
3. Go to **Settings** tab
4. Set **Root Directory**: `SaveBackUpProjectAML/react-flask-app`
5. Railway will auto-detect Python ✅

### Step 4: Get Your Backend URL
1. Go to **Settings** → **Networking**
2. Click **"Generate Domain"**
3. Copy the URL (e.g., `https://your-app.railway.app`)

### Step 5: Configure Vercel
1. Go to: https://vercel.com/dashboard
2. Select your **medicalchatbot** project
3. Go to **Settings** → **Environment Variables**
4. Click **"Add New"**
5. Add:
   - **Name**: `VITE_API_URL`
   - **Value**: `https://your-app.railway.app` (from Step 4)
   - **Environments**: Check all (Production, Preview, Development)
6. Click **"Save"**

### Step 6: Redeploy Vercel
1. Go to **Deployments** tab
2. Click **⋯** (three dots) on latest deployment
3. Click **"Redeploy"**
4. Wait for deployment ✅

### Step 7: Test!
1. Open your Vercel app
2. Click "Logo 1" (Medical Prediction)
3. Enter symptoms and click "Predict"
4. It should work! 🎉

## ✅ That's It!

Your backend is now deployed and connected to your frontend!

## 🆘 Troubleshooting

**If Railway deployment fails:**
- Check Railway logs for errors
- Make sure Root Directory is set correctly
- Verify all files are in the repository

**If Vercel still shows errors:**
- Make sure you redeployed after adding environment variable
- Check that the Railway URL is correct
- Test the Railway URL in browser (should show Flask app)

## 📝 Next Steps (Optional)

Deploy Image Recognition and Chatbot the same way:
- Image Recognition: Deploy `SaveBackUpProjectAML/Image_Recognition` to Streamlit Cloud
- Chatbot: Deploy `SaveBackUpProjectAML/zexp3` to Railway

Then add `VITE_IMAGE_URL` and `VITE_CHATBOT_URL` to Vercel!

