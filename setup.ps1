# Video Downloader - Quick Setup Script
# Run this script to set up both backend and frontend

Write-Host "🎬 Video Downloader - Quick Setup" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
Write-Host "Checking Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found! Please install Python 3.8+" -ForegroundColor Red
    exit 1
}

# Check Node.js
Write-Host "Checking Node.js..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version 2>&1
    Write-Host "✓ Node.js $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Node.js not found! Please install Node.js 18+" -ForegroundColor Red
    exit 1
}

# Check FFmpeg
Write-Host "Checking FFmpeg..." -ForegroundColor Yellow
try {
    $ffmpegVersion = ffmpeg -version 2>&1 | Select-Object -First 1
    Write-Host "✓ FFmpeg installed" -ForegroundColor Green
} catch {
    Write-Host "⚠ FFmpeg not found! Please install FFmpeg for full functionality" -ForegroundColor Yellow
    Write-Host "  Install with: choco install ffmpeg" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "📦 Setting up Backend..." -ForegroundColor Cyan

# Backend setup
Set-Location backend

# Create virtual environment
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Install dependencies
Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Create .env if not exists
if (-not (Test-Path ".env")) {
    Write-Host "Creating .env file..." -ForegroundColor Yellow
    Copy-Item .env.example .env
}

# Deactivate venv
deactivate

Write-Host "✓ Backend setup complete!" -ForegroundColor Green
Write-Host ""

# Frontend setup
Set-Location ../frontend

Write-Host "📦 Setting up Frontend..." -ForegroundColor Cyan

# Install dependencies
Write-Host "Installing Node.js dependencies..." -ForegroundColor Yellow
npm install

# Create .env if not exists
if (-not (Test-Path ".env")) {
    Write-Host "Creating .env file..." -ForegroundColor Yellow
    Copy-Item .env.example .env
}

Write-Host "✓ Frontend setup complete!" -ForegroundColor Green
Write-Host ""

# Back to root
Set-Location ..

Write-Host "=================================" -ForegroundColor Cyan
Write-Host "✅ Setup Complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📝 Next Steps:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Start Backend:" -ForegroundColor Yellow
Write-Host "   cd backend" -ForegroundColor White
Write-Host "   .\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "   python main.py" -ForegroundColor White
Write-Host ""
Write-Host "2. Start Frontend (in new terminal):" -ForegroundColor Yellow
Write-Host "   cd frontend" -ForegroundColor White
Write-Host "   npm run dev" -ForegroundColor White
Write-Host ""
Write-Host "3. Open browser:" -ForegroundColor Yellow
Write-Host "   http://localhost:5173" -ForegroundColor White
Write-Host ""
Write-Host "=================================" -ForegroundColor Cyan
