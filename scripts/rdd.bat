@echo off
REM RDD Framework Launcher for Windows
REM Launches the RDD interactive menu

REM Check if .rdd/scripts/rdd.py exists
if not exist ".rdd\scripts\rdd.py" (
    echo Error: RDD framework not found in this directory
    echo Please run this script from the root of your RDD-enabled project
    pause
    exit /b 1
)

REM Check for Python
where python >nul 2>&1
if %ERRORLEVEL% neq 0 (
    where python3 >nul 2>&1
    if %ERRORLEVEL% neq 0 (
        echo Error: Python is not installed or not in PATH
        echo Please install Python from https://www.python.org/downloads/
        pause
        exit /b 1
    )
    REM Use python3 if python is not found
    python3 .rdd\scripts\rdd.py %*
) else (
    REM Use python command
    python .rdd\scripts\rdd.py %*
)

REM Keep window open if launched by double-click
if "%1"=="" pause
