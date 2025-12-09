## Deployment Architecture

### Build System
The RDD framework uses a Python-based build system to create release packages:

#### Build Script (build/build.py)
- **Purpose**: Creates cross-platform release archives with all necessary files
- **Version Management**: Extracts version from `.rdd/about.json` as single source of truth
- **Conflict Detection**: Checks for existing build artifacts (zip and sha256 files) before starting build
- **Conflict Resolution**: When artifacts exist, prompts user with three options:
  1. Stop build process (cancel)
  2. Increment patch version (with confirmation)
  3. Overwrite existing files (with confirmation)
- **Interactive Version Control**: Displays current version and prompts user to either increment patch version or rebuild with same version (only if no conflicts detected)
- **Version Persistence**: Automatically updates `.rdd/about.json` when user chooses to increment version
- **Template Processing**: Reads README.md and installer scripts from templates/ directory with {{VERSION}} placeholder substitution
- **Archive Creation**: Generates single `rdd-v{version}.zip` file containing:
  - Framework files (.rdd/scripts/, .rdd/templates/)
  - Prompt files (.github/prompts/)
  - Installation script (install.py) - generated from scripts/install.py
  - Documentation (README.md) - generated from template
  - VS Code settings template (.vscode/settings.json)
  - Seed templates (.rdd-docs/ with config.json, data-model.md, requirements.md, tech-spec.md)
- **Verification**: Generates SHA256 checksum file for archive integrity verification
- **Cleanup**: Removes temporary build directories, keeping only archive and checksum

#### Build Process Steps
1. Extract version from `.rdd/about.json` and validate SemVer format
2. Check for existing build artifacts (rdd-v{version}.zip and .sha256)
3. IF artifacts exist:
   - Display conflict warning with list of existing files
   - Prompt for resolution: stop, increment, or overwrite
   - If increment chosen: confirm and update `.rdd/about.json`
   - If overwrite chosen: confirm and proceed
   - If stop chosen: exit cleanly
4. ELSE (no conflicts):
   - Display current version and prompt for version increment (patch only)
   - Update `.rdd/about.json` if user chooses to increment
5. Create build directory structure (including .rdd-docs/)
6. Copy framework files (prompts, scripts, about.json, templates, LICENSE)
7. Copy VS Code settings template to .vscode/settings.json
8. Copy seed templates to .rdd-docs/ (config.json, data-model.md, requirements.md, tech-spec.md)
9. Generate README.md from templates/README.md with version substitution
10. Generate install.py from scripts/install.py template with version substitution
11. Create ZIP archive with nested directory structure
12. Generate SHA256 checksum file
13. Clean up temporary staging directories

### Installation System
The RDD framework provides Python-based cross-platform installation with GUI and command-line options:

#### Installer Launcher Scripts (Recommended Installation Method)
**Bash Launcher (install.sh - Linux/macOS)**:
- Checks for `python` command first, then `python3`
- Displays clear error messages with installation URLs if Python not found
- Verifies install.py exists in same directory
- Executes Python installer with proper exit code handling
- Color-coded output for user feedback
- Can be double-clicked or run from terminal after `chmod +x`

**Batch Launcher (install.bat - Windows)**:
- Checks for `python` command first, then `python3`
- Displays clear error messages with installation guidance if Python not found
- Verifies install.py exists in same directory
- Executes Python installer with proper exit code handling
- Color-coded output using ANSI escape codes
- Can be double-clicked for easy installation without opening terminal
- Includes `pause` command to keep window open after completion

#### Python Installation (install.py)
**Python Installer (install.py)**:
- Cross-platform installer using Python standard library + optional Tkinter for GUI
- **GUI Folder Selection** (if Tkinter available):
  - Presents menu: "1. Browse for folder (GUI)" or "2. Enter path manually"
  - Opens native folder browser dialog for easy directory selection
  - Automatically falls back to text input if GUI fails or user prefers
- **Installation Description**: Displays clear preview of actions before prompting for directory:
  - Copy RDD framework files (.rdd/)
  - Copy GitHub prompts (.github/prompts/)
  - Copy seed templates (.rdd-docs/)
  - Merge VS Code settings
  - Update .gitignore
  - Verify installation
- **Pre-flight checks**:
  - Python version verification (≥ 3.7)
  - Git installation check
  - Target directory validation (must be Git repository)
- **Enhanced existing installation detection**:
  - Scans for .rdd/, .github/prompts/, .rdd-docs/ directories
  - Lists specific files/directories that will be affected
  - Distinguishes between framework files (overwritten) and user data (preserved)
  - Clear warnings about overwrite behavior
- **Interactive prompts** for target directory (text or GUI)
- **Obsolete file archiving** (upgrade scenarios):
  - Detects obsolete files from previous RDD versions (data-model.md, folder-structure.md)
  - Reads version from existing `.rdd/about.json` if present
  - Creates archive directory `.rdd-docs/archive/installation_<version>/`
  - Moves obsolete files to archive preserving original content
  - Displays clear message explaining files replaced by tech-spec.md sections
  - Recommends manual review for important information
- **Automated file operations**:
  - Copy prompts to `.github/prompts/` (removes all existing `rdd.*.prompt.md` files first to ensure clean replacement)
  - Copy framework to `.rdd/`
  - Copy user guide from `templates/user-guide.md` to `.rdd/user-guide.md`
  - Intelligent VS Code settings merge
  - .gitignore update with workspace exclusion
- **Post-installation verification**:
  - File existence checks
  - RDD command test (`python .rdd/scripts/rdd.py --version`)
- Clear success/error messages with next steps

**Settings Merge Logic**:
- **Array settings** (chat.promptFilesRecommendations, chat.tools.terminal.autoApprove):
  - Handles both object and array formats
  - Appends unique values without duplicates
- **Object settings** (files.associations):
  - Merges keys, RDD values overwrite existing
- **Editor settings** (editor.rulers):
  - Replaces with RDD requirements (80, 120 character columns)

#### Direct Python Installation
For users who prefer direct control:
- Navigate to project directory
- Run: `python /path/to/extracted/rdd-vX.X.X/install.py`
- Same features as launcher-based installation
- Useful for scripted or automated installations

#### RDD Launcher Scripts (Post-Installation)
After installation, the RDD framework provides convenient launcher scripts in the project root for easy access to the RDD menu:

**Windows Launcher (rdd.bat)**:
- Located in project root after installation
- Double-click to launch RDD interactive menu
- Can also be run from terminal: `rdd.bat`
- Checks for Python availability (python or python3)
- Validates RDD framework installation
- Passes command-line arguments to rdd.py
- Keeps window open after execution if double-clicked

**Linux/macOS Launcher (rdd.sh)**:
- Located in project root after installation
- Executable permissions set automatically during installation
- Double-click from file manager or run from terminal: `./rdd.sh`
- Checks for Python availability (python or python3)
- Validates RDD framework installation
- Passes command-line arguments to rdd.py
- Displays clear error messages with installation guidance

**Installation Process**:
- Installer detects OS using `os.name == 'nt'` (Windows vs Unix)
- Copies appropriate launcher (rdd.bat or rdd.sh) to project root
- Sets executable permissions on Unix systems (chmod 0o755)
- Provides usage instructions after installation

### Platform Compatibility
- **Python-based**: Single implementation works on all platforms (Windows, Linux, macOS)
- **No platform-specific scripts needed**: Python provides cross-platform compatibility
- **Python command**: Uses `python` (not `python3`) for universal compatibility

### VS Code Integration
The framework integrates with VS Code through:
- **Chat prompt recommendations**: `.vscode/settings.json` configures `chat.promptFilesRecommendations`
- **Script auto-approval**: Auto-approves script execution for `.rdd/scripts/` directory
- **JSONL file association**: Associates `*.jsonl` files with jsonlines language

