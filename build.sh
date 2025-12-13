#!/bin/bash
# Pre-build script that runs BEFORE Vercel installs dependencies
# This removes requirements.txt to prevent heavy dependency installation

echo "🔧 Pre-install: Removing requirements.txt files..."

# Remove root requirements.txt if it exists
if [ -f "requirements.txt" ]; then
  rm -f requirements.txt
  echo "✅ Removed root requirements.txt"
fi

# Remove requirements-backend-only.txt if it exists
if [ -f "requirements-backend-only.txt" ]; then
  rm -f requirements-backend-only.txt
  echo "✅ Removed requirements-backend-only.txt"
fi

# Ensure api/requirements.txt is empty
if [ -f "api/requirements.txt" ]; then
  echo "# Empty - No dependencies" > api/requirements.txt
  echo "# Serverless functions use pure Python standard library only" >> api/requirements.txt
  echo "✅ Cleared api/requirements.txt"
else
  mkdir -p api
  echo "# Empty - No dependencies" > api/requirements.txt
  echo "# Serverless functions use pure Python standard library only" >> api/requirements.txt
  echo "✅ Created empty api/requirements.txt"
fi

echo "✅ Pre-install cleanup complete!"
echo "Now Vercel will install no Python dependencies"

