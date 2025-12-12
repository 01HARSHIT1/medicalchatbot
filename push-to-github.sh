#!/bin/bash
# Bash script to push code to GitHub
# Usage: ./push-to-github.sh https://github.com/username/repo-name.git

if [ -z "$1" ]; then
    echo "❌ Error: Please provide GitHub repository URL"
    echo "Usage: ./push-to-github.sh <GITHUB_REPO_URL>"
    exit 1
fi

REPO_URL=$1

echo "🚀 Pushing code to GitHub..."
echo ""

# Check if remote already exists
if git remote | grep -q "origin"; then
    echo "⚠️  Remote 'origin' already exists. Updating..."
    git remote set-url origin $REPO_URL
else
    echo "✅ Adding remote repository..."
    git remote add origin $REPO_URL
fi

echo ""
echo "📤 Pushing to GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Successfully pushed to GitHub!"
    echo "🌐 Your code is now available at: $REPO_URL"
else
    echo ""
    echo "❌ Error pushing to GitHub. Please check:"
    echo "   1. Repository URL is correct"
    echo "   2. You have push access to the repository"
    echo "   3. You're authenticated with GitHub"
fi

