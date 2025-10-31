#!/bin/bash
# Script to create a new change folder under docs/changes from template

# Check if change name parameter is provided
if [ -z "$1" ]; then
    echo "Error: Change name is required as parameter"
    echo "Usage: ./create-change.sh <change-name> [type]"
    echo "  type: feat (default) or fix"
    exit 1
fi

CHANGE_NAME="$1"
CHANGE_TYPE="${2:-feat}"  # Default to 'feat' if not provided

# Validate change type
if [[ "$CHANGE_TYPE" != "feat" && "$CHANGE_TYPE" != "fix" ]]; then
    echo "Error: Invalid change type '$CHANGE_TYPE'"
    echo "Valid types: feat, fix"
    exit 1
fi

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

# Check for required files in docs/ and copy templates if missing
REQUIRED_FILES=(requirements.md tech-spec.md data-model.md folder-structure.md version-control.md)
for FILE in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "docs/$FILE" ]; then
        cp ".rdd/scripts/templates/$FILE" "docs/$FILE"
        echo "Copied template for missing $FILE to docs/$FILE"
    fi
done

# Compose new folder name

# Compose new folder and branch name
NEW_FOLDER="docs/changes/${DATE_TIME}-${CHANGE_NAME}"
BRANCH_NAME="${CHANGE_TYPE}/${DATE_TIME}-${CHANGE_NAME}"
git checkout main
git pull
git checkout -b "$BRANCH_NAME"

# Create new change folder
mkdir "$NEW_FOLDER"

# Copy template file
cp .rdd/templates/change.md "$NEW_FOLDER/change.md"

echo "New change folder created: $NEW_FOLDER"
echo "Created and switched to branch: $BRANCH_NAME"