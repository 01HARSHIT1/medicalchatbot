# 🚀 Complete Deployment Guide - All Services

This guide will help you deploy all three backend services so your Vercel app works perfectly!

## 📋 Services Overview

1. **Medical Prediction API** - Flask backend (Port 5000)
2. **Image Recognition** - Streamlit app (Port 8501)
3. **AI Chatbot** - Flask backend (Port 5002)

---

## 🏥 Service 1: Medical Prediction API

### Deploy to Railway (Recommended - 5 minutes)

1. **Go to Railway**: https://railway.app/new
2. **Deploy from GitHub**: Select `01HARSHIT1/medicalchatbot`
3. **Set Root Directory**: `backend-api`
4. **Generate Domain**: Settings → Networking → Generate Domain
5. **Copy URL**: e.g., `https://your-app.railway.app`

### Configure Vercel

1. Go to Vercel Dashboard → Your Project
2. **Settings** → **Environment Variables**
3. Add:
   - **Name**: `VITE_API_URL`
   - **Value**: `https://your-app.railway.app` (from Railway)
   - **Environments**: ✅ Production, ✅ Preview, ✅ Development
4. **Save**
5. **Redeploy**: Deployments → ⋯ → Redeploy

✅ **Done!** Medical prediction should now work.

---

## 🖼️ Service 2: Image Recognition

### Option A: Streamlit Cloud (Easiest - Free)

1. **Go to**: https://share.streamlit.io
2. **Sign in** with GitHub
3. **New app** → Select repository: `01HARSHIT1/medicalchatbot`
4. **Main file path**: `SaveBackUpProjectAML/Image_Recognition/Main3.py`
5. **Deploy!**
6. **Copy URL**: e.g., `https://your-app.streamlit.app`

### Option B: Railway

1. Create new service in Railway
2. **Root Directory**: `SaveBackUpProjectAML/Image_Recognition`
3. **Build Command**: `pip install -r requirements.txt`
4. **Start Command**: `streamlit run Main3.py --server.port $PORT --server.address 0.0.0.0`
5. **Generate Domain** and copy URL

### Configure Vercel

1. **Settings** → **Environment Variables**
2. Add:
   - **Name**: `VITE_IMAGE_URL`
   - **Value**: Your Streamlit/Railway URL
   - **Environments**: ✅ All
3. **Save** and **Redeploy**

✅ **Done!** Image recognition should now work.

---

## 💬 Service 3: AI Chatbot

### Deploy to Railway

1. **Go to Railway**: https://railway.app/new
2. **New Service** → **Deploy from GitHub**
3. **Repository**: `01HARSHIT1/medicalchatbot`
4. **Root Directory**: `backend-api/chatbot-service`
5. **Environment Variables** (in Railway):
   - `OPENAI_API_KEY` = Your OpenAI API key (get from https://platform.openai.com/api-keys)
6. **Generate Domain** and copy URL

### Configure Vercel

1. **Settings** → **Environment Variables**
2. Add:
   - **Name**: `VITE_CHATBOT_URL`
   - **Value**: Your Railway chatbot URL
   - **Environments**: ✅ All
3. **Save** and **Redeploy**

✅ **Done!** Chatbot should now work.

---

## ✅ Final Checklist

After deploying all services, verify:

- [ ] `VITE_API_URL` is set in Vercel
- [ ] `VITE_IMAGE_URL` is set in Vercel
- [ ] `VITE_CHATBOT_URL` is set in Vercel
- [ ] All three services are accessible (test URLs in browser)
- [ ] Vercel app has been redeployed
- [ ] Test each feature on your Vercel site

---

## 🆘 Troubleshooting

### Service not accessible?
- Check Railway/Streamlit logs for errors
- Verify the service is running (green status)
- Test the URL directly in browser

### Still seeing errors on Vercel?
- Make sure you **redeployed** after adding environment variables
- Check that variable names are exactly: `VITE_API_URL`, `VITE_IMAGE_URL`, `VITE_CHATBOT_URL`
- Verify URLs don't have trailing slashes

### Need help?
- Check service-specific README files in `backend-api/` folders
- Railway has excellent documentation: https://docs.railway.app
- Streamlit Cloud docs: https://docs.streamlit.io/streamlit-community-cloud

---

## 🎉 You're Done!

All three services should now be working on your Vercel deployment! 🚀

