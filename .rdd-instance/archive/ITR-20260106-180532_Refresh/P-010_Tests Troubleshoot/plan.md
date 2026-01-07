# Plan for Tests Troubleshoot

## Test Failure Analysis

The GitHub Actions test run shows 13 test failures across three categories:

### 1. Build and Install Test Module Import Failures (2 failures)
- `tests/build/test_build.py` - ModuleNotFoundError: No module named 'build'
- `tests/install/test_install.py` - ModuleNotFoundError: No module named 'install'

### 2. Manifest and Configuration Test Failures (5 failures)
- `test_parse_params_from_argv` - Assertion failure expecting 'title ' key with space
- `test_manifest_has_required_paths` - Missing 'rddInstance' key in manifest
- `test_manifest_has_prompt_snippets` - promptSnippets expected to be dict but is list
- `test_manifest_prompt_snippet_files_exist` - AttributeError: list has no 'items' method
- `test_technical_design_form_structure` - JSONDecodeError reading empty technical-design.json

### 3. Integration Test Failures (6 failures)
- `test_archive_creates_proper_structure` - Archive folder not created
- `test_full_prompt_lifecycle` - Work iteration registry not found
- `test_create_multiple_prompts_enforces_single_active` - Work iteration registry not found
- `test_modification_lifecycle` - Work iteration registry not found
- `test_bidirectional_state_transitions` - Work iteration registry not found
- `test_create_modify_delete_ur` - Requirement not created
- `test_create_modify_delete_tr` - Requirement not created
- `test_sequential_ur_ids` - Requirement not created

## Root Cause Analysis

### Issue 1: Build and Install Module Imports
The test files are trying to import modules named 'build' and 'install' which don't exist. These tests are trying to import the actual build.py and install scripts but they are not structured as Python modules. The tests should either:
- Import from the actual file locations using sys.path manipulation
- Or the build/install scripts should be refactored into proper modules

### Issue 2: Manifest Schema Changes
The tests expect an old manifest schema structure ('rddInstance' key, promptSnippets as dict) but the actual manifest has been updated to a new structure with 'canonicalRoots' and promptSnippets as an array. The tests need to be updated to match the current manifest schema.

### Issue 3: Technical Design Empty File
The test expects a valid JSON in technical-design.json but the file is empty. This is likely intentional for new instances, but the test should handle this gracefully.

### Issue 4: Integration Tests Missing Workdir Setup
Integration tests are failing because they don't properly set up the workdir structure (.rdd-instance/workdir/work-iteration-registry.json) before running. The conftest.py fixtures need enhancement.

### Issue 5: Parameter Parsing Test Expecting Wrong Behavior
The test `test_parse_params_from_argv` expects the key to include a trailing space ('title ') but the actual implementation correctly trims the key. The test assertion is wrong.

## Implementation Steps

### Step 1: Fix Build and Install Test Import Issues
**Action**: Update `tests/build/test_build.py` and `tests/install/test_install.py` to properly import the build and install scripts.

**Details**: 
- Instead of `import build`, use `sys.path` manipulation to add the build directory to the path and import the module, or use `importlib` to load the module from the file path
- Similarly fix the install test
- Alternatively, restructure build.py and any install scripts as proper Python packages

### Step 2: Update Manifest Validation Tests to Match Current Schema
**Action**: Update all failing tests in `tests/rdd-framework/config/test_manifest_validation.py` to match the current manifest.json structure.

**Details**:
- Remove or update the test checking for 'rddInstance' key to check for 'canonicalRoots' instead
- Update `test_manifest_has_prompt_snippets` to expect a list instead of dict
- Update `test_manifest_prompt_snippet_files_exist` to iterate over the list structure using array iteration instead of dict.items()
- Verify all assertions match the actual manifest.json structure

### Step 3: Fix Technical Design Form Structure Test
**Action**: Update `test_technical_design_form_structure` to handle empty technical-design.json files gracefully.

**Details**:
- Check if file is empty before attempting JSON parse
- Either skip the test if empty, or validate against an expected empty/default structure
- Alternatively, create a minimal valid JSON structure for testing

### Step 4: Fix Parameter Parsing Test Assertion
**Action**: Fix the assertion in `test_parse_params_from_argv` test.

**Details**:
- Change `assert "title " in params` to `assert "title" in params` (without trailing space)
- Verify the expected behavior - keys should be trimmed, not preserved with spaces
- Update test to reflect correct implementation behavior

### Step 5: Enhance Integration Test Fixtures for Workdir Setup
**Action**: Update `tests/rdd-framework/conftest.py` to properly initialize workdir structure for integration tests.

**Details**:
- Ensure integration test fixtures create the required `.rdd-instance/workdir/` directory structure
- Create a minimal valid `work-iteration-registry.json` file with proper schema
- Initialize empty prompts array and proper iteration metadata
- Ensure archive directory exists when testing archive functionality

### Step 6: Fix Requirement Creation in Integration Tests
**Action**: Debug why requirement creation commands are not working in integration tests.

**Details**:
- Verify the requirement creation scripts are being called correctly
- Check if the requirements.md file is properly initialized in test fixtures
- Ensure the file has the required section headers (## User Requirements, ## Technical Requirements)
- Verify script paths and execution permissions

### Step 7: Verify Archive Folder Creation Logic
**Action**: Investigate the archive creation logic to ensure proper folder structure.

**Details**:
- Review the archive action script to ensure it creates folders with correct naming
- Verify path construction in the test matches actual behavior
- Check for any path separator or naming convention issues

## Requirements Updates

After implementation is complete, the following requirement updates should be made:

### New Technical Requirements to Add:

**TR-XXXX**: The system test suite shall properly import and test build and install scripts using appropriate Python import mechanisms.

**TR-XXXX**: The system test suite shall validate the manifest.json schema against the current structure including canonicalRoots and promptSnippets as an array.

**TR-XXXX**: The system test suite shall gracefully handle empty specification files during testing.

**TR-XXXX**: The system integration test fixtures shall initialize complete workdir structure including work-iteration-registry.json with valid schema.

**TR-XXXX**: The system requirement creation tests shall properly initialize requirements.md template files with required section headers.

### Requirement Creation Commands:

```bash
python .rdd/src/actions/requirement_tr_create.py text="The system test suite shall properly import and test build and install scripts using appropriate Python import mechanisms."

python .rdd/src/actions/requirement_tr_create.py text="The system test suite shall validate the manifest.json schema against the current structure including canonicalRoots and promptSnippets as an array."

python .rdd/src/actions/requirement_tr_create.py text="The system test suite shall gracefully handle empty specification files during testing."

python .rdd/src/actions/requirement_tr_create.py text="The system integration test fixtures shall initialize complete workdir structure including work-iteration-registry.json with valid schema."

python .rdd/src/actions/requirement_tr_create.py text="The system requirement creation tests shall properly initialize requirements.md template files with required section headers."
```

## Specification Updates

No updates needed for technical-design.json at this time.

Update files-and-folders.md to ensure test fixture initialization is documented if it's not already covered.

## Success Criteria

All tests should pass:
- Build tests: 0 errors
- Install tests: 0 errors  
- RDD framework tests: 73 passed, 0 failed
- Total test suites: 3 passed, 0 failed

Coverage should remain at or above 65%.
