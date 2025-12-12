# 🏥 Medical Prediction Backend API

Flask backend for medical disease prediction.

## 🚀 Quick Deploy to Railway

### Option 1: One-Click Deploy

1. Go to https://railway.app/new
2. Click "Deploy from GitHub"
3. Select repository: `01HARSHIT1/medicalchatbot`
4. Set **Root Directory**: `SaveBackUpProjectAML/react-flask-app`
5. Railway will auto-detect Python and deploy!
6. Copy the URL (e.g., `https://your-app.railway.app`)

### Option 2: Railway CLI

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Initialize
railway init

# Deploy
railway up
```

## 🔧 Environment Variables

No environment variables needed - everything is configured!

## 📝 API Endpoints

- `POST /predict` - Predict disease from symptoms
- `POST /check_disease` - Get all symptoms for a disease

## ✅ After Deployment

1. Copy your Railway URL
2. Go to Vercel → Your Project → Settings → Environment Variables
3. Add: `VITE_API_URL` = `https://your-app.railway.app`
4. Redeploy Vercel app

## 🧪 Test the API

```bash
curl -X POST https://your-app.railway.app/predict \
  -H "Content-Type: application/json" \
  -d '{"symptoms": ["itching", "skin_rash"]}'
```

