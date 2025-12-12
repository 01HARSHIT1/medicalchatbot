# 🔧 Backend Setup Guide

## Problem
The frontend is deployed on Vercel but cannot connect to the backend because:
- The backend is not deployed
- `VITE_API_URL` environment variable is not configured in Vercel

## Solution Options

### Option 1: Deploy Backend to Railway (Recommended - Easiest)

1. **Create Railway Account**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Select the backend folder: `SaveBackUpProjectAML/react-flask-app`

3. **Configure Railway**
   - Railway will auto-detect Python
   - Set start command: `python main.py`
   - Add environment variables if needed

4. **Get Backend URL**
   - Railway will provide a URL like: `https://your-app.railway.app`
   - Copy this URL

5. **Update Vercel Environment Variables**
   - Go to Vercel dashboard → Your project → Settings → Environment Variables
   - Add: `VITE_API_URL` = `https://your-app.railway.app`
   - Redeploy your Vercel app

### Option 2: Deploy Backend to Render

1. **Create Render Account**
   - Go to [render.com](https://render.com)
   - Sign up

2. **Create Web Service**
   - Click "New" → "Web Service"
   - Connect your GitHub repository
   - Set:
     - **Root Directory**: `SaveBackUpProjectAML/react-flask-app`
     - **Environment**: Python 3
     - **Build Command**: `pip install -r requirements.txt` (create this file if needed)
     - **Start Command**: `python main.py`

3. **Get Backend URL**
   - Render will provide: `https://your-app.onrender.com`

4. **Update Vercel Environment Variables**
   - Same as Option 1, step 5

### Option 3: Deploy Backend to Vercel (Serverless Functions)

This requires converting Flask to serverless functions. More complex but keeps everything on Vercel.

### Option 4: Use a Public Backend API (If Available)

If you have access to a public backend API, just set `VITE_API_URL` to that URL.

## Quick Fix for Testing

If you want to test locally:
1. Run the backend locally: `cd SaveBackUpProjectAML/react-flask-app && python main.py`
2. The frontend will automatically use `http://localhost:5000` when running locally

## Required Backend Files

Make sure your backend has:
- `main.py` (Flask app)
- `requirements.txt` (Python dependencies)
- CORS enabled (already done in `main.py`)

## CORS Configuration

The backend already has CORS enabled. If you deploy to a new platform, ensure:
- CORS allows requests from your Vercel domain
- Or use `Access-Control-Allow-Origin: *` for development

## Testing the Backend

Once deployed, test the backend:
```bash
curl -X POST https://your-backend-url.com/predict \
  -H "Content-Type: application/json" \
  -d '{"symptoms": ["itching", "skin_rash"]}'
```

## Environment Variables Checklist

In Vercel, set:
- ✅ `VITE_API_URL` = Your deployed backend URL
- ⚠️ `VITE_IMAGE_URL` = Image recognition URL (optional)
- ⚠️ `VITE_CHATBOT_URL` = Chatbot URL (optional)

After setting variables, **redeploy** your Vercel app!

