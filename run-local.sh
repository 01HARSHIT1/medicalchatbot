#!/bin/bash
# Local Deployment Script for Linux/Mac
# Runs everything locally without external services

echo "========================================"
echo "  Local Deployment - All Services"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed!"
    echo "Please install Python 3.8+ from https://python.org"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "ERROR: Node.js is not installed!"
    echo "Please install Node.js from https://nodejs.org"
    exit 1
fi

echo "[1/4] Installing Python dependencies..."
cd backend-api
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install -r requirements.txt --quiet
cd ..

echo "[2/4] Installing Node.js dependencies..."
npm install --silent

echo "[3/4] Building React frontend..."
npm run build

echo "[4/4] Starting services..."
echo ""
echo "Starting Flask backend on http://localhost:5000"
cd backend-api
source venv/bin/activate
python main.py &
BACKEND_PID=$!
cd ..

sleep 3

echo "Starting React frontend on http://localhost:5173"
npm run dev &
FRONTEND_PID=$!

echo ""
echo "========================================"
echo "  Services Running!"
echo "========================================"
echo ""
echo "Frontend: http://localhost:5173"
echo "Backend API: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop all services..."

# Trap Ctrl+C and kill processes
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT TERM

wait

