@echo off
title GEODIA Backend (FastAPI :8000)
cd /d "%~dp0"
echo.
echo  ========================================
echo   GEODIA Backend  ^|  http://localhost:8000
echo   API Docs        ^|  http://localhost:8000/docs
echo  ========================================
echo.

if not exist "venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment not found.
    echo         Please run start.cmd first to set up the backend.
    pause
    exit /b 1
)

venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
if errorlevel 1 (
    echo.
    echo [ERROR] Backend crashed. See error above.
    pause
)
