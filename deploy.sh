#!/bin/bash

# AgriVoice Deployment Script
# This script helps deploy the AgriVoice application

set -e

echo "🚀 AgriVoice Deployment Script"
echo "=============================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi

    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
}

# Setup environment
setup_environment() {
    print_status "Setting up environment..."

    # Create .env file if it doesn't exist
    if [ ! -f ".env" ]; then
        cat > .env << EOF
# Database
DB_NAME=agrivoice
DB_USER=agrivoice_user
DB_PASSWORD=your-secure-db-password

# Django
DJANGO_SECRET_KEY=your-production-secret-key-here
DJANGO_SETTINGS_MODULE=agrivoice.settings_prod

# API Keys
OPENAI_API_KEY=your-openai-api-key
SARVAM_API_KEY=your-sarvam-api-key

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-email-app-password
DEFAULT_FROM_EMAIL=noreply@your-domain.com
EOF
        print_warning "Created .env file. Please update it with your actual values!"
    fi
}

# Deploy with Docker Compose
deploy_docker() {
    print_status "Deploying with Docker Compose..."

    # Build and start services
    docker-compose up -d --build

    print_status "Waiting for services to start..."
    sleep 10

    # Run migrations
    docker-compose exec backend python manage.py migrate

    # Collect static files
    docker-compose exec backend python manage.py collectstatic --noinput

    print_status "Deployment completed!"
    print_status "Frontend: http://localhost:3000"
    print_status "Backend API: http://localhost:8000"
}

# Deploy to production server
deploy_production() {
    print_status "Deploying to production server..."

    # This would typically involve:
    # 1. Pushing to Git
    # 2. CI/CD pipeline
    # 3. Server deployment

    print_warning "Production deployment requires:"
    print_warning "1. A server (AWS, DigitalOcean, etc.)"
    print_warning "2. Domain name"
    print_warning "3. SSL certificate"
    print_warning "4. Reverse proxy (nginx)"
    print_warning "5. CI/CD pipeline"

    print_status "For now, use Docker deployment for testing"
}

# Main menu
main() {
    echo "Choose deployment option:"
    echo "1. Local Docker deployment"
    echo "2. Production deployment"
    echo "3. Setup environment"
    echo "4. Exit"

    read -p "Enter choice (1-4): " choice

    case $choice in
        1)
            check_docker
            setup_environment
            deploy_docker
            ;;
        2)
            deploy_production
            ;;
        3)
            setup_environment
            ;;
        4)
            exit 0
            ;;
        *)
            print_error "Invalid choice"
            main
            ;;
    esac
}

# Run main function
main