#!/bin/bash
# Technical Design Schema Editor - Launcher Script for Linux/Mac
# This script starts the editor web server and opens the browser

cd "$(dirname "$0")"

echo "Starting Technical Design Schema Editor..."
echo ""

# Check if Python 3 is available
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
elif command -v python &> /dev/null; then
    PYTHON_CMD=python
else
    echo "ERROR: Python 3 is not installed or not in PATH"
    echo "Please install Python 3 to use this editor"
    exit 1
fi

# Start the server
$PYTHON_CMD server.py
