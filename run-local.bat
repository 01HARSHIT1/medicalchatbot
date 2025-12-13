@echo off
REM Local Deployment Script for Windows
REM Runs everything locally without external services

echo ========================================
echo   Local Deployment - All Services
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed!
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed!
    echo Please install Node.js from https://nodejs.org
    pause
    exit /b 1
)

echo [1/4] Installing Python dependencies...
cd backend-api
if not exist "venv" (
    python -m venv venv
)
call venv\Scripts\activate.bat
pip install -r requirements.txt --quiet
cd ..

echo [2/4] Installing Node.js dependencies...
call npm install --silent

echo [3/4] Building React frontend...
call npm run build

echo [4/4] Starting services...
echo.
echo Starting Flask backend on http://localhost:5000
start "Flask Backend" cmd /k "cd backend-api && venv\Scripts\activate.bat && python main.py"

timeout /t 3 /nobreak >nul

echo Starting React frontend on http://localhost:5173
start "React Frontend" cmd /k "npm run dev"

echo.
echo ========================================
echo   Services Running!
echo ========================================
echo.
echo Frontend: http://localhost:5173
echo Backend API: http://localhost:5000
echo.
echo Press any key to stop all services...
pause >nul

taskkill /FI "WINDOWTITLE eq Flask Backend*" /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq React Frontend*" /F >nul 2>&1

