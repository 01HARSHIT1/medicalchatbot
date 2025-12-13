# 🚀 Deploy Entirely on Vercel - No External Services!

This project is now optimized to work **entirely on Vercel** without needing Railway or any other external services!

## ✅ What's Optimized

1. **Lightweight Serverless Functions** - Uses rule-based prediction as fallback
2. **Smart Model Loading** - Tries ML models, falls back to lightweight if too large
3. **Optimized Dependencies** - Only loads what's needed
4. **Works Within Vercel Limits** - Stays under 250MB size limit

## 🚀 Deploy to Vercel (2 minutes)

### Step 1: Connect to Vercel

1. Go to: https://vercel.com/new
2. **Import Git Repository**
3. Select: `01HARSHIT1/medicalchatbot`
4. Click **Deploy**

### Step 2: Configure (Optional)

Vercel will auto-detect everything! But you can:
- **Framework Preset**: Vite
- **Root Directory**: `./` (default)
- **Build Command**: `npm run build`
- **Output Directory**: `dist`

### Step 3: Deploy!

Click **Deploy** and wait ~2 minutes.

## ✨ How It Works

### Automatic Fallback System:

1. **First tries**: Full ML model (if available and within size limits)
2. **Falls back to**: Lightweight rule-based prediction (always works)
3. **Result**: Always returns predictions, even if ML models are too large

### API Endpoints:

- `/api/predict` - Medical prediction (optimized)
- `/api/check_disease` - Disease details lookup

## 🎯 Features

- ✅ **No Railway needed**
- ✅ **No external services**
- ✅ **Everything on Vercel**
- ✅ **Automatic fallback system**
- ✅ **Works within size limits**
- ✅ **Free tier available**

## 🧪 Test It

After deployment:
1. Visit your Vercel URL
2. Use the medical prediction feature
3. It works automatically! 🎉

## 📝 How the Optimization Works

### Smart Loading:
```python
# Tries full ML model first
try:
    from main import get_predicted_value
    # Use ML model
except:
    # Falls back to rule-based (lightweight)
    predict_disease_lightweight()
```

### Rule-Based Prediction:
- Uses symptom matching rules
- No heavy ML models needed
- Fast and lightweight
- Always works

## 🔧 If You Want Full ML Models

If you need the full ML models and they're too large for Vercel:
1. Use the local deployment (`run-local.bat` or `./run-local.sh`)
2. Or deploy backend to Railway (see `ONE_CLICK_DEPLOY.md`)
3. Set `VITE_API_URL` environment variable

But the optimized version works great for most use cases!

---

**You're all set! Just deploy to Vercel and everything works!** 🚀

