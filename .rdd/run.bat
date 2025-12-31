@echo off
REM RDD Web Interface Launcher for Windows
REM This script starts the RDD Web UI server and automatically opens it in the default browser

echo.
echo ========================================
echo RDD Web Interface Launcher
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Remediation: Please install Python 3.11 or higher and ensure it is in your PATH
    echo Download from: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo Starting RDD Web UI server...
echo.

REM Start the server - it will automatically open the browser
python "%~dp0src\web\server.py"

REM If the server exits with an error, pause so the user can read the error message
if errorlevel 1 (
    echo.
    echo Server exited with an error. Press any key to close this window.
    pause >nul
)
