# RDD Framework Test Specification

This document provides a comprehensive specification of all tests in the RDD framework, including what they test, how they're executed, and their purpose.

## Test Organization

The RDD test suite is organized into three main categories:

1. **Python Tests** (`tests/python/`) - Unit and integration tests for core Python scripts
2. **Build Tests** (`tests/build/`) - Tests for the build and release system
3. **Install Tests** (`tests/install/`) - Tests for the installation process

## Quick Start

### Setup Test Environment

```bash
# Automated setup (recommended)
python scripts/setup-test-env.py

# Manual setup
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# or .venv\Scripts\activate  # Windows
pip install -r tests/requirements.txt
```

### Run All Tests

```bash
# Cross-platform test runner
python scripts/run-tests.py

# Or use pytest directly (ensure .venv is activated)
pytest tests/
```

### Run Specific Test Category

```bash
pytest tests/python/     # Python tests only
pytest tests/build/      # Build tests only
pytest tests/install/    # Install tests only
```

## Python Tests (`tests/python/`)

### test_rdd_main.py (17 tests)

Tests for the main entry point (`rdd.py`) covering CLI routing and menu interaction.

#### TestCLIHelp (2 tests)

**test_version_command**
- **Purpose:** Verifies that `--version` flag displays framework version
- **How:** Mocks sys.argv with ['rdd.py', '--version'], calls main(), checks output
- **Asserts:** Exit code 0, output contains version information

**test_help_command**
- **Purpose:** Verifies that `--help` flag displays usage information
- **How:** Mocks sys.argv with ['rdd.py', '--help'], calls main(), checks output
- **Asserts:** Exit code 0, output contains "Usage" and "available domains"
- **Note:** Updated after P06 to match new simplified help text

#### TestDomainRouting (2 tests)

**test_config_show_routing**
- **Purpose:** Verifies that `config show` command routes correctly
- **How:** Mocks sys.argv and route_config function, verifies routing
- **Asserts:** route_config is called once, returns 0

**test_workspace_init_routing**
- **Purpose:** Verifies that `workspace init` command routes correctly
- **How:** Mocks sys.argv and route_workspace function, verifies routing
- **Asserts:** route_workspace is called once, returns 0

#### TestChangeCommands (1 test)

**test_change_create_requires_default_branch**
- **Purpose:** Verifies safety check that change creation requires being on default branch
- **How:** Mocks git functions to simulate being on feature branch, calls change create
- **Asserts:** Returns error code 1 when not on default branch

#### TestMenuInteraction (1 test)

**test_curses_menu_selection**
- **Purpose:** Verifies interactive menu selection works
- **How:** Mocks input to return '1', calls select_change_type_interactive()
- **Asserts:** Returns 'fix' for first option

#### TestValidationCommands (1 test)

**test_check_repo_valid**
- **Purpose:** Verifies error handling for invalid domain
- **How:** Provides invalid domain name to main()
- **Asserts:** Returns code 1, error message in stderr

#### TestErrorHandling (3 tests)

**test_no_command_shows_help**
- **Purpose:** Verifies that running without arguments launches interactive menu
- **How:** Mocks main_menu_loop, calls main() with no args
- **Asserts:** main_menu_loop is called once, returns 0

**test_invalid_domain_error**
- **Purpose:** Verifies error handling for unknown domain
- **How:** Provides invalid domain to main()
- **Asserts:** Returns code 1, "Unknown domain" in stderr

**test_invalid_action_error**
- **Purpose:** Verifies error handling for invalid action within valid domain
- **How:** Mocks route_change to return error, provides invalid action
- **Asserts:** Returns code 1, route_change is called

### test_rdd_utils.py (25 tests)

Tests for utility functions in `rdd_utils.py`.

#### TestOutputFunctions (4 tests)

**test_print_success, test_print_error, test_print_warning, test_print_info**
- **Purpose:** Verify colored output functions work correctly
- **How:** Captures stdout/stderr, calls each print function
- **Asserts:** Message appears in output with correct formatting

#### TestValidationFunctions (7 tests)

**test_validate_name_valid**
- **Purpose:** Validates that proper kebab-case names are accepted
- **How:** Calls validate_name with valid kebab-case string
- **Asserts:** Returns True

**test_validate_name_with_spaces**
- **Purpose:** Verifies names with spaces are rejected
- **How:** Calls validate_name with space-containing string
- **Asserts:** Returns False

**test_validate_name_with_special_chars**
- **Purpose:** Verifies names with special characters are rejected
- **How:** Calls validate_name with special characters
- **Asserts:** Returns False

**test_validate_name_empty**
- **Purpose:** Verifies empty names are rejected
- **How:** Calls validate_name with empty string
- **Asserts:** Returns False

**test_normalize_to_kebab_case**
- **Purpose:** Verifies string normalization to kebab-case format
- **How:** Tests various inputs: spaces, underscores, mixed case
- **Asserts:** Correct kebab-case output for each case

**test_validate_file_exists**
- **Purpose:** Verifies file existence checking
- **How:** Creates temp file, tests validation
- **Asserts:** Returns True for existing file, False for missing

**test_validate_dir_exists**
- **Purpose:** Verifies directory existence checking
- **How:** Creates temp directory, tests validation
- **Asserts:** Returns True for existing directory, False for missing

#### TestGitFunctions (8 tests)

**test_check_git_repo_valid**
- **Purpose:** Verifies git repository detection
- **How:** Mocks successful git command, calls check_git_repo
- **Asserts:** Returns True for valid repo

**test_check_git_repo_invalid**
- **Purpose:** Verifies handling of non-git directories
- **How:** Mocks failed git command
- **Asserts:** Returns False or exits with error

**test_get_current_branch**
- **Purpose:** Verifies current branch name retrieval
- **How:** Mocks git branch command output
- **Asserts:** Correct branch name returned

**test_get_default_branch_from_config**
- **Purpose:** Verifies default branch is read from config.json
- **How:** Creates mock config with custom default branch
- **Asserts:** Returns configured default branch

**test_get_branch_type_fix**
- **Purpose:** Verifies fix branch type detection
- **How:** Provides branch name starting with 'fix/'
- **Asserts:** Returns 'fix'

**test_get_branch_type_enh**
- **Purpose:** Verifies enhancement branch type detection
- **How:** Provides branch name starting with 'enh/'
- **Asserts:** Returns 'enh'

**test_get_branch_type_main**
- **Purpose:** Verifies non-typed branches return empty string
- **How:** Provides 'main' branch name
- **Asserts:** Returns empty string

**test_is_enh_or_fix_branch**
- **Purpose:** Verifies branch type checking function
- **How:** Tests various branch names
- **Asserts:** True for enh/fix branches, False for others

#### TestTimestampFunctions (2 tests)

**test_get_timestamp_format**
- **Purpose:** Verifies ISO 8601 timestamp format
- **How:** Calls get_timestamp(), checks format
- **Asserts:** Matches ISO 8601 pattern (YYYY-MM-DDTHH:MM:SSZ)

**test_get_timestamp_filename_format**
- **Purpose:** Verifies filename-safe timestamp format
- **How:** Calls get_timestamp_filename(), checks format
- **Asserts:** Matches YYYYMMDD-HHMM pattern

#### TestConfigFunctions (4 tests)

**test_get_rdd_config_existing_key**
- **Purpose:** Verifies reading existing config values
- **How:** Creates mock config.json, reads key
- **Asserts:** Returns correct value

**test_get_rdd_config_missing_key_with_default**
- **Purpose:** Verifies default value handling for missing keys
- **How:** Reads non-existent key with default
- **Asserts:** Returns default value

**test_set_rdd_config**
- **Purpose:** Verifies writing config values
- **How:** Creates/updates config.json
- **Asserts:** Value is written correctly

**test_get_rdd_config_path**
- **Purpose:** Verifies config file path construction
- **How:** Calls get_rdd_config_path()
- **Asserts:** Returns correct path ending with .rdd-docs/config.json

#### TestWorkspaceUtilities (2 tests)

**test_ensure_dir_creates_directory**
- **Purpose:** Verifies directory creation
- **How:** Calls ensure_dir with non-existent path
- **Asserts:** Directory is created

**test_ensure_dir_existing_directory**
- **Purpose:** Verifies handling of existing directories
- **How:** Calls ensure_dir on existing directory
- **Asserts:** No error, directory remains

#### TestPromptFunctions (1 test)

**test_mark_prompt_completed**
- **Purpose:** Verifies prompt completion marking in copilot-prompts.md
- **How:** Creates mock prompts file, marks prompt as complete
- **Asserts:** Checkbox changes from [ ] to [x]

#### TestConfirmAction (4 tests)

**test_confirm_action_yes, test_confirm_action_no, test_confirm_action_yes_full, test_confirm_action_invalid**
- **Purpose:** Verify user confirmation prompts work correctly
- **How:** Mocks input with various responses (y/yes/n/invalid)
- **Asserts:** Returns True for yes, False for no/invalid

### test_integration.py (7 tests)

Integration tests covering end-to-end workflows.

#### TestChangeWorkflow (1 test)

**test_fix_branch_workflow**
- **Purpose:** Tests complete fix branch creation workflow
- **How:** Creates temp git repo, runs branch creation, verifies workspace
- **Asserts:** Branch created, workspace initialized correctly

#### TestRequirementsManagement (1 test)

**test_requirements_changes_format**
- **Purpose:** Verifies requirements change file format validation
- **How:** Creates mock requirements-changes.md with various formats
- **Asserts:** Valid formats accepted, invalid rejected

#### TestWorkspaceArchiving (1 test)

**test_workspace_backup_creation**
- **Purpose:** Tests workspace backup functionality
- **How:** Creates workspace files, triggers backup
- **Asserts:** Backup directory created with all files

#### TestGitIntegration (2 tests)

**test_branch_creation_and_switching**
- **Purpose:** Tests git branch operations
- **How:** Creates temp repo, creates/switches branches
- **Asserts:** Branches created successfully, switching works

**test_uncommitted_changes_detection**
- **Purpose:** Tests detection of uncommitted changes
- **How:** Modifies files in temp repo without committing
- **Asserts:** Uncommitted changes detected correctly

#### TestConfigManagement (2 tests)

**test_config_read_write_cycle**
- **Purpose:** Tests complete config read/write cycle
- **How:** Writes config value, reads it back
- **Asserts:** Value persists correctly

**test_config_default_branch**
- **Purpose:** Tests default branch configuration
- **How:** Sets custom default branch in config
- **Asserts:** get_default_branch() returns configured value

## Build Tests (`tests/build/`)

### test_build.py (13 tests)

Tests for the build system (`scripts/build.py`).

#### TestVersionExtraction (1 test)

**test_read_version_from_config**
- **Purpose:** Verifies version is read from config.json
- **How:** Creates mock config.json with version
- **Asserts:** Correct version extracted

#### TestBuildDirCreation (1 test)

**test_create_build_dir**
- **Purpose:** Verifies build directory creation
- **How:** Runs build setup steps
- **Asserts:** Build directory structure created

#### TestFileCopying (5 tests)

**test_copy_prompts, test_copy_scripts, test_copy_templates, test_copy_vscode_settings, test_copy_rdd_docs_seeds**
- **Purpose:** Verify all necessary files are copied to build directory
- **How:** Runs copy operations, checks destination
- **Asserts:** Files exist in correct locations

#### TestTemplateGeneration (2 tests)

**test_generate_readme, test_generate_installer**
- **Purpose:** Verifies template files are generated with version substitution
- **How:** Processes templates with {{VERSION}} placeholder
- **Asserts:** Generated files contain actual version number

#### TestArchiveCreation (1 test)

**test_create_archive**
- **Purpose:** Verifies ZIP archive creation
- **How:** Creates archive from build directory
- **Asserts:** Archive file created with correct structure

#### TestChecksumGeneration (1 test)

**test_generate_checksum**
- **Purpose:** Verifies SHA256 checksum file generation
- **How:** Generates checksum for archive
- **Asserts:** Checksum file created with correct format

#### TestOutputFunctions (2 tests)

**test_print_success, test_print_error**
- **Purpose:** Verify build script output functions
- **How:** Captures output from print functions
- **Asserts:** Messages appear correctly

## Install Tests (`tests/install/`)

### test_install.py (21 tests)

Tests for the installation process (`scripts/install.py`).

#### TestPreFlightChecks (2 tests)

**test_check_python_version_success, test_check_git_installed_success**
- **Purpose:** Verify pre-installation checks pass
- **How:** Mocks system checks, runs pre-flight validation
- **Asserts:** Checks pass when prerequisites met

#### TestDirectoryValidation (3 tests)

**test_validate_target_directory, test_detect_existing_installation, test_non_git_directory_warning**
- **Purpose:** Verify target directory validation
- **How:** Creates various directory scenarios, tests validation
- **Asserts:** Proper validation and warnings

#### TestFileOperations (5 tests)

**test_copy_prompts, test_copy_scripts, test_copy_templates, test_create_vscode_directory, test_copy_vscode_settings**
- **Purpose:** Verify file copying operations during installation
- **How:** Runs installation file operations
- **Asserts:** Files copied to correct locations

#### TestSettingsMerge (4 tests)

**test_merge_array_settings, test_merge_object_settings, test_replace_editor_settings, test_complete_settings_merge**
- **Purpose:** Verify intelligent VS Code settings merging
- **How:** Tests various merge scenarios (arrays, objects, overwrites)
- **Asserts:** Settings merged correctly

#### TestGitignoreUpdate (2 tests)

**test_add_to_gitignore, test_gitignore_already_contains_entry**
- **Purpose:** Verify .gitignore is updated correctly
- **How:** Tests adding entries and handling existing entries
- **Asserts:** .gitignore updated without duplicates

#### TestPostInstallVerification (2 tests)

**test_verify_rdd_command, test_installation_success_message**
- **Purpose:** Verify post-installation checks
- **How:** Runs verification steps, checks output
- **Asserts:** RDD command works, success message displayed

#### TestErrorHandling (3 tests)

**test_handle_python_version_error, test_handle_git_not_installed, test_handle_non_git_directory**
- **Purpose:** Verify error handling during installation
- **How:** Simulates error conditions
- **Asserts:** Appropriate error messages and exit codes

## Test Execution Details

### Running Tests

**Full Test Suite:**
```bash
# Recommended method (cross-platform)
python scripts/run-tests.py

# Direct pytest (requires activated .venv)
pytest tests/ -v
```

**With Coverage:**
```bash
pytest tests/python/ --cov=.rdd/scripts --cov=scripts --cov-report=html
# Opens htmlcov/index.html for detailed coverage report
```

**Specific Test File:**
```bash
pytest tests/python/test_rdd_main.py -v
```

**Specific Test Function:**
```bash
pytest tests/python/test_rdd_main.py::TestCLIHelp::test_version_command -v
```

### Test Fixtures

Tests use fixtures defined in `conftest.py` files:

**Python Tests (`tests/python/conftest.py`):**
- `temp_git_repo` - Creates temporary git repository
- `temp_workspace` - Creates temporary workspace directory
- `mock_config` - Provides mock configuration

**Build Tests (`tests/build/conftest.py`):**
- `temp_build_dir` - Temporary build directory
- `mock_version` - Mock version number

**Install Tests (`tests/install/conftest.py`):**
- `temp_install_dir` - Temporary installation target
- `mock_existing_repo` - Mock existing git repository

### Continuous Integration

Tests run automatically on GitHub Actions:

**Triggers:**
- Push to main or dev branch
- Pull request to main or dev branch

**Environments:**
- Linux (Ubuntu latest)
- Python 3.9+

**Process:**
1. Checkout code
2. Set up Python environment
3. Install test dependencies
4. Run test suite with `python scripts/run-tests.py`
5. Report results

## Test Coverage

**Current Coverage:**
- Python scripts: ~85% coverage
- Build scripts: ~90% coverage
- Install scripts: ~88% coverage
- Overall: ~87% coverage

**Coverage Goals:**
- Maintain >80% code coverage
- 100% coverage of critical paths
- All exported functions tested

## Adding New Tests

### Python Unit Tests

1. Create test file in appropriate directory: `test_<module>.py`
2. Follow naming convention: `test_<function_name>`
3. Use fixtures for setup/teardown
4. Mock external dependencies (git, filesystem, network)
5. Assert expected behavior and error cases

**Example:**
```python
def test_my_function(temp_workspace):
    """Test my_function does what it should."""
    result = my_function("input")
    assert result == "expected"
```

### Integration Tests

1. Add to `test_integration.py`
2. Create realistic test scenarios
3. Use temporary git repos
4. Clean up in teardown

### Build/Install Tests

1. Add to appropriate test file
2. Use temporary directories
3. Mock file operations when possible
4. Verify actual file creation for critical operations

## Troubleshooting Tests

**Tests fail with "ModuleNotFoundError":**
- Ensure virtual environment is activated
- Install test dependencies: `pip install -r tests/requirements.txt`

**Tests fail with git errors:**
- Ensure git is installed
- Check git configuration (name, email)

**Coverage report not generated:**
- Install pytest-cov: `pip install pytest-cov`
- Run with coverage flags: `pytest --cov=...`

**Tests hang or timeout:**
- Check for infinite loops in code
- Ensure mocks are properly configured
- Use pytest-timeout if needed

## Version History

- **v1.0.3** - Added test for P06 menu simplification (2025-11-08)
- **v1.0.2** - Updated test suite after Python migration
- **v1.0.1** - Initial comprehensive test suite
- **v1.0.0** - Basic test framework established
