#!/bin/bash

# Exit on error
set -e

echo "🚀 Preparing to deploy to Netlify..."

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

# Build the application
echo "🏗️ Building the Next.js application..."
NEXT_DISABLE_ESLINT=1 npm run build

# Check if Netlify CLI is installed
if ! command -v netlify &> /dev/null; then
    echo "🔧 Installing Netlify CLI..."
    npm install -g netlify-cli
fi

# Deploy to Netlify
echo "🚀 Deploying to Netlify..."
netlify deploy --prod --dir=out

echo "✅ Deployment process completed!" 