#!/bin/bash

# Build script for requirements-driven-development project
# This script creates two platform-specific release archives:
# - rdd-linux-<version>.zip for Linux with .sh scripts
# - rdd-windows-<version>.zip for Windows with .ps1 scripts

set -e  # Exit on error

# Get the script's directory and the project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Navigate to project root
cd "$PROJECT_ROOT"

# Extract version from rdd.sh
VERSION=$(grep '^RDD_VERSION=' .rdd/scripts/rdd.sh | cut -d'"' -f2)
if [ -z "$VERSION" ]; then
    echo "Error: Could not extract version from .rdd/scripts/rdd.sh"
    exit 1
fi

echo "========================================"
echo "RDD Build Process - Version $VERSION"
echo "========================================"
echo ""

# Step 1: Create or clean the build folder
echo "Step 1: Preparing build/ folder..."
if [ -d "build" ]; then
    echo "  - Removing existing build/ folder content..."
    rm -rf build/*
else
    echo "  - Creating build/ folder..."
    mkdir -p build
fi

# Create temporary directories for Linux and Windows builds
LINUX_BUILD="build/rdd-linux"
WINDOWS_BUILD="build/rdd-windows"
mkdir -p "$LINUX_BUILD"
mkdir -p "$WINDOWS_BUILD"

# Step 2: Create directory structures for both builds
echo "Step 2: Creating directory structures..."
for BUILD_DIR in "$LINUX_BUILD" "$WINDOWS_BUILD"; do
    mkdir -p "$BUILD_DIR/.rdd"
    mkdir -p "$BUILD_DIR/.github"
done

# Step 3: Copy .github/prompts/ to both builds
echo "Step 3: Copying .github/prompts/..."
if [ -d ".github/prompts" ]; then
    cp -r .github/prompts "$LINUX_BUILD/.github/"
    cp -r .github/prompts "$WINDOWS_BUILD/.github/"
    echo "  - Copied .github/prompts/"
else
    echo "  - Warning: .github/prompts/ does not exist"
fi

# Step 4: Copy .github/copilot-instructions.md
echo "Step 4: Copying .github/copilot-instructions.md..."
if [ -f ".github/copilot-instructions.md" ]; then
    mkdir -p "$LINUX_BUILD/.github/templates"
    mkdir -p "$WINDOWS_BUILD/.github/templates"
    cp .github/copilot-instructions.md "$LINUX_BUILD/.github/templates/"
    cp .github/copilot-instructions.md "$WINDOWS_BUILD/.github/templates/"
    echo "  - Copied .github/copilot-instructions.md"
else
    echo "  - Warning: .github/copilot-instructions.md does not exist"
fi

# Step 5: Copy .rdd/templates/
echo "Step 5: Copying .rdd/templates/..."
if [ -d ".rdd/templates" ]; then
    cp -r .rdd/templates "$LINUX_BUILD/.rdd/"
    cp -r .rdd/templates "$WINDOWS_BUILD/.rdd/"
    echo "  - Copied .rdd/templates/"
else
    echo "  - Warning: .rdd/templates/ does not exist"
fi

# Step 6: Copy .rdd/scripts/ for Linux and convert for Windows
echo "Step 6: Processing .rdd/scripts/..."
if [ -d ".rdd/scripts" ]; then
    # Copy shell scripts to Linux build
    cp -r .rdd/scripts "$LINUX_BUILD/.rdd/"
    echo "  - Copied .rdd/scripts/ to Linux build"
    
    # Create scripts directory for Windows
    mkdir -p "$WINDOWS_BUILD/.rdd/scripts"
    
    # Copy non-script files (README, etc.)
    find .rdd/scripts -type f ! -name "*.sh" -exec cp {} "$WINDOWS_BUILD/.rdd/scripts/" \;
    
    # Check if python3 is available
    if ! command -v python3 &> /dev/null; then
        echo "  - Error: python3 is required for script conversion but not found in PATH"
        exit 1
    fi
    
    # Check if converter script exists
    if [ ! -f "$SCRIPT_DIR/bash-to-powershell.py" ]; then
        echo "  - Error: bash-to-powershell.py not found at $SCRIPT_DIR/bash-to-powershell.py"
        exit 1
    fi
    
    # Convert shell scripts to PowerShell for Windows build
    echo "  - Converting shell scripts to PowerShell..."
    SCRIPT_COUNT=0
    for sh_file in .rdd/scripts/*.sh; do
        if [ -f "$sh_file" ]; then
            filename=$(basename "$sh_file" .sh)
            ps_file="$WINDOWS_BUILD/.rdd/scripts/${filename}.ps1"
            python3 "$SCRIPT_DIR/bash-to-powershell.py" "$sh_file" "$ps_file"
            SCRIPT_COUNT=$((SCRIPT_COUNT + 1))
        fi
    done
    echo "  - Converted $SCRIPT_COUNT shell scripts to PowerShell"
else
    echo "  - Warning: .rdd/scripts/ does not exist"
fi

# Step 7: Remove .sh files from Windows build (ensure only .ps1 files)
echo "Step 7: Cleaning Windows build..."
find "$WINDOWS_BUILD" -type f -name "*.sh" -delete
echo "  - Removed all .sh files from Windows build"

# Step 8: Create zip archives
echo "Step 8: Creating release archives..."

# Linux zip
LINUX_ZIP="build/rdd-linux-v${VERSION}.zip"
cd build
zip -r -q "rdd-linux-v${VERSION}.zip" rdd-linux/
cd "$PROJECT_ROOT"
echo "  - Created $LINUX_ZIP"

# Windows zip
WINDOWS_ZIP="build/rdd-windows-v${VERSION}.zip"
cd build
zip -r -q "rdd-windows-v${VERSION}.zip" rdd-windows/
cd "$PROJECT_ROOT"
echo "  - Created $WINDOWS_ZIP"

# Step 9: Clean up temporary directories
echo "Step 9: Cleaning up temporary directories..."
rm -rf "$LINUX_BUILD"
rm -rf "$WINDOWS_BUILD"
echo "  - Removed temporary build directories"

# Final summary
echo ""
echo "========================================"
echo "Build completed successfully!"
echo "========================================"
echo "Version: $VERSION"
echo ""
echo "Build artifacts:"
echo "  - $LINUX_ZIP"
echo "  - $WINDOWS_ZIP"
echo ""
echo "Archive contents:"
echo "  - Both archives have identical folder structure"
echo "  - Linux archive contains .sh scripts"
echo "  - Windows archive contains .ps1 scripts"
echo "========================================"

