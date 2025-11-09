@echo off
REM ========================================================================
REM RDD Framework Installer Launcher (Windows)
REM Version: {{VERSION}}
REM
REM This script launches the Python installer for the RDD Framework.
REM It checks for Python availability and runs install.py.
REM ========================================================================

setlocal enabledelayedexpansion

echo.
echo ======================================================================
echo   RDD Framework Installer Launcher
echo ======================================================================
echo.

REM Check for Python
where python >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    set PYTHON_CMD=python
    goto :python_found
)

where python3 >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    set PYTHON_CMD=python3
    goto :python_found
)

echo [91m✗[0m Python is not installed or not in PATH
echo.
echo Please install Python 3.7+ from: https://www.python.org/downloads/
echo.
echo Make sure to check "Add Python to PATH" during installation.
echo.
pause
exit /b 1

:python_found
REM Check Python version
echo [94mℹ[0m Checking Python version...
for /f "tokens=2" %%v in ('%PYTHON_CMD% --version 2^>^&1') do set PYTHON_VERSION=%%v
echo [92m✓[0m Found Python !PYTHON_VERSION!
echo.

REM Get the directory where this script is located
set SCRIPT_DIR=%~dp0

REM Check if install.py exists
if not exist "%SCRIPT_DIR%install.py" (
    echo [91m✗[0m install.py not found in %SCRIPT_DIR%
    echo.
    echo Please ensure install.py is in the same directory as this script.
    echo.
    pause
    exit /b 1
)

REM Run the Python installer
echo [94mℹ[0m Launching Python installer...
echo.
%PYTHON_CMD% "%SCRIPT_DIR%install.py" %*

set EXIT_CODE=%ERRORLEVEL%

if %EXIT_CODE% EQU 0 (
    echo.
    echo [92m✓[0m Installation completed successfully!
) else (
    echo.
    echo [91m✗[0m Installation failed with exit code %EXIT_CODE%
)

echo.
pause
exit /b %EXIT_CODE%
