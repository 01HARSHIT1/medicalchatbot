#!/bin/bash
# Automated Railway Deployment Script
# This script helps you deploy the backend to Railway with minimal manual steps

echo "🚀 Railway Deployment Helper Script"
echo "===================================="
echo ""

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "📦 Installing Railway CLI..."
    npm install -g @railway/cli
    echo "✅ Railway CLI installed!"
else
    echo "✅ Railway CLI already installed"
fi

echo ""
echo "🔐 Step 1: Login to Railway"
echo "   Run: railway login"
echo "   (This will open your browser for authentication)"
echo ""
read -p "Press Enter after you've logged in to Railway..."

echo ""
echo "📁 Step 2: Navigate to backend directory"
cd backend-api

echo ""
echo "🚀 Step 3: Initialize Railway project"
railway init

echo ""
echo "🌐 Step 4: Deploy to Railway"
railway up

echo ""
echo "🔗 Step 5: Get your Railway URL"
echo "   Run: railway domain"
RAILWAY_URL=$(railway domain)
echo ""
echo "✅ Your Railway URL: $RAILWAY_URL"
echo ""
echo "📝 Next Steps:"
echo "   1. Copy the URL above"
echo "   2. Go to Vercel → Settings → Environment Variables"
echo "   3. Add VITE_API_URL = $RAILWAY_URL"
echo "   4. Redeploy your Vercel app"
echo ""

