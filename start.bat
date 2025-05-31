@echo off
REM WhisperWorkPro Backend Startup Script for Windows
REM This script sets up and runs the WhisperWorkPro backend

echo 🚀 Starting WhisperWorkPro Backend...
echo ==================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.11+ first.
    pause
    exit /b 1
)

REM Check if we're in the right directory
if not exist "main.py" (
    echo ❌ main.py not found. Please run this script from the WhisperWorkPro-Backend directory.
    pause
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo 📥 Installing dependencies...
pip install -r requirements.txt

REM Set environment variable
set DATABASE_URL=postgresql://postgres:#Addidas123@db.lkxsnmolnhduuiuaaswb.supabase.co:5432/postgres

echo ✅ Setup complete!
echo.
echo 🌟 Starting WhisperWorkPro API server...
echo 📍 Server will be available at: http://localhost:10000
echo 📚 API Documentation: http://localhost:10000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start the server
uvicorn main:app --host 0.0.0.0 --port 10000 --reload

pause