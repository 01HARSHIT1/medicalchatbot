# PowerShell script to push code to GitHub
# Usage: .\push-to-github.ps1 -RepoUrl "https://github.com/username/repo-name.git"

param(
    [Parameter(Mandatory=$true)]
    [string]$RepoUrl
)

Write-Host "🚀 Pushing code to GitHub..." -ForegroundColor Green
Write-Host ""

# Check if remote already exists
$remoteExists = git remote | Select-String -Pattern "origin"

if ($remoteExists) {
    Write-Host "⚠️  Remote 'origin' already exists. Updating..." -ForegroundColor Yellow
    git remote set-url origin $RepoUrl
} else {
    Write-Host "✅ Adding remote repository..." -ForegroundColor Green
    git remote add origin $RepoUrl
}

Write-Host ""
Write-Host "📤 Pushing to GitHub..." -ForegroundColor Green
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Successfully pushed to GitHub!" -ForegroundColor Green
    Write-Host "🌐 Your code is now available at: $RepoUrl" -ForegroundColor Cyan
} else {
    Write-Host ""
    Write-Host "❌ Error pushing to GitHub. Please check:" -ForegroundColor Red
    Write-Host "   1. Repository URL is correct" -ForegroundColor Yellow
    Write-Host "   2. You have push access to the repository" -ForegroundColor Yellow
    Write-Host "   3. You're authenticated with GitHub" -ForegroundColor Yellow
}

