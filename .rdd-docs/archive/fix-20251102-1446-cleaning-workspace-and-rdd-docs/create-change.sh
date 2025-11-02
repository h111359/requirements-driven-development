#!/bin/bash
# Script to create a new change in the workspace with flat structure

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

# Check if .rdd-docs folder exists, create if not
if [ ! -d ".rdd-docs" ]; then
    mkdir -p .rdd-docs
    echo "Created .rdd-docs folder"
fi

# Check if workspace folder exists, create if not
if [ ! -d ".rdd-docs/workspace" ]; then
    mkdir -p .rdd-docs/workspace
    echo "Created .rdd-docs/workspace folder"
fi

# Check for required files in .rdd-docs/ and copy templates if missing
REQUIRED_FILES=(requirements.md tech-spec.md data-model.md folder-structure.md version-control.md clarity-taxonomy.md)
for FILE in "${REQUIRED_FILES[@]}"; do
    if [ ! -f ".rdd-docs/$FILE" ]; then
        cp ".rdd/templates/$FILE" ".rdd-docs/$FILE"
        echo "Copied template for missing $FILE to .rdd-docs/$FILE"
    fi
done

# Compose change ID and branch name
CHANGE_ID="${DATE_TIME}-${CHANGE_NAME}"
BRANCH_NAME="${CHANGE_TYPE}/${CHANGE_ID}"

# Switch to main, pull latest, create new branch
git checkout main
git pull
git checkout -b "$BRANCH_NAME"

# Copy template files to workspace
cp .rdd/templates/change.md ".rdd-docs/workspace/change.md"
echo "Created change.md in workspace"

# Copy clarity-taxonomy.md to workspace
if [ -f ".rdd-docs/clarity-taxonomy.md" ]; then
    cp ".rdd-docs/clarity-taxonomy.md" ".rdd-docs/workspace/clarity-taxonomy.md"
    echo "Copied clarity-taxonomy.md to workspace"
fi

# Create .current-change config file
cat > ".rdd-docs/workspace/.current-change" << EOF
{
  "changeName": "${CHANGE_NAME}",
  "changeId": "${CHANGE_ID}",
  "branchName": "${BRANCH_NAME}",
  "changeType": "${CHANGE_TYPE}",
  "startedAt": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "phase": "init",
  "status": "in-progress"
}
EOF
echo "Created .current-change config file"

# Initialize clarification-log.jsonl
cat > ".rdd-docs/workspace/clarification-log.jsonl" << EOF
{"timestamp":"$(date -u +%Y-%m-%dT%H:%M:%SZ)","question":"Change created","answer":"New change '${CHANGE_NAME}' (${CHANGE_TYPE}) initialized in workspace","answeredBy":"system","sessionId":"init-${CHANGE_ID}"}
EOF
echo "Initialized clarification-log.jsonl"

# Initialize open-questions.md
cat > ".rdd-docs/workspace/open-questions.md" << 'EOFQ'
# Open Questions - Requirements Clarification

> This file tracks open questions and clarifications needed for the current change.
> Questions are inspired by the clarity-taxonomy.md but can include any critical questions for execution.

## Status Legend
- [ ] Open / Not answered
- [?] Partially answered / Needs more detail
- [x] Answered / Resolved

---

## Questions

<!-- Add questions below. Use the taxonomy as inspiration but feel free to add custom questions -->

EOFQ
echo "Created open-questions.md template"

# Initialize requirements-changes.md
cat > ".rdd-docs/workspace/requirements-changes.md" << 'EOFREQ'
# Requirements Changes

> This file documents changes to be made to the main requirements.md file.
> Each statement is prefixed with [ADDED|MODIFIED|DELETED] to indicate the type of change.
>
> **For detailed formatting guidelines, see:** `.rdd/templates/requirements-format.md`

## Format Guidelines

- **[ADDED]**: New requirement not present in current requirements.md
- **[MODIFIED]**: Change to an existing requirement (include the old requirement ID/text for reference)
- **[DELETED]**: Requirement to be removed from requirements.md

---

## General Functionalities

<!-- Add general functionality changes here -->

---

## Functional Requirements

<!-- Add functional requirement changes here -->

---

## Non-Functional Requirements

<!-- Add non-functional requirement changes here -->

---

## Technical Requirements

<!-- Add technical requirement changes here -->

EOFREQ
echo "Created requirements-changes.md template"

echo ""
echo "✓ Change workspace initialized successfully!"
echo "  - Branch: ${BRANCH_NAME}"
echo "  - Change ID: ${CHANGE_ID}"
echo "  - Workspace: .rdd-docs/workspace/"
echo ""
echo "Next steps:"
echo "  1. Edit .rdd-docs/workspace/change.md with your change details"
echo "  2. Run clarification prompt: Use .github/prompts/rdd.02-clarify-requirements.prompt.md"