# Implementation Plan for P-010: Set complete status before git commit command

## Problem Statement

The current implementation in `.rdd/src/actions/prompt_complete.py` executes git commit before updating the prompt state to "completed" in the registry. This creates uncommitted changes after the commit because the registry state change happens after the commit. The requirement is to reverse this order.

## Questionnaire Decisions

Based on the answered questionnaire:
- Q1: Keep the current generic commit message format from git_commit.py (Option B)
- Q2: Rollback the state change and report error if state update fails (Option A)
- Q3: Trust that the write operation succeeded without verification (Option B)
- Q4: Always persist the state change regardless of git-enabled setting (Option A)
- Q5: Always follow the git-enabled flag setting (Option B + C clarification)

## Implementation Steps

### Step 1: Reorder operations in prompt_complete.py

Modify the logic in `.rdd/src/actions/prompt_complete.py` to execute operations in the following order:

1. Load and validate the registry
2. Determine the target prompt (either explicit or active)
3. Check if already completed (early exit if so)
4. Update the prompt state to "completed" in memory
5. Write the updated registry to disk (this persists the state change)
6. If git-enabled is true, execute git commit script
7. Report results to stdout

The key change is moving the state update and registry write BEFORE the git commit operation, rather than after.

### Step 2: Error handling for state write failures

Since we are following Q2 decision (Option A - rollback on failure), the implementation should:
- If the registry write fails (Python will raise an exception), the exception will propagate and prevent git commit
- The error will be caught by the try/except at the script level and reported to the user
- No explicit rollback is needed since we haven't written to disk yet if the write fails

This is already the natural behavior of Python's error handling, so no additional code is required.

### Step 3: Maintain consistent behavior for git-disabled case

When git-enabled is false:
- The script will still update the state to "completed"
- The script will still write the registry to disk
- The script will skip the git commit operation entirely
- This behavior is already consistent and doesn't require changes beyond reordering

### Step 4: Validate the implementation

After making the code changes:
- Review the reordered code to ensure correct flow
- Verify error handling still works as expected
- Ensure output messages are still accurate

### Step 5: Update requirements.md

No new requirements need to be added. The existing requirements already cover this functionality:

- [TR-20251231-0103] specifies that prompt_complete.py sets state and conditionally executes git commit
- [UR-20251231-0101] specifies the prompt completion command transitions to completed state and optionally triggers git commit

These requirements don't specify the order, so they are already fulfilled by the corrected implementation. No modifications to requirements.md are needed.

## Files to be Modified

1. `.rdd/src/actions/prompt_complete.py` - Reorder the state update and git commit operations

## Files NOT Modified

1. `.rdd-instance/specifications/requirements.md` - No changes needed, existing requirements already cover this
2. `.rdd/src/actions/git_commit.py` - No changes needed to the git commit script itself
3. Any Web UI files - The UI calls the script and will benefit from the fix automatically

## Expected Outcome

After implementation:
- When prompt_complete.py is executed with git-enabled=true, the sequence will be:
  1. Load registry
  2. Find target prompt
  3. Update state to "completed"
  4. Write registry to disk
  5. Execute git commit (now the commit includes the registry change)
  6. Report completion
- After the git commit completes, there will be no uncommitted changes
- The git commit will include the state change to "completed" in the registry file
