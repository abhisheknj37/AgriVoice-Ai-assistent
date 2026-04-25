@echo off
REM Start AgriVoice Project on Windows

echo.
echo 🚀 Starting AgriVoice Project
echo =============================
echo.

echo [1/2] Starting Django Backend...
cd /d d:\agrivoice\backend
start "AgriVoice Backend" cmd /k "python manage.py runserver"

echo [2/2] Starting React Frontend...
cd /d d:\agrivoice\agrivoice-ui
start "AgriVoice Frontend" cmd /k "npm install && npm start"

echo.
echo 🌐 Application is starting...
echo Frontend: http://localhost:3000
echo Backend:  http://localhost:8000
echo.
echo Close these windows when you're done.