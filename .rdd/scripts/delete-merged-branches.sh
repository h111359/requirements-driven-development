#!/bin/bash
# Script to delete branches that have been merged into main, both locally and on origin

set -e  # Exit on error

# Fetch latest changes
git fetch --all

# Update local main to match remote
git checkout main
git pull origin main

echo "Finding branches merged into main..."

# Get list of remote branches merged into main, excluding main and HEAD
MERGED_BRANCHES=$(git branch -r --merged origin/main | grep -v 'origin/main' | grep -v 'origin/HEAD' | sed 's/^[[:space:]]*//')

if [ -z "$MERGED_BRANCHES" ]; then
    echo "No merged branches found."
    exit 0
fi

echo "Merged branches to delete:"
echo "$MERGED_BRANCHES"

# Ask for confirmation
read -p "Do you want to delete these branches? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Aborted."
    exit 0
fi

# Delete remote branches
echo "$MERGED_BRANCHES" | sed 's/origin\///' | xargs -r -n 1 git push origin --delete

# Delete local branches merged into main, excluding main and HEAD
LOCAL_MERGED_BRANCHES=$(git branch --merged main | grep -vE '^\*|^[[:space:]]*main$|^[[:space:]]*HEAD$' | sed 's/^[[:space:]]*//')

if [ -n "$LOCAL_MERGED_BRANCHES" ]; then
    echo "Deleting local merged branches..."
    echo "$LOCAL_MERGED_BRANCHES" | xargs -r git branch -d
else
    echo "No local merged branches to delete."
fi

echo "Done."
