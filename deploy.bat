@echo off
REM AgriVoice Deployment Script for Windows

echo 🚀 AgriVoice Deployment Script
echo ===============================

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker is not installed. Please install Docker first.
    pause
    exit /b 1
)

docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker Compose is not installed. Please install Docker Compose first.
    pause
    exit /b 1
)

echo [INFO] Setting up environment...

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo # Database > .env
    echo DB_NAME=agrivoice >> .env
    echo DB_USER=agrivoice_user >> .env
    echo DB_PASSWORD=your-secure-db-password >> .env
    echo. >> .env
    echo # Django >> .env
    echo DJANGO_SECRET_KEY=your-production-secret-key-here >> .env
    echo DJANGO_SETTINGS_MODULE=agrivoice.settings_prod >> .env
    echo. >> .env
    echo # API Keys >> .env
    echo OPENAI_API_KEY=your-openai-api-key >> .env
    echo SARVAM_API_KEY=your-sarvam-api-key >> .env
    echo. >> .env
    echo # Email >> .env
    echo EMAIL_HOST=smtp.gmail.com >> .env
    echo EMAIL_PORT=587 >> .env
    echo EMAIL_HOST_USER=your-email@gmail.com >> .env
    echo EMAIL_HOST_PASSWORD=your-email-app-password >> .env
    echo DEFAULT_FROM_EMAIL=noreply@your-domain.com >> .env
    echo [WARNING] Created .env file. Please update it with your actual values!
    pause
)

echo [INFO] Deploying with Docker Compose...

REM Build and start services
docker-compose up -d --build

echo [INFO] Waiting for services to start...
timeout /t 10 /nobreak >nul

REM Run migrations
docker-compose exec backend python manage.py migrate

REM Collect static files
docker-compose exec backend python manage.py collectstatic --noinput

echo [INFO] Deployment completed!
echo [INFO] Frontend: http://localhost:3000
echo [INFO] Backend API: http://localhost:8000
echo.
echo Press any key to exit...
pause >nul