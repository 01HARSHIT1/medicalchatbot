# 🧹 Clear Vercel Cache - Step by Step

## Which Cache to Clear?

For the **build size error**, you need to clear the **Build Cache**.

## Step-by-Step Instructions

### Option 1: Clear Build Cache (Recommended)

1. Go to **Vercel Dashboard** → Your Project
2. Click **Settings** tab
3. Scroll down to **"Build & Development Settings"**
4. Look for **"Clear Build Cache"** or **"Build Cache"** section
5. Click **"Clear"** or **"Purge"**

### Option 2: If Build Cache Option Not Available

If you only see:
- **Data Cache** - This is for serverless function data (not needed)
- **CDN Cache** - This is for static assets (not needed)

Then do this instead:

1. Go to **Deployments** tab
2. Find the latest deployment
3. Click **⋯** (three dots) on the deployment
4. Click **"Redeploy"**
5. **IMPORTANT**: Uncheck **"Use existing Build Cache"**
6. Click **"Redeploy"**

### Option 3: Force Fresh Build via Git

1. Make a small change to any file (or just add a space)
2. Commit and push to GitHub
3. Vercel will automatically do a fresh build

## What Each Cache Does

- **Build Cache**: Stores build artifacts (this is what's causing the issue)
- **Data Cache**: Stores serverless function data (not related)
- **CDN Cache**: Stores static assets like images (not related)

## Quick Fix

The easiest way is **Option 2** - Redeploy without build cache:
1. Deployments → Latest deployment → ⋯ → Redeploy
2. **Uncheck "Use existing Build Cache"**
3. Redeploy

This forces a completely fresh build with the new empty `requirements.txt`!

---

**After clearing cache, Vercel will:**
- ✅ Do a fresh build
- ✅ Find empty `requirements.txt`
- ✅ Install no Python packages
- ✅ Deploy successfully!

