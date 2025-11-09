#!/bin/bash
################################################################################
# RDD Framework Installer Launcher (Linux/macOS)
# Version: {{VERSION}}
#
# This script launches the Python installer for the RDD Framework.
# It checks for Python availability and runs install.py.
################################################################################

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo ""
echo "======================================================================"
echo "  RDD Framework Installer Launcher"
echo "======================================================================"
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check for Python
if command_exists python; then
    PYTHON_CMD="python"
elif command_exists python3; then
    PYTHON_CMD="python3"
else
    echo -e "${RED}✗${NC} Python is not installed or not in PATH"
    echo ""
    echo "Please install Python 3.7+ from: https://www.python.org/downloads/"
    echo ""
    echo "On Linux, you may also need to install python-is-python3:"
    echo "  sudo apt-get install python-is-python3"
    echo ""
    exit 1
fi

# Check Python version
echo -e "${BLUE}ℹ${NC} Checking Python version..."
PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | cut -d' ' -f2)
echo -e "${GREEN}✓${NC} Found Python $PYTHON_VERSION"
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Check if install.py exists
if [ ! -f "$SCRIPT_DIR/install.py" ]; then
    echo -e "${RED}✗${NC} install.py not found in $SCRIPT_DIR"
    echo ""
    echo "Please ensure install.py is in the same directory as this script."
    exit 1
fi

# Run the Python installer
echo -e "${BLUE}ℹ${NC} Launching Python installer..."
echo ""
$PYTHON_CMD "$SCRIPT_DIR/install.py" "$@"

exit_code=$?

if [ $exit_code -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✓${NC} Installation completed successfully!"
else
    echo ""
    echo -e "${RED}✗${NC} Installation failed with exit code $exit_code"
fi

exit $exit_code
