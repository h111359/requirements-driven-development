# Implementation Plan for Files and Folders (P-026)

## Overview

This plan implements functionality for tracking repository files in a CSV format with support for manual descriptions. Based on questionnaire answers, the implementation will use CSV format (tab-separated), store the file at `.rdd-instance/specifications/files-list.csv`, and include fields: File Name, Relative Path, Modification Time, and Description.

## Implementation Steps

### Step 1: Create the files_list_csv_refresh.py script

Create a new Python script at `.rdd/src/actions/files_list_csv_refresh.py` that:

- Scans the repository root directory recursively to discover all files and folders
- Excludes directories and files that start with "." (hidden files/folders)
- Excludes directories named "venv" 
- Reads the existing `.rdd-instance/specifications/files-list.csv` file if it exists (create parent directories and file if not)
- Uses CSV format with tab character as delimiter
- Includes the following columns in order: "File Name", "Relative Path", "Modification Time", "Description"
- For new files (not present in existing CSV):
  - Add a new row with File Name (basename of the file)
  - Add Relative Path (path relative to repository root)
  - Add Modification Time (timestamp of file's last modification in ISO8601 format)
  - Leave Description field empty
- For existing files with newer modification time:
  - Update the Modification Time field to the new timestamp
  - Clear the Description field (set to empty string)
- For files that no longer exist in the repository:
  - Remove the corresponding row from the CSV
- For files that exist and have not been modified:
  - Keep all fields unchanged (preserve Description if present)
- Write the updated data back to `.rdd-instance/specifications/files-list.csv`
- Use Python's csv module for proper CSV handling
- Handle edge cases: empty repository, special characters in file names, unicode characters

### Step 2: Create the files_list_csv_set_description.py script

Create a new Python script at `.rdd/src/actions/files_list_csv_set_description.py` that:

- Accepts command-line parameters: `file-name=<name>`, `relative-path=<path>`, and `description=<text>`
- Reads the existing `.rdd-instance/specifications/files-list.csv` file
- Locates the row where both "File Name" equals the provided file-name AND "Relative Path" equals the provided relative-path
- Updates the "Description" field for that row with the provided description text
- Writes the updated CSV back to `.rdd-instance/specifications/files-list.csv`
- Provides clear error messages if:
  - The CSV file doesn't exist
  - No matching file is found
  - Required parameters are missing
- Returns success status when the description is updated successfully

### Step 3: Update requirements.md

Add the following new technical requirements to `.rdd-instance/specifications/requirements.md` in the "Technical Requirements" section:

```
- [TR-20260102-1700] The framework shall provide a script `.rdd/src/actions/files_list_csv_refresh.py` that generates a CSV listing of all repository files and stores it at `.rdd-instance/specifications/files-list.csv`, excluding directories beginning with `.` and directories named `venv`, and listing for each entry: `File Name` (file name), `Relative Path` (relative path from repository root), `Modification Time` (file modification timestamp in ISO8601 format), and `Description` (manually-maintained description field).

- [TR-20260102-1701] The `files_list_csv_refresh.py` script shall update the CSV file incrementally by adding new files with empty descriptions, updating modification times and clearing descriptions for modified files, removing deleted files, and preserving descriptions for unchanged files.

- [TR-20260102-1702] The framework shall provide a script `.rdd/src/actions/files_list_csv_set_description.py` that accepts `file-name=`, `relative-path=`, and `description=` parameters and updates the Description field for the matching entry in `.rdd-instance/specifications/files-list.csv`.

- [TR-20260102-1703] The files listing CSV shall use tab character as field delimiter and shall be stored with UTF-8 encoding to support international characters in file names and descriptions.
```
Modify TR-20251224-0923 so it reflects exactly the prompt instructions (replace).

### Step 4: Skip

### Step 5: Test the implementation

Test the scripts by:
- Running `files_list_csv_refresh.py` on the repository to generate initial CSV
- Verifying CSV format (tab-delimited, correct columns)
- Modifying a file and re-running refresh script to verify modification time update and description clearing
- Adding a new file and re-running refresh script to verify new entry
- Deleting a file and re-running refresh script to verify removal
- Using `files_list_csv_set_description.py` to set a description for a file
- Verifying the description persists through refresh operations when the file is unchanged
- Verifying the description is cleared when the file is modified

## Notes

- This implementation creates a separate file tracking mechanism using CSV format in the specifications folder, which differs from the existing TR-20251224-0923 requirement for JSON format in workdir
- The CSV approach allows easier manual editing and review in spreadsheet applications
- The Description field provides a way for developers to document file purposes manually via the copilot
- Both mechanisms can coexist: JSON for workdir file listings, CSV for specifications documentation
