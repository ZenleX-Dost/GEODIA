@echo off
title GEODIA Backend (FastAPI :8000)
cd /d "%~dp0"
echo.
echo  ========================================
echo   GEODIA Backend  ^|  http://localhost:8000
echo   API Docs        ^|  http://localhost:8000/docs
echo  ========================================
echo.
call venv\Scripts\activate.bat
python -m uvicorn app.main:app --reload --port 8000
