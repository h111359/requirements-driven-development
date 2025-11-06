# P02 Implementation: Build Implementation Plan

## Task Summary
Create a refined implementation plan based on P01 analysis, focusing exclusively on Option C (Zip Archive with Installer), replace bash build script with Python implementation, and create detailed verbose prompts for the next implementation steps.

## Execution Started
Date: 2025-11-05
Status: In Progress

## Step 1: Analysis of P01 Implementation

Reading `.rdd-docs/workspace/P01-implementation.md`...

### Key Findings from P01

1. **Recommended Approach**: Option C - Zip Archive with Installer
   - Self-contained distribution
   - No external dependencies (except Python)
   - Works offline
   - Easy to audit before installation
   - VS Code integration preserved

2. **Current Build System Issues**:
   - `scripts/build.sh` creates separate Linux/Windows archives (no longer needed with Python)
   - Converts bash scripts to PowerShell (obsolete with Python migration)
   - Extracts version from legacy `rdd.sh` (should use `rdd.py`)
   - References bash scripts that have been archived

3. **Framework is Python-Based**:
   - Python 3.7+ requirement
   - Cross-platform single codebase
   - Uses `python` command (not `python3`)
   - All bash scripts migrated to Python

## Step 2: Refined Build Implementation Plan

### Overview
Replace `scripts/build.sh` with `scripts/build.py` that creates a single cross-platform zip archive containing:
- Installation script (`install.py`)
- README.md with installation instructions
- All prompts from `.github/prompts/`
- Complete `.rdd/` framework folder
- VS Code settings template for merging

### Build System Architecture

#### scripts/build.py
Python script that orchestrates the entire build process with the following capabilities:

**Version Management**:
- Extract version from `.rdd/scripts/rdd.py` by reading the `__version__` variable
- Validate version follows SemVer format (MAJOR.MINOR.PATCH)
- Use version for archive naming: `rdd-v{version}.zip`

**Build Directory Structure**:
```
build/
└── rdd-v{version}/
    ├── install.py              # Installation script
    ├── README.md               # Installation instructions
    ├── LICENSE                 # Project license
    ├── .github/
    │   └── prompts/            # All prompt files (*.prompt.md)
    ├── .rdd/
    │   ├── scripts/            # Python scripts (rdd.py, rdd_utils.py)
    │   └── templates/          # All template files
    └── .vscode/
        └── settings.json       # Settings to merge
```

**Build Process Steps**:
1. Clean/create build directory
2. Extract version from `rdd.py`
3. Create version-specific subdirectory
4. Copy files maintaining structure:
   - `.github/prompts/` → all `.prompt.md` files
   - `.rdd/scripts/` → `rdd.py` and `rdd_utils.py`
   - `.rdd/templates/` → all template files
   - `.rdd/templates/settings.json` → `.vscode/settings.json`
5. Generate `install.py` from template
6. Generate `README.md` with installation instructions
7. Copy LICENSE file
8. Create zip archive
9. Generate SHA256 checksum file
10. Clean up temporary directory

**Error Handling**:
- Validate Python version (>= 3.7)
- Check all required source files exist
- Verify directory structure
- Rollback on failure

#### scripts/install.py (Generated)
Python installation script included in the archive with these capabilities:

**Pre-flight Checks**:
- Verify Python version >= 3.7
- Check if Git is installed
- Validate target directory is a Git repository
- Detect existing RDD installation

**Interactive Installation**:
- Prompt for confirmation if existing installation detected
- Ask to proceed with file copying
- Confirm VS Code settings merge
- Confirm .gitignore update

**Installation Operations**:
1. **Copy Prompts**:
   - Create `.github/prompts/` if not exists
   - Copy all prompt files from archive
   - Report number of prompts installed

2. **Copy Framework Files**:
   - Create `.rdd/` if not exists
   - Copy `scripts/` directory
   - Copy `templates/` directory
   - Set executable permissions on `rdd.py` (Linux/macOS)

3. **Merge VS Code Settings**:
   - Read archive `.vscode/settings.json`
   - Read existing `.vscode/settings.json` (if exists)
   - Merge configurations:
     - `chat.promptFilesRecommendations`: append unique values
     - `chat.tools.terminal.autoApprove`: append unique values
     - `files.associations`: merge dictionary
     - `editor.rulers`: use archive values
   - Write merged settings to `.vscode/settings.json`
   - Create `.vscode/` directory if needed

4. **Update .gitignore**:
   - Read existing `.gitignore` or create new
   - Check if `.rdd-docs/workspace/` already present
   - Append `.rdd-docs/workspace/` if not present
   - Preserve existing content and formatting

**Verification**:
- Confirm all files copied successfully
- Test `python .rdd/scripts/rdd.py --version`
- Report installation location
- Display next steps

**Error Handling**:
- Graceful error messages with suggestions
- Rollback capability on failure
- Detailed logging of operations

#### README.md (Generated for Archive)
Installation guide included in the archive:

**Content Sections**:
1. **What is RDD**: Brief description of the framework
2. **System Requirements**:
   - Python 3.7 or higher
   - Git 2.23 or higher
   - VS Code (recommended)
   - GitHub Copilot (optional but recommended)
3. **Quick Installation**:
   - Extract zip archive
   - Run `python install.py` from archive directory
   - Follow interactive prompts
4. **Manual Installation** (if automated installation fails):
   - Step-by-step file copying instructions
   - Manual VS Code settings merge
   - Manual .gitignore update
5. **Verification**:
   - Test command: `python .rdd/scripts/rdd.py --version`
   - Expected output
6. **Getting Started**:
   - Link to main documentation
   - First steps with RDD workflow
7. **Troubleshooting**:
   - Python command not found (Linux: `python-is-python3`)
   - Permission issues
   - VS Code settings conflicts
   - Installation in wrong directory

## Step 3: Removing scripts/build.sh

The current `scripts/build.sh` will be removed as it:
- Creates platform-specific archives (Linux/Windows) - no longer needed
- Contains bash-to-PowerShell conversion logic - obsolete
- References legacy bash scripts - archived
- Does not align with current Python-based architecture

The new `scripts/build.py` will be a complete replacement with proper Python implementation.

## Step 4: Detailed Implementation Prompts

Below are the revised and expanded prompts for implementing the build system.

---

### Prompt P03: Implement build.py Script

**Objective**: Create a comprehensive Python build script that generates a single cross-platform release archive with all necessary components for RDD framework installation.

**Context**:
- You are implementing the build system for the RDD framework
- The framework is Python-based (Python 3.7+) and cross-platform
- Current bash-based build.sh needs to be replaced with Python implementation
- The build should create a single zip archive (not separate Linux/Windows versions)
- Read the following files for context:
  - `.rdd-docs/requirements.md`
  - `.rdd-docs/tech-spec.md`
  - `.rdd-docs/folder-structure.md`
  - `.rdd-docs/workspace/P01-implementation.md`
  - `.rdd-docs/workspace/P02-implementation.md`

**Detailed Requirements**:

1. **Script Location and Structure**:
   - Create file: `scripts/build.py`
   - Make script executable: `chmod +x scripts/build.py`
   - Add shebang line: `#!/usr/bin/env python3`
   - Use Python 3.7+ compatible syntax (no f-strings requiring 3.8+)
   - Structure: Functions for each major operation with clear docstrings

2. **Version Extraction**:
   - Read `.rdd/scripts/rdd.py` file
   - Extract version from line matching: `__version__ = "X.Y.Z"`
   - Use regex pattern: `__version__\s*=\s*["']([^"']+)["']`
   - Validate version matches SemVer format: `^\d+\.\d+\.\d+$`
   - If version not found or invalid, exit with error message
   - Store version in variable for use throughout script

3. **Build Directory Management**:
   - Define build root: `build/` directory at project root
   - If `build/` exists: remove all contents recursively
   - If `build/` doesn't exist: create directory
   - Create version-specific directory: `build/rdd-v{version}/`
   - Create subdirectories:
     - `build/rdd-v{version}/.github/prompts/`
     - `build/rdd-v{version}/.rdd/scripts/`
     - `build/rdd-v{version}/.rdd/templates/`
     - `build/rdd-v{version}/.vscode/`

4. **File Copying Operations**:
   
   a. **Copy Prompts**:
   - Source: `.github/prompts/`
   - Destination: `build/rdd-v{version}/.github/prompts/`
   - Copy all files matching pattern: `*.prompt.md`
   - Preserve file permissions
   - Count and report number of prompt files copied
   - Error if no prompt files found

   b. **Copy RDD Scripts**:
   - Source files:
     - `.rdd/scripts/rdd.py`
     - `.rdd/scripts/rdd_utils.py`
   - Destination: `build/rdd-v{version}/.rdd/scripts/`
   - Preserve executable permissions
   - Verify both files exist before copying
   - Error if either file missing

   c. **Copy Templates**:
   - Source: `.rdd/templates/`
   - Destination: `build/rdd-v{version}/.rdd/templates/`
   - Copy all files recursively
   - Preserve directory structure
   - Count and report number of template files copied
   - Error if templates directory doesn't exist

   d. **Copy VS Code Settings**:
   - Source: `.rdd/templates/settings.json`
   - Destination: `build/rdd-v{version}/.vscode/settings.json`
   - This is the template that install.py will merge
   - Verify file exists
   - Error if settings.json template missing

   e. **Copy LICENSE**:
   - Source: `LICENSE` (project root)
   - Destination: `build/rdd-v{version}/LICENSE`
   - Verify file exists
   - Error if LICENSE missing

5. **Generate install.py**:
   - Generate Python installation script at: `build/rdd-v{version}/install.py`
   - Script should be self-contained (no external dependencies beyond Python stdlib)
   - Include detailed docstring explaining usage
   - Make script executable (Linux/macOS): `chmod +x`
   - See **Prompt P04** for detailed install.py implementation

6. **Generate README.md**:
   - Generate installation guide at: `build/rdd-v{version}/README.md`
   - Include version number in title
   - Content sections (see Step 2 above for detailed structure):
     - What is RDD
     - System Requirements (Python 3.7+, Git 2.23+, VS Code, Copilot)
     - Quick Installation (using install.py)
     - Manual Installation (step-by-step fallback)
     - Verification (test command and expected output)
     - Getting Started (first steps)
     - Troubleshooting (common issues and solutions)
   - Use clear formatting with proper Markdown headings and code blocks
   - Include examples of commands with expected output

7. **Create Zip Archive**:
   - Archive name: `build/rdd-v{version}.zip`
   - Archive contents: entire `build/rdd-v{version}/` directory
   - Use Python's `zipfile` module
   - Compression: ZIP_DEFLATED
   - Preserve file permissions in archive
   - Archive should expand to `rdd-v{version}/` directory (not flat)
   - Verify archive created successfully

8. **Generate Checksum**:
   - Generate SHA256 checksum of zip archive
   - Save to file: `build/rdd-v{version}.zip.sha256`
   - Format: `{checksum}  rdd-v{version}.zip\n`
   - Use format compatible with `sha256sum` command
   - Include verification instructions in output

9. **Cleanup**:
   - After zip archive created, remove temporary directory: `build/rdd-v{version}/`
   - Keep only zip archive and checksum file in build/
   - Confirm cleanup successful

10. **Logging and Output**:
    - Print clear section headers for each build step
    - Use visual separators (like "=" lines) for clarity
    - Report progress: "Step X/Y: Description..."
    - Show counts: "Copied N prompt files", "Copied M template files"
    - Display final summary:
      - Version built
      - Archive location
      - Archive size
      - Checksum file location
    - Use colors if terminal supports it (optional enhancement)

11. **Error Handling**:
    - Catch and report all exceptions with clear messages
    - Include context in error messages: "Failed to copy X to Y: reason"
    - Suggest remediation steps for common errors
    - Exit with non-zero code on any failure
    - Ensure cleanup happens even on error (use try/finally)

12. **Command-Line Interface**:
    - Accept optional flags:
      - `--help` or `-h`: Display usage information
      - `--version`: Display build script version
      - `--verbose` or `-v`: Show detailed output
      - `--clean-only`: Only clean build directory, don't build
    - Use argparse module for argument parsing
    - Provide clear help text for each option

**Testing Requirements**:
- Test on clean checkout (no existing build/ directory)
- Test with existing build/ directory (verify cleanup works)
- Test that generated archive extracts correctly
- Test that all files present in extracted archive
- Verify file permissions preserved (especially for .py scripts)
- Verify checksum file can be used with `sha256sum -c` command
- Test error handling: missing source files, permission issues

**Success Criteria**:
- Script runs without errors
- Single zip archive created: `build/rdd-v{version}.zip`
- Checksum file created: `build/rdd-v{version}.zip.sha256`
- Archive contains all required files in correct structure
- README.md is clear and complete
- install.py is functional (will be tested in P04)
- Temporary directory cleaned up
- Clear output messages guide user through process

**Deliverables**:
1. `scripts/build.py` - Complete build script
2. Successfully generated `build/rdd-v{version}.zip`
3. Successfully generated `build/rdd-v{version}.zip.sha256`
4. Test report confirming all success criteria met
5. Update documentation (if needed) with build instructions

**Notes**:
- Do not modify `scripts/build.sh` - it will be deleted after build.py is complete and tested
- Use Python pathlib for cross-platform path handling
- Include comprehensive docstrings for maintainability
- Follow PEP 8 style guidelines
- Add comments for complex logic sections

---

### Prompt P04: Implement install.py Script

**Objective**: Create a comprehensive Python installation script that automates the installation of the RDD framework into an existing Git repository with full error handling, validation, and user interaction.

**Context**:
- This script will be included in the release archive created by build.py
- Users will extract the archive and run this script to install RDD framework
- The script must be self-contained (no dependencies beyond Python standard library)
- Target environment: Any directory with Git repository initialized
- Must handle existing RDD installations gracefully
- Read the following files for context:
  - `.rdd-docs/requirements.md`
  - `.rdd-docs/tech-spec.md`
  - `.rdd-docs/workspace/P01-implementation.md`
  - `.rdd-docs/workspace/P02-implementation.md`

**Detailed Requirements**:

1. **Script Header and Metadata**:
   - File: `install.py` (generated by build.py)
   - Shebang: `#!/usr/bin/env python3`
   - Module docstring explaining purpose, usage, requirements
   - Version: Match RDD framework version
   - No external dependencies beyond Python 3.7+ standard library

2. **Required Imports**:
   ```python
   import os
   import sys
   import json
   import shutil
   import subprocess
   from pathlib import Path
   ```

3. **Pre-flight Validation Functions**:

   a. **Check Python Version**:
   - Function: `check_python_version()`
   - Validate running Python >= 3.7
   - If version too old: print error with current version, required version
   - Exit with code 1 if check fails
   - Return True if check passes

   b. **Check Git Installation**:
   - Function: `check_git_installed()`
   - Run command: `git --version`
   - Capture output
   - If git not found: print error message with installation instructions
   - Return True if git found, False otherwise

   c. **Check Git Repository**:
   - Function: `check_git_repository(target_dir)`
   - Check if `target_dir/.git` exists
   - If not: print error that target must be git repository
   - Suggest: `git init` to initialize repository
   - Return True if git repo found, False otherwise

   d. **Detect Existing Installation**:
   - Function: `detect_existing_installation(target_dir)`
   - Check for existence of:
     - `target_dir/.rdd/scripts/rdd.py`
     - `target_dir/.github/prompts/` with any `.prompt.md` files
   - Return dict: `{"exists": bool, "components": list}`
   - Components list contains names of found components

4. **User Interaction Functions**:

   a. **Confirm Installation**:
   - Function: `confirm_installation(existing_installation)`
   - If existing installation found: display warning message
   - List found components
   - Ask: "Do you want to proceed? This will overwrite existing files. [y/N]"
   - Read user input (stdin)
   - Return True if user confirms (y/yes case-insensitive), False otherwise

   b. **Get Target Directory**:
   - Function: `get_target_directory()`
   - Default: current working directory
   - Prompt: "Enter target directory for installation (default: current directory):"
   - Accept user input or use default if empty
   - Expand tilde and environment variables in path
   - Convert to absolute path
   - Validate directory exists
   - Return Path object

5. **Installation Operations**:

   a. **Copy Prompts**:
   - Function: `install_prompts(source_dir, target_dir)`
   - Source: `source_dir/.github/prompts/`
   - Target: `target_dir/.github/prompts/`
   - Operations:
     - Create target directory if not exists (including parent)
     - Copy all `.prompt.md` files
     - Count files copied
     - Print: "Installed N prompt files"
   - Error handling: catch and report IOError, OSError
   - Return: number of files copied

   b. **Copy RDD Framework**:
   - Function: `install_rdd_framework(source_dir, target_dir)`
   - Source: `source_dir/.rdd/`
   - Target: `target_dir/.rdd/`
   - Operations:
     - Create target directory if not exists
     - Copy `scripts/` directory recursively
     - Copy `templates/` directory recursively
     - Preserve directory structure
     - On Linux/macOS: set executable permission on `rdd.py`
       - Command: `chmod +x target_dir/.rdd/scripts/rdd.py`
     - Print: "Installed RDD framework"
   - Error handling: catch and report all filesystem errors
   - Return: True if successful

   c. **Merge VS Code Settings**:
   - Function: `merge_vscode_settings(source_dir, target_dir)`
   - Source settings: `source_dir/.vscode/settings.json`
   - Target settings: `target_dir/.vscode/settings.json`
   - Operations:
     - Read source settings (JSON)
     - Read target settings if exists, otherwise create empty dict
     - Merge rules:
       - **chat.promptFilesRecommendations** (array): 
         - Append source items to target
         - Remove duplicates
         - Preserve order
       - **chat.tools.terminal.autoApprove** (array):
         - Append source items to target
         - Remove duplicates
       - **files.associations** (object):
         - Merge keys
         - Source values overwrite target values
       - **editor.rulers** (array):
         - Use source values (replace target)
     - Create `.vscode/` directory if not exists
     - Write merged settings to target (JSON, indent=2)
     - Print: "Merged VS Code settings"
   - Error handling:
     - If source settings invalid JSON: print error, skip merge
     - If target settings invalid JSON: print warning, treat as empty
     - Catch and report filesystem errors
   - Return: True if successful, False if skipped

   d. **Update .gitignore**:
   - Function: `update_gitignore(target_dir)`
   - Target file: `target_dir/.gitignore`
   - Entry to add: `.rdd-docs/workspace/`
   - Operations:
     - Read existing .gitignore if exists
     - Check if `.rdd-docs/workspace/` already present
       - Look for exact line match
       - Look for pattern matches (e.g., `.rdd-docs/workspace`, `.rdd-docs/workspace/*`)
     - If not present:
       - Append blank line (if file not empty)
       - Append: `# RDD framework workspace (auto-generated)`
       - Append: `.rdd-docs/workspace/`
     - If already present:
       - Print: ".gitignore already contains workspace exclusion"
       - Skip update
     - Write updated .gitignore
     - Print: "Updated .gitignore"
   - Error handling: catch and report filesystem errors
   - Return: True if updated, False if already present

6. **Verification**:

   a. **Verify Installation**:
   - Function: `verify_installation(target_dir)`
   - Checks:
     - `.rdd/scripts/rdd.py` exists and is readable
     - At least one prompt file in `.github/prompts/`
     - `.vscode/settings.json` exists
     - `.gitignore` contains workspace exclusion
   - For each check: print status (✓ or ✗)
   - Return: True if all checks pass, False otherwise

   b. **Test RDD Command**:
   - Function: `test_rdd_command(target_dir)`
   - Change to target directory
   - Run command: `python .rdd/scripts/rdd.py --version`
   - Capture output
   - Check if output contains version string
   - Print command and output
   - Return: True if successful, False otherwise

7. **Main Installation Flow**:
   - Function: `main()`
   - Steps:
     1. Print welcome banner with RDD version
     2. Get script directory (where install.py is located)
     3. Run pre-flight checks:
        - Check Python version
        - Check Git installed
     4. Get target directory from user
     5. Validate target is Git repository
     6. Detect existing installation
     7. Get user confirmation (if existing installation found)
     8. Print "Starting installation..."
     9. Perform installation operations:
        - Install prompts
        - Install RDD framework
        - Merge VS Code settings
        - Update .gitignore
     10. Run verification checks
     11. Test RDD command
     12. Print success summary:
         - Installation location
         - Next steps (first command to run)
         - Documentation link
     13. Exit with code 0

8. **Error Handling Strategy**:
   - Wrap main() in try-except block
   - Catch all exceptions at top level
   - Print clear error messages with context
   - Include troubleshooting suggestions
   - Exit with non-zero code on any failure
   - For recoverable errors: ask user whether to continue

9. **User Output and UX**:
   - Use clear section headers for each step
   - Show progress: "Step 1/5: Copying prompts..."
   - Use visual indicators: ✓ for success, ✗ for failure, ℹ for info
   - Include blank lines for readability
   - Print summary of actions taken
   - Provide actionable next steps

10. **Logging**:
    - Create installation log file: `target_dir/.rdd-install.log`
    - Log all operations with timestamps
    - Include: actions taken, files copied, errors encountered
    - Print log location at end of installation
    - Log format: `[TIMESTAMP] LEVEL: message`

**Testing Requirements**:
- Test fresh installation in empty Git repository
- Test installation over existing RDD installation
- Test with non-Git directory (should fail gracefully)
- Test with Python 3.6 (should fail with clear message)
- Test without Git installed (should fail with clear message)
- Test VS Code settings merge with:
  - No existing settings.json
  - Existing settings.json with some overlapping keys
  - Existing settings.json with invalid JSON
- Test .gitignore update with:
  - No existing .gitignore
  - Existing .gitignore without workspace entry
  - Existing .gitignore with workspace entry
- Test verification checks with incomplete installation
- Test rollback/cleanup on error

**Success Criteria**:
- Script runs without errors in happy path
- All files copied to correct locations
- VS Code settings merged correctly
- .gitignore updated correctly
- Verification checks pass
- RDD command works after installation
- Clear user feedback throughout process
- Graceful error handling with helpful messages
- Installation log created

**Deliverables**:
1. `install.py` script (generated by build.py)
2. Test report covering all test cases
3. Documentation of edge cases handled
4. Sample installation log output

**Notes**:
- Keep code self-contained - no external dependencies
- Use pathlib for cross-platform path handling
- Include comprehensive docstrings
- Add inline comments for complex logic
- Follow PEP 8 style guidelines
- Make code readable and maintainable
- Consider: this script may be the user's first experience with RDD

---

### Prompt P05: Implement GitHub Actions Release Workflow

**Objective**: Create a GitHub Actions workflow that automates the creation and publishing of RDD framework releases, triggered by version tags, using the build.py script to generate release artifacts.

**Context**:
- The workflow will automate the entire release process
- Trigger: pushing version tags (e.g., `v1.0.0`)
- Output: GitHub Release with attached zip archive and checksum
- Uses `scripts/build.py` created in P03
- Read the following files for context:
  - `.rdd-docs/requirements.md`
  - `.rdd-docs/tech-spec.md`
  - `.rdd-docs/workspace/P01-implementation.md`
  - `.rdd-docs/workspace/P02-implementation.md`

**Detailed Requirements**:

1. **Workflow File**:
   - Location: `.github/workflows/release.yml`
   - Name: `"Create Release"`
   - Description: Automated release workflow for RDD framework

2. **Trigger Configuration**:
   - Trigger on:
     - Push of tags matching pattern: `v*.*.*` (e.g., v1.0.0, v1.2.3)
     - Manual workflow dispatch with version input
   - Configuration:
   ```yaml
   on:
     push:
       tags:
         - 'v*.*.*'
     workflow_dispatch:
       inputs:
         version:
           description: 'Release version (e.g., 1.0.0)'
           required: true
           type: string
   ```

3. **Job: build-and-release**:
   - Runs on: `ubuntu-latest`
   - Permissions needed:
     - `contents: write` (for creating release)
   
4. **Workflow Steps**:

   **Step 1: Checkout Code**:
   - Action: `actions/checkout@v4`
   - Options:
     - `fetch-depth: 0` (fetch all history for changelog)
     - `fetch-tags: true` (fetch all tags)

   **Step 2: Set up Python**:
   - Action: `actions/setup-python@v5`
   - Python version: `3.10`
   - Purpose: Run build.py script

   **Step 3: Extract Version**:
   - For tag trigger: Extract version from tag name
     - Command: `echo ${GITHUB_REF#refs/tags/v}`
     - Store in environment variable: `VERSION`
   - For manual trigger: Use input version
   - Validate version format (SemVer)
   - Exit if invalid

   **Step 4: Validate Version Match**:
   - Extract version from `.rdd/scripts/rdd.py`
   - Compare with tag/input version
   - If mismatch: fail workflow with clear error message
   - Purpose: Ensure version tag matches code version

   **Step 5: Run Build Script**:
   - Command: `python scripts/build.py`
   - Build creates: `build/rdd-v{version}.zip` and checksum
   - Verify build artifacts exist
   - Exit if build fails

   **Step 6: Generate Release Notes**:
   - If `CHANGELOG.md` exists:
     - Extract section for current version
     - Use as release body
   - If `CHANGELOG.md` doesn't exist:
     - Generate simple release notes with:
       - Version number
       - Release date
       - Link to compare view
       - Installation instructions
   - Save to file: `release-notes.md`

   **Step 7: Create GitHub Release**:
   - Action: `softprops/action-gh-release@v1` or similar
   - Configuration:
     - Tag name: From trigger (tag) or manual input
     - Release name: `RDD Framework v{version}`
     - Body: Contents of `release-notes.md`
     - Draft: false
     - Prerelease: Detect from version (if contains alpha/beta/rc)
     - Files to attach:
       - `build/rdd-v{version}.zip`
       - `build/rdd-v{version}.zip.sha256`
   
   **Step 8: Upload Build Artifacts** (for workflow debugging):
   - Action: `actions/upload-artifact@v4`
   - Artifacts:
     - Name: `rdd-release-v{version}`
     - Path: `build/rdd-v*.zip*`
     - Retention: 90 days

5. **Error Handling**:
   - Each step should have clear failure messages
   - Workflow fails fast on any error
   - Provide actionable error messages in workflow logs
   - Consider: If release creation fails, should we cleanup?

6. **Environment Variables**:
   - Define at job level:
     - `PYTHONUNBUFFERED: 1` (for real-time output)
   - Use workflow-level secrets if needed (currently none)

7. **Notifications** (Optional Enhancement):
   - Consider adding step to post release announcement
   - Options: Slack, Discord, GitHub Discussions
   - Only on successful release

8. **Security Considerations**:
   - Use pinned versions of actions (with SHA)
   - Validate all inputs
   - Don't expose sensitive information in logs
   - Use GITHUB_TOKEN for authentication (automatic)

**Testing Requirements**:
- Test workflow with test tag on feature branch
- Test manual trigger with version input
- Test with mismatched versions (should fail)
- Test with invalid version format (should fail)
- Verify release created with correct artifacts
- Verify checksum file attached
- Verify release notes generated correctly
- Test with and without CHANGELOG.md

**Success Criteria**:
- Workflow triggers on version tags
- Build script runs successfully
- Release created automatically
- Zip archive attached to release
- Checksum file attached to release
- Release notes generated (from CHANGELOG or auto-generated)
- Clear workflow logs for debugging
- Workflow fails gracefully with helpful errors

**Deliverables**:
1. `.github/workflows/release.yml` - Complete workflow file
2. Test release created from workflow
3. Documentation of workflow usage for maintainers
4. Troubleshooting guide for workflow issues

**Notes**:
- Consider rate limits when using GitHub API
- Workflow should be idempotent where possible
- Document how to trigger workflow manually
- Include link to workflow in main README.md
- Consider adding changelog automation in future

---

### Prompt P06: Create Release Documentation and Update README

**Objective**: Create comprehensive documentation for the release process, update main README.md with installation instructions, and create CHANGELOG.md template for tracking releases.

**Context**:
- Build system and release workflow now complete
- Users need clear instructions for installing and using RDD
- Maintainers need documentation for creating releases
- Project needs CHANGELOG for version history
- Read context files: P01-implementation.md, P02-implementation.md

**Detailed Requirements**:

1. **Create CHANGELOG.md**:
   - Location: Project root
   - Format: Keep a Changelog format (https://keepachangelog.com/)
   - Sections:
     - `[Unreleased]` - for upcoming changes
     - `[1.0.0] - YYYY-MM-DD` - first release
   - Change categories:
     - `Added` - new features
     - `Changed` - changes in existing functionality
     - `Deprecated` - soon-to-be removed features
     - `Removed` - removed features
     - `Fixed` - bug fixes
     - `Security` - security fixes
   - Include compare links at bottom
   - Populate first release (1.0.0) with:
     - Python-based implementation
     - Cross-platform support
     - All current prompts
     - Build and release automation
     - Migration from bash to Python

2. **Create RELEASE-PROCESS.md**:
   - Location: `.rdd-docs/` or project root
   - Audience: Repository maintainers
   - Content:
     - **Overview**: High-level release process
     - **Prerequisites**:
       - Maintainer access to repository
       - All changes merged to main
       - Tests passing
       - Documentation updated
     - **Release Steps**:
       1. Update CHANGELOG.md with release notes
       2. Update version in `rdd.py`
       3. Commit version bump: `git commit -m "chore: bump version to X.Y.Z"`
       4. Create tag: `git tag vX.Y.Z`
       5. Push tag: `git push origin vX.Y.Z`
       6. GitHub Actions workflow runs automatically
       7. Verify release created on GitHub
       8. Test installation from release
       9. Announce release (if applicable)
     - **Manual Release** (fallback):
       - Steps to create release manually if workflow fails
       - Run build.py locally
       - Create GitHub release manually
       - Attach artifacts
     - **Versioning Guidelines**:
       - When to increment MAJOR, MINOR, PATCH
       - Pre-release versions (alpha, beta, rc)
       - Version naming conventions
     - **Troubleshooting**:
       - Workflow fails: check logs
       - Version mismatch: update rdd.py
       - Build fails: run build.py locally
       - Release exists: delete tag and release, retry
     - **Post-Release Tasks**:
       - Update documentation site (if exists)
       - Announce in discussions/social media
       - Monitor for installation issues

3. **Update README.md**:
   - Add or update sections:
   
   a. **Installation Section** (near top, after overview):
   ```markdown
   ## Installation
   
   ### Prerequisites
   - Python 3.7 or higher
   - Git 2.23 or higher
   - VS Code (recommended for best experience)
   - GitHub Copilot (optional but recommended)
   
   ### Quick Installation
   
   1. Download the latest release from [Releases](link-to-releases)
   2. Extract the zip archive
   3. Navigate to the extracted directory
   4. Run the installation script:
      ```bash
      python install.py
      ```
   5. Follow the interactive prompts
   
   ### Verify Installation
   
   After installation, verify RDD is working:
   ```bash
   python .rdd/scripts/rdd.py --version
   ```
   
   Expected output: `RDD Framework v1.0.0` (or current version)
   
   ### Manual Installation
   
   If the automatic installation fails, you can install manually:
   
   1. Copy `.github/prompts/` to your repository
   2. Copy `.rdd/` to your repository
   3. Merge `.vscode/settings.json` with your settings
   4. Add `.rdd-docs/workspace/` to `.gitignore`
   
   See the [Installation Guide](link) for detailed instructions.
   ```
   
   b. **System Requirements Section**:
   - List all dependencies
   - Note about `python` command vs `python3`
   - Linux users: mention `python-is-python3` package
   - Link to Python installation guide
   
   c. **Getting Started Section**:
   - First command to run after installation
   - Link to workflow documentation
   - Link to prompt documentation
   
   d. **Links Section**:
   - Link to releases page
   - Link to documentation
   - Link to changelog
   - Link to issues/discussions

4. **Create INSTALLATION.md** (Detailed Guide):
   - Location: `.rdd-docs/` or project root
   - Audience: End users installing RDD
   - Content:
     - **Overview**: What RDD is and why install it
     - **Prerequisites**: Detailed requirements with installation links
     - **Installation Methods**:
       - Automated (using install.py) - step by step
       - Manual - complete detailed steps
     - **Platform-Specific Instructions**:
       - Linux: python-is-python3 setup
       - macOS: Python installation if needed
       - Windows: Python installation notes
     - **Post-Installation Configuration**:
       - VS Code setup
       - Git configuration
       - First-time initialization
     - **Verification**: Testing installation
     - **Troubleshooting**:
       - Python not found
       - Permission errors
       - Git not found
       - VS Code settings issues
       - Installation in wrong directory
     - **Uninstallation**: How to remove RDD
     - **Updating**: How to update to new version
     - **Getting Help**: Where to ask questions

5. **Update Project Documentation References**:
   - Update `.rdd-docs/tech-spec.md`:
     - Add build system section
     - Add release process section
     - Update deployment architecture
   - Update `.rdd-docs/folder-structure.md`:
     - Add `scripts/build.py`
     - Add `build/` directory description
     - Update `.github/workflows/` section
   - Create or update `.rdd-docs/development-guide.md`:
     - How to contribute
     - How to test changes
     - How to create releases

**Testing Requirements**:
- Review all documentation for clarity
- Test all command examples
- Verify all links work
- Have someone unfamiliar with project review installation docs
- Test installation following new documentation

**Success Criteria**:
- CHANGELOG.md follows standard format
- RELEASE-PROCESS.md is clear and complete
- README.md has clear installation section
- INSTALLATION.md covers all scenarios
- All technical docs updated
- All commands in docs are tested and work
- Documentation readable by beginners

**Deliverables**:
1. `CHANGELOG.md` with first release
2. `RELEASE-PROCESS.md` for maintainers
3. Updated `README.md` with installation section
4. `INSTALLATION.md` detailed guide
5. Updated technical documentation
6. Documentation review report

**Notes**:
- Keep documentation clear and concise
- Use examples liberally
- Include screenshots if helpful
- Update documentation with each release
- Consider creating video tutorial (future enhancement)

---

### Prompt P07: Testing, Cleanup, and Final Validation

**Objective**: Comprehensive testing of the complete build and release system, cleanup of legacy files, and final validation that everything works end-to-end before marking the implementation complete.

**Context**:
- All components implemented: build.py, install.py, GitHub Actions workflow, documentation
- Need to test entire system end-to-end
- Need to remove legacy build.sh and related files
- Need to validate with real-world usage scenarios
- Read context: All previous implementation files

**Detailed Requirements**:

1. **End-to-End Testing**:

   a. **Local Build Testing**:
   - Test build.py on clean checkout:
     - Clone repository fresh
     - Run `python scripts/build.py`
     - Verify zip archive created
     - Verify checksum file created
     - Extract archive and inspect contents
     - Verify all files present and correct
   - Test build.py with existing build/ directory:
     - Run build twice
     - Verify cleanup works
     - Verify no leftover files
   - Test build.py error handling:
     - Temporarily rename rdd.py (simulate missing file)
     - Verify error message is clear
     - Restore file
   - Test on multiple Python versions:
     - Python 3.7 (minimum supported)
     - Python 3.10 (current)
     - Python 3.11 (latest)

   b. **Installation Testing**:
   - Test install.py in various scenarios:
     - **Fresh installation**:
       - Create test Git repository
       - Extract release archive
       - Run install.py
       - Verify all files installed
       - Verify VS Code settings created
       - Verify .gitignore updated
       - Run RDD command to verify
     - **Existing installation**:
       - Install once
       - Run install.py again
       - Verify warning displayed
       - Confirm and verify overwrite works
     - **Non-Git directory**:
       - Create directory without Git
       - Run install.py
       - Verify clear error message
     - **Existing VS Code settings**:
       - Create .vscode/settings.json with custom settings
       - Run install.py
       - Verify settings merged correctly
       - Verify custom settings preserved
     - **Existing .gitignore**:
       - Create .gitignore with entries
       - Run install.py
       - Verify workspace entry added
       - Run again, verify not duplicated
   - Test install.py on different platforms:
     - Linux
     - macOS (if available)
     - Windows (if available)

   c. **GitHub Actions Workflow Testing**:
   - Create test tag on feature branch:
     - Tag: `v0.0.1-test`
     - Push tag
     - Monitor workflow execution
     - Verify build succeeds
     - Verify release created (draft/prerelease)
     - Download artifact and test
   - Test manual workflow dispatch:
     - Trigger workflow manually
     - Provide version input
     - Verify release created
   - Test error scenarios:
     - Tag with version mismatch
     - Invalid version format
     - Verify workflow fails gracefully

2. **Integration Testing**:
   - Complete workflow test:
     - Install RDD using install.py
     - Initialize new enhancement branch
     - Run through complete RDD workflow
     - Verify all prompts work
     - Verify all scripts work
     - Complete and wrap up
   - Test with real project:
     - Install in actual development project
     - Use for real feature development
     - Document any issues found

3. **Cleanup Legacy Files**:
   
   a. **Remove scripts/build.sh**:
   - Delete file: `scripts/build.sh`
   - Verify no references to build.sh in:
     - Documentation
     - Workflows
     - Other scripts
   - Update any documentation that mentioned build.sh
   
   b. **Remove bash-to-powershell.py** (if exists):
   - Delete file: `scripts/bash-to-powershell.py`
   - No longer needed with Python-only build
   
   c. **Remove src/ directory** (if all migrated):
   - Verify all functionality migrated to Python
   - Archive src/ directory (don't just delete):
     - Create archive: `archive/legacy-platform-specific-src.zip`
     - Document what's in archive
   - Delete src/ directory
   - Update .gitignore if needed
   
   d. **Update Documentation References**:
   - Search for references to removed files
   - Update or remove outdated sections
   - Verify all links work

4. **Performance Testing**:
   - Measure build time:
     - Time build.py execution
     - Should complete in < 30 seconds
   - Measure installation time:
     - Time install.py execution
     - Should complete in < 15 seconds
   - Measure archive size:
     - Check zip file size
     - Should be < 1 MB
   - Document results

5. **Security Audit**:
   - Review install.py for security issues:
     - No arbitrary code execution
     - No unsafe file operations
     - Input validation present
   - Review build.py for security issues:
     - No sensitive data in archives
     - File permissions correct
   - Review workflow for security:
     - No secrets exposed
     - Actions from trusted sources
     - Minimal permissions

6. **Documentation Review**:
   - Review all documentation created/updated:
     - README.md
     - INSTALLATION.md
     - CHANGELOG.md
     - RELEASE-PROCESS.md
     - P02-implementation.md (this file)
   - Check for:
     - Accuracy (commands work as documented)
     - Completeness (no missing steps)
     - Clarity (readable by beginners)
     - Consistency (terminology consistent)
   - Fix any issues found

7. **Create Test Report**:
   - Document all tests performed
   - For each test:
     - Test description
     - Expected result
     - Actual result
     - Pass/Fail status
     - Issues found (if any)
   - Summary of findings
   - Sign-off that testing complete

8. **Final Validation Checklist**:
   - [ ] build.py runs without errors
   - [ ] install.py runs without errors
   - [ ] GitHub Actions workflow succeeds
   - [ ] Archive contains all required files
   - [ ] Installation in fresh repo works
   - [ ] Installation over existing works
   - [ ] VS Code settings merge correctly
   - [ ] .gitignore updated correctly
   - [ ] RDD commands work after installation
   - [ ] Documentation is complete
   - [ ] Legacy files removed
   - [ ] No references to removed files
   - [ ] Tests pass on all target platforms
   - [ ] Performance metrics acceptable
   - [ ] Security audit complete
   - [ ] Test report created

**Testing Requirements**:
- Test on multiple OS: Linux (primary), Windows, macOS
- Test with different Python versions: 3.7, 3.10, 3.11
- Test both happy path and error scenarios
- Document all test cases and results
- Get peer review of testing approach

**Success Criteria**:
- All tests pass
- No critical issues found
- Performance metrics met
- Security audit clean
- Documentation complete and accurate
- Legacy files removed
- No broken references
- System ready for production use

**Deliverables**:
1. Complete test report with all results
2. Updated documentation (fixes from testing)
3. List of known issues/limitations (if any)
4. Removal of legacy files committed
5. Sign-off that implementation complete

**Notes**:
- Testing is critical - don't rush this step
- Document all issues found, even if minor
- Create GitHub issues for future enhancements
- Consider creating automated tests (future work)
- Get second person to review if possible

---

## Step 5: Summary of Changes from P01

### Simplified Approach
- **Single Archive**: No separate Linux/Windows builds - Python is cross-platform
- **Python Build**: Replace bash build.sh with Python build.py
- **Self-Contained Installer**: install.py has no external dependencies
- **Automated Release**: GitHub Actions handles entire release process

### Key Decisions
1. **Keep it Simple**: Single zip archive for all platforms
2. **Python All the Way**: No bash-to-PowerShell conversion needed
3. **User-Friendly**: Interactive installation with clear prompts
4. **Automatable**: Can be scripted for CI/CD

### Removed Complexity
- No platform-specific archives
- No script conversion logic
- No separate src/linux and src/windows directories
- No bash scripts in release

## Step 6: Next Actions

After this document is reviewed and approved:

1. **Execute P03**: Implement build.py
2. **Execute P04**: Implement install.py (via build.py generation)
3. **Execute P05**: Create GitHub Actions workflow
4. **Execute P06**: Update all documentation
5. **Execute P07**: Comprehensive testing and cleanup

Each prompt is detailed enough to be executed independently by an AI agent or developer.

## Completion Status

- [x] Read P01-implementation.md
- [x] Create refined implementation plan (Option C only)
- [x] Remove references to build.sh usage
- [x] Design Python-based build.py
- [x] Design comprehensive install.py
- [x] Create detailed verbose prompts (P03-P07)
- [ ] Mark P02 as completed
- [ ] Log execution

## Notes

This implementation plan provides:
- Clear separation of concerns (each script has single responsibility)
- Comprehensive error handling throughout
- User-friendly interactive installation
- Complete automation via GitHub Actions
- Thorough testing strategy
- Detailed prompts that can be executed step-by-step

The verbose style of the prompts ensures that anyone (human or AI) implementing them has complete clarity on requirements and expectations.
