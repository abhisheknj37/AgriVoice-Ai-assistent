#!/bin/bash

# Quick Railway Deployment Setup
# Run this locally before pushing to GitHub

echo "🚀 Preparing AgriVoice for Railway Deployment"
echo "============================================"

# Check if we're in the right directory
if [ ! -f "backend/requirements.txt" ]; then
    echo "❌ Error: Run this script from the agrivoice project root"
    exit 1
fi

# Update railway.toml with correct Dockerfile path
cat > backend/railway.toml << 'EOF'
[build]
builder = "dockerfile"
dockerfilePath = "Dockerfile.railway"

[deploy]
healthcheckPath = "/api/"
healthcheckTimeout = 300
restartPolicyType = "ON_FAILURE"
EOF

echo "✅ Created backend/railway.toml"

# Create .env.example for Railway
cat > backend/.env.railway << 'EOF'
# Railway Environment Variables
DJANGO_SETTINGS_MODULE=agrivoice.settings_prod
DJANGO_SECRET_KEY=your-super-secret-key-here
OPENAI_API_KEY=sk-your-openai-key-here
SARVAM_API_KEY=your-sarvam-key-here
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com

# Railway will auto-provide:
# DATABASE_URL=postgresql://...
# RAILWAY_STATIC_URL=https://...
EOF

echo "✅ Created backend/.env.railway"

# Update vercel.json with placeholder
sed -i 's/your-railway-backend-url.railway.app/your-backend-url.vercel.app/g' agrivoice-ui/vercel.json

echo "✅ Updated agrivoice-ui/vercel.json"

echo ""
echo "🎉 Ready for Railway deployment!"
echo ""
echo "Next steps:"
echo "1. Push this code to GitHub:"
echo "   git add ."
echo "   git commit -m 'Ready for Railway deployment'"
echo "   git push origin main"
echo ""
echo "2. Go to https://railway.app and deploy from your GitHub repo"
echo ""
echo "3. Add PostgreSQL database in Railway dashboard"
echo ""
echo "4. Set environment variables (copy from backend/.env.railway)"
echo ""
echo "5. Deploy frontend to Vercel:"
echo "   - Go to https://vercel.com"
echo "   - Import agrivoice-ui folder"
echo "   - Update vercel.json with your Railway backend URL"
echo ""
echo "Your app will be live at:"
echo "Frontend: https://your-app.vercel.app"
echo "Backend: https://your-project.railway.app"