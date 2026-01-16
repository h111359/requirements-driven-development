# Implementation Plan for ZIP Timestamp Error Fix

## Problem Analysis

The error "ZIP does not support timestamps before 1980" occurs when creating a zip archive from the workdir. This is a known limitation of the ZIP file format, which uses MS-DOS timestamp format that cannot represent dates before 1980-01-01.

The error happens in the `_create_zip_archive()` function in `workdir_archive.py` when calling `zipf.write(file_path, arcname)`. If any file in the workdir has a modification time earlier than 1980, the zip creation will fail.

## Implementation Steps

### Step 1: Add Timestamp Normalization Function

Create a helper function `_normalize_file_timestamp(file_path: Path) -> None` in `workdir_archive.py` that:
- Checks if a file's modification time is before 1980-01-01 00:00:00
- If so, sets the file's modification time to 1980-01-01 00:00:00
- Uses `os.utime()` to update the timestamp
- Logs a warning when normalizing timestamps

This function will be defensive and handle edge cases gracefully.

### Step 2: Modify _create_zip_archive Function

Update the `_create_zip_archive()` function to normalize timestamps before adding files to the zip:
- Before the `zipf.write(file_path, arcname)` call, invoke `_normalize_file_timestamp(file_path)` 
- Add a counter to track how many files had their timestamps normalized
- Print a summary at the end if any timestamps were normalized

This ensures all files have valid timestamps before being added to the zip archive.

### Step 3: Test the Fix

Create a test scenario to verify the fix works:
- Create a temporary test directory structure
- Create test files with timestamps before 1980 using `os.utime()`
- Call the archive function
- Verify that:
  - The zip file is created successfully
  - No error about timestamps occurs
  - Files with old timestamps are included in the archive
  - The timestamps in the zip are >= 1980-01-01

Important: Do not corrupt the actual workdir. Use a separate test setup or mock the archive process.

### Step 4: Code Review and Edge Cases

Review the implementation for edge cases:
- Files that cannot have their timestamps modified (permission issues)
- Symbolic links
- Directories (only files need timestamp normalization for zip)
- Empty files
- Very large files

Add appropriate error handling and logging.

### Step 5: Update Requirements (if needed)

No new requirements need to be added. The existing requirements already cover:
- [UR-0009] Archive functionality
- [TR-0020] Zip archive format
- [UR-0027] Error messages with remediation steps
- [UR-0028] All destructive operations shall create backups (already implemented via two-phase commit)

The fix is a bug fix that ensures the existing archive functionality works correctly under all conditions, including when files have very old timestamps.

## Technical Design Updates

No technical design file exists (it's empty), so no updates are needed.

## Files and Folders Updates

No updates needed to the files-and-folders.md specification. The change is internal to an existing file.

## Summary

This is a straightforward bug fix that adds timestamp normalization to prevent ZIP format errors. The solution is defensive, well-logged, and maintains backward compatibility. The existing two-phase commit pattern in the archive function ensures safety is maintained.
