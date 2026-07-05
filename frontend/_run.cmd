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

for /f "tokens=* usebackq" %%P in (`where npm.cmd 2^>nul`) do (
    if not defined NPM_CMD set "NPM_CMD=%%P"
)
if not defined NPM_CMD (
    for /f "tokens=* usebackq" %%P in (`where npm 2^>nul`) do (
        if not defined NPM_CMD set "NPM_CMD=%%P"
    )
)
if not defined NPM_CMD (
    echo [ERROR] npm could not be found. Please install Node.js.
    pause
    exit /b 1
)

"%NPM_CMD%" run dev
if errorlevel 1 (
    echo.
    echo [ERROR] Frontend crashed. See error above.
    pause
)
