# 🚀 Free Deployment Options for AgriVoice

## Best Free Options (Ranked by Ease & Features)

---

## 🥇 **#1 RECOMMENDED: Railway + Vercel (Most Complete)**

### **Railway** (Backend + Database) - FREE
- ✅ **Free Tier**: 512MB RAM, 1GB disk, PostgreSQL included
- ✅ **Full Django support** with Docker
- ✅ **PostgreSQL database** (no extra cost)
- ✅ **Custom domains** free
- ✅ **Automatic SSL**

### **Vercel** (Frontend) - FREE
- ✅ **React deployment** optimized
- ✅ **Global CDN** 
- ✅ **Custom domains** free
- ✅ **Automatic SSL**

---

## 🥈 **#2: Render (All-in-One)**

### **Render** - FREE
- ✅ **Free Tier**: 750 hours/month, PostgreSQL included
- ✅ **Django + React** support
- ✅ **Free SSL certificates**
- ✅ **Custom domains** free
- ✅ **Static site hosting**

---

## 🥉 **#3: Fly.io (High Performance)**

### **Fly.io** - FREE
- ✅ **Free Tier**: 3 shared CPUs, 256MB RAM each
- ✅ **Global deployment** (multiple regions)
- ✅ **PostgreSQL** available
- ✅ **Custom domains** free

---

## 📋 **Step-by-Step: Railway + Vercel Deployment**

### **Step 1: Railway Backend Setup**

1. **Create Railway Account**
   - Go to https://railway.app
   - Sign up with GitHub

2. **Create Project**
   - Click "New Project"
   - Choose "Deploy from GitHub repo"
   - Connect your AgriVoice repository

3. **Configure Backend Service**
   - Railway auto-detects Django
   - Set environment variables:
     ```
     DJANGO_SETTINGS_MODULE=agrivoice.settings_prod
     DJANGO_SECRET_KEY=your-secret-key-here
     OPENAI_API_KEY=your-openai-key
     SARVAM_API_KEY=your-sarvam-key
     EMAIL_HOST_USER=your-email@gmail.com
     EMAIL_HOST_PASSWORD=your-app-password
     DATABASE_URL=postgresql://... (auto-provided)
     ```

4. **Add PostgreSQL Database**
   - In Railway dashboard: Add → Database → PostgreSQL
   - Links automatically to your Django app

5. **Deploy**
   - Railway auto-deploys on git push
   - Get your backend URL: `https://your-project.railway.app`

### **Step 2: Vercel Frontend Setup**

1. **Create Vercel Account**
   - Go to https://vercel.com
   - Sign up with GitHub

2. **Deploy Frontend**
   - Click "New Project"
   - Import your `agrivoice-ui` folder
   - Set build settings:
     ```
     Build Command: npm run build
     Output Directory: build
     Install Command: npm install
     ```

3. **Configure API Proxy**
   - In `vercel.json`, update the backend URL:
     ```json
     {
       "src": "/api/(.*)",
       "dest": "https://your-railway-backend.railway.app/api/$1"
     }
     ```

4. **Environment Variables**
   ```
   REACT_APP_API_BASE_URL=https://your-vercel-app.vercel.app
   ```

5. **Deploy**
   - Vercel auto-deploys on git push
   - Get your frontend URL: `https://your-app.vercel.app`

---

## 📋 **Alternative: Render All-in-One**

### **Step 1: Create Render Account**
- Go to https://render.com
- Sign up with GitHub

### **Step 2: Deploy Backend**
1. **Create Web Service**
   - New → Web Service
   - Connect GitHub repo
   - Set build settings:
     ```
     Environment: Python 3
     Build Command: pip install -r requirements.txt
     Start Command: python manage.py migrate && python manage.py collectstatic --noinput && gunicorn agrivoice.wsgi:application --bind 0.0.0.0:$PORT
     ```

2. **Add PostgreSQL Database**
   - New → PostgreSQL
   - Free tier available
   - Copy database URL to environment

3. **Environment Variables**
   ```
   DJANGO_SETTINGS_MODULE=agrivoice.settings_prod
   DATABASE_URL=postgresql://...
   DJANGO_SECRET_KEY=your-key
   OPENAI_API_KEY=your-key
   etc.
   ```

### **Step 3: Deploy Frontend**
1. **Create Static Site**
   - New → Static Site
   - Connect GitHub repo (agrivoice-ui folder)
   - Build settings:
     ```
     Build Command: npm run build
     Publish Directory: build
     ```

2. **Update API URL**
   - Set environment: `REACT_APP_API_BASE_URL=https://your-render-backend.onrender.com`

---

## 🔧 **Configuration Updates Needed**

### **For Railway/Render Deployment:**

1. **Update settings_prod.py**:
   ```python
   DATABASES = {
       'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))
   }
   ```

2. **Add to requirements.txt**:
   ```
   dj-database-url
   ```

3. **Update Dockerfile** (if using Docker):
   ```dockerfile
   CMD python manage.py migrate && python manage.py collectstatic --noinput && gunicorn agrivoice.wsgi:application --bind 0.0.0.0:$PORT
   ```

---

## 📊 **Free Tier Limits**

| Platform | Free Limits | Paid Upgrade |
|----------|-------------|--------------|
| **Railway** | 512MB RAM, 1GB disk, 1GB bandwidth/month | $5/month for 1GB RAM |
| **Render** | 750 hours/month, 750MB disk | $7/month for persistent apps |
| **Vercel** | Unlimited bandwidth, 100GB/month | $20/month for pro features |
| **Fly.io** | 3 shared CPUs, 256MB RAM each | $10/month for dedicated |

---

## 🚀 **Quick Start Commands**

### **Railway + Vercel (Recommended)**
```bash
# 1. Push to GitHub
git add .
git commit -m "Ready for deployment"
git push origin main

# 2. Deploy backend on Railway
# - Connect repo to Railway
# - Add PostgreSQL database
# - Set environment variables

# 3. Deploy frontend on Vercel
# - Connect agrivoice-ui folder
# - Update vercel.json with Railway URL
```

### **Render All-in-One**
```bash
# Push to GitHub, then:
# 1. Create Render account
# 2. New Web Service → Connect repo
# 3. New PostgreSQL → Link to web service
# 4. New Static Site → Connect repo (agrivoice-ui)
```

---

## 🎯 **Which to Choose?**

### **Choose Railway + Vercel if:**
- Want most reliable free deployment
- Need PostgreSQL included
- Want global CDN for frontend
- Plan to scale easily

### **Choose Render if:**
- Want simplest all-in-one solution
- Don't mind 750hr/month limit
- Prefer single platform management

### **Choose Fly.io if:**
- Need high performance
- Want global deployment
- Comfortable with advanced config

---

## 💡 **Pro Tips**

1. **Custom Domain**: All platforms support free custom domains
2. **SSL**: Automatic on all platforms
3. **Monitoring**: Check platform dashboards for logs
4. **Scaling**: Easy upgrades when you need more resources
5. **Backups**: Set up database backups in platform settings

---

## 🆘 **Need Help?**

**Common Issues:**
- **Build fails**: Check logs, ensure all dependencies in requirements.txt
- **Database connection**: Verify DATABASE_URL format
- **Environment vars**: Check spelling, no extra spaces
- **CORS**: Update ALLOWED_HOSTS with your deployment URLs

Your AgriVoice app will be live for FREE! 🌾🚀