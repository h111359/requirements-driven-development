#!/bin/bash
# RDD Framework Launcher for Linux/macOS
# Launches the RDD interactive menu

# Check if .rdd/scripts/rdd.py exists
if [ ! -f ".rdd/scripts/rdd.py" ]; then
    echo "Error: RDD framework not found in this directory"
    echo "Please run this script from the root of your RDD-enabled project"
    exit 1
fi

# Check for Python
if command -v python &> /dev/null; then
    PYTHON_CMD="python"
elif command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
else
    echo "Error: Python is not installed or not in PATH"
    echo "Please install Python:"
    echo "  Ubuntu/Debian: sudo apt install python3 python-is-python3"
    echo "  macOS: brew install python3"
    echo "  Other: https://www.python.org/downloads/"
    exit 1
fi

# Launch RDD
$PYTHON_CMD .rdd/scripts/rdd.py "$@"
