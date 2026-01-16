# Implementation Plan for Issue 84 - Workdir Archive Improvement

## Context

The current issue (GitHub issue #84) is that when archiving a work iteration, empty folders remain in `.rdd-instance/workdir/`. The current implementation in `.rdd/src/actions/workdir_archive.py` uses a "best-effort" cleanup approach that catches exceptions but continues execution, which can result in incomplete cleanup when folder deletion fails.

The prompt requires:
1. Root cause analysis of the issue
2. Testing with mockup folders to reproduce the problem
3. Improvements to the existing script without changing overall structure
4. Implementation of a two-phase commit approach
5. Better error handling and verification

## Implementation Steps

### Step 1: Create Root Cause Analysis File

Create a new file `issue_84_analysis.md` in the prompt folder (`.rdd-instance/workdir/P-001_Analysis of the issue/`) that documents:
- The exact cause of the issue: The current cleanup logic in `workdir_archive.py` uses a try-except block that catches and logs errors but continues execution, meaning if `shutil.rmtree()` or `child.unlink()` fails for any reason (permissions, file locks, OS restrictions), the folder/file remains and execution continues
- Why empty folders might persist: Empty folders can fail to delete due to OS-level locks, permissions issues, or if they contain hidden files/system files that the iterator doesn't catch
- Analysis of the cleanup loop: The current approach iterates over `workdir.iterdir()` and tries to delete each child, but doesn't verify the cleanup was complete
- Best practices for reliable cleanup operations in Python
- The two-phase commit approach as a robust solution

### Step 2: Create Test Script for Issue Reproduction

Create a test script `test_archive_cleanup.py` in the prompt folder that:
- Creates a mockup workdir structure with various scenarios (normal folders, empty folders, folders with hidden files, nested structures)
- Uses similar code logic as the current `workdir_archive.py` cleanup section
- Attempts to reproduce the issue by creating problematic folder states
- **IMPORTANT**: This script operates only on temporary/mockup folders, NOT on the actual `.rdd-instance/workdir`
- Demonstrates which scenarios cause cleanup failures with the current approach
- Tests both the current approach and proposed improvements

### Step 3: Implement Improved Archive Script

Modify `.rdd/src/actions/workdir_archive.py` to implement the following improvements while preserving the overall structure:

**3.1 Add verification that archive copy is complete**
- After `shutil.copytree()`, verify the copy was successful by comparing file counts and directory structure
- Use a helper function `_verify_archive_complete()` that checks:
  - The destination directory exists
  - The number of files in destination matches source
  - The directory tree structure is identical
- If verification fails, raise an exception before proceeding to cleanup

**3.2 Implement two-phase commit approach**
- After successful archive copy and verification, rename `workdir` to `workdir.deleting`
- This creates an atomic point: if deletion fails, the renamed folder makes it obvious something went wrong
- Delete the renamed `workdir.deleting` folder completely
- Create a fresh empty `workdir` folder
- This approach ensures we never have a partially-deleted workdir

**3.3 Replace best-effort cleanup with strict cleanup**
- Remove the try-except block that allows cleanup to continue on errors
- Use `shutil.rmtree()` on the entire `workdir.deleting` folder without catching exceptions
- If deletion fails, the script should fail fast with a clear error message
- The renamed folder remains as evidence of the failed operation

**3.4 Add retry logic for transient failures**
- Implement a helper function `_delete_with_retry()` that:
  - Attempts deletion with a configurable number of retries (e.g., 3)
  - Waits a short delay between retries (e.g., 0.5 seconds)
  - This handles transient issues like temporary file locks
- Use this function for the main deletion operation

**3.5 Add detailed error messages**
- When deletion fails, provide specific information:
  - Which folder failed to delete (the path)
  - What error occurred (exception type and message)
  - Suggestions for remediation (check permissions, close file handles, etc.)
- Include the path to the successfully created archive in the error message

**3.6 Add final verification step**
- After creating the fresh workdir, verify it is empty
- List any remaining contents and fail if anything unexpected is found
- This ensures we don't silently leave files behind

### Step 4: Update Error Messages and Documentation

**4.1 Update script docstring**
- Document the two-phase commit approach
- Document the verification steps
- Document the retry logic
- Note that the script fails fast on errors rather than using best-effort cleanup

**4.2 Add inline comments**
- Comment each phase of the two-phase commit
- Comment the verification logic
- Explain why we rename before deleting

### Step 5: Test the Implementation

Run the test script created in Step 2 to:
- Verify the improved implementation handles all test scenarios correctly
- Confirm that failures are detected and reported properly
- Validate that successful operations leave no residual files/folders
- Test retry logic with simulated transient failures

### Step 6: Update Documentation (if needed)

Check if any user-facing documentation needs to be updated to reflect:
- The improved reliability of the archiving process
- The two-phase approach (users might see `workdir.deleting` if they run the script at exactly the wrong moment)
- Error recovery procedures (what to do if archiving fails)

### Step 7: Requirements Updates

No new requirements need to be added. The existing requirements already cover the expected behavior:
- UR-0009: Framework shall archive working directory content
- UR-0011: System shall clear workdir after archiving
- UR-0028: All destructive operations shall create backups before proceeding (satisfied by archive-then-delete approach)
- UR-0029: Scripts shall validate prerequisites before executing operations (satisfied by verification steps)
- UR-0030: Scripts shall handle errors gracefully and provide recovery guidance (improved by this implementation)

However, we should consider adding a technical requirement to document the two-phase commit approach if it proves successful. This would be done during implementation mode.

## Key Design Decisions

**Why two-phase commit?**
The two-phase commit (archive → rename → delete → create fresh) provides several benefits:
1. Clear atomic boundary: after archive verification, we know the backup is safe
2. Failure visibility: a `workdir.deleting` folder makes it obvious something went wrong
3. No partial state: we never have a half-empty workdir that looks complete
4. Recovery path: if deletion fails, user can manually investigate the renamed folder

**Why strict cleanup instead of best-effort?**
Best-effort cleanup silently hides problems. If cleanup fails, we should know about it immediately and fix the root cause rather than accumulating technical debt.

**Why verification steps?**
Verification ensures we never delete the source until we're certain the backup is complete. This protects against subtle bugs like filesystem errors during copy, permission issues, or disk space problems.

**Why retry logic?**
Transient failures (temporary file locks, antivirus scanning, etc.) are common on Windows and sometimes on Linux. Retry with delay handles these gracefully without failing unnecessarily.

## Success Criteria

The implementation is successful when:
1. The root cause analysis clearly explains the issue
2. The test script demonstrates the problem with the current code and validates the fix
3. The improved script successfully handles all test scenarios
4. No empty folders remain after successful archiving
5. Failures are detected and reported with clear error messages
6. The archive is verified complete before cleanup begins
7. The two-phase commit ensures safe, atomic operation
8. Retry logic handles transient failures gracefully

## Risk Mitigation

**Risk**: The improved script might be too strict and fail in edge cases that the old script tolerated
**Mitigation**: Comprehensive test coverage and retry logic for transient issues

**Risk**: The rename operation might fail on some filesystems
**Mitigation**: Include this in error handling; if rename fails, the original workdir remains intact and archive is already created

**Risk**: The verification step might have false positives/negatives
**Mitigation**: Use simple, reliable checks (directory existence, file count) that are unlikely to fail incorrectly

**Risk**: Testing with mockup folders might not catch all real-world issues
**Mitigation**: Document the improvement thoroughly in the analysis file and include the reasoning for each change
