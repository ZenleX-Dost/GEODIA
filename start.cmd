@echo off
setlocal EnableDelayedExpansion
title GEODIA SentinelCare - Launcher
color 0A

echo.
echo  ================================================
echo   GEODIA SentinelCare GC - Application Launcher
echo  ================================================
echo.

:: ─────────────────────────────────────────────────
:: 0. Locate script directory (works even if run from elsewhere)
:: ─────────────────────────────────────────────────
set "ROOT=%~dp0"
set "ROOT=%ROOT:~0,-1%"
set "BACKEND=%ROOT%\backend"
set "FRONTEND=%ROOT%\frontend"
set "VENV=%BACKEND%\venv"

:: ─────────────────────────────────────────────────
:: 1. Check Python — resolve full path via where
:: ─────────────────────────────────────────────────
echo [1/5] Checking Python installation...
for /f "tokens=* usebackq" %%P in (`where python 2^>nul`) do (
    if not defined PYTHON_EXE set "PYTHON_EXE=%%P"
)
if not defined PYTHON_EXE (
    echo [ERROR] Python is not installed or not in PATH.
    echo         Please install Python 3.10+ from https://www.python.org/downloads/
    echo         Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)
for /f "tokens=*" %%V in ('"%PYTHON_EXE%" --version 2^>^&1') do echo         Found: %%V ^| Path: %PYTHON_EXE%

:: ─────────────────────────────────────────────────
:: 2. Check Node / npm — resolve full paths via where
:: ─────────────────────────────────────────────────
echo.
echo [2/5] Checking Node.js / npm installation...
for /f "tokens=* usebackq" %%P in (`where node 2^>nul`) do (
    if not defined NODE_EXE set "NODE_EXE=%%P"
)
if not defined NODE_EXE (
    echo [ERROR] Node.js is not installed or not in PATH.
    echo         Please install Node.js 18+ from https://nodejs.org/
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
    echo [ERROR] npm is not available. Please reinstall Node.js.
    pause
    exit /b 1
)
for /f "tokens=*" %%V in ('"%NODE_EXE%" --version 2^>^&1') do echo         Found Node: %%V
for /f "tokens=*" %%V in ('"%NPM_CMD%" --version 2^>^&1') do echo         Found npm:  %%V

:: ─────────────────────────────────────────────────
:: 3. Backend setup — virtual env + pip install
:: ─────────────────────────────────────────────────
echo.
echo [3/5] Setting up Python backend...

if not exist "%VENV%\Scripts\python.exe" (
    echo         Creating virtual environment...
    "%PYTHON_EXE%" -m venv "%VENV%"
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
    echo         Virtual environment created.
)

set "VENV_PY=%VENV%\Scripts\python.exe"
set "VENV_PIP=%VENV%\Scripts\pip.exe"

echo         Checking / installing Python dependencies...
"%VENV_PIP%" install --quiet --upgrade pip
"%VENV_PIP%" install --quiet -r "%BACKEND%\requirements.txt"
if errorlevel 1 (
    echo [ERROR] pip install failed. Check your internet connection and requirements.txt.
    pause
    exit /b 1
)
echo         Python dependencies OK.

:: ─────────────────────────────────────────────────
:: 4. Frontend setup — npm install if node_modules missing
:: ─────────────────────────────────────────────────
echo.
echo [4/5] Setting up Node frontend...

if not exist "%FRONTEND%\node_modules" (
    echo         node_modules not found - running npm install...
    pushd "%FRONTEND%"
    "%NPM_CMD%" install
    if errorlevel 1 (
        echo [ERROR] npm install failed. Check your internet connection.
        popd
        pause
        exit /b 1
    )
    popd
    echo         npm install complete.
) else (
    echo         node_modules already present. Skipping install.
    echo         (Delete frontend\node_modules to force a fresh install.)
)

:: ─────────────────────────────────────────────────
:: 5. Write resolved paths into helper scripts and launch
:: ─────────────────────────────────────────────────
echo.
echo [5/5] Launching servers...

:: Launch Backend — calls _run.cmd which uses absolute venv python path
start "GEODIA Backend" cmd /k "%BACKEND%\_run.cmd"

:: Give backend a moment to start
timeout /t 3 /nobreak >nul

:: Launch Frontend — calls _run.cmd which uses absolute npm path
start "GEODIA Frontend" cmd /k "%FRONTEND%\_run.cmd"

echo.
echo  Backend   ^>  http://localhost:8000
echo  API Docs  ^>  http://localhost:8000/docs
echo  Frontend  ^>  http://localhost:5173
echo.
echo  Waiting for servers to initialize...
timeout /t 6 /nobreak >nul

echo  Opening app in browser...
start "" "http://localhost:5173"

echo.
echo  Both servers are running in their own windows.
echo  Close those windows to stop the servers.
echo.
pause
endlocal
