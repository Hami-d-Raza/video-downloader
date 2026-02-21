#!/bin/bash

# Video Downloader - Quick Setup Script (Linux/macOS)
# Run this script to set up both backend and frontend

echo "🎬 Video Downloader - Quick Setup"
echo "================================="
echo ""

# Check Python
echo "Checking Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✓ $PYTHON_VERSION"
else
    echo "✗ Python not found! Please install Python 3.8+"
    exit 1
fi

# Check Node.js
echo "Checking Node.js..."
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo "✓ Node.js $NODE_VERSION"
else
    echo "✗ Node.js not found! Please install Node.js 18+"
    exit 1
fi

# Check FFmpeg
echo "Checking FFmpeg..."
if command -v ffmpeg &> /dev/null; then
    echo "✓ FFmpeg installed"
else
    echo "⚠ FFmpeg not found! Please install FFmpeg for full functionality"
    echo "  macOS: brew install ffmpeg"
    echo "  Linux: sudo apt install ffmpeg"
fi

echo ""
echo "📦 Setting up Backend..."

# Backend setup
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Create .env if not exists
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
fi

# Deactivate venv
deactivate

echo "✓ Backend setup complete!"
echo ""

# Frontend setup
cd ../frontend

echo "📦 Setting up Frontend..."

# Install dependencies
echo "Installing Node.js dependencies..."
npm install

# Create .env if not exists
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
fi

echo "✓ Frontend setup complete!"
echo ""

# Back to root
cd ..

echo "================================="
echo "✅ Setup Complete!"
echo ""
echo "📝 Next Steps:"
echo ""
echo "1. Start Backend:"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   python main.py"
echo ""
echo "2. Start Frontend (in new terminal):"
echo "   cd frontend"
echo "   npm run dev"
echo ""
echo "3. Open browser:"
echo "   http://localhost:5173"
echo ""
echo "================================="
