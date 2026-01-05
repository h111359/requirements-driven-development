# Implementation Plan for P-013: Web UI Launcher Files

## Overview
This plan details the creation of easy-to-use launcher files for the RDD Web UI on both Windows (`.bat`) and Linux (`.sh`) platforms, enabling users to start the Web UI with minimal effort, ideally by double-clicking the launcher file.

## Context from Questionnaire
The following decisions have been made based on the questionnaire responses:
- **Launch method**: Platform-specific launchers with Python core logic (Option B)
- **Browser behavior**: Automatically open browser after server starts (Yes)
- **Port configuration**: Auto-detect available port (Option B)
- **Error handling**: Display errors in terminal/console window that stays open (Option A)
- **File location**: `.rdd/` directory (Option B)
- **Shutdown method**: Both Ctrl+C in terminal and shutdown button in Web UI (Option C)
- **File naming**: `rdd.bat` and `rdd.sh` (Custom naming)

## Implementation Steps

### Step 1: Create run.bat for Windows
Create the file `.rdd/run.bat` with the following functionality:
- Execute the Python web server script `.rdd/src/web/server.py`
- Use the `python` command for cross-platform consistency (per TR-20251224-0902)
- Keep the console window open on errors to allow users to read error messages
- Pass appropriate parameters to enable automatic browser opening
- Include error checking to ensure Python is available
- Add clear console messages indicating server startup status

**Technical details:**
- Use `python .rdd/src/web/server.py` as the main command
- Add `pause` command on error conditions to keep window open
- Include `@echo off` for cleaner output
- Display helpful messages during startup

### Step 2: Create run.sh for Linux
Create the file `.rdd/run.sh` with the following functionality:
- Execute the Python web server script `.rdd/src/web/server.py`
- Use the `python` command for cross-platform consistency (per TR-20251224-0902)
- Make the script executable with proper shebang (`#!/bin/bash`)
- Keep the terminal open on errors to allow users to read error messages
- Pass appropriate parameters to enable automatic browser opening
- Include error checking to ensure Python is available
- Add clear console messages indicating server startup status

**Technical details:**
- Use shebang `#!/bin/bash` at the beginning
- Use `python .rdd/src/web/server.py` as the main command
- Include error handling with `set -e` and informative error messages
- Add instructions to make file executable: `chmod +x .rdd/run.sh`
- Display helpful messages during startup

### Step 3: Verify server.py supports required features
Review and potentially update `.rdd/src/web/server.py` to ensure:
- It supports automatic port detection or fallback mechanism (addressing Question 3 - auto-detect available port)
- It automatically opens the default browser when started (addressing Question 2 - auto-open browser)
- It handles errors gracefully with informative messages
- It provides clear console output about the server status (URL, port, etc.)

If the server.py file needs modifications:
- Add command-line argument for controlling auto-browser-open behavior (default: enabled)
- Implement port auto-detection logic if not already present
- Ensure clear error messages are displayed for common issues (Python version, missing dependencies, port conflicts)

### Step 4: Add shutdown button in Web UI (if not present)
Based on Question 6 (shutdown method - both options), verify and implement:
- Check if the Web UI already has a shutdown button
- If not present, add a shutdown endpoint to the server API (POST /api/shutdown)
- Add a shutdown button to the Web UI interface
- Implement graceful server shutdown when the button is clicked
- Update the Web UI HTML template and JavaScript to include the shutdown functionality

**Technical details:**
- Add shutdown endpoint in `.rdd/src/web/server.py`
- Update `.rdd/src/web/templates/index.html` to include shutdown button in navigation
- Update `.rdd/src/web/static/app.js` to handle shutdown action
- Ensure shutdown is graceful (closes server properly, displays confirmation message)

### Step 5: Update documentation
Update relevant documentation files to explain how to use the launcher files:
- Update `README.md` in the project root to include instructions for launching the Web UI using the launcher files
- Add platform-specific instructions:
  - **Windows**: "Double-click `run.bat` in the `.rdd/` folder"
  - **Linux**: "Run `./run.sh` from the `.rdd/` folder (ensure it's executable: `chmod +x .rdd/run.sh`)"
- Document the auto-browser-open behavior
- Explain how to stop the server (Ctrl+C or shutdown button)

### Step 6: Test the launchers
Verify the implementation works correctly:
- Test `run.bat` on Windows (if available in testing environment)
- Test `run.sh` on Linux
- Verify browser automatically opens
- Verify error messages display correctly when issues occur
- Verify shutdown button works properly
- Verify Ctrl+C shutdown works properly

### Step 7: Update requirements.md
Add new requirements to `.rdd-instance/specifications/requirements.md` to reflect the new launcher functionality:

**New User Requirements to add:**
- `[UR-YYYYMMDD-HHmm]` The framework shall provide easy-to-use launcher scripts for starting the Web UI on both Windows and Linux platforms without requiring manual terminal commands.
- `[UR-YYYYMMDD-HHmm]` The Web UI launchers shall automatically open the default web browser when the server starts successfully.
- `[UR-YYYYMMDD-HHmm]` The Web UI shall provide a shutdown button to allow users to stop the server without using terminal commands.

**New Technical Requirements to add:**
- `[TR-YYYYMMDD-HHmm]` The framework shall provide launcher scripts `run.bat` for Windows and `run.sh` for Linux located in the `.rdd/` directory.
- `[TR-YYYYMMDD-HHmm]` The launcher scripts shall execute `.rdd/src/web/server.py` using the `python` command with automatic browser opening enabled.
- `[TR-YYYYMMDD-HHmm]` The launcher scripts shall display clear error messages and keep the console/terminal window open when errors occur to allow users to read the error information.
- `[TR-YYYYMMDD-HHmm]` The Web UI server shall support automatic detection of available ports and use a fallback mechanism if the default port is occupied.
- `[TR-YYYYMMDD-HHmm]` The Web UI shall implement a POST /api/shutdown endpoint that gracefully stops the web server when invoked.
- `[TR-YYYYMMDD-HHmm]` The Linux launcher script `run.sh` shall include proper shebang (`#!/bin/bash`) and require executable permissions to be set before use.

**Note**: The actual requirement IDs (YYYYMMDD-HHmm) will be generated with current timestamp during implementation step.

### Step 8: Verify compliance with existing requirements
Ensure the implementation complies with existing requirements from `.rdd-instance/specifications/requirements.md`:
- UR-20251224-0906: Framework operates on both Windows and Linux ✓ (launchers for both platforms)
- TR-20251224-0902: Use `python` command for all scripts ✓ (launchers will use `python` command)
- TR-20251230-1430: Web server on localhost port 8080 with --port parameter ✓ (will be verified in Step 3)
- TR-20251230-1430: Automatically open default browser on startup ✓ (will be implemented/verified in Step 3)
- UR-20251224-0927: Error messages with specific problem description and remediation ✓ (launchers will include error handling)

All existing requirements are observed by this plan.

## Summary
This implementation will create easy-to-use launcher files that allow users to start the RDD Web UI with a simple double-click (Windows) or single command (Linux), automatically opening their browser to the Web UI. The implementation addresses all points from the user's request and questionnaire answers, while maintaining compliance with existing framework requirements.
