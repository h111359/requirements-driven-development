#!/bin/bash
# Script to update src/ folder with copies of .github/ and .rdd/ folders

# Remove existing content in src/ folder
if [ -d "src" ]; then
    echo "Removing existing content in src/ folder..."
    rm -rf src/* src/.*
else
    echo "Creating src/ folder..."
    mkdir src
fi

# Copy .github/ folder to src/
if [ -d ".github" ]; then
    echo "Copying .github/ folder to src/..."
    cp -r .github src/
    echo ".github/ folder copied to src/"
else
    echo "Warning: .github/ folder not found"
fi

# Copy .rdd/ folder to src/
if [ -d ".rdd" ]; then
    echo "Copying .rdd/ folder to src/..."
    cp -r .rdd src/
    echo ".rdd/ folder copied to src/"
else
    echo "Warning: .rdd/ folder not found"
fi

echo "Update completed successfully!"
