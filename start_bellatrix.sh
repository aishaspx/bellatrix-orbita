#!/bin/bash
echo "🚀 Initializing Bellatrix Fullstack..."

# 1. Clean up old processes (Force kill ports 8000 and 8080)
echo "🧹 Cleaning up ports..."
lsof -ti :8000 | xargs kill -9 2>/dev/null
lsof -ti :8080 | xargs kill -9 2>/dev/null
lsof -ti :8081 | xargs kill -9 2>/dev/null
lsof -ti :8082 | xargs kill -9 2>/dev/null
lsof -ti :8083 | xargs kill -9 2>/dev/null
lsof -ti :8084 | xargs kill -9 2>/dev/null

# 2. Start Backend (Port 8000)
echo "🛰️ Starting Backend (FastAPI) on port 8000..."
cd backend
# Run in background & save PID
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 > ../backend.log 2>&1 &
BACKEND_PID=$!
cd ..

# 3. Start Frontend (Port 8080)
echo "🌍 Starting Frontend (HTTP Server) on port 8084..."
# Serve the 'frontend' directory as root
python3 -m http.server 8084 --directory frontend > ../frontend.log 2>&1 &
FRONTEND_PID=$!

echo "✅ Services Started!"
echo "   Backend PID: $BACKEND_PID"
echo "   Frontend PID: $FRONTEND_PID"

# 4. Open Application
echo "🔓 Opening http://localhost:8084..."
sleep 2
open http://localhost:8084

# 5. Keep alive and handle exit
trap "kill $BACKEND_PID $FRONTEND_PID; exit" SIGINT SIGTERM
echo "Press CTRL+C to stop servers."
wait