@echo off
title Create Desktop Shortcut
color 0B

echo.
echo ========================================
echo    📈 Market Screener Shortcut
echo ========================================
echo.
echo This will create a desktop shortcut for easy access
echo.

:: Get the current directory
set "CURRENT_DIR=%~dp0"
set "BATCH_FILE=%CURRENT_DIR%install_and_run.bat"

:: Get desktop path
for /f "tokens=2*" %%a in ('reg query "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders" /v Desktop 2^>nul') do set "DESKTOP=%%b"

:: Create shortcut
echo Creating desktop shortcut...
echo Set oWS = WScript.CreateObject("WScript.Shell") > "%TEMP%\CreateShortcut.vbs"
echo sLinkFile = "%DESKTOP%\Market Screener.lnk" >> "%TEMP%\CreateShortcut.vbs"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%TEMP%\CreateShortcut.vbs"
echo oLink.TargetPath = "%BATCH_FILE%" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.WorkingDirectory = "%CURRENT_DIR%" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.Description = "Market Screener - Stock Market Analysis Platform" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.IconLocation = "%CURRENT_DIR%static\images\icon.ico,0" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.Save >> "%TEMP%\CreateShortcut.vbs"
cscript //nologo "%TEMP%\CreateShortcut.vbs"
del "%TEMP%\CreateShortcut.vbs"

if exist "%DESKTOP%\Market Screener.lnk" (
    echo ✅ Desktop shortcut created successfully!
    echo.
    echo You can now double-click the shortcut on your desktop
    echo to launch Market Screener anytime.
) else (
    echo ❌ Failed to create desktop shortcut
    echo.
    echo You can still run the program by double-clicking:
    echo install_and_run.bat
)

echo.
echo Press any key to exit...
pause >nul
