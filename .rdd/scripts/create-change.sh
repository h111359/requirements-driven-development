#!/bin/bash
# Script to create a new change folder under docs/changes from template

# Check if change name parameter is provided
if [ -z "$1" ]; then
    echo "Error: Change name is required as parameter"
    echo "Usage: ./create-change.sh <change-name>"
    exit 1
fi

CHANGE_NAME="$1"

# Get current date and time in YYYYMMDD-HHmm format
DATE_TIME=$(date +"%Y%m%d-%H%M")

# Check if docs folder exists, create if not
if [ ! -d "docs" ]; then
    mkdir docs
    echo "Created docs folder"
fi

# Check if docs/changes folder exists, create if not
if [ ! -d "docs/changes" ]; then
    mkdir docs/changes
    echo "Created docs/changes folder"
fi

# Compose new folder name
NEW_FOLDER="docs/changes/${DATE_TIME}-${CHANGE_NAME}"

# Create git branch from main
BRANCH_NAME="cng/${CHANGE_NAME}"
git checkout main
git pull
git checkout -b "$BRANCH_NAME"

# Create new change folder
mkdir "$NEW_FOLDER"

# Copy template file
cp .rdd/templates/change.md "$NEW_FOLDER/change.md"

echo "New change folder created: $NEW_FOLDER"
echo "Created and switched to branch: $BRANCH_NAME"