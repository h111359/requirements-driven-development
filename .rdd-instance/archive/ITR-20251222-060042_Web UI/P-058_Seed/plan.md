# Implementation Plan for P-058: RDD Instance Initialization Script

## Overview

This plan describes the detailed steps for creating the `rdd-instance_seed.py` script that validates and initializes the RDD instance structure. The script will ensure all required files and folders exist with correct content, following the answers from the questionnaire and adhering to existing requirements.

## Step 1: Create the seed script structure

Create the file `.rdd/src/actions/rdd-instance_seed.py` with the basic structure including:
- Module docstring explaining the purpose
- Import statements for required libraries (pathlib, json, sys, logging)
- Command-line argument parsing using argparse to support `--verbose` flag
- Main function setup with logging configuration (INFO level by default, DEBUG level with --verbose flag)
- Exit code handling (0 on success, 1 on failure)

## Step 2: Implement manifest loading and validation

Implement a function `_load_manifest()` that:
- Constructs the path to `.rdd/config/manifest.json`
- Verifies the file exists (fail fast if missing with specific error message)
- Loads and parses the JSON content (fail fast if malformed)
- Validates that required keys exist: `requiredPaths.instance` and `requiredInstanceFiles`
- Returns the parsed manifest data structure

## Step 3: Implement folder validation and creation

Implement a function `_ensure_folders(manifest_data)` that:
- Extracts the list of required folders from `manifest_data["requiredPaths"]["instance"]`
- Iterates through each required folder path
- Checks if each folder exists using pathlib
- Creates missing folders recursively (using `Path.mkdir(parents=True, exist_ok=True)`) per questionnaire answer Q1-A
- Logs each folder creation with INFO level, including the full absolute path
- Returns a count of created folders

## Step 4: Implement file validation and initialization

Implement a function `_ensure_files(manifest_data)` that:
- Extracts the list of required files from `manifest_data["requiredInstanceFiles"]`
- Iterates through each required file entry (which contains `path` and `convention` fields)
- For each file:
  - Checks if the file already exists
  - If exists: logs at INFO level that file is skipped (per questionnaire answer Q2-A)
  - If does not exist: calls a helper function to create the file
- Returns tuple of (created_count, skipped_count)

## Step 5: Implement file creation logic

Implement a function `_create_instance_file(file_path, convention_path)` that:
- Verifies the convention file exists (fail fast if missing per questionnaire answer Q3-A with specific error about which convention file is missing and suggest checking framework installation)
- Reads the convention file to understand the expected format
- Generates appropriate initial content based on the file type:
  - For `.rdd-instance/specifications/requirements.md`: Generate a minimal valid requirements file with sections (Product Name, Product Overview, Definitions, User Requirements, Technical Requirements) but empty content
  - For `.rdd-instance/specifications/technical-design.json`: Create an empty JSON object `{}`
  - For `.rdd-instance/specifications/files-and-folders.md`: Generate a minimal valid structure documentation with at least the root folder
- Writes the generated content to the file path
- Calls validation function for the created file
- Logs the file creation with INFO level, including full absolute path

## Step 6: Implement file validation

Implement a function `_validate_file(file_path)` that (per questionnaire answer Q4-A):
- Determines file type based on extension
- For JSON files (.json):
  - Attempts to parse the JSON content
  - Fails fast if JSON syntax is invalid with specific error message
- For Markdown files (.md):
  - Verifies the file is valid UTF-8 encoded text
  - Fails fast if encoding is invalid
- Returns True if validation passes
- This validation ensures convention files are correct and created files are well-formed

## Step 7: Implement summary reporting

Implement a function `_print_summary(folders_created, files_created, files_skipped)` that:
- Formats and prints a summary message to stdout
- Format: "Seed complete: X folders created, Y files created, Z files skipped"
- Logs the same information at INFO level

## Step 8: Integrate all components in main function

Update the main function to:
- Set up logging based on --verbose flag
- Call `_load_manifest()` and handle any exceptions
- Call `_ensure_folders(manifest)` and capture created folder count
- Call `_ensure_files(manifest)` and capture created/skipped file counts
- Call `_print_summary()` with the counts
- Return exit code 0 on success
- On any exception:
  - Log the error at ERROR level
  - Print error message to stderr with remediation steps
  - Return exit code 1

## Step 9: Integrate seed script into web server

Modify `.rdd/src/web/server.py` to:
- Import subprocess module
- In the `main()` function, immediately after argument parsing and before starting the HTTP server:
  - Construct the path to `.rdd/src/actions/rdd-instance_seed.py`
  - Execute the seed script using `subprocess.run()` with appropriate parameters
  - Capture the exit code
  - If exit code is non-zero:
    - Log error message about seeding failure
    - Print error to console
    - Abort server startup (sys.exit(1))
  - If exit code is zero:
    - Log success message about seeding
    - Continue with server startup
- Ensure all seed script output is visible in the console

## Step 10: Create test file structure

Create the test file `tests/python/test_seed.py` with:
- Imports for pytest, pathlib, json, subprocess, tempfile
- Fixture for creating a temporary test repository structure
- Fixture for creating a minimal valid manifest.json

## Step 11: Implement test cases

Create the following test functions in `test_seed.py`:

1. `test_creates_missing_folders`: Verifies the script creates missing required folders
2. `test_creates_missing_files`: Verifies the script creates missing required files with valid content
3. `test_skips_existing_files`: Verifies the script does not overwrite existing files
4. `test_validates_json_files`: Verifies JSON files are validated after creation
5. `test_idempotent_behavior`: Verifies running the script twice produces the same result (same files, no overwrites)
6. `test_expected_log_output`: Verifies the script produces expected INFO level log messages
7. `test_fails_on_missing_manifest`: Verifies the script fails with exit code 1 when manifest.json is missing
8. `test_fails_on_malformed_manifest`: Verifies the script fails with exit code 1 when manifest.json is malformed
9. `test_fails_on_missing_convention_file`: Verifies the script fails with exit code 1 when a referenced convention file is missing
10. `test_verbose_flag`: Verifies the --verbose flag enables DEBUG level logging

## Step 12: Update requirements

Using the requirement management scripts, add new technical requirements:

```bash
python .rdd/src/actions/requirement_tr_create.py text="The framework shall provide a seed script at .rdd/src/actions/rdd-instance_seed.py that validates and initializes the RDD instance structure by creating missing folders and files based on manifest.json configuration"

python .rdd/src/actions/requirement_tr_create.py text="The seed script shall create folders recursively using mkdir -p semantics, ensuring all parent directories are created as needed"

python .rdd/src/actions/requirement_tr_create.py text="The seed script shall preserve existing files without modification, implementing idempotent behavior safe for repeated execution"

python .rdd/src/actions/requirement_tr_create.py text="The seed script shall validate JSON files after creation using JSON parsing and verify UTF-8 encoding for Markdown files"

python .rdd/src/actions/requirement_tr_create.py text="The seed script shall fail fast with specific error messages and exit code 1 when manifest.json is missing, malformed, or references non-existent convention files"

python .rdd/src/actions/requirement_tr_create.py text="The seed script shall support a --verbose flag for DEBUG level logging and provide summary output showing folder and file creation statistics"

python .rdd/src/actions/requirement_tr_create.py text="The web server startup sequence shall execute the seed script before starting the HTTP server and abort startup if seeding fails with non-zero exit code"

python .rdd/src/actions/requirement_tr_create.py text="The seed script shall complete initialization in under 100ms for typical cases where all required files and folders already exist"
```

Rationale for requirements additions: These technical requirements formalize the implementation details of the seed script functionality, ensuring it follows the questionnaire answers (recursive folder creation, preservation of existing files, validation, fail-fast error handling) and integrates properly with the web server. The requirements specify the exact behavior needed for a robust, production-ready initialization script.

## Step 13: Update files-and-folders.md

Update `.rdd-instance/specifications/files-and-folders.md` to include documentation for:
- The new `.rdd/src/actions/rdd-instance_seed.py` script file
- Description: "Validates and initializes RDD instance structure by creating missing folders and files based on manifest.json configuration. Idempotent and safe for repeated execution."
- Location in the appropriate ASCII diagram under `.rdd/src/actions/`
- The new `tests/python/test_seed.py` test file
- Description: "Test suite for rdd-instance_seed.py script, verifying folder creation, file initialization, validation, idempotency, and error handling"

## Step 14: Verify integration and testing

After implementation:
- Run the seed script independently: `python .rdd/src/actions/rdd-instance_seed.py`
- Verify it completes successfully with appropriate log output
- Run the seed script with --verbose flag to verify DEBUG logging
- Start the web server and verify seed script runs automatically
- Run the test suite: `python scripts/run-tests.py` or `pytest tests/python/test_seed.py`
- Verify all tests pass
- Manually verify the script is truly idempotent by running it multiple times

## Notes

- The script implements "convention over configuration" - it generates file content based on conventions, not templates
- No template files are needed; content is generated programmatically by the script
- Users can customize files after seeding; the script will preserve customizations
- The script is designed to be fast (<100ms) when all files exist, making it suitable for automatic execution on every web server startup
- Error messages include specific remediation steps (e.g., "Check framework installation", "Verify manifest.json syntax")
