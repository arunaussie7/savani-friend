# 🚀 Quick Installation Guide

## 📱 **Windows Users (Easiest)**

1. **Download** the project from GitHub
2. **Double-click** `install_and_run.bat`
3. **Wait** for automatic setup
4. **Website opens automatically** in your browser

## 🍎 **macOS Users**

1. **Download** the project from GitHub
2. **Open Terminal** in the project folder
3. **Run**: `./install_and_run.sh`
4. **Website opens automatically** in your browser

## 🐧 **Linux Users**

1. **Download** the project from GitHub
2. **Open Terminal** in the project folder
3. **Run**: `./install_and_run.sh`
4. **Website opens automatically** in your browser

## 🔧 **Manual Installation**

If the automatic scripts don't work:

### **Prerequisites**
- Python 3.9 or higher
- pip (Python package installer)

### **Steps**
```bash
# 1. Install dependencies
python -m pip install -r requirements.txt

# 2. Setup database
python manage.py makemigrations
python manage.py migrate

# 3. Start server
python manage.py runserver

# 4. Open browser
# Go to: http://127.0.0.1:8000
```

## ❓ **Need Help?**

- **Check Python version**: `python --version`
- **Check pip**: `python -m pip --version`
- **Common issues**: See README.md troubleshooting section
- **GitHub Issues**: Report problems on the repository

## 🌐 **Access the Website**

Once running, open your browser and go to:
**http://127.0.0.1:8000**

---

**🎉 That's it! Your Market Screener is ready to use!**
