# PowerShell Script for Railway Deployment
# Automated deployment helper for Windows

Write-Host "🚀 Railway Deployment Helper Script" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Green
Write-Host ""

# Check if Railway CLI is installed
$railwayInstalled = Get-Command railway -ErrorAction SilentlyContinue

if (-not $railwayInstalled) {
    Write-Host "📦 Installing Railway CLI..." -ForegroundColor Yellow
    npm install -g @railway/cli
    Write-Host "✅ Railway CLI installed!" -ForegroundColor Green
} else {
    Write-Host "✅ Railway CLI already installed" -ForegroundColor Green
}

Write-Host ""
Write-Host "🔐 Step 1: Login to Railway" -ForegroundColor Cyan
Write-Host "   Run: railway login" -ForegroundColor White
Write-Host "   (This will open your browser for authentication)" -ForegroundColor Gray
Write-Host ""
$null = Read-Host "Press Enter after you've logged in to Railway"

Write-Host ""
Write-Host "📁 Step 2: Navigate to backend directory" -ForegroundColor Cyan
Set-Location backend-api

Write-Host ""
Write-Host "🚀 Step 3: Initialize Railway project" -ForegroundColor Cyan
railway init

Write-Host ""
Write-Host "🌐 Step 4: Deploy to Railway" -ForegroundColor Cyan
railway up

Write-Host ""
Write-Host "🔗 Step 5: Get your Railway URL" -ForegroundColor Cyan
Write-Host "   Run: railway domain" -ForegroundColor White
$railwayUrl = railway domain
Write-Host ""
Write-Host "✅ Your Railway URL: $railwayUrl" -ForegroundColor Green
Write-Host ""
Write-Host "📝 Next Steps:" -ForegroundColor Yellow
Write-Host "   1. Copy the URL above" -ForegroundColor White
Write-Host "   2. Go to Vercel → Settings → Environment Variables" -ForegroundColor White
Write-Host "   3. Add VITE_API_URL = $railwayUrl" -ForegroundColor White
Write-Host "   4. Redeploy your Vercel app" -ForegroundColor White
Write-Host ""

