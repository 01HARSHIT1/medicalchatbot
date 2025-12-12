# 🚀 Deployment Guide

## GitHub Deployment

### Step 1: Create a GitHub Repository

1. Go to [GitHub](https://github.com) and create a new repository
2. Name it (e.g., `ai-healthcare-platform`)
3. Don't initialize with README (we already have one)

### Step 2: Push to GitHub

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: AI Healthcare Platform"

# Add remote (replace with your repo URL)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Vercel Deployment

### Step 1: Install Vercel CLI

```bash
npm install -g vercel
```

### Step 2: Deploy to Vercel

```bash
# Navigate to project directory
cd ProjectAML

# Deploy
vercel

# Follow the prompts:
# - Set up and deploy? Yes
# - Which scope? (Select your account)
# - Link to existing project? No
# - Project name? (Enter a name)
# - Directory? ./
# - Override settings? No
```

### Step 3: Configure Environment Variables

1. Go to your Vercel project dashboard
2. Navigate to Settings > Environment Variables
3. Add the following variables:

```
VITE_API_URL=https://your-backend-url.vercel.app
VITE_IMAGE_URL=https://your-image-recognition-url.vercel.app
VITE_CHATBOT_URL=https://your-chatbot-url.vercel.app
```

### Step 4: Redeploy

After adding environment variables, trigger a new deployment:

```bash
vercel --prod
```

Or redeploy from the Vercel dashboard.

## Backend Deployment

### Option 1: Deploy Backend to Vercel (Serverless Functions)

1. Create a separate Vercel project for the backend
2. Deploy the Flask backend from `SaveBackUpProjectAML/react-flask-app`
3. Update frontend environment variables with the backend URL

### Option 2: Deploy Backend to Railway/Render

1. Create account on [Railway](https://railway.app) or [Render](https://render.com)
2. Connect your GitHub repository
3. Deploy the Flask backend
4. Update frontend environment variables

## Post-Deployment Checklist

- [ ] Frontend deployed and accessible
- [ ] Environment variables configured
- [ ] Backend API deployed and accessible
- [ ] CORS configured on backend
- [ ] All services tested
- [ ] Custom domain configured (optional)

## Troubleshooting

### Build Errors

If you encounter build errors:

1. Check Node.js version (should be 16+)
2. Clear node_modules and reinstall:
   ```bash
   rm -rf node_modules package-lock.json
   npm install
   ```

### API Connection Issues

1. Verify environment variables are set correctly
2. Check CORS settings on backend
3. Ensure backend is deployed and accessible
4. Check browser console for errors

### Vercel Build Failures

1. Check build logs in Vercel dashboard
2. Ensure `package.json` has correct build script
3. Verify `vite.config.js` is configured correctly

