#!/bin/bash
# RDD Web Interface Launcher for Linux
# This script starts the RDD Web UI server and automatically opens it in the default browser

echo
echo "========================================"
echo "RDD Web Interface Launcher"
echo "========================================"
echo

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Check if Python is available
if ! command -v python &> /dev/null; then
    echo "ERROR: Python is not installed or not in PATH"
    echo
    echo "Remediation: Please install Python 3.11 or higher"
    echo "  Ubuntu/Debian: sudo apt-get install python3"
    echo "  Fedora/RHEL: sudo dnf install python3"
    echo "  Arch: sudo pacman -S python"
    echo
    read -p "Press Enter to close this window..."
    exit 1
fi

echo "Starting RDD Web UI server..."
echo

# Start the server - it will automatically open the browser
python "$SCRIPT_DIR/src/web/server.py"

# Capture the exit code
EXIT_CODE=$?

# If the server exits with an error, pause so the user can read the error message
if [ $EXIT_CODE -ne 0 ]; then
    echo
    echo "Server exited with an error. Press Enter to close this window."
    read
fi

exit $EXIT_CODE
