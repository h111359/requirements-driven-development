@echo off
REM Technical Design Schema Editor - Launcher Script for Windows
REM This script starts the editor web server and opens the browser

cd /d "%~dp0"

echo Starting Technical Design Schema Editor...
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3 to use this editor
    pause
    exit /b 1
)

REM Start the server
python server.py
pause
