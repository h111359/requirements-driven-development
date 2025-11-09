# Technical Specification

## System Overview

The RDD (Requirements-Driven Development) framework is a structured workflow automation system designed to guide developers through requirement clarification, implementation, and documentation processes. The system consists of:

- **Prompt-driven workflows**: Structured markdown prompts that guide AI agents and developers through RDD phases
- **Script automation**: Bash (Linux) and PowerShell (Windows) scripts that automate repetitive tasks
- **Documentation management**: Structured documentation files that track requirements, changes, and project state
- **Workspace management**: Isolated workspace for active development with archiving capabilities

## Technology Stack

### Programming Languages & Scripts
- **Python**: Primary scripting language for cross-platform automation (`.py` files)
- **Bash**: Legacy scripting language for Linux/macOS (archived, replaced by Python)
- **PowerShell**: Legacy Windows-compatible scripting language (in `src/windows/`)
- **Markdown**: Documentation format for prompts, requirements, and guides
- **JSON/JSONL**: Configuration and logging data format

### Development Tools
- **Git**: Version control and branch management
- **VS Code**: Recommended IDE with GitHub Copilot integration
- **GitHub Copilot**: AI assistant configured for RDD workflow execution

### Dependencies
- **Python 3.7+**: Required for running all RDD scripts
- **Git 2.23+**: Required for version control operations
- **python-is-python3** (Linux only): Optional package to make `python` command available on older Linux systems

## Architecture Patterns

### Domain-Driven Script Organization
The framework uses a domain-based architecture where functionality is organized into specialized utility scripts:

- **Core utilities**: Common functions (logging, validation, configuration)
- **Git utilities**: Git operations and comparisons
- **Branch utilities**: Branch creation, deletion, and management
- **Workspace utilities**: Workspace initialization, archiving, and cleanup
- **Requirements utilities**: Requirements validation and merging
- **Change utilities**: Change workflow orchestration
- **Clarify utilities**: Clarification phase management
- **Prompt utilities**: Prompt execution tracking

### Command Routing Pattern
The main entry point (`rdd.py`) uses a domain-based routing pattern:
```
python .rdd/scripts/rdd.py <domain> <action> [options]
```
Examples:
- `python .rdd/scripts/rdd.py change create` (interactive menu for type selection)
- `python .rdd/scripts/rdd.py workspace init change`
- `python .rdd/scripts/rdd.py requirements merge`
- `python .rdd/scripts/rdd.py config show`
- `python .rdd/scripts/rdd.py config set defaultBranch dev`

**Cross-Platform Compatibility**: The framework uses the `python` command (not `python3`) to ensure compatibility across Windows, Linux, and macOS. On older Linux systems where the `python` command is not available, users can install the `python-is-python3` package or create an alias/symlink.

This Python implementation replaced the previous bash scripts (`rdd.sh`) which are now archived.

### Branch Naming Flexibility
The framework provides flexible branch naming while preserving workspace initialization context:

**User Control**: Users provide complete branch names without automatic prefixes
- Valid examples: `my-feature`, `fix/my-bugfix`, `20251107-0541-install-scripts-outside`, `feature/add-authentication`
- The system only validates kebab-case format with support for forward slashes
- No automatic timestamp injection or type-based prefixes

**Type Selection Purpose**: The fix/enhancement selection during change creation:
- Determines workspace initialization content (fix-specific vs enhancement-specific files)
- Does NOT affect the branch name provided by users
- Allows users to choose their own naming conventions (with or without prefixes)

**Validation**: Branch names must follow kebab-case format:
- Lowercase letters, numbers, hyphens, and forward slashes allowed
- Pattern: `^[a-z0-9]+([/-][a-z0-9]+)*$`
- Examples: `my-branch`, `fix/bug-123`, `20251107-feature-name`, `team/user/feature`

**Wrap-Up Validation**: The wrap-up process validates that the current branch is not a protected branch:
- Protected branches: default branch (from config.json), "main", "master"
- All other branch names are accepted regardless of prefix or naming convention
- Provides clear error messages indicating which branches are protected
- Allows flexible branch naming while protecting critical branches

### Template-Based File Generation
All workspace files are generated from templates stored in `.rdd/templates/` or `src/{platform}/.rdd/templates/`, ensuring consistency across projects and changes.

### Phase-Based Workflow
The framework follows a sequential phase workflow:
1. **Initiate**: Create branch and initialize workspace
2. **Clarify**: Iteratively clarify requirements using structured questions
3. **Execute**: Implement changes following clarified requirements
4. **Update Docs**: Synchronize documentation with implementation
5. **Wrap-Up**: Archive workspace, merge requirements, prepare for PR
6. **Clean-Up**: After PR merge, clean up local environment and remove merged branches

### Simplified Workflow (v1.0.3+)

The framework provides a streamlined 4-option workflow focused on core iteration tasks:

**Main Menu Options**:
1. **Create new iteration** - Start work on a new feature/fix
2. **Update from default** - Sync current branch with latest changes from default branch
3. **Complete current iteration** - Archive work, commit changes, and return to default branch
4. **Delete merged branches** - Interactive cleanup of fully merged branches

**Interactive Menu System**:
- Numeric selection system where users enter numbers to select options
- Clear numbered menu options for easy navigation
- Reliable and error-resistant compared to arrow-based navigation
- Works consistently across all terminal types and platforms
- Support for custom text input when needed
- Color-coded output for improved readability

**Implementation**:
- Simplified numeric menu functions in rdd.py
- Main menu launched when running `python .rdd/scripts/rdd.py` without arguments
- Used for legacy change type selection (Fix/Enhancement) when using CLI commands
- Used for default branch selection during installation
- Prompts user to enter option number or text input

**Workflow Functions**:
- `create_iteration()` - Creates new branch and initializes workspace
- `update_from_default_branch()` - Fetches/merges default branch into current
- `complete_iteration()` - Archives workspace, commits, optionally pushes
- `interactive_branch_cleanup()` - Lists and deletes merged branches

**Example Interaction**:
```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║            RDD Framework                                     ║
║    Requirements-Driven Development                           ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

Current branch: dev
Default branch: dev

RDD Framework - Main Menu:
1. Create new iteration
2. Update from default
3. Complete current iteration
4. Delete merged branches
5. Exit

Enter your choice (1-5): 1
```

**Legacy CLI Access**:
```python
# Legacy commands still available for scripting
python .rdd/scripts/rdd.py change create
python .rdd/scripts/rdd.py branch cleanup
python .rdd/scripts/rdd.py git update-from-default-branch
```

### Iteration Workflow Architecture (v1.0.3+)

The framework's core workflow is built around four iteration management functions:

#### 1. Create New Iteration (`create_iteration()`)

**Purpose**: Start work on a new feature or fix

**Safety Checks**:
- Verifies user IS on default branch (stops if not)
- Verifies workspace IS empty (stops if not empty)

**Process**:
1. Prompts for branch name with normalization and validation
2. Pulls latest from default branch (if not local-only mode)
3. Creates and checks out new branch
4. Initializes workspace with `.rdd/templates/copilot-prompts.md`

**Branch Naming**:
- Accepts user input with normalization to kebab-case
- Validates format (lowercase, hyphens, forward slashes)
- No automatic prefixes or timestamps added

#### 2. Update From Default (`update_from_default_branch()`)

**Purpose**: Sync current branch with latest changes from default branch

**Safety Checks**:
- Stops if already on default branch

**Process**:
1. Stashes any uncommitted changes
2. Fetches and pulls latest from default branch (if not local-only mode)
3. Merges default branch into current branch
4. Restores stashed changes
5. Shows clear error messages on conflicts

#### 3. Complete Current Iteration (`complete_iteration()`)

**Purpose**: Archive work, commit changes, and return to default branch

**Safety Checks**:
- Verifies user is NOT on default branch (stops if on default)
- Verifies workspace is NOT empty (stops if empty)

**Process**:
1. Archives all workspace files to `.rdd-docs/archive/<sanitized-branch-name>/`
2. Creates archive metadata with timestamp, branch, author, commit info
3. Commits all changes with message "Completing work on <branch-name>"
4. Asks user if they want to push to remote (if not local-only mode)
5. If yes, pushes branch and reminds about pull request
6. Checks out to default branch

**Archive Naming**:
- Uses sanitized branch name (replaces `/` and `\` with `-`)
- Example: `fix/bug-123` → `.rdd-docs/archive/fix-bug-123/`

#### 4. Delete Merged Branches (`interactive_branch_cleanup()`)

**Purpose**: Clean up branches that have been fully merged

**Process**:
1. Fetches from remote (if not local-only mode)
2. Checks out default branch
3. Lists all branches fully merged into default branch
4. Excludes protected branches (default, main, master, dev)
5. Prompts user to select branches by number or "all"
6. Deletes selected branches locally
7. Optionally deletes from remote (if not local-only mode)

**Protected Branches**:
- Default branch (from config.json)
- "main", "master", "dev"

**User Interaction**:
```
The following branches are fully merged:
  1. fix/bug-123
  2. feature/add-login
  3. hotfix/urgent-fix

Enter numbers to delete (comma-sep or 'all' to delete all, ENTER to cancel): 1,3
```

### Configuration Management
The framework uses a configuration file system for repository-wide settings:

**Configuration Storage**:
- **Location**: `.rdd-docs/config.json`
- **Format**: JSON with version, defaultBranch, localOnly, timestamps
- **Version Control**: File is tracked in repository and shared across team

**Configuration Access**:
- **CLI Commands**:
  - `python .rdd/scripts/rdd.py config show` - Display all configuration
  - `python .rdd/scripts/rdd.py config get <key>` - Get specific value
  - `python .rdd/scripts/rdd.py config set <key> <value>` - Update value
- **Programmatic Access**:
  - `get_rdd_config(key, default)` - Read configuration value
  - `set_rdd_config(key, value)` - Write configuration value
  - `get_rdd_config_path()` - Get path to config file

**Default Branch Configuration**:
- Config file allows custom default branch (not just main/master)
- `get_default_branch()` function prioritizes config over auto-detection
- Interactive selection during initialization populates config.json
- Supports any branch name (main, dev, develop, master, etc.)

**Configuration Priority**:
1. Read from `.rdd-docs/config.json` if exists
2. Fall back to branch detection (main → master)
3. Default to "main"

**Local-Only Mode Configuration**:
- **Purpose**: Allows repositories to operate without GitHub remote
- **Configuration**: Set `localOnly: true` in config.json to enable
- **Installation**: User prompted during installation to choose mode
- **Default**: `localOnly: false` (GitHub remote enabled)
- **Behavior**: When enabled, all remote git operations (fetch, push, pull) are skipped
- **Implementation**:
  - `is_local_only_mode()` function checks config.json for localOnly setting
  - `pull_main()` skips remote fetch when local-only mode enabled
  - `interactive_branch_cleanup()` skips remote fetch and deletion prompts
  - Clear informational messages displayed when operations skipped
- **Use Cases**: 
  - Repositories without GitHub/remote hosting
  - Local-only development workflows
  - Offline development environments
  - Testing and experimentation without remote side effects

## Component Architecture

### Script Components

#### Main Entry Point
- **File**: `.rdd/scripts/rdd.py`
- **Purpose**: Unified command interface with domain routing
- **Version Management**: Uses `get_framework_version()` to read version from `.rdd-docs/config.json` instead of hardcoded version variable
- **Responsibilities**:
  - Parse command-line arguments
  - Route commands to appropriate domain handlers
  - Display help and version information
  - Execute workflow operations

**Note**: Legacy bash implementation (rdd.sh and utility scripts) archived in workspace during migration to Python.

#### Utility Scripts (Domain-Specific)
The Python implementation (`rdd_utils.py`) provides utility functions organized by domain:

1. **Core utilities**: Foundation functions
   - Color output (print_success, print_error, print_info, print_warning)
   - Validation (validate_name, normalize_to_kebab_case)
   - Configuration management (get_config, set_config)
   - Timestamp generation

2. **Git utilities**: Git operations
   - Repository validation
   - Branch operations
   - Stashing and merging
   - Diff and comparison

3. **Branch utilities**: Branch lifecycle
   - Branch creation with naming conventions
   - Branch deletion (single and bulk)
   - Merge status checking
   - Post-merge cleanup

4. **Workspace utilities**: Workspace management
   - Workspace initialization
   - Archiving with metadata
   - Backup and restore
   - Complete workspace clearing

5. **Requirements utilities**: Requirements handling
   - Format validation
   - Requirements merging
   - ID assignment for new requirements
   - Impact analysis

6. **Change utilities**: Change workflow
   - Change creation
   - Change tracking
   - Workflow orchestration
   - Completion and wrap-up

7. **Clarify utilities**: Clarification phase
   - Clarification initialization
   - Question logging
   - Clarification status tracking

8. **Prompt utilities**: Prompt management
   - Prompt completion marking
   - Execution logging
   - Status checking

9. **Config utilities**: Configuration management
   - Configuration file reading (get_rdd_config)
   - Configuration file writing (set_rdd_config)
   - Configuration path resolution (get_rdd_config_path)
   - Default branch detection with config priority

**Legacy Note**: Previous bash implementation (branch-utils.sh, change-utils.sh, etc.) has been archived.

### Cross-Platform Implementation

**Current Implementation**: Python-based (`rdd.py` and `rdd_utils.py`)
- Cross-platform compatible (Windows, Linux, macOS)
- Single codebase for all platforms
- Native Python libraries for file operations, JSON handling, and subprocess management

**Legacy Implementation**: Bash and PowerShell scripts (archived)
- Previously maintained separate implementations for Linux (bash) and Windows (PowerShell)
- Located in `src/linux/.rdd/scripts/` and `src/windows/.rdd/scripts/`
- Bash scripts from `.rdd/scripts/` archived to workspace during Python migration

## Data Architecture

### Configuration Files
- **Change config**: `.rdd.[fix|enh].<branch-name>` - JSON file tracking current change
- **Archive metadata**: `.archive-metadata` - JSON file documenting archived changes
- **Execution log**: `log.jsonl` - JSONL file logging prompt executions
- **RDD config**: `.rdd-docs/config.json` - JSON file storing framework configuration (defaultBranch, version, timestamps)

### Configuration File Schema

#### config.json
Located in `.rdd-docs/config.json`, version-controlled with repository:
```json
{
  "version": "1.0.0",
  "defaultBranch": "main",
  "localOnly": false,
  "created": "2025-11-06T08:00:00Z",
  "lastModified": "2025-11-06T08:00:00Z"
}
```

Fields:
- **version**: Framework version (semantic versioning)
- **defaultBranch**: Name of the repository's default branch (e.g., "main", "dev", "master")
- **localOnly**: Boolean flag for local-only mode (true = no remote operations, false = normal GitHub remote mode)
- **created**: ISO 8601 timestamp of initial configuration creation
- **lastModified**: ISO 8601 timestamp of last configuration update

### Documentation Files
- **Requirements**: `.rdd-docs/requirements.md` - Structured requirements with IDs
- **Technical spec**: `.rdd-docs/tech-spec.md` - Technical architecture and design
- **Data model**: `.rdd-docs/data-model.md` - Configuration and file schemas
- **Folder structure**: `.rdd-docs/folder-structure.md` - Project organization

### Workspace Files
- **Stand-alone prompts**: `.rdd.copilot-prompts.md` - Checklist of executable prompts
- **Open questions**: `open-questions.md` - Clarification questions and answers
- **Requirements changes**: `requirements-changes.md` - Requirements modifications for merge

Note: The `change.md` template has been **removed** from the framework and is no longer created in workspace.

## Deployment Architecture

### Build System
The RDD framework uses a Python-based build system to create release packages:

#### Build Script (scripts/build.py)
- **Purpose**: Creates cross-platform release archives with all necessary files
- **Version Management**: Extracts version from `.rdd-docs/config.json` as single source of truth (fixed from previous hardcoded version in rdd.py)
- **Interactive Version Control**: Displays current version and prompts user to either increment patch version or rebuild with same version
- **Version Persistence**: Automatically updates `.rdd-docs/config.json` when user chooses to increment version
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
1. Extract version from `.rdd-docs/config.json` and validate SemVer format
2. Display current version and prompt for version increment (patch only)
3. Update `.rdd-docs/config.json` with new version if user chooses to increment
4. Create build directory structure (including .rdd-docs/)
5. Copy framework files (prompts, scripts, templates, LICENSE)
6. Copy VS Code settings template to .vscode/settings.json
7. Copy seed templates to .rdd-docs/ (config.json, data-model.md, requirements.md, tech-spec.md)
8. Generate README.md from templates/README.md with version substitution
9. Generate install.py from scripts/install.py template with version substitution
10. Create ZIP archive with nested directory structure
11. Generate SHA256 checksum file
12. Clean up temporary staging directories

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
- **Automated file operations**:
  - Copy prompts to `.github/prompts/`
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

## Testing Infrastructure

### Test Organization

The framework includes a comprehensive testing suite organized by test type:

```
tests/
├── python/              # Python script tests (pytest)
│   ├── test_rdd_main.py       # Main entry point tests
│   ├── test_rdd_utils.py      # Utility function tests
│   ├── test_integration.py    # Integration tests
│   └── conftest.py            # Pytest fixtures
├── build/               # Build script tests
│   ├── test_build.py          # Build system tests
│   └── conftest.py            # Build fixtures
├── install/             # Installation tests
│   ├── test_install.py        # Installer tests
│   └── conftest.py            # Install fixtures
├── fixtures/            # Shared test fixtures
│   └── README.md              # Fixtures documentation
├── requirements.txt     # Test dependencies
└── README.md            # Testing documentation
```

### Test Frameworks

- **Python Tests**: pytest with pytest-cov for coverage reporting
- **Test Coverage**: 80+ tests covering all framework scripts
- **Pass Rate**: 100% (all Python tests passing)

### Test Isolation

All tests use isolation mechanisms to prevent corruption of existing code:
- **Temporary directories**: Each test creates and cleans up temp dirs
- **Mock git repositories**: Fresh git repos for each test
- **Subprocess mocking**: Git commands mocked where appropriate
- **No side effects**: Tests don't modify actual project files
- **Parallel safe**: Tests can run concurrently without conflicts

### Virtual Environment

The framework provides automated virtual environment setup for test execution:
- **Script**: `scripts/setup-test-env.py` creates `.venv/` directory
- **Smart handling**: Preserves existing environment, only updates packages
- **Test dependencies**: pytest, pytest-cov, pytest-mock, pytest-timeout, pytest-xdist
- **Build exclusion**: .venv/ excluded from release archives
- **CI/CD isolation**: GitHub Actions creates fresh environments per run

### Test Runner Scripts

The framework provides a unified Python-based test runner:

**Python Test Runner (scripts/run-tests.py)**:
- Cross-platform test execution (Windows, Linux, macOS)
- Color-coded output for readability
- Progress indicators
- Prerequisites checking
- Virtual environment activation
- Runs pytest for Python, build, and install tests
- Clear test summary with pass/fail counts
- Exit code reflects test success/failure

**Usage**:
```bash
python scripts/run-tests.py
```

### GitHub Actions CI/CD

Automated testing on push and pull requests:
- **Python version**: Python 3.9+ (expandable to matrix)
- **Test execution**: Uses `python scripts/run-tests.py` for unified cross-platform testing
- **Code coverage**: Coverage report generated during test run
- **Test summary**: Aggregated results with pass/fail status

### Test Coverage

**Current Coverage**:
- **rdd.py**: CLI routing, domain handlers, interactive menus
- **rdd_utils.py**: All utility functions (git, branch, workspace, config)
- **build.py**: Version extraction, archive creation, checksums
- **install.py**: Pre-flight checks, file operations, settings merge
- **run-tests.py**: Test runner, virtual environment activation, cross-platform execution

**Coverage Metrics**:
- 80+ tests total
- 49 Python unit tests (100% passing)
- 13 build tests (100% passing)
- 21 install tests (100% passing)

## Performance

### Script Execution
- **Startup time**: < 1 second for command routing
- **Workspace initialization**: < 5 seconds
- **Requirements merge**: < 10 seconds for typical changes
- **Test execution**: < 30 seconds for full Python test suite
- **Build process**: < 10 seconds for archive creation

### Scalability
- Supports unlimited concurrent changes (via separate branches)
- Archive storage scales linearly with number of completed changes
- No performance degradation with large requirements files (< 1000 requirements)
- Test suite scales linearly with added tests (parallel execution supported)

## Security

### Script Execution Safety
- Scripts use `set -e` (Bash) or `$ErrorActionPreference = 'Stop'` (PowerShell) to fail fast
- No arbitrary code execution from user input
- Git operations use local repository only (no remote credential handling)

### Data Protection
- All data stored in local git repository
- No external service dependencies
- Workspace files cleared after archiving (no sensitive data retention)

### Access Control
- Relies on OS-level file permissions
- Git credentials managed by user's git configuration
- No authentication or authorization system within framework

## Infrastructure

### Project Folder Structure
```
repo-root/
├── .github/                      # GitHub-specific files
│   ├── prompts/                  # Shared prompt templates
│   └── copilot-instructions.md   # Copilot configuration
├── .rdd/                         # Legacy scripts (deprecated)
│   ├── scripts/                  # To be migrated to src/{platform}
│   └── templates/                # Shared templates
├── src/                          # Platform-specific implementations
│   ├── linux/                    # Linux/macOS scripts
│   └── windows/                  # Windows scripts
├── .rdd-docs/                    # Documentation and workspace
│   ├── workspace/                # Active development workspace
│   ├── archive/                  # Completed change archives
│   └── *.md                      # Project documentation
├── build/                        # Build artifacts (gitignored)
└── scripts/                      # Project-specific automation
```

### Database & Storage
- **No database required**: All data in text files (Markdown, JSON, JSONL)
- **Git as storage**: Version history and branching managed by git
- **Archive storage**: Filesystem-based archives in `.rdd-docs/archive/`

### Third-Party Dependencies
- **GitHub Copilot**: AI assistant for executing prompts (optional but recommended)
- **Git**: Required for version control operations
- **Python 3.8+**: Required for running RDD scripts

## Migration Notes

### Recent Changes
1. **Python migration**: All bash scripts migrated to Python for true cross-platform compatibility
2. **Bash scripts archived**: Legacy bash implementation (9 scripts) moved to workspace archive
3. **Unified codebase**: Single Python implementation replaces separate bash/PowerShell codebases
4. **fix-management.sh removal**: All fix management functionality consolidated into `rdd.py` with domain routing
5. **change.md template removal**: The `change.md` template file removed from `.rdd/templates/`; workspace no longer includes this file during initialization
6. **Cross-platform command standardization**: All prompt files updated to use `python` command instead of `python3` for Windows/Linux/macOS compatibility
7. **Python setup documentation**: README.md updated with clear instructions for installing `python` command on Linux systems using `python-is-python3` package

### Deprecated Components
- ~~All bash scripts (.sh)~~ - Replaced by Python implementation (`rdd.py` and `rdd_utils.py`); archived in workspace
- ~~`fix-management.sh`~~ - Replaced by `rdd.py` commands
- ~~`.rdd/templates/change.md`~~ - Template removed; no longer used in workspace
- ~~PowerShell scripts (.ps1) in `src/windows/`~~ - No longer needed with Python implementation
