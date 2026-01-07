%%PROMPT P-001 "Files view activated from icons"
On "Active Prompt" page, The user could press the execution-mode buttons by mistake while they intend to see the respective file. Instead of having tabs for showing the different files on one place and execution-mode buttons on another, they need to be united in same place on the page. I want the buttons ("Clarity", "Analyze", "Plan", "Implement", "Modifications") under the status icons to be used to show the respective file. Same placeholder where the prompt.md is shown should be reused for the other files (be sure it is the same placeholder as now in some situations several files appear one after another). 

This means the current "No Action" button to be titled "Prompt" and when clicked to show the prompt.md. The "Clarify" button to be titled "Questionnaire" and to show questionnaire.md file of the active prompt. Respectively Analyze -> Analysys to show analysis.md, Plan -> Plan to show plan.md, Implement -> Implementation to show implementation.md. Modification should show a Modifications list as in the modal. 

The current functionality of these buttons - to set execution-mode - should be realized with a new radio button group with labels equal to the current buttons - "Clarify", "Analyze", "Plan", "Implement". The status icon, the file button and the radio for execution-mode setting should be visually grouped together in areas. The "No action" should be in the "Prompt" area. The buttons should be disabled when the statuses are not true (this will mean the respective file is not ready).


### Modification 001

Move the new areas in the same place where the buttons were before - between "Create Modification" button and "Copy Execute Cmd) as a centered sub-area
%%ENDPROMPT

%%PROMPT P-002 "UX changes"
[[[ROLE_SOFTWARE_DEVELOPER]]]

Place the Config tab between Requirements and Help
%%ENDPROMPT

%%PROMPT P-003 "Workdir metadata"
Move the area from Workdir tab with Iteration Metadata (the ID, Name) to the title area of the Active Prompt page.
Do not show Total Prompts, Next ID, Git
%%ENDPROMPT

%%PROMPT P-004 "Refreshes stay on same page"
Currently when the page is refreshed - the page goes on the Active Prompt page and shows Prompt. Change so when refresh button is pressed, the current page and file displayed selected stays the same.


### Modification 001

When Questionnaire is opened, when page is refreshed, a message appears that there is no questionnaire file is found, but when I click on the Questionnaire button, the form with questions appears. This is a bug - fix it
%%ENDPROMPT

%%PROMPT P-005 "Archive Iteration"
Move the "Archive Iteration" button to appear in "Active Prompt" header banner only when there is no active prompt. The iteration should not be archived if active prompt execution is in progress.
%%ENDPROMPT

%%PROMPT P-006 "Prompts History tab"
Rename Workdir tab to be named Prompts History


### Modification 001

Check if requirements should be updated because of the prompts in Workdir implemented so far
%%ENDPROMPT

%%PROMPT P-007 "Bug fix - execution-mode"
The radio buttons for execution mode in Active Prompt page should reflect always the value of "execution-mode" entry in `.rdd-instance/workdir/work-iteration-registry.json`. Every refresh of the statuses of the files in Active Prompt should include radio buttons update as well.
%%ENDPROMPT

%%PROMPT P-008 "Delete execution modes"
In the respective cards for execution-modes Clarify, Analyze and Plan in Active Prompt page should be created buttons with icon trash bin which when pressed, deletes the respective file and toggle the status - as if the execution-mode was never executed.

In `.rdd/src/actions` should be created the respective "prompt_*" scripts which to be invoked by the prompt. The prompt should not directly delete the prompt workdir files.
%%ENDPROMPT

%%PROMPT P-009 "Tests"
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
%%ENDPROMPT
