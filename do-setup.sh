#!/bin/bash

# AgriVoice DigitalOcean Deployment Script
# Run this on your DO droplet after initial setup

set -e

echo "🚀 AgriVoice DigitalOcean Deployment"
echo "==================================="

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

# Update system
print_status "Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install required packages
print_status "Installing required packages..."
sudo apt install -y curl wget git ufw nginx certbot python3-certbot-nginx

# Install Docker
print_status "Installing Docker..."
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
print_status "Installing Docker Compose..."
sudo curl -L "https://github.com/docker/compose/releases/download/v2.17.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Enable firewall
print_status "Configuring firewall..."
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw --force enable

# Create application directory
print_status "Setting up application directory..."
sudo mkdir -p /var/www/agrivoice
sudo chown -R $USER:$USER /var/www/agrivoice
cd /var/www/agrivoice

print_status "✅ Server setup complete!"
print_warning "Next steps:"
echo "1. Clone your repository: git clone <your-repo-url> ."
echo "2. Configure environment: cp backend/.env.example backend/.env"
echo "3. Edit .env file with your API keys"
echo "4. Run: cd backend && docker-compose -f docker-compose.prod.yml up -d --build"
echo "5. Configure nginx and SSL certificates"