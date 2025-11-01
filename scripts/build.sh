#!/bin/bash

# Build script for requirements-driven-development project
# This script creates a build directory with the necessary project structure
# and copies essential files and folders according to the RDD methodology

set -e  # Exit on error

# Get the script's directory and the project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Navigate to project root
cd "$PROJECT_ROOT"

echo "Starting build process..."

# Step 1: Create or clean the build folder
echo "Step 1: Preparing build/ folder..."
if [ -d "build" ]; then
    echo "  - Removing existing build/ folder content..."
    rm -rf build/*
else
    echo "  - Creating build/ folder..."
    mkdir -p build
fi

# Step 2: Create build/.rdd/ folder
echo "Step 2: Creating build/.rdd/ folder..."
mkdir -p build/.rdd

# Step 3: Create build/.github/ folder
echo "Step 3: Creating build/.github/ folder..."
mkdir -p build/.github

# Step 4: Copy .github/prompts/ to build/.github/
echo "Step 4: Copying .github/prompts/ to build/.github/..."
if [ -d ".github/prompts" ]; then
    cp -r .github/prompts build/.github/
    echo "  - Copied .github/prompts/"
else
    echo "  - Warning: .github/prompts/ does not exist"
fi

# Step 5: Copy .github/copilot-instructions.md to build/.github/templates/
echo "Step 5: Copying .github/copilot-instructions.md to build/.github/templates/..."
if [ -f ".github/copilot-instructions.md" ]; then
    mkdir -p build/.github/templates
    cp .github/copilot-instructions.md build/.github/templates/
    echo "  - Copied .github/copilot-instructions.md"
else
    echo "  - Warning: .github/copilot-instructions.md does not exist"
fi

# Step 6: Copy .rdd/templates/ to build/.rdd/
echo "Step 6: Copying .rdd/templates/ to build/.rdd/..."
if [ -d ".rdd/templates" ]; then
    cp -r .rdd/templates build/.rdd/
    echo "  - Copied .rdd/templates/"
else
    echo "  - Warning: .rdd/templates/ does not exist"
fi

# Step 7: Copy .rdd/scripts/ to build/.rdd/
echo "Step 7: Copying .rdd/scripts/ to build/.rdd/..."
if [ -d ".rdd/scripts" ]; then
    cp -r .rdd/scripts build/.rdd/
    echo "  - Copied .rdd/scripts/"
else
    echo "  - Warning: .rdd/scripts/ does not exist"
fi

echo ""
echo "Build process completed successfully!"
echo "Output directory: $PROJECT_ROOT/build/"
