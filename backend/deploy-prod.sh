#!/bin/bash

# Complete AgriVoice DigitalOcean Deployment Script
# Run this after the initial server setup

set -e

DOMAIN=${1:-"yourdomain.com"}
EMAIL=${2:-"admin@yourdomain.com"}

echo "🚀 AgriVoice Production Deployment to DigitalOcean"
echo "================================================="
echo "Domain: $DOMAIN"
echo "Email: $EMAIL"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're running as root or with sudo
if [[ $EUID -eq 0 ]]; then
   print_error "Don't run this script as root. Use your regular user account."
   exit 1
fi

# Update domain in configuration files
print_status "Updating configuration with your domain..."

# Update nginx config
sed -i "s/yourdomain.com/$DOMAIN/g" nginx.conf

# Update production settings
sed -i "s/your-domain.com/$DOMAIN/g" agrivoice/settings_prod.py

# Update frontend API URL
sed -i "s/your-domain.com/$DOMAIN/g" ../agrivoice-ui/src/utils/api.js

# Copy environment file
if [ ! -f ".env" ]; then
    cp .env.example .env
    print_warning "Created .env file. You MUST edit it with your actual credentials!"
    print_warning "Required: DJANGO_SECRET_KEY, API keys, email credentials"
    echo ""
    read -p "Press Enter after you've edited the .env file..."
fi

# Build and deploy
print_status "Building and deploying application..."
docker-compose -f docker-compose.prod.yml down 2>/dev/null || true
docker-compose -f docker-compose.prod.yml up -d --build

# Wait for services to start
print_status "Waiting for services to initialize..."
sleep 30

# Run migrations
print_status "Running database migrations..."
docker-compose -f docker-compose.prod.yml exec -T backend python manage.py migrate

# Collect static files
print_status "Collecting static files..."
docker-compose -f docker-compose.prod.yml exec -T backend python manage.py collectstatic --noinput

# Restart services
print_status "Restarting services..."
docker-compose -f docker-compose.prod.yml restart

# Setup nginx
print_status "Setting up nginx..."
sudo cp ../nginx.conf /etc/nginx/sites-available/$DOMAIN
sudo ln -sf /etc/nginx/sites-available/$DOMAIN /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# Setup SSL
print_status "Setting up SSL certificate..."
sudo certbot --nginx -d $DOMAIN -d www.$DOMAIN --email $EMAIL --agree-tos --non-interactive

# Final restart
print_status "Final service restart..."
docker-compose -f docker-compose.prod.yml restart

# Setup monitoring
print_status "Setting up basic monitoring..."
docker-compose -f docker-compose.prod.yml logs -f --tail=50

print_status "🎉 Deployment completed successfully!"
echo ""
echo "🌐 Your application is now live at:"
echo "   https://$DOMAIN"
echo "   https://www.$DOMAIN"
echo ""
echo "🔧 Useful commands:"
echo "   Check logs: docker-compose -f docker-compose.prod.yml logs -f"
echo "   Restart: docker-compose -f docker-compose.prod.yml restart"
echo "   Update: git pull && docker-compose -f docker-compose.prod.yml up -d --build"
echo ""
echo "📊 Monitor your app:"
echo "   Backend health: https://$DOMAIN/api/"
echo "   Frontend: https://$DOMAIN"
echo ""
print_warning "Don't forget to:"
echo "   - Update DNS records to point to this server"
echo "   - Test all features thoroughly"
echo "   - Set up backups for the database"
echo "   - Configure monitoring alerts"