# Implementation Plan: Windows Test Failures Fix

## Context

The Windows GitHub Actions tests fail during git checkout due to Windows path length limitations (260 characters). The repository contains archived test validation data with deeply nested .rdd-instance directories that create paths exceeding 278 characters.

Based on questionnaire answers:
- Q1: Use approach A - Compress workdir to zip file during archiving
- Q2: Use approach C - Create zip, verify, then delete directory (two-phase approach)
- Q3: Use approach B - Leave existing archives as-is, only new archives will be zipped
- Q4: Use approach B - Tests should clean up their test archives after completion

## Implementation Steps

### Step 1: Modify workdir_archive.py to Create Zip Archives

Modify `.rdd/src/actions/workdir_archive.py` to implement a two-phase archiving approach:
- Phase 1: Copy workdir to archive directory as currently done
- Phase 2: Create a zip file from the archived directory
- Phase 3: Verify zip integrity by testing file listing
- Phase 4: Delete the directory-based archive, keeping only the zip file

The archived zip file will be named `<iteration-id>_<iteration-name>.zip` in `.rdd-instance/archive/`.

This eliminates deeply nested directory structures in archives and significantly reduces path lengths, preventing Windows path length issues.

### Step 2: Update Test Files to Clean Up Test Archives

Modify test files that create archive structures to clean up after test completion:
- Review test files in `.rdd-instance/workdir/P-001_Windows test failures/` directory
- Identify tests that create nested `.rdd-instance` structures during validation
- Add teardown logic to remove test-created archives after test completion
- Ensure cleanup happens even when tests fail (use try/finally or pytest fixtures)

Files to examine and modify:
- `test_archive_cleanup.py` 
- `test_workdir_archive_improved.py`
- `validate_improved_implementation.py`

### Step 3: Deleted - continue with step 4

### Step 4: Clean Up Existing Problematic Archives - Make a zip archive of the directory: `.rdd-instance/archive/ITR-20260113-195937_Issue 84 archive workdir` in ``.rdd-instance/archive` and remove the directory after successful zip creation

### Step 5: Verify Windows Tests Pass

After implementing changes:
- Push changes to a test branch
- Verify that Windows tests pass in GitHub Actions
- Verify that 100% of tests succeed on both Windows and Linux platforms
- Verify that new archives are created as zip files
- Verify that the zip files can be extracted and contain all expected content

### Step 6: Update Documentation

Update relevant documentation to reflect the new archiving behavior:
- Update `.rdd/conventions/` files if there are conventions about archiving
- Update any README or help files that describe the archiving process
- Document that archives are now stored as zip files instead of directories
- Document that existing directory-based archives will remain as-is

## Requirements Updates

Do necessary requirements updates

## Technical Design Updates

No updates to technical design are needed as the technical design file is currently empty.

## Files and Folders Updates

The files-and-folders.md should be updated to document that archives are stored as zip files:
- Update the description of `.rdd-instance/archive/` to indicate that archives are stored as `<iteration-id>_<iteration-name>.zip` files
- This is a documentation update only, no structural changes to the repository

## Success Criteria

1. Windows tests pass 100% in GitHub Actions
2. New workdir archives are created as zip files
3. Zip files contain all workdir content and are properly structured
4. Test cleanup prevents accumulation of test artifacts
5. No test artifacts are committed to the repository
6. Linux tests continue to pass 100%
7. Existing directory-based archives remain untouched and functional
