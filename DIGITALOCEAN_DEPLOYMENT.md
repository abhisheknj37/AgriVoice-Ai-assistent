# 🚀 AgriVoice DigitalOcean Deployment Guide

## Prerequisites
- DigitalOcean account ($5/month droplet)
- Domain name ($10-15/year)
- GitHub repository with your code

---

## Step 1: Create DigitalOcean Droplet

### 1.1 Create Account & Droplet
1. Go to [digitalocean.com](https://digitalocean.com)
2. Sign up/Login to your account
3. Click "Create" → "Droplets"
4. Choose configuration:
   - **Image**: Ubuntu 22.04 LTS
   - **Plan**: Basic ($6/month - 1GB RAM, 1 CPU)
   - **Datacenter**: Choose closest to your users
   - **Authentication**: SSH Key (recommended) or password

### 1.2 Initial Server Setup
```bash
# Connect to your droplet
ssh root@your-droplet-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Create a non-root user
adduser agrivoice
usermod -aG sudo agrivoice

# Setup SSH for the new user
mkdir -p /home/agrivoice/.ssh
cp ~/.ssh/authorized_keys /home/agrivoice/.ssh/
chown -R agrivoice:agrivoice /home/agrivoice/.ssh

# Switch to the new user
su - agrivoice
```

---

## Step 2: Domain & DNS Setup

### 2.1 Point Domain to DigitalOcean
1. Login to your domain registrar
2. Update nameservers to:
   ```
   ns1.digitalocean.com
   ns2.digitalocean.com
   ns3.digitalocean.com
   ```

### 2.2 Create DNS Records
1. In DigitalOcean dashboard → Networking → Domains
2. Add your domain
3. Create A records:
   ```
   Type: A
   Hostname: @
   Value: your-droplet-ip

   Type: A
   Hostname: www
   Value: your-droplet-ip
   ```

---

## Step 3: Deploy Application

### 3.1 Clone Repository
```bash
# On your droplet as agrivoice user
cd ~
git clone https://github.com/yourusername/agrivoice.git
cd agrivoice
```

### 3.2 Run Initial Setup
```bash
# Make scripts executable
chmod +x do-setup.sh backend/deploy-prod.sh

# Run initial server setup
./do-setup.sh
```

### 3.3 Configure Environment
```bash
cd backend

# Copy environment template
cp .env.example .env

# Edit with your values
nano .env
```

**Required environment variables:**
```env
# Generate a secure Django secret key
DJANGO_SECRET_KEY=your-64-char-secret-here

# Get from OpenAI: https://platform.openai.com/api-keys
OPENAI_API_KEY=sk-your-key-here

# Get from Sarvam AI: https://sarvam.ai
SARVAM_API_KEY=your-sarvam-key-here

# Gmail app password: https://myaccount.google.com/apppasswords
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Your domain
DOMAIN=yourdomain.com
```

### 3.4 Deploy Application
```bash
# Run production deployment
./deploy-prod.sh yourdomain.com admin@yourdomain.com
```

---

## Step 4: Verify Deployment

### 4.1 Check Services
```bash
# Check running containers
docker ps

# Check logs
docker-compose -f docker-compose.prod.yml logs -f
```

### 4.2 Test Application
- **Frontend**: https://yourdomain.com
- **Backend API**: https://yourdomain.com/api/
- **Registration**: Try creating a user account

### 4.3 SSL Certificate
The script automatically sets up Let's Encrypt SSL certificates.

---

## Step 5: Post-Deployment Tasks

### 5.1 Database Backup
```bash
# Create backup script
cat > ~/backup-db.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
docker-compose -f agrivoice/backend/docker-compose.prod.yml exec -T db pg_dump -U agrivoice_user agrivoice_prod > ~/backup_$DATE.sql
echo "Backup created: ~/backup_$DATE.sql"
EOF

chmod +x ~/backup-db.sh

# Setup cron for daily backups
crontab -e
# Add: 0 2 * * * /home/agrivoice/backup-db.sh
```

### 5.2 Monitoring Setup
```bash
# Install monitoring tools
sudo apt install htop iotop

# Check resource usage
htop
df -h  # Disk usage
docker stats  # Container resources
```

### 5.3 Security Hardening
```bash
# Setup fail2ban for SSH protection
sudo apt install fail2ban
sudo systemctl enable fail2ban

# Disable root login
sudo nano /etc/ssh/sshd_config
# Set: PermitRootLogin no
sudo systemctl restart sshd
```

---

## Troubleshooting

### Common Issues

**1. Port 80/443 already in use**
```bash
sudo netstat -tulpn | grep :80
sudo netstat -tulpn | grep :443
# Kill conflicting processes
```

**2. SSL Certificate Issues**
```bash
sudo certbot certificates
sudo certbot renew
```

**3. Database Connection Issues**
```bash
# Check database logs
docker-compose -f docker-compose.prod.yml logs db

# Test connection
docker-compose -f docker-compose.prod.yml exec db psql -U agrivoice_user -d agrivoice_prod
```

**4. Application Not Loading**
```bash
# Check nginx config
sudo nginx -t
sudo systemctl reload nginx

# Check application logs
docker-compose -f docker-compose.prod.yml logs backend
docker-compose -f docker-compose.prod.yml logs frontend
```

---

## Maintenance Commands

```bash
# Update application
cd ~/agrivoice
git pull
cd backend
docker-compose -f docker-compose.prod.yml up -d --build

# View logs
docker-compose -f docker-compose.prod.yml logs -f

# Restart services
docker-compose -f docker-compose.prod.yml restart

# Scale resources (if needed)
# In DigitalOcean dashboard: Resize droplet
```

---

## Cost Breakdown

- **DigitalOcean Droplet**: $6/month (1GB RAM)
- **Domain**: $10-15/year
- **SSL Certificate**: Free (Let's Encrypt)
- **Total**: ~$17/month + domain

---

## Next Steps

1. **Test all features** thoroughly
2. **Set up monitoring** (optional: DataDog, New Relic)
3. **Configure backups** (automated off-server backups)
4. **Set up CDN** (optional: Cloudflare for static assets)
5. **Add analytics** (Google Analytics, etc.)

Your AgriVoice application is now live! 🌾🚀

**Need help?** Check the logs or contact support.