#!/bin/bash

# Start AgriVoice Project
echo "🚀 Starting AgriVoice Project"
echo "============================"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Start backend
echo -e "${GREEN}[1/2]${NC} Starting Django Backend..."
cd d:/agrivoice/backend
python manage.py runserver &
BACKEND_PID=$!
echo -e "${GREEN}✅ Backend started (PID: $BACKEND_PID)${NC}"

# Give backend time to start
sleep 3

# Start frontend
echo -e "${GREEN}[2/2]${NC} Starting React Frontend..."
cd d:/agrivoice/agrivoice-ui
npm start &
FRONTEND_PID=$!
echo -e "${GREEN}✅ Frontend started (PID: $FRONTEND_PID)${NC}"

echo ""
echo -e "${YELLOW}🌐 Application is starting...${NC}"
echo "Frontend: http://localhost:3000"
echo "Backend:  http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for both processes
wait