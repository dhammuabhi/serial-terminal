@echo off
REM Builds dist\SerialTerminal.exe on Windows. Requires Python 3.8+ from python.org (with tcl/tk).
REM Right-click this file and select "Run as administrator" for COM port access

echo.
echo ============================================
echo Serial Terminal - Windows Build Script
echo ============================================
echo.

cd /d "%~dp0"

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo Installing/upgrading build tools...
python -m pip install --upgrade pip pyserial pyinstaller
if errorlevel 1 goto :err

echo.
echo Building Serial Terminal executable...
python -m PyInstaller --noconfirm --onefile --windowed ^
    --name SerialTerminal ^
    --icon=NONE ^
    serial_terminal.py
if errorlevel 1 goto :err

echo.
echo ============================================
echo ✓ Successfully built dist\SerialTerminal.exe
echo ============================================
echo.
echo To run the application:
echo   1. Double-click dist\SerialTerminal.exe
echo   2. Or run from Command Prompt: dist\SerialTerminal.exe
echo.
pause
exit /b 0

:err
echo.
echo ============================================
echo ✗ Build failed
echo ============================================
echo.
echo Troubleshooting:
echo - Ensure Python 3.8+ is installed with tcl/tk
echo - Run as Administrator for COM port access
echo - Check that you're in the correct directory
echo.
pause
exit /b 1
