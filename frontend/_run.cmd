@echo off
title GEODIA Frontend (Vite :5173)
cd /d "%~dp0"
echo.
echo  ========================================
echo   GEODIA Frontend  ^|  http://localhost:5173
echo  ========================================
echo.

if not exist "node_modules" (
    echo [ERROR] node_modules not found.
    echo         Please run start.cmd first to install npm dependencies.
    pause
    exit /b 1
)

npm.cmd run dev
if errorlevel 1 (
    echo.
    echo [ERROR] Frontend crashed. See error above.
    pause
)
