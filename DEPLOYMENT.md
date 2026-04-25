# AgriVoice Deployment Guide

This guide will help you deploy the AgriVoice application to production.

## 🚀 Quick Start

### Option 1: Local Docker Deployment (Recommended for Testing)

1. **Prerequisites:**
   - Docker and Docker Compose installed
   - Git

2. **Clone and setup:**
   ```bash
   git clone <your-repo-url>
   cd agrivoice
   ```

3. **Run deployment script:**
   ```bash
   # Linux/Mac
   chmod +x deploy.sh
   ./deploy.sh

   # Windows
   deploy.bat
   ```

4. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

### Option 2: Manual Docker Deployment

```bash
cd backend
docker-compose up -d --build
```

## 🏭 Production Deployment

### 1. Server Requirements

- Ubuntu 20.04+ or similar Linux distribution
- 2GB RAM minimum, 4GB recommended
- 20GB storage
- Domain name with SSL certificate

### 2. Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.17.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Install nginx
sudo apt install nginx -y
```

### 3. Application Deployment

1. **Clone repository:**
   ```bash
   git clone <your-repo-url>
   cd agrivoice
   ```

2. **Configure environment:**
   ```bash
   cp backend/.env.example backend/.env
   nano backend/.env
   ```

   Update the following variables:
   ```env
   DJANGO_SECRET_KEY=your-secure-secret-key
   DB_PASSWORD=your-secure-db-password
   OPENAI_API_KEY=your-openai-key
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   ```

3. **Deploy with Docker:**
   ```bash
   cd backend
   docker-compose -f docker-compose.prod.yml up -d --build
   ```

### 4. Nginx Configuration

Create `/etc/nginx/sites-available/agrivoice`:

```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com www.your-domain.com;

    # SSL configuration
    ssl_certificate /path/to/your/certificate.crt;
    ssl_certificate_key /path/to/your/private.key;

    # Frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Backend API
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Static files
    location /static/ {
        alias /path/to/your/static/files/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Media files
    location /media/ {
        alias /path/to/your/media/files/;
        expires 30d;
    }
}
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/agrivoice /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 5. SSL Certificate (Let's Encrypt)

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx -y

# Get certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
# Database
DB_NAME=agrivoice
DB_USER=agrivoice_user
DB_PASSWORD=your-secure-password

# Django
DJANGO_SECRET_KEY=your-64-character-secret-key
DJANGO_SETTINGS_MODULE=agrivoice.settings_prod

# API Keys
OPENAI_API_KEY=sk-your-openai-key
SARVAM_API_KEY=your-sarvam-key

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@your-domain.com
```

### Domain Configuration

Update these files with your actual domain:
- `backend/agrivoice/settings_prod.py`
- `agrivoice-ui/src/utils/api.js`
- Nginx configuration

## 📊 Monitoring

### Health Checks

The application includes health check endpoints:
- `GET /api/` - API health check
- `GET /` - Frontend health check

### Logs

View logs with:
```bash
# Backend logs
docker-compose logs backend

# Frontend logs
docker-compose logs frontend

# All logs
docker-compose logs
```

## 🔄 Updates

To update the application:

```bash
# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose down
docker-compose up -d --build
```

## 🛠 Troubleshooting

### Common Issues

1. **Port conflicts:**
   - Change ports in `docker-compose.yml`

2. **Database connection:**
   - Check database credentials in `.env`
   - Ensure PostgreSQL is running

3. **Static files not loading:**
   - Run `python manage.py collectstatic` in backend container

4. **CORS errors:**
   - Update `CORS_ALLOWED_ORIGINS` in settings

### Database Migration

If you need to run migrations manually:
```bash
docker-compose exec backend python manage.py migrate
```

### Backup Database

```bash
# Create backup
docker-compose exec db pg_dump -U agrivoice_user agrivoice > backup.sql

# Restore backup
docker-compose exec -T db psql -U agrivoice_user agrivoice < backup.sql
```

## 📞 Support

For issues or questions:
1. Check the logs
2. Verify configuration
3. Test locally first
4. Check network connectivity

## 🎯 Performance Tips

1. Use a CDN for static files
2. Enable gzip compression in nginx
3. Configure database connection pooling
4. Set up monitoring and alerts
5. Use Redis for caching (future enhancement)

---

Happy deploying! 🌾🚀