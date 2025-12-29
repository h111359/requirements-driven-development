@echo off
REM RDD Framework Launcher for Windows

REM Get the directory where this script is located
set SCRIPT_DIR=%~dp0

REM Remove trailing backslash
set SCRIPT_DIR=%SCRIPT_DIR:~0,-1%

REM Execute rdd.py using python command
python "%SCRIPT_DIR%\rdd.py" %*
