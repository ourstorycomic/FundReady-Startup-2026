@echo off
echo Starting FundReady-AI Servers...

echo Starting Backend Server (Uvicorn) on port 8001...
start "Backend" cmd /k "cd backend_open && python -m uvicorn main:app --port 8001 --reload"

echo Starting Frontend Server (HTTP) on port 3000...
start "Frontend" cmd /k "cd frontend && python -m http.server 3000"

echo Servers are running!
echo Backend API is at: http://localhost:8001
echo Frontend UI is at: http://localhost:3000
