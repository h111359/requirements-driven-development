# Implementation Plan: Test Coverage Enhancement for RDD Framework Core

## Overview
This plan outlines the implementation of comprehensive test coverage for the RDD framework core components. Based on the questionnaire answers, we will:
- Completely replace existing tests in `tests/python/` with a new test suite
- Use component-based subdirectories in `tests/rdd-framework/`
- Employ pytest-mock for mocking with heavy mocking approach
- Use shared `.rdd-instance-test/` directory for integration tests
- Implement selective coverage reporting
- Keep CI/CD workflow unchanged (default run-all-tests behavior)
- Prioritize action scripts to achieve 80% coverage first

## Step 1: Remove Obsolete Tests
Remove all existing tests in `tests/python/` directory since they are obsolete after recent framework changes and the prompt explicitly allows complete replacement.

**Files to delete:**
- `tests/python/conftest.py`
- `tests/python/test_integration.py`
- `tests/python/test_rdd_main.py`
- `tests/python/test_rdd_utils.py`
- `tests/python/test_seed.py`
- `tests/python/__pycache__/` (if exists)

**Rationale:** Clean slate approach ensures tests match current framework architecture without legacy baggage (per Questionnaire Q1, Answer A).

## Step 2: Create Test Directory Structure
Create the new `tests/rdd-framework/` directory with component-based subdirectories to organize tests clearly by the framework components they cover.

**Directories to create:**
- `tests/rdd-framework/` - Root directory for all RDD framework tests
- `tests/rdd-framework/actions/` - Tests for action scripts in `.rdd/src/actions/`
- `tests/rdd-framework/config/` - Tests for configuration validation (manifest.json, etc.)
- `tests/rdd-framework/integration/` - End-to-end integration tests
- `tests/rdd-framework/conftest.py` - Shared pytest fixtures and configuration

**Rationale:** Component-based organization mirrors source structure, makes tests easy to locate, and supports selective execution via `--actions` flag (per Questionnaire Q2, Answer B).

## Step 3: Update Test Dependencies
Update `tests/requirements.txt` to include pytest-mock for cleaner mocking syntax and ensure all necessary test dependencies are present.

**Dependencies to verify/add:**
- `pytest>=7.0.0` - Core test framework (already exists)
- `pytest-cov>=4.0.0` - Coverage reporting (already exists)
- `pytest-mock>=3.10.0` - Mocking fixture wrapper (ADD NEW)
- Other existing dependencies remain unchanged

**Rationale:** pytest-mock provides cleaner syntax than unittest.mock while integrating well with pytest (per Questionnaire Q3, Answer B).

## Step 4: Create Shared Test Fixtures and Utilities
Implement `tests/rdd-framework/conftest.py` with shared fixtures for common test setup patterns.

**Fixtures to implement:**
- `temp_rdd_instance()` - Creates temporary `.rdd-instance-test/` directory with required structure
- `mock_registry()` - Provides mock work-iteration-registry.json with configurable prompts
- `sample_prompt()` - Creates sample prompt folder with prompt.md
- `mock_requirements_file()` - Provides mock requirements.md for requirement tests
- Cleanup fixtures to ensure `.rdd-instance-test/` is removed after each test

**Integration test approach:** Shared `.rdd-instance-test/` directory cleaned before each test run (per Questionnaire Q4, Answer A).

**Rationale:** Centralized fixtures reduce code duplication and ensure consistent test setup across all test modules.

## Step 5: Implement Action Script Unit Tests - Prompt Management
Create comprehensive unit tests for prompt-related action scripts achieving ≥80% coverage.

**Test file:** `tests/rdd-framework/actions/test_prompt_actions.py`

**Scripts to test:**
- `prompt_create.py` - Test prompt creation with auto-incrementing IDs
- `prompt_set_state.py` - Test state transitions (active ↔ completed), single-active-prompt invariant
- `prompt_complete.py` - Test completion workflow including registry update
- `prompt_add_to_registry.py` - Test registry formatting and modification inclusion
- `prompt_list.py` - Test prompt listing functionality

**Test coverage includes:**
- Happy path scenarios
- Edge cases (missing files, malformed JSON, duplicate IDs)
- Error handling (invalid states, missing prompts)
- File I/O operations (mocked using pytest-mock)
- Argument validation

**Module docstring:** Describe that this module tests prompt lifecycle management scripts, covering creation, state transitions, completion, and registry updates with mocked filesystem operations.

## Step 6: Implement Action Script Unit Tests - Questionnaire/Plan/Analysis Management
Create unit tests for workflow artifact generation scripts.

**Test file:** `tests/rdd-framework/actions/test_workflow_actions.py`

**Scripts to test:**
- `prompt_questionnaire_generated_on.py` - Test setting questionnaire-generated flag
- `prompt_questionnaire_generated_off.py` - Test unsetting questionnaire-generated flag
- `prompt_questionnaire_delete.py` - Test questionnaire file deletion
- `prompt_questionnaire_answered_off.py` - Test resetting answered flag
- `prompt_plan_generated_on.py` - Test setting plan-generated flag
- `prompt_plan_delete.py` - Test plan file deletion (if exists)
- `prompt_analysis_generated_on.py` - Test setting analysis-generated flag
- `prompt_analysis_delete.py` - Test analysis file deletion
- `questionnaire_check_complete.py` - Test questionnaire completion validation

**Test coverage includes:**
- Flag toggling operations
- File deletion with status reset
- JSON registry updates
- Error cases (file not found, invalid state)

**Module docstring:** Tests for workflow artifact management scripts (questionnaire, plan, analysis) covering flag management, file deletion, and state synchronization.

## Step 7: Implement Action Script Unit Tests - Implementation/Execution Management
Create unit tests for implementation and execution tracking scripts.

**Test file:** `tests/rdd-framework/actions/test_execution_actions.py`

**Scripts to test:**
- `prompt_implementation_completed_on.py` - Test implementation completion flag
- `prompt_implementation_completed_off.py` - Test resetting implementation flag
- `prompt_set_executed_on.py` - Test execution marking
- `prompt_set_execution_mode.py` - Test execution mode switching
- `prompt_delete_execution_mode.py` - Test execution mode deletion (if exists)

**Test coverage includes:**
- Execution mode transitions
- Implementation status tracking
- Registry state updates
- Validation of mode changes

**Module docstring:** Tests for implementation and execution management covering completion flags, execution tracking, and mode switching.

## Step 8: Implement Action Script Unit Tests - Modification Management
Create unit tests for modification workflow scripts.

**Test file:** `tests/rdd-framework/actions/test_modification_actions.py`

**Scripts to test:**
- `modification_create.py` - Test modification creation with sequential IDs
- `modification_complete.py` - Test modification completion workflow
- `modification_list.py` - Test modification listing
- Modification metadata tracking in `modifications-log.json`

**Test coverage includes:**
- Modification ID generation (001, 002, etc.)
- Single active modification constraint
- Modification file creation
- Metadata log updates
- State transitions

**Module docstring:** Tests for modification workflow covering creation, completion, listing, and metadata tracking for prompt corrections.

## Step 9: Implement Action Script Unit Tests - Requirement Management
Create unit tests for requirement CRUD operation scripts.

**Test file:** `tests/rdd-framework/actions/test_requirement_actions.py`

**Scripts to test:**
- `requirement_ur_create.py` - Test UR creation with validation
- `requirement_tr_create.py` - Test TR creation with validation
- `requirement_ur_modify.py` - Test UR modification
- `requirement_tr_modify.py` - Test TR modification
- `requirement_ur_delete.py` - Test UR deletion (marks as [DELETED])
- `requirement_tr_delete.py` - Test TR deletion (marks as [DELETED])

**Test coverage includes:**
- ID auto-increment logic (finding max ID + 1)
- Validation rules (shall language, length constraints)
- Validation bypass (validation=none parameter)
- File format preservation
- [DELETED] marker insertion

**Module docstring:** Tests for requirement management scripts covering CRUD operations, validation, ID generation, and deletion marking.

## Step 10: Implement Action Script Unit Tests - Workdir Management
Create unit tests for workdir and iteration management scripts.

**Test file:** `tests/rdd-framework/actions/test_workdir_actions.py`

**Scripts to test:**
- `workdir_new-setup.py` - Test workdir initialization
- `workdir_archive.py` - Test iteration archiving
- `workdir_clear.py` - Test workdir clearing
- Related archive operations

**Test coverage includes:**
- Workdir structure creation
- Archive folder creation with naming convention
- Workdir clearing preserving registry files
- Safety checks (archive validation)

**Module docstring:** Tests for working directory and iteration management covering initialization, archiving, and cleanup operations.

## Step 11: Implement Action Script Unit Tests - Miscellaneous Actions
Create unit tests for remaining action scripts and utilities.

**Test file:** `tests/rdd-framework/actions/test_misc_actions.py`

**Scripts to test:**
- `files_list_csv_refresh.py` - Test CSV file listing generation
- `files_list_csv_set_description.py` - Test CSV description updates
- `print_timestamp.py` - Test timestamp generation
- Any other utility scripts

**Test coverage includes:**
- File listing generation
- CSV format validation
- Timestamp formatting
- Utility functions

**Module docstring:** Tests for miscellaneous utility scripts including file listing, timestamps, and other helper functions.

## Step 12: Implement Configuration Validation Tests
Create tests for manifest.json validation and configuration integrity.

**Test file:** `tests/rdd-framework/config/test_manifest_validation.py`

**Test scenarios:**
- Manifest JSON schema validation
- Required paths existence verification
- Prompt snippet key resolution
- Framework version extraction
- Component configuration validation
- Upgrade policy validation

**Test coverage includes:**
- Schema structure validation
- Path verification (all paths in requiredPaths exist)
- Prompt snippet mapping resolution
- Version format validation (semantic versioning)

**Module docstring:** Tests for configuration validation including manifest schema, path verification, snippet resolution, and version management.

## Step 13: Implement Integration Tests - Prompt Lifecycle
Create end-to-end integration tests for complete prompt workflows using temporary `.rdd-instance-test/` directory.

**Test file:** `tests/rdd-framework/integration/test_prompt_lifecycle.py`

**Test scenarios:**
1. **Complete prompt workflow**: Create prompt → Set to active → Generate questionnaire → Generate plan → Implement → Complete
2. **Modification workflow**: Complete prompt → Create modification → Execute modification → Complete modification
3. **Multiple prompts workflow**: Create multiple prompts → Ensure single active constraint → Complete prompts in sequence

**Test approach:**
- Use real filesystem in temporary directory
- Execute actual action scripts (subprocess calls)
- Validate JSON/Markdown file contents
- Verify state transitions

**Module docstring:** End-to-end integration tests validating complete prompt lifecycle workflows from creation through completion including questionnaire, plan, and implementation phases.

## Step 14: Implement Integration Tests - Requirement Management
Create integration tests for requirement management workflows.

**Test file:** `tests/rdd-framework/integration/test_requirement_workflows.py`

**Test scenarios:**
1. **Requirement CRUD cycle**: Create UR → Modify UR → Create TR → Delete UR (verify [DELETED])
2. **ID auto-increment**: Create multiple requirements → Verify sequential IDs
3. **Validation enforcement**: Attempt invalid requirement → Verify error, then bypass with validation=none

**Test approach:**
- Real requirements.md manipulation
- Actual script execution
- File format validation

**Module docstring:** Integration tests for requirement management workflows covering CRUD operations, validation, and ID sequencing.

## Step 15: Implement Integration Tests - Iteration Archiving
Create integration tests for iteration archiving workflow.

**Test file:** `tests/rdd-framework/integration/test_iteration_archive.py`

**Test scenarios:**
1. **Full iteration cycle**: Create iteration → Add prompts → Complete prompts → Archive → Verify archive structure
2. **Workdir cleanup**: Archive iteration → Verify workdir cleared → Verify registry preserved
3. **Archive integrity**: Verify archived files match source → Verify folder naming

**Test approach:**
- Real workdir operations
- Actual archiving scripts
- Directory structure validation

**Module docstring:** Integration tests for iteration archiving covering complete workflows from active development through archiving and cleanup.

## Step 16: Update Test Runner for Selective Execution
Enhance `scripts/run-tests.py` to support selective test execution flags while preserving default run-all behavior for CI/CD.

**New command-line flags to add:**
- `--rdd-framework` - Run only tests in `tests/rdd-framework/`
- `--actions` - Run only `tests/rdd-framework/actions/` tests
- `--config` - Run only `tests/rdd-framework/config/` tests
- `--integration` - Run only `tests/rdd-framework/integration/` tests
- `--quick` - Run unit tests only, skip integration tests
- `--coverage` - Generate coverage report (default: enabled)
- `--no-coverage` - Skip coverage reporting

**Default behavior (no flags):** Run all tests in all directories (`tests/build/`, `tests/install/`, `tests/rdd-framework/`) for CI/CD compatibility.

**Coverage reporting approach:**
- Selective coverage: Measure coverage only for code tested by selected category (per Questionnaire Q5, Answer B)
- Default coverage target: `.rdd/src/actions/` and `.rdd/src/web/server.py`
- Coverage enforcement: Fail if coverage < 80% for action scripts

**Implementation notes:**
- Use pytest's `-k` flag for pattern matching
- Use pytest's `--cov-report` for coverage output
- Parse arguments before pytest invocation
- Maintain colored output support (existing TR-0035)

## Step 17: Update Test Environment Setup Script
Enhance `scripts/setup-test-env.py` to ensure pytest-mock is installed in the test environment.

**Changes needed:**
- Add `pytest-mock` to the dependencies installed in virtual environment
- Verify installation success
- Maintain existing colored output and error handling
- Keep existing virtual environment creation logic

**No functional changes** - only dependency addition to support new test requirements.

## Step 18: Create Test Fixtures Directory
Organize test fixtures in `tests/fixtures/rdd-framework/` with minimal realistic data sets.

**Fixture files to create:**
- `tests/fixtures/rdd-framework/sample-registry.json` - Sample work-iteration-registry with varied states
- `tests/fixtures/rdd-framework/sample-requirements.md` - Sample requirements file
- `tests/fixtures/rdd-framework/sample-manifest.json` - Valid manifest for validation tests
- `tests/fixtures/rdd-framework/README.md` - Document fixture purpose and structure

**Rationale:** Fixtures organized by test category with realistic but minimal data reduce maintenance burden (per prompt constraint).

## Step 19: Update Files and Folders Specification
Update `.rdd-instance/specifications/files-and-folders.md` to document the new test structure.

**Additions:**
- Document `tests/rdd-framework/` and its subdirectories
- Document test fixtures in `tests/fixtures/rdd-framework/`
- Update descriptions for `scripts/run-tests.py` to mention selective execution
- Update descriptions for `scripts/setup-test-env.py` to mention pytest-mock

**Format:** Follow existing structure with paths, types, and descriptions.

## Step 20: Verify and Run Complete Test Suite
Execute the complete test suite to verify all tests pass and coverage targets are met.

**Validation steps:**
1. Run `python scripts/setup-test-env.py` - Verify environment setup
2. Run `python scripts/run-tests.py` - Verify all tests pass (default behavior)
3. Run `python scripts/run-tests.py --rdd-framework` - Verify selective execution
4. Run `python scripts/run-tests.py --actions` - Verify action tests only
5. Run `python scripts/run-tests.py --quick` - Verify unit tests only
6. Verify coverage ≥ 80% for `.rdd/src/actions/`
7. Verify existing tests in `tests/build/` and `tests/install/` still pass

**Success criteria validation:**
- ✓ All action scripts in `.rdd/src/actions/` have ≥80% test coverage
- ✓ Manifest validation tests pass with existing manifest.json
- ✓ Integration tests validate full prompt → completion workflow
- ✓ Test runner supports selective execution flags
- ✓ Existing tests in build/ and install/ continue to pass
- ✓ All test files include module-level docstrings

## Requirements Updates

### New Requirements to Create

**UR-0095**: The system shall provide comprehensive automated test coverage for RDD framework core components including action scripts, configuration validation, and integration workflows with minimum 80% code coverage for action scripts.

**Rationale:** Establishes user requirement for test coverage matching the prompt objective.

**Command:**
```bash
python .rdd/src/actions/requirement_ur_create.py text="The system shall provide comprehensive automated test coverage for RDD framework core components including action scripts, configuration validation, and integration workflows with minimum 80% code coverage for action scripts."
```

**UR-0096**: The test runner shall support selective test execution with command-line flags including --rdd-framework for framework tests, --actions for action script tests, --config for configuration tests, --integration for integration tests, and --quick for unit tests only, while maintaining default run-all behavior for CI/CD compatibility.

**Rationale:** Codifies selective execution requirement from prompt for developer workflow efficiency.

**Command:**
```bash
python .rdd/src/actions/requirement_ur_create.py text="The test runner shall support selective test execution with command-line flags including --rdd-framework for framework tests, --actions for action script tests, --config for configuration tests, --integration for integration tests, and --quick for unit tests only, while maintaining default run-all behavior for CI/CD compatibility."
```

**TR-0054**: The framework test suite shall be organized in component-based subdirectories under tests/rdd-framework/ including actions/ for action script tests, config/ for configuration validation tests, and integration/ for end-to-end workflow tests, with shared fixtures in conftest.py.

**Rationale:** Documents technical organization decision from questionnaire answer.

**Command:**
```bash
python .rdd/src/actions/requirement_tr_create.py text="The framework test suite shall be organized in component-based subdirectories under tests/rdd-framework/ including actions/ for action script tests, config/ for configuration validation tests, and integration/ for end-to-end workflow tests, with shared fixtures in conftest.py."
```

**TR-0055**: The framework tests shall use pytest-mock for mocking filesystem operations and external calls in unit tests, providing cleaner syntax than unittest.mock while maintaining compatibility with pytest test runner.

**Rationale:** Documents technical mocking strategy decision from questionnaire.

**Command:**
```bash
python .rdd/src/actions/requirement_tr_create.py text="The framework tests shall use pytest-mock for mocking filesystem operations and external calls in unit tests, providing cleaner syntax than unittest.mock while maintaining compatibility with pytest test runner."
```

**TR-0056**: Integration tests shall use a shared .rdd-instance-test/ temporary directory that is cleaned before each test run to provide realistic filesystem testing while maintaining test isolation through cleanup fixtures.

**Rationale:** Documents integration test approach from questionnaire answer.

**Command:**
```bash
python .rdd/src/actions/requirement_tr_create.py text="Integration tests shall use a shared .rdd-instance-test/ temporary directory that is cleaned before each test run to provide realistic filesystem testing while maintaining test isolation through cleanup fixtures."
```

**TR-0057**: The test runner shall implement selective coverage reporting that measures code coverage only for the components tested by the selected test category, enabling focused development workflows while CI/CD runs all tests for complete coverage metrics.

**Rationale:** Documents selective coverage approach from questionnaire answer.

**Command:**
```bash
python .rdd/src/actions/requirement_tr_create.py text="The test runner shall implement selective coverage reporting that measures code coverage only for the components tested by the selected test category, enabling focused development workflows while CI/CD runs all tests for complete coverage metrics."
```

**TR-0058**: All test modules shall include a module-level docstring describing the component under test, key test scenarios covered, and any special setup requirements to provide context for test maintenance.

**Rationale:** Codifies documentation requirement from prompt success criteria.

**Command:**
```bash
python .rdd/src/actions/requirement_tr_create.py text="All test modules shall include a module-level docstring describing the component under test, key test scenarios covered, and any special setup requirements to provide context for test maintenance."
```

**TR-0059**: Test fixtures shall be organized in tests/fixtures/rdd-framework/ with component-specific subdirectories using realistic but minimal data sets to reduce maintenance burden while providing adequate test coverage.

**Rationale:** Documents fixture organization from prompt constraints.

**Command:**
```bash
python .rdd/src/actions/requirement_tr_create.py text="Test fixtures shall be organized in tests/fixtures/rdd-framework/ with component-specific subdirectories using realistic but minimal data sets to reduce maintenance burden while providing adequate test coverage."
```

### Requirements to Modify

**TR-0029**: Current text references outdated script paths (`.rdd/src/setup-test-env.py` and `.rdd/src/run-tests.py`) that should be `scripts/setup-test-env.py` and `scripts/run-tests.py`.

**Modified text:** "The `.github/workflows/tests.yaml` workflow shall define a job `all-tests-linux` that runs on `ubuntu-latest`, checks out the repository, installs Python 3.9 using `actions/setup-python@v5`, installs BATS, sets up the test environment by running `python scripts/setup-test-env.py`, and executes all tests by running `python scripts/run-tests.py`."

**Rationale:** Correct script paths to match actual file locations in `scripts/` directory.

**Command:**
```bash
python .rdd/src/actions/requirement_tr_modify.py id="TR-0029" text="The .github/workflows/tests.yaml workflow shall define a job all-tests-linux that runs on ubuntu-latest, checks out the repository, installs Python 3.9 using actions/setup-python@v5, installs BATS, sets up the test environment by running python scripts/setup-test-env.py, and executes all tests by running python scripts/run-tests.py."
```

**TR-0032**: Similar path correction needed for Windows test job.

**Modified text:** "The `.github/workflows/tests.yaml` workflow shall define a job `all-tests-windows` that runs on `windows-latest`, checks out the repository, installs Python 3.9 using `actions/setup-python@v5`, installs the Pester module using PowerShell, sets up the test environment by running `python scripts/setup-test-env.py`, and executes all tests by running `python scripts/run-tests.py`."

**Rationale:** Correct script paths for consistency.

**Command:**
```bash
python .rdd/src/actions/requirement_tr_modify.py id="TR-0032" text="The .github/workflows/tests.yaml workflow shall define a job all-tests-windows that runs on windows-latest, checks out the repository, installs Python 3.9 using actions/setup-python@v5, installs the Pester module using PowerShell, sets up the test environment by running python scripts/setup-test-env.py, and executes all tests by running python scripts/run-tests.py."
```

## Files and Folders Specification Updates

### New Entries to Add

**tests/rdd-framework/**
- **Path**: `repo-root/tests/rdd-framework/`
- **Type**: Directory
- **Description**: Comprehensive test suite for RDD framework core components organized by component type

**tests/rdd-framework/conftest.py**
- **Path**: `repo-root/tests/rdd-framework/conftest.py`
- **Type**: Python script
- **Description**: Shared pytest fixtures and configuration for RDD framework tests including temporary instance creation and mock registry utilities

**tests/rdd-framework/actions/**
- **Path**: `repo-root/tests/rdd-framework/actions/`
- **Type**: Directory
- **Description**: Unit tests for action scripts in .rdd/src/actions/ covering prompt management, workflow artifacts, requirements, and workdir operations

**tests/rdd-framework/actions/test_prompt_actions.py**
- **Path**: `repo-root/tests/rdd-framework/actions/test_prompt_actions.py`
- **Type**: Python script
- **Description**: Unit tests for prompt lifecycle management scripts including creation, state transitions, completion, and registry updates

**tests/rdd-framework/actions/test_workflow_actions.py**
- **Path**: `repo-root/tests/rdd-framework/actions/test_workflow_actions.py`
- **Type**: Python script
- **Description**: Unit tests for workflow artifact management scripts covering questionnaire, plan, and analysis flag management and file operations

**tests/rdd-framework/actions/test_execution_actions.py**
- **Path**: `repo-root/tests/rdd-framework/actions/test_execution_actions.py`
- **Type**: Python script
- **Description**: Unit tests for implementation and execution management including completion flags, execution tracking, and mode switching

**tests/rdd-framework/actions/test_modification_actions.py**
- **Path**: `repo-root/tests/rdd-framework/actions/test_modification_actions.py`
- **Type**: Python script
- **Description**: Unit tests for modification workflow scripts covering creation, completion, listing, and metadata tracking

**tests/rdd-framework/actions/test_requirement_actions.py**
- **Path**: `repo-root/tests/rdd-framework/actions/test_requirement_actions.py`
- **Type**: Python script
- **Description**: Unit tests for requirement management scripts covering CRUD operations, validation, ID generation, and deletion marking

**tests/rdd-framework/actions/test_workdir_actions.py**
- **Path**: `repo-root/tests/rdd-framework/actions/test_workdir_actions.py`
- **Type**: Python script
- **Description**: Unit tests for working directory and iteration management covering initialization, archiving, and cleanup operations

**tests/rdd-framework/actions/test_misc_actions.py**
- **Path**: `repo-root/tests/rdd-framework/actions/test_misc_actions.py`
- **Type**: Python script
- **Description**: Unit tests for miscellaneous utility scripts including file listing, timestamps, and helper functions

**tests/rdd-framework/config/**
- **Path**: `repo-root/tests/rdd-framework/config/`
- **Type**: Directory
- **Description**: Tests for configuration validation including manifest schema and path verification

**tests/rdd-framework/config/test_manifest_validation.py**
- **Path**: `repo-root/tests/rdd-framework/config/test_manifest_validation.py`
- **Type**: Python script
- **Description**: Tests for manifest.json validation including schema structure, path verification, snippet resolution, and version format validation

**tests/rdd-framework/integration/**
- **Path**: `repo-root/tests/rdd-framework/integration/`
- **Type**: Directory
- **Description**: End-to-end integration tests validating complete workflows using temporary .rdd-instance-test/ directory

**tests/rdd-framework/integration/test_prompt_lifecycle.py**
- **Path**: `repo-root/tests/rdd-framework/integration/test_prompt_lifecycle.py`
- **Type**: Python script
- **Description**: End-to-end integration tests validating complete prompt lifecycle workflows from creation through completion including questionnaire, plan, and implementation phases

**tests/rdd-framework/integration/test_requirement_workflows.py**
- **Path**: `repo-root/tests/rdd-framework/integration/test_requirement_workflows.py`
- **Type**: Python script
- **Description**: Integration tests for requirement management workflows covering CRUD operations, validation, and ID sequencing with real file manipulation

**tests/rdd-framework/integration/test_iteration_archive.py**
- **Path**: `repo-root/tests/rdd-framework/integration/test_iteration_archive.py`
- **Type**: Python script
- **Description**: Integration tests for iteration archiving covering complete workflows from active development through archiving and cleanup

**tests/fixtures/rdd-framework/**
- **Path**: `repo-root/tests/fixtures/rdd-framework/`
- **Type**: Directory
- **Description**: Test fixtures for RDD framework tests organized with realistic but minimal data sets

**tests/fixtures/rdd-framework/sample-registry.json**
- **Path**: `repo-root/tests/fixtures/rdd-framework/sample-registry.json`
- **Type**: JSON file
- **Description**: Sample work-iteration-registry with varied prompt states for testing

**tests/fixtures/rdd-framework/sample-requirements.md**
- **Path**: `repo-root/tests/fixtures/rdd-framework/sample-requirements.md`
- **Type**: Markdown file
- **Description**: Sample requirements file for requirement management tests

**tests/fixtures/rdd-framework/sample-manifest.json**
- **Path**: `repo-root/tests/fixtures/rdd-framework/sample-manifest.json`
- **Type**: JSON file
- **Description**: Valid manifest configuration for validation tests

**tests/fixtures/rdd-framework/README.md**
- **Path**: `repo-root/tests/fixtures/rdd-framework/README.md`
- **Type**: Markdown file
- **Description**: Documentation of fixture purpose, structure, and usage guidelines

### Entries to Modify

**scripts/run-tests.py**
- **Current Description**: "Cross-platform test runner for RDD Framework that runs all platform-appropriate tests"
- **New Description**: "Cross-platform test runner for RDD Framework with selective execution support via flags (--rdd-framework, --actions, --config, --integration, --quick) and coverage reporting, defaulting to run all tests for CI/CD compatibility"

**scripts/setup-test-env.py**
- **Current Description**: "Setup script for creating or updating RDD test environment and installing test dependencies"
- **New Description**: "Setup script for creating or updating RDD test environment and installing test dependencies including pytest, pytest-cov, and pytest-mock in dedicated virtual environment"

### Entries to Delete

**tests/python/conftest.py** - Remove (obsolete test)
**tests/python/test_integration.py** - Remove (obsolete test)
**tests/python/test_rdd_main.py** - Remove (obsolete test)
**tests/python/test_rdd_utils.py** - Remove (obsolete test)
**tests/python/test_seed.py** - Remove (obsolete test)

## Summary

This plan provides a systematic approach to implementing comprehensive test coverage for the RDD framework core:

1. **Steps 1-2**: Clean up obsolete tests and create new structure
2. **Steps 3-4**: Setup dependencies and shared fixtures
3. **Steps 5-11**: Implement action script unit tests (prioritized for 80% coverage)
4. **Step 12**: Implement configuration validation tests
5. **Steps 13-15**: Implement integration tests for critical workflows
6. **Steps 16-17**: Enhance test infrastructure for selective execution
7. **Step 18**: Organize test fixtures
8. **Steps 19-20**: Update documentation and validate complete suite

All requirements from the active prompt and questionnaire answers are covered by this plan, ensuring compliance with framework conventions and maintaining CI/CD compatibility.
