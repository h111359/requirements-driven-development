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

### Interactive Menu System
The framework provides interactive menus for user input using Python's curses library:

**Features**:
- Visual navigation with arrow keys (↑/↓)
- Selection with Enter or Space
- Automatic fallback to numeric input when curses unavailable
- Beautiful Unicode box drawing (╔═╗╚╝║╠╣) for professional appearance
- Clear visual indicators (→ for current selection with bold + reverse video)
- Support for custom text input options
- Dynamic box width (adapts to terminal, max 80 chars)
- Centered title and help text

**Implementation**:
- `_curses_menu()` function in rdd.py provides core menu functionality
- Used for change type selection (Fix/Enhancement)
- Used for default branch selection during initialization
- Handles terminal compatibility issues gracefully

**Example Visual**:
```
╔═══════════════════════════════════════════════════════════╗
║                  Select change type                        ║
╠═══════════════════════════════════════════════════════════╣
║  Use ↑/↓ arrows to navigate, Enter to select, ESC/q...   ║
╠═══════════════════════════════════════════════════════════╣
║ → Fix                                                      ║  (highlighted)
║   Enhancement                                              ║
╚═══════════════════════════════════════════════════════════╝
```

**Example Usage**:
```python
python .rdd/scripts/rdd.py change create
# Displays interactive menu:
# → Fix
#   Enhancement (hidden by default)
```

### Configuration Management
The framework uses a configuration file system for repository-wide settings:

**Configuration Storage**:
- **Location**: `.rdd-docs/config.json`
- **Format**: JSON with version, defaultBranch, timestamps
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
  "created": "2025-11-06T08:00:00Z",
  "lastModified": "2025-11-06T08:00:00Z"
}
```

Fields:
- **version**: Framework version (semantic versioning)
- **defaultBranch**: Name of the repository's default branch (e.g., "main", "dev", "master")
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
1. Extract version from rdd.py and validate SemVer format
2. Create build directory structure (including .rdd-docs/)
3. Copy framework files (prompts, scripts, templates, LICENSE)
4. Copy VS Code settings template to .vscode/settings.json
5. Copy seed templates to .rdd-docs/ (config.json, data-model.md, requirements.md, tech-spec.md)
6. Generate README.md from templates/README.md with version substitution
7. Generate install.py from scripts/install.py template with version substitution
8. Create ZIP archive with nested directory structure
9. Generate SHA256 checksum file
10. Clean up temporary staging directories

### Installation System
The RDD framework provides Python-based cross-platform installation:

#### Python Installation (install.py)
**Python Installer (install.py)**:
- Cross-platform installer using Python standard library only
- Pre-flight checks:
  - Python version verification (≥ 3.7)
  - Git installation check
  - Target directory validation (must be Git repository)
- Existing installation detection with upgrade warnings
- Interactive prompts for target directory
- Automated file operations:
  - Copy prompts to `.github/prompts/`
  - Copy framework to `.rdd/`
  - Intelligent VS Code settings merge
  - .gitignore update with workspace exclusion
- Post-installation verification:
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

#### Manual Installation
For users who prefer manual control:
- Step-by-step file copying instructions
- Platform-specific commands (PowerShell/Bash)
- Manual VS Code settings merge guidance
- Manual .gitignore update steps

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
