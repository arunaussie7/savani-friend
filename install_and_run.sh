#!/bin/bash

# Market Screener - Installation and Setup Script
# For macOS and Linux

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Clear screen and show header
clear
echo "========================================"
echo "    📈 Market Screener Setup"
echo "========================================"
echo
echo "This script will automatically:"
echo "1. Check Python installation"
echo "2. Install all dependencies"
echo "3. Set up the database"
echo "4. Start the website"
echo

# Check if Python is installed
print_status "Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    print_success "Python3 found: $(python3 --version)"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
    print_success "Python found: $(python --version)"
else
    print_error "Python is not installed"
    echo
    echo "Please install Python 3.9+ from: https://python.org"
    echo "Or use your package manager:"
    echo "  Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "  macOS: brew install python3"
    echo "  CentOS/RHEL: sudo yum install python3 python3-pip"
    echo
    exit 1
fi

# Check if pip is available
print_status "Checking pip installation..."
if $PYTHON_CMD -m pip --version &> /dev/null; then
    print_success "pip is available"
else
    print_error "pip is not available"
    echo
    echo "Please install pip:"
    echo "  curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py"
    echo "  $PYTHON_CMD get-pip.py"
    echo
    exit 1
fi

# Upgrade pip
print_status "Upgrading pip..."
$PYTHON_CMD -m pip install --upgrade pip
echo

# Install requirements
print_status "Installing project dependencies..."
echo "This may take a few minutes..."
$PYTHON_CMD -m pip install -r requirements.txt

if [ $? -ne 0 ]; then
    print_error "Failed to install dependencies"
    echo
    echo "Please check your internet connection and try again"
    echo
    exit 1
fi

print_success "Dependencies installed successfully"
echo

# Run database migrations
print_status "Setting up database..."
$PYTHON_CMD manage.py makemigrations
$PYTHON_CMD manage.py migrate

if [ $? -ne 0 ]; then
    print_error "Database setup failed"
    echo
    echo "Please check the error messages above"
    echo
    exit 1
fi

print_success "Database setup complete"
echo

# Start the server
echo "========================================"
echo "    🚀 Starting Market Screener"
echo "========================================"
echo
echo "Website will open automatically in your browser"
echo "If it doesn't open, go to: http://127.0.0.1:8000"
echo
echo "Press Ctrl+C to stop the server"
echo

# Open browser after a short delay (macOS and Linux)
sleep 3
if command -v xdg-open &> /dev/null; then
    # Linux
    xdg-open http://127.0.0.1:8000 &
elif command -v open &> /dev/null; then
    # macOS
    open http://127.0.0.1:8000 &
fi

# Start Django server
$PYTHON_CMD manage.py runserver

echo
echo "Server stopped."
