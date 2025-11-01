
#!/bin/bash
# Script: merge-fixes-to-main.sh
# Purpose: Automate merging all fixes from the current branch to main, including uncommitted changes, using 'fix/20251101-1324-cleaning-workspace' as branch name. No parameters required.
# Usage: ./merge-fixes-to-main.sh

set -e

# Get current branch name
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)

if [ "$CURRENT_BRANCH" = "main" ]; then
  echo "You are already on main. No fixes to merge."
  exit 0
fi

# Stash uncommitted changes if any
if ! git diff --quiet || ! git diff --cached --quiet; then
  echo "Stashing uncommitted changes..."
  git stash push -u -m "merge-fixes-to-main.sh auto-stash"
  STASHED=1
else
  STASHED=0
fi

# Fetch and update main
git fetch origin main
git checkout main
git pull origin main

# Create new branch from main
git checkout -b fix/20251101-1324-cleaning-workspace

# Find all commits in current branch not in main
COMMITS=$(git log main..$CURRENT_BRANCH --pretty=format:"%H")

if [ -z "$COMMITS" ]; then
  echo "No new commits to cherry-pick from $CURRENT_BRANCH."
else
  for COMMIT in $COMMITS; do
    echo "Cherry-picking commit $COMMIT..."
    git cherry-pick $COMMIT
  done
fi

# Apply stashed changes if any
if [ "$STASHED" -eq 1 ]; then
  echo "Applying stashed changes..."
  git stash pop || true
fi

# Push new branch
git push -u origin fix/20251101-1324-cleaning-workspace

echo "\nAll fixes have been pushed to branch 'fix/20251101-1324-cleaning-workspace'."
echo "Open a pull request from 'fix/20251101-1324-cleaning-workspace' to 'main' to merge your fixes."
