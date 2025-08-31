@echo off
title Market Screener - Installation and Setup
color 0A

echo.
echo ========================================
echo    📈 Market Screener Setup
echo ========================================
echo.
echo This script will automatically:
echo 1. Check Python installation
echo 2. Install all dependencies
echo 3. Set up the database
echo 4. Start the website
echo.

:: Check if Python is installed
echo [1/4] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo.
    echo Please install Python 3.9+ from: https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

python --version
echo ✅ Python is installed
echo.

:: Check if pip is available
echo [2/4] Checking pip installation...
python -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip is not available
    echo.
    echo Please reinstall Python and ensure pip is included
    echo.
    pause
    exit /b 1
)

echo ✅ pip is available
echo.

:: Upgrade pip
echo [3/4] Upgrading pip...
python -m pip install --upgrade pip
echo.

:: Install requirements
echo [4/4] Installing project dependencies...
echo This may take a few minutes...
python -m pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies
    echo.
    echo Please check your internet connection and try again
    echo.
    pause
    exit /b 1
)

echo ✅ Dependencies installed successfully
echo.

:: Run database migrations
echo [5/5] Setting up database...
python manage.py makemigrations
python manage.py migrate

if %errorlevel% neq 0 (
    echo ❌ Database setup failed
    echo.
    echo Please check the error messages above
    echo.
    pause
    exit /b 1
)

echo ✅ Database setup complete
echo.

:: Start the server
echo ========================================
echo    🚀 Starting Market Screener
echo ========================================
echo.
echo Website will open automatically in your browser
echo If it doesn't open, go to: http://127.0.0.1:8000
echo.
echo Press Ctrl+C to stop the server
echo.

:: Open browser after a short delay
timeout /t 3 /nobreak >nul
start http://127.0.0.1:8000

:: Start Django server
python manage.py runserver

echo.
echo Server stopped. Press any key to exit...
pause >nul
