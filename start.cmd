@echo off
echo Starting GEODIA Application...

echo Starting Backend (FastAPI)...
start "GEODIA Backend" cmd /k "cd backend && uvicorn app.main:app --reload --port 8000"

echo Starting Frontend (React/Vite)...
start "GEODIA Frontend" cmd /k "cd frontend && npm run dev"

echo Both servers are starting up!
echo Backend should be available at http://localhost:8000
echo Frontend should be available at http://localhost:5173
