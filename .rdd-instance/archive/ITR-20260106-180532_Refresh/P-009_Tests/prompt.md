# Test Coverage Enhancement for RDD Framework Core

## Context

The RDD framework has existing test infrastructure for build, install, and some Python modules. 
However, the core framework components in the `.rdd/` directory lack comprehensive test coverage.

Current state:
- Existing tests in `tests/build/`, `tests/install/`, `tests/python/` 
- Parts from the tests are missing. Some tests are obsolete and not valid anymore. 
- GitHub workflow `.github/workflows/tests.yml` is functional (preserve)
- Test runners `scripts/run-tests.py` and `scripts/setup-test-env.py` exist (enhance, don't recreate)
- It is OK to replace all the tests - a lot of the code was changed as building a new version and there is no user impact yet.

## Objective

Add comprehensive test coverage for RDD framework core components while preserving existing 
working tests and infrastructure.

## Scope

Create new tests which should cover the whole RDD functionality in .rdd folder - scripts, manifest, prompts. 
Create new tests in `tests/rdd-framework/` covering:

1. **Action Scripts** (`.rdd/src/actions/*.py`):
   - Prompt management: create, state transitions, completion
   - Modification workflows
   - Requirement CRUD operations (create, modify, delete)
   - Execution mode management
   - Questionnaire/plan/analysis generation markers
   - JSON schema validation

2. **Configuration Validation**:
   - `manifest.json` schema validation
   - Verify all referenced paths exist
   - Test prompt snippet key resolution
   - Framework version extraction

3. **Integration Workflows**:
   - End-to-end prompt lifecycle (create → questionnaire → plan → implement → complete)
   - Modification creation and completion
   - Iteration archiving
   - Requirement auto-updates during execution

You should recreate `scripts/run-tests.py` and `scripts/setup-test-env.py`. 

## Test Approach

- **Unit tests**: Action scripts with mocked filesystem (fast, isolated)
- **Integration tests**: Critical workflows with temporary .rdd-instance-test/
- **Coverage target**: 80% minimum for action scripts and core modules

## Enhancements to Existing Infrastructure

Enhance `scripts/run-tests.py` to support selective execution:
- `--rdd-framework`: Run only new RDD framework tests
- `--actions`: Run only action script tests
- `--integration`: Run only integration tests
- `--quick`: Skip slow integration tests
- (default): Run all tests (for CI/CD)

Add coverage enforcement:
- Fail if coverage < 80% for `.rdd/src/actions/` and `.rdd/src/web/server.py`
- Generate both terminal and XML reports
- Maintain Codecov upload in CI/CD

## Constraints

- Do NOT modify `.github/workflows/tests.yml` unless adding new test categories
- Preserve CI/CD compatibility
- Test fixtures shall be organized in tests/fixtures/ with subdirectories by test category, using realistic but minimal data sets to reduce maintenance burden.

## Success Criteria

1. All action scripts in `.rdd/src/actions/` have ≥80% test coverage
2. Manifest validation tests pass with existing manifest.json
3. Integration tests validate full prompt → completion workflow
4. All tests pass in CI/CD on both Linux and Windows
5. Test runner supports selective execution flags
6. Existing tests continue to pass unchanged
7. All test files shall include a module-level docstring describing the component under test, key test scenarios covered, and any special setup requirements.

## Additional considerations

- Component scope: Action scripts + Manifest + Config validation
- Organization: Hybrid - tests/rdd-framework/ with component subdirs 
- Testing approach: Unit tests with heavy mocking 
- Selective execution: Support component/type flags 
- Coverage target: 80% industry standard 
- Manifest validation: Full - schema + path verification 