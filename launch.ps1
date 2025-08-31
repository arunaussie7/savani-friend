# Market Screener - PowerShell Launcher
# For Windows users who prefer PowerShell

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    📈 Market Screener Setup" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "This script will automatically:" -ForegroundColor White
Write-Host "1. Check Python installation" -ForegroundColor White
Write-Host "2. Install all dependencies" -ForegroundColor White
Write-Host "3. Set up the database" -ForegroundColor White
Write-Host "4. Start the website" -ForegroundColor White
Write-Host ""

# Check if Python is installed
Write-Host "[1/4] Checking Python installation..." -ForegroundColor Blue
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Python is installed: $pythonVersion" -ForegroundColor Green
    } else {
        throw "Python not found"
    }
} catch {
    Write-Host "❌ Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Python 3.9+ from: https://python.org" -ForegroundColor Yellow
    Write-Host "Make sure to check 'Add Python to PATH' during installation" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if pip is available
Write-Host "[2/4] Checking pip installation..." -ForegroundColor Blue
try {
    $pipVersion = python -m pip --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ pip is available: $pipVersion" -ForegroundColor Green
    } else {
        throw "pip not found"
    }
} catch {
    Write-Host "❌ pip is not available" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please reinstall Python and ensure pip is included" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

# Upgrade pip
Write-Host "[3/4] Upgrading pip..." -ForegroundColor Blue
python -m pip install --upgrade pip
Write-Host ""

# Install requirements
Write-Host "[4/4] Installing project dependencies..." -ForegroundColor Blue
Write-Host "This may take a few minutes..." -ForegroundColor Yellow
python -m pip install -r requirements.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please check your internet connection and try again" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "✅ Dependencies installed successfully" -ForegroundColor Green
Write-Host ""

# Run database migrations
Write-Host "[5/5] Setting up database..." -ForegroundColor Blue
python manage.py makemigrations
python manage.py migrate

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Database setup failed" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please check the error messages above" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "✅ Database setup complete" -ForegroundColor Green
Write-Host ""

# Start the server
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    🚀 Starting Market Screener" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Website will open automatically in your browser" -ForegroundColor White
Write-Host "If it doesn't open, go to: http://127.0.0.1:8000" -ForegroundColor White
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Open browser after a short delay
Start-Sleep -Seconds 3
Start-Process "http://127.0.0.1:8000"

# Start Django server
python manage.py runserver

Write-Host ""
Write-Host "Server stopped. Press Enter to exit..." -ForegroundColor Yellow
Read-Host
