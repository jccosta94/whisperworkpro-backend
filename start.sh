#!/bin/bash

# WhisperWorkPro Backend Startup Script
# This script sets up and runs the WhisperWorkPro backend

echo "🚀 Starting WhisperWorkPro Backend..."
echo "=================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11+ first."
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "main.py" ]; then
    echo "❌ main.py not found. Please run this script from the WhisperWorkPro-Backend directory."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Set environment variable
export DATABASE_URL="postgresql://postgres:#Addidas123@db.lkxsnmolnhduuiuaaswb.supabase.co:5432/postgres"

echo "✅ Setup complete!"
echo ""
echo "🌟 Starting WhisperWorkPro API server..."
echo "📍 Server will be available at: http://localhost:10000"
echo "📚 API Documentation: http://localhost:10000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the server
uvicorn main:app --host 0.0.0.0 --port 10000 --reload