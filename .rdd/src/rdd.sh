#!/bin/bash
# RDD Framework Launcher for Linux/macOS

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Repository root is two levels up from .rdd/src/
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Execute rdd.py using python command
python "$SCRIPT_DIR/rdd.py" "$@"
