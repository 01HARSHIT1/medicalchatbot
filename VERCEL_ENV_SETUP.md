# 🔗 Vercel Environment Variables Setup

## ✅ Railway Backend is Deployed!

Now you need to connect it to your Vercel frontend.

## Step 1: Get Your Railway Backend URL

1. Go to **Railway Dashboard** → Your Service
2. Click on your service
3. Go to **"Settings"** tab
4. Scroll to **"Domains"** section
5. You'll see a Railway-provided domain like: `your-app.up.railway.app`
6. **Copy this URL** (e.g., `https://your-app.up.railway.app`)

## Step 2: Set Environment Variables in Vercel

1. Go to **Vercel Dashboard** → Your Project
2. Click **"Settings"** tab
3. Click **"Environment Variables"** in the left sidebar
4. Add the following variables:

### For Medical Prediction (Logo 1):
- **Key:** `VITE_API_URL`
- **Value:** Your Railway URL (e.g., `https://your-app.up.railway.app`)
- **Environment:** Production, Preview, Development (select all)
- Click **"Save"**

### For Chatbot (Logo 3):
- **Key:** `VITE_CHATBOT_URL`
- **Value:** Your Railway URL (e.g., `https://your-app.up.railway.app`)
- **Environment:** Production, Preview, Development (select all)
- Click **"Save"**

### For Image Recognition (Logo 2):
- **Key:** `VITE_IMAGE_URL`
- **Value:** Your Streamlit app URL (if deployed) OR Railway URL
- **Environment:** Production, Preview, Development (select all)
- Click **"Save"**

## Step 3: Redeploy Vercel

After adding environment variables:

1. Go to **"Deployments"** tab
2. Click **"⋯"** (three dots) on the latest deployment
3. Click **"Redeploy"**
4. Wait for deployment to complete

## Step 4: Test

1. Open your Vercel app URL
2. Click on **Logo 1** (Medical Prediction) - should work!
3. Click on **Logo 3** (Chatbot) - should work!
4. Click on **Logo 2** (Image Recognition) - needs Streamlit deployment

## Quick Setup Summary

```
VITE_API_URL = https://your-railway-app.up.railway.app
VITE_CHATBOT_URL = https://your-railway-app.up.railway.app
VITE_IMAGE_URL = (optional - for Streamlit app)
```

## Notes

- **Medical Prediction** and **Chatbot** use the same Railway backend
- **Image Recognition** needs a separate Streamlit deployment (or you can deploy it to Railway too)
- After adding environment variables, **always redeploy** Vercel for changes to take effect

---

**That's it! Your app should work now!** 🚀

