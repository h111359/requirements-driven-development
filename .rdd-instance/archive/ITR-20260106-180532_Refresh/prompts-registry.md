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

%%PROMPT P-010 "Tests Troubleshoot"
This is the test log from pull request to merge to DEV branch (executing .github/workflows/tests.yml). Find the issues and fix them:

2026-01-07T05:35:38.0826297Z Current runner version: '2.330.0'
2026-01-07T05:35:38.0851641Z ##[group]Runner Image Provisioner
2026-01-07T05:35:38.0852446Z Hosted Compute Agent
2026-01-07T05:35:38.0852969Z Version: 20251211.462
2026-01-07T05:35:38.0853654Z Commit: 6cbad8c2bb55d58165063d031ccabf57e2d2db61
2026-01-07T05:35:38.0854316Z Build Date: 2025-12-11T16:28:49Z
2026-01-07T05:35:38.0855011Z Worker ID: {e05a02e0-ec14-4344-b495-c90ecbb91e85}
2026-01-07T05:35:38.0855735Z ##[endgroup]
2026-01-07T05:35:38.0856228Z ##[group]Operating System
2026-01-07T05:35:38.0856788Z Ubuntu
2026-01-07T05:35:38.0857256Z 24.04.3
2026-01-07T05:35:38.0857732Z LTS
2026-01-07T05:35:38.0858187Z ##[endgroup]
2026-01-07T05:35:38.0858720Z ##[group]Runner Image
2026-01-07T05:35:38.0859248Z Image: ubuntu-24.04
2026-01-07T05:35:38.0859754Z Version: 20251215.174.1
2026-01-07T05:35:38.0861002Z Included Software: https://github.com/actions/runner-images/blob/ubuntu24/20251215.174/images/ubuntu/Ubuntu2404-Readme.md
2026-01-07T05:35:38.0862544Z Image Release: https://github.com/actions/runner-images/releases/tag/ubuntu24%2F20251215.174
2026-01-07T05:35:38.0863574Z ##[endgroup]
2026-01-07T05:35:38.0864616Z ##[group]GITHUB_TOKEN Permissions
2026-01-07T05:35:38.0866546Z Contents: read
2026-01-07T05:35:38.0867155Z Metadata: read
2026-01-07T05:35:38.0867636Z Packages: read
2026-01-07T05:35:38.0868213Z ##[endgroup]
2026-01-07T05:35:38.0870446Z Secret source: Actions
2026-01-07T05:35:38.0871498Z Prepare workflow directory
2026-01-07T05:35:38.1196570Z Prepare all required actions
2026-01-07T05:35:38.1234737Z Getting action download info
2026-01-07T05:35:38.4552287Z Download action repository 'actions/checkout@v4' (SHA:34e114876b0b11c390a56381ad16ebd13914f8d5)
2026-01-07T05:35:38.7432856Z Download action repository 'actions/setup-python@v5' (SHA:a26af69be951a213d495a4c3e4e4022e16d87065)
2026-01-07T05:35:38.8264329Z Download action repository 'codecov/codecov-action@v4' (SHA:b9fd7d16f6d7d1b5d2bec1a2887e65ceed900238)
2026-01-07T05:35:39.1291158Z Complete job name: All Tests (Linux)
2026-01-07T05:35:39.1997183Z ##[group]Run actions/checkout@v4
2026-01-07T05:35:39.1998022Z with:
2026-01-07T05:35:39.1998502Z   repository: h111359/requirements-driven-development
2026-01-07T05:35:39.1999267Z   token: ***
2026-01-07T05:35:39.1999641Z   ssh-strict: true
2026-01-07T05:35:39.2000023Z   ssh-user: git
2026-01-07T05:35:39.2000418Z   persist-credentials: true
2026-01-07T05:35:39.2001269Z   clean: true
2026-01-07T05:35:39.2001669Z   sparse-checkout-cone-mode: true
2026-01-07T05:35:39.2002147Z   fetch-depth: 1
2026-01-07T05:35:39.2002521Z   fetch-tags: false
2026-01-07T05:35:39.2002907Z   show-progress: true
2026-01-07T05:35:39.2003300Z   lfs: false
2026-01-07T05:35:39.2003662Z   submodules: false
2026-01-07T05:35:39.2004057Z   set-safe-directory: true
2026-01-07T05:35:39.2004806Z ##[endgroup]
2026-01-07T05:35:39.3107045Z Syncing repository: h111359/requirements-driven-development
2026-01-07T05:35:39.3108807Z ##[group]Getting Git version info
2026-01-07T05:35:39.3109840Z Working directory is '/home/runner/work/requirements-driven-development/requirements-driven-development'
2026-01-07T05:35:39.3111476Z [command]/usr/bin/git version
2026-01-07T05:35:39.3187757Z git version 2.52.0
2026-01-07T05:35:39.3214891Z ##[endgroup]
2026-01-07T05:35:39.3230345Z Temporarily overriding HOME='/home/runner/work/_temp/57cfdc60-2147-4f8d-986a-8bfff4a1c274' before making global git config changes
2026-01-07T05:35:39.3232063Z Adding repository directory to the temporary git global config as a safe directory
2026-01-07T05:35:39.3236463Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/requirements-driven-development/requirements-driven-development
2026-01-07T05:35:39.3276773Z Deleting the contents of '/home/runner/work/requirements-driven-development/requirements-driven-development'
2026-01-07T05:35:39.3280304Z ##[group]Initializing the repository
2026-01-07T05:35:39.3285221Z [command]/usr/bin/git init /home/runner/work/requirements-driven-development/requirements-driven-development
2026-01-07T05:35:39.3377481Z hint: Using 'master' as the name for the initial branch. This default branch name
2026-01-07T05:35:39.3379277Z hint: will change to "main" in Git 3.0. To configure the initial branch name
2026-01-07T05:35:39.3381011Z hint: to use in all of your new repositories, which will suppress this warning,
2026-01-07T05:35:39.3382134Z hint: call:
2026-01-07T05:35:39.3382688Z hint:
2026-01-07T05:35:39.3383428Z hint: 	git config --global init.defaultBranch <name>
2026-01-07T05:35:39.3384079Z hint:
2026-01-07T05:35:39.3384679Z hint: Names commonly chosen instead of 'master' are 'main', 'trunk' and
2026-01-07T05:35:39.3385541Z hint: 'development'. The just-created branch can be renamed via this command:
2026-01-07T05:35:39.3386220Z hint:
2026-01-07T05:35:39.3386590Z hint: 	git branch -m <name>
2026-01-07T05:35:39.3387014Z hint:
2026-01-07T05:35:39.3387582Z hint: Disable this message with "git config set advice.defaultBranchName false"
2026-01-07T05:35:39.3389442Z Initialized empty Git repository in /home/runner/work/requirements-driven-development/requirements-driven-development/.git/
2026-01-07T05:35:39.3395285Z [command]/usr/bin/git remote add origin https://github.com/h111359/requirements-driven-development
2026-01-07T05:35:39.3430462Z ##[endgroup]
2026-01-07T05:35:39.3431774Z ##[group]Disabling automatic garbage collection
2026-01-07T05:35:39.3434752Z [command]/usr/bin/git config --local gc.auto 0
2026-01-07T05:35:39.3464351Z ##[endgroup]
2026-01-07T05:35:39.3465353Z ##[group]Setting up auth
2026-01-07T05:35:39.3471249Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-01-07T05:35:39.3501564Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-01-07T05:35:39.3820180Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-01-07T05:35:39.3851056Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'http\.https\:\/\/github\.com\/\.extraheader' && git config --local --unset-all 'http.https://github.com/.extraheader' || :"
2026-01-07T05:35:39.4076864Z [command]/usr/bin/git config --local --name-only --get-regexp ^includeIf\.gitdir:
2026-01-07T05:35:39.4118359Z [command]/usr/bin/git submodule foreach --recursive git config --local --show-origin --name-only --get-regexp remote.origin.url
2026-01-07T05:35:39.4347996Z [command]/usr/bin/git config --local http.https://github.com/.extraheader AUTHORIZATION: basic ***
2026-01-07T05:35:39.4383830Z ##[endgroup]
2026-01-07T05:35:39.4385071Z ##[group]Fetching the repository
2026-01-07T05:35:39.4394239Z [command]/usr/bin/git -c protocol.version=2 fetch --no-tags --prune --no-recurse-submodules --depth=1 origin +7960fb0144dfb47d8a157124e80bba65ce05e7a4:refs/remotes/pull/81/merge
2026-01-07T05:35:39.8031441Z From https://github.com/h111359/requirements-driven-development
2026-01-07T05:35:39.8035007Z  * [new ref]         7960fb0144dfb47d8a157124e80bba65ce05e7a4 -> pull/81/merge
2026-01-07T05:35:39.8065661Z ##[endgroup]
2026-01-07T05:35:39.8066622Z ##[group]Determining the checkout info
2026-01-07T05:35:39.8068206Z ##[endgroup]
2026-01-07T05:35:39.8073087Z [command]/usr/bin/git sparse-checkout disable
2026-01-07T05:35:39.8115573Z [command]/usr/bin/git config --local --unset-all extensions.worktreeConfig
2026-01-07T05:35:39.8144729Z ##[group]Checking out the ref
2026-01-07T05:35:39.8148120Z [command]/usr/bin/git checkout --progress --force refs/remotes/pull/81/merge
2026-01-07T05:35:39.8607243Z Note: switching to 'refs/remotes/pull/81/merge'.
2026-01-07T05:35:39.8608240Z 
2026-01-07T05:35:39.8609009Z You are in 'detached HEAD' state. You can look around, make experimental
2026-01-07T05:35:39.8611230Z changes and commit them, and you can discard any commits you make in this
2026-01-07T05:35:39.8613551Z state without impacting any branches by switching back to a branch.
2026-01-07T05:35:39.8615066Z 
2026-01-07T05:35:39.8616017Z If you want to create a new branch to retain commits you create, you may
2026-01-07T05:35:39.8618702Z do so (now or later) by using -c with the switch command. Example:
2026-01-07T05:35:39.8620041Z 
2026-01-07T05:35:39.8620846Z   git switch -c <new-branch-name>
2026-01-07T05:35:39.8621798Z 
2026-01-07T05:35:39.8622305Z Or undo this operation with:
2026-01-07T05:35:39.8623118Z 
2026-01-07T05:35:39.8623514Z   git switch -
2026-01-07T05:35:39.8624202Z 
2026-01-07T05:35:39.8625426Z Turn off this advice by setting config variable advice.detachedHead to false
2026-01-07T05:35:39.8627154Z 
2026-01-07T05:35:39.8628999Z HEAD is now at 7960fb0 Merge 3c74563356a143f3290d599d7a2bb1b644da720f into 9b7421448c99d223f451bd96adab6acbaa6756fd
2026-01-07T05:35:39.8634612Z ##[endgroup]
2026-01-07T05:35:39.8664828Z [command]/usr/bin/git log -1 --format=%H
2026-01-07T05:35:39.8689311Z 7960fb0144dfb47d8a157124e80bba65ce05e7a4
2026-01-07T05:35:39.9013931Z ##[group]Run actions/setup-python@v5
2026-01-07T05:35:39.9015015Z with:
2026-01-07T05:35:39.9015730Z   python-version: 3.9
2026-01-07T05:35:39.9016571Z   check-latest: false
2026-01-07T05:35:39.9017721Z   token: ***
2026-01-07T05:35:39.9018478Z   update-environment: true
2026-01-07T05:35:39.9019416Z   allow-prereleases: false
2026-01-07T05:35:39.9020339Z   freethreaded: false
2026-01-07T05:35:39.9021329Z ##[endgroup]
2026-01-07T05:35:40.0866209Z ##[group]Installed versions
2026-01-07T05:35:40.0978859Z Successfully set up CPython (3.9.25)
2026-01-07T05:35:40.0981683Z ##[endgroup]
2026-01-07T05:35:40.1223120Z ##[group]Run sudo apt-get update
2026-01-07T05:35:40.1224615Z [36;1msudo apt-get update[0m
2026-01-07T05:35:40.1225931Z [36;1msudo apt-get install -y bats[0m
2026-01-07T05:35:40.1275189Z shell: /usr/bin/bash -e {0}
2026-01-07T05:35:40.1276067Z env:
2026-01-07T05:35:40.1276928Z   pythonLocation: /opt/hostedtoolcache/Python/3.9.25/x64
2026-01-07T05:35:40.1278535Z   PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.9.25/x64/lib/pkgconfig
2026-01-07T05:35:40.1280116Z   Python_ROOT_DIR: /opt/hostedtoolcache/Python/3.9.25/x64
2026-01-07T05:35:40.1281729Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.9.25/x64
2026-01-07T05:35:40.1283154Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.9.25/x64
2026-01-07T05:35:40.1284603Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.9.25/x64/lib
2026-01-07T05:35:40.1285808Z ##[endgroup]
2026-01-07T05:35:40.2077605Z Get:1 file:/etc/apt/apt-mirrors.txt Mirrorlist [144 B]
2026-01-07T05:35:40.2389018Z Hit:2 http://azure.archive.ubuntu.com/ubuntu noble InRelease
2026-01-07T05:35:40.2410398Z Hit:6 https://packages.microsoft.com/repos/azure-cli noble InRelease
2026-01-07T05:35:40.2421064Z Get:3 http://azure.archive.ubuntu.com/ubuntu noble-updates InRelease [126 kB]
2026-01-07T05:35:40.2483518Z Get:4 http://azure.archive.ubuntu.com/ubuntu noble-backports InRelease [126 kB]
2026-01-07T05:35:40.2488493Z Get:7 https://packages.microsoft.com/ubuntu/24.04/prod noble InRelease [3600 B]
2026-01-07T05:35:40.2511741Z Get:5 http://azure.archive.ubuntu.com/ubuntu noble-security InRelease [126 kB]
2026-01-07T05:35:40.4037331Z Get:8 http://azure.archive.ubuntu.com/ubuntu noble-updates/main amd64 Packages [1684 kB]
2026-01-07T05:35:40.4246063Z Get:9 http://azure.archive.ubuntu.com/ubuntu noble-updates/main Translation-en [311 kB]
2026-01-07T05:35:40.4274820Z Get:10 http://azure.archive.ubuntu.com/ubuntu noble-updates/main amd64 Components [175 kB]
2026-01-07T05:35:40.4298294Z Get:11 http://azure.archive.ubuntu.com/ubuntu noble-updates/main amd64 c-n-f Metadata [15.8 kB]
2026-01-07T05:35:40.4317548Z Get:12 http://azure.archive.ubuntu.com/ubuntu noble-updates/universe amd64 Packages [1506 kB]
2026-01-07T05:35:40.4416277Z Get:13 http://azure.archive.ubuntu.com/ubuntu noble-updates/universe Translation-en [306 kB]
2026-01-07T05:35:40.4448226Z Get:14 http://azure.archive.ubuntu.com/ubuntu noble-updates/universe amd64 Components [377 kB]
2026-01-07T05:35:40.4479311Z Get:15 http://azure.archive.ubuntu.com/ubuntu noble-updates/universe amd64 c-n-f Metadata [31.4 kB]
2026-01-07T05:35:40.4498826Z Get:16 http://azure.archive.ubuntu.com/ubuntu noble-updates/restricted amd64 Packages [2413 kB]
2026-01-07T05:35:40.4581245Z Get:24 https://packages.microsoft.com/ubuntu/24.04/prod noble/main amd64 Packages [77.7 kB]
2026-01-07T05:35:40.4645978Z Get:17 http://azure.archive.ubuntu.com/ubuntu noble-updates/restricted Translation-en [550 kB]
2026-01-07T05:35:40.4679400Z Get:25 https://packages.microsoft.com/ubuntu/24.04/prod noble/main armhf Packages [11.4 kB]
2026-01-07T05:35:40.4723862Z Get:26 https://packages.microsoft.com/ubuntu/24.04/prod noble/main arm64 Packages [59.3 kB]
2026-01-07T05:35:40.5146215Z Get:18 http://azure.archive.ubuntu.com/ubuntu noble-updates/restricted amd64 Components [212 B]
2026-01-07T05:35:40.5160068Z Get:19 http://azure.archive.ubuntu.com/ubuntu noble-updates/restricted amd64 c-n-f Metadata [516 B]
2026-01-07T05:35:40.5170497Z Get:20 http://azure.archive.ubuntu.com/ubuntu noble-updates/multiverse amd64 Packages [30.3 kB]
2026-01-07T05:35:40.5197697Z Get:21 http://azure.archive.ubuntu.com/ubuntu noble-updates/multiverse Translation-en [6048 B]
2026-01-07T05:35:40.5210992Z Get:22 http://azure.archive.ubuntu.com/ubuntu noble-updates/multiverse amd64 Components [940 B]
2026-01-07T05:35:40.5231237Z Get:23 http://azure.archive.ubuntu.com/ubuntu noble-updates/multiverse amd64 c-n-f Metadata [488 B]
2026-01-07T05:35:40.5252435Z Get:27 http://azure.archive.ubuntu.com/ubuntu noble-backports/main amd64 Packages [40.4 kB]
2026-01-07T05:35:40.5284754Z Get:28 http://azure.archive.ubuntu.com/ubuntu noble-backports/main amd64 Components [7284 B]
2026-01-07T05:35:40.5294130Z Get:29 http://azure.archive.ubuntu.com/ubuntu noble-backports/main amd64 c-n-f Metadata [368 B]
2026-01-07T05:35:40.5305505Z Get:30 http://azure.archive.ubuntu.com/ubuntu noble-backports/universe amd64 Packages [29.5 kB]
2026-01-07T05:35:40.5329878Z Get:31 http://azure.archive.ubuntu.com/ubuntu noble-backports/universe Translation-en [17.9 kB]
2026-01-07T05:35:40.5343399Z Get:32 http://azure.archive.ubuntu.com/ubuntu noble-backports/universe amd64 Components [10.5 kB]
2026-01-07T05:35:40.5364645Z Get:33 http://azure.archive.ubuntu.com/ubuntu noble-backports/universe amd64 c-n-f Metadata [1444 B]
2026-01-07T05:35:40.5385827Z Get:34 http://azure.archive.ubuntu.com/ubuntu noble-backports/restricted amd64 Components [216 B]
2026-01-07T05:35:40.5851687Z Get:35 http://azure.archive.ubuntu.com/ubuntu noble-backports/multiverse amd64 Components [212 B]
2026-01-07T05:35:40.5871865Z Get:36 http://azure.archive.ubuntu.com/ubuntu noble-security/main amd64 Packages [1391 kB]
2026-01-07T05:35:40.5975849Z Get:37 http://azure.archive.ubuntu.com/ubuntu noble-security/main Translation-en [225 kB]
2026-01-07T05:35:40.5999996Z Get:38 http://azure.archive.ubuntu.com/ubuntu noble-security/main amd64 Components [21.5 kB]
2026-01-07T05:35:40.6014311Z Get:39 http://azure.archive.ubuntu.com/ubuntu noble-security/main amd64 c-n-f Metadata [9504 B]
2026-01-07T05:35:40.6028403Z Get:40 http://azure.archive.ubuntu.com/ubuntu noble-security/universe amd64 Packages [916 kB]
2026-01-07T05:35:40.6094361Z Get:41 http://azure.archive.ubuntu.com/ubuntu noble-security/universe amd64 Components [71.4 kB]
2026-01-07T05:35:40.6117416Z Get:42 http://azure.archive.ubuntu.com/ubuntu noble-security/universe amd64 c-n-f Metadata [19.4 kB]
2026-01-07T05:35:40.6136512Z Get:43 http://azure.archive.ubuntu.com/ubuntu noble-security/restricted amd64 Components [208 B]
2026-01-07T05:35:40.6142552Z Get:44 http://azure.archive.ubuntu.com/ubuntu noble-security/multiverse amd64 Components [212 B]
2026-01-07T05:35:49.2872728Z Fetched 10.7 MB in 1s (8264 kB/s)
2026-01-07T05:35:50.1093574Z Reading package lists...
2026-01-07T05:35:50.1429168Z Reading package lists...
2026-01-07T05:35:50.3460285Z Building dependency tree...
2026-01-07T05:35:50.3468661Z Reading state information...
2026-01-07T05:35:50.5369922Z The following NEW packages will be installed:
2026-01-07T05:35:50.5378697Z   bats
2026-01-07T05:35:50.5563170Z 0 upgraded, 1 newly installed, 0 to remove and 69 not upgraded.
2026-01-07T05:35:50.5564386Z Need to get 45.5 kB of archives.
2026-01-07T05:35:50.5564735Z After this operation, 166 kB of additional disk space will be used.
2026-01-07T05:35:50.5565157Z Get:1 file:/etc/apt/apt-mirrors.txt Mirrorlist [144 B]
2026-01-07T05:35:50.5847328Z Get:2 http://azure.archive.ubuntu.com/ubuntu noble/universe amd64 bats all 1.10.0-1 [45.5 kB]
2026-01-07T05:35:50.8561746Z Fetched 45.5 kB in 0s (1106 kB/s)
2026-01-07T05:35:50.8777480Z Selecting previously unselected package bats.
2026-01-07T05:35:50.9025980Z (Reading database ... 
2026-01-07T05:35:50.9026493Z (Reading database ... 5%
2026-01-07T05:35:50.9026887Z (Reading database ... 10%
2026-01-07T05:35:50.9027275Z (Reading database ... 15%
2026-01-07T05:35:50.9027636Z (Reading database ... 20%
2026-01-07T05:35:50.9028027Z (Reading database ... 25%
2026-01-07T05:35:50.9029510Z (Reading database ... 30%
2026-01-07T05:35:50.9029959Z (Reading database ... 35%
2026-01-07T05:35:50.9030323Z (Reading database ... 40%
2026-01-07T05:35:50.9030981Z (Reading database ... 45%
2026-01-07T05:35:50.9031436Z (Reading database ... 50%
2026-01-07T05:35:50.9104923Z (Reading database ... 55%
2026-01-07T05:35:51.0304445Z (Reading database ... 60%
2026-01-07T05:35:51.1384501Z (Reading database ... 65%
2026-01-07T05:35:51.1953039Z (Reading database ... 70%
2026-01-07T05:35:51.2920129Z (Reading database ... 75%
2026-01-07T05:35:51.4874952Z (Reading database ... 80%
2026-01-07T05:35:51.6753496Z (Reading database ... 85%
2026-01-07T05:35:51.9095964Z (Reading database ... 90%
2026-01-07T05:35:52.0744379Z (Reading database ... 95%
2026-01-07T05:35:52.0744702Z (Reading database ... 100%
2026-01-07T05:35:52.0745076Z (Reading database ... 217374 files and directories currently installed.)
2026-01-07T05:35:52.0792526Z Preparing to unpack .../archives/bats_1.10.0-1_all.deb ...
2026-01-07T05:35:52.0819239Z Unpacking bats (1.10.0-1) ...
2026-01-07T05:35:52.1345524Z Setting up bats (1.10.0-1) ...
2026-01-07T05:35:52.1407194Z Processing triggers for man-db (2.12.0-4build2) ...
2026-01-07T05:35:52.1435401Z Not building database; man-db/auto-update is not 'true'.
2026-01-07T05:35:52.7791639Z 
2026-01-07T05:35:52.7792147Z Running kernel seems to be up-to-date.
2026-01-07T05:35:52.7792587Z 
2026-01-07T05:35:52.7792730Z No services need to be restarted.
2026-01-07T05:35:52.7792969Z 
2026-01-07T05:35:52.7793106Z No containers need to be restarted.
2026-01-07T05:35:52.7793342Z 
2026-01-07T05:35:52.7793494Z No user sessions are running outdated binaries.
2026-01-07T05:35:52.7793779Z 
2026-01-07T05:35:52.7794075Z No VM guests are running outdated hypervisor (qemu) binaries on this host.
2026-01-07T05:35:53.8060846Z ##[group]Run python scripts/setup-test-env.py
2026-01-07T05:35:53.8061222Z [36;1mpython scripts/setup-test-env.py[0m
2026-01-07T05:35:53.8095666Z shell: /usr/bin/bash -e {0}
2026-01-07T05:35:53.8095897Z env:
2026-01-07T05:35:53.8096141Z   pythonLocation: /opt/hostedtoolcache/Python/3.9.25/x64
2026-01-07T05:35:53.8096544Z   PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.9.25/x64/lib/pkgconfig
2026-01-07T05:35:53.8096935Z   Python_ROOT_DIR: /opt/hostedtoolcache/Python/3.9.25/x64
2026-01-07T05:35:53.8097260Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.9.25/x64
2026-01-07T05:35:53.8097594Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.9.25/x64
2026-01-07T05:35:53.8097918Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.9.25/x64/lib
2026-01-07T05:35:53.8098204Z ##[endgroup]
2026-01-07T05:36:03.7207462Z 
2026-01-07T05:36:03.7207939Z ============================================================
2026-01-07T05:36:03.7208421Z   RDD Test Environment Setup
2026-01-07T05:36:03.7208748Z ============================================================
2026-01-07T05:36:03.7208928Z 
2026-01-07T05:36:03.7209251Z ✓ Python 3.9.25 detected
2026-01-07T05:36:03.7209400Z 
2026-01-07T05:36:03.7209705Z Repository root: /home/runner/work/requirements-driven-development/requirements-driven-development
2026-01-07T05:36:03.7210422Z Virtual environment: /home/runner/work/requirements-driven-development/requirements-driven-development/.venv
2026-01-07T05:36:03.7211919Z Requirements file: /home/runner/work/requirements-driven-development/requirements-driven-development/tests/requirements.txt
2026-01-07T05:36:03.7212403Z 
2026-01-07T05:36:03.7212898Z ℹ Creating virtual environment at /home/runner/work/requirements-driven-development/requirements-driven-development/.venv...
2026-01-07T05:36:03.7213509Z ✓ Virtual environment created
2026-01-07T05:36:03.7213757Z ℹ Upgrading pip...
2026-01-07T05:36:03.7213980Z ✓ pip upgraded
2026-01-07T05:36:03.7214225Z ℹ Installing/updating test dependencies...
2026-01-07T05:36:03.7214549Z ✓ Test dependencies installed/updated
2026-01-07T05:36:03.7214716Z 
2026-01-07T05:36:03.7214805Z ============================================================
2026-01-07T05:36:03.7215075Z Setup completed successfully!
2026-01-07T05:36:03.7215298Z ============================================================
2026-01-07T05:36:03.7215472Z 
2026-01-07T05:36:03.7215561Z To activate the virtual environment:
2026-01-07T05:36:03.7216067Z   source /home/runner/work/requirements-driven-development/requirements-driven-development/.venv/bin/activate
2026-01-07T05:36:03.7216477Z 
2026-01-07T05:36:03.7216544Z To run tests:
2026-01-07T05:36:03.7216722Z   pytest tests/python/
2026-01-07T05:36:03.7216844Z 
2026-01-07T05:36:03.7216912Z To deactivate:
2026-01-07T05:36:03.7217085Z   deactivate
2026-01-07T05:36:03.7217182Z 
2026-01-07T05:36:03.7293381Z ##[group]Run python scripts/run-tests.py
2026-01-07T05:36:03.7293743Z [36;1mpython scripts/run-tests.py[0m
2026-01-07T05:36:03.7327403Z shell: /usr/bin/bash -e {0}
2026-01-07T05:36:03.7327637Z env:
2026-01-07T05:36:03.7327880Z   pythonLocation: /opt/hostedtoolcache/Python/3.9.25/x64
2026-01-07T05:36:03.7328269Z   PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.9.25/x64/lib/pkgconfig
2026-01-07T05:36:03.7328658Z   Python_ROOT_DIR: /opt/hostedtoolcache/Python/3.9.25/x64
2026-01-07T05:36:03.7329018Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.9.25/x64
2026-01-07T05:36:03.7329350Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.9.25/x64
2026-01-07T05:36:03.7329710Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.9.25/x64/lib
2026-01-07T05:36:03.7329997Z ##[endgroup]
2026-01-07T05:36:04.6069928Z ============================= test session starts ==============================
2026-01-07T05:36:04.6071593Z platform linux -- Python 3.9.25, pytest-8.4.2, pluggy-1.6.0 -- /home/runner/work/requirements-driven-development/requirements-driven-development/.venv/bin/python
2026-01-07T05:36:04.6072487Z cachedir: .pytest_cache
2026-01-07T05:36:04.6073079Z rootdir: /home/runner/work/requirements-driven-development/requirements-driven-development
2026-01-07T05:36:04.6073700Z plugins: timeout-2.4.0, cov-7.0.0, xdist-3.8.0, mock-3.15.1
2026-01-07T05:36:04.8295205Z collecting ... collected 0 items / 1 error
2026-01-07T05:36:04.8295490Z 
2026-01-07T05:36:04.8295603Z ==================================== ERRORS ====================================
2026-01-07T05:36:04.8296001Z __________________ ERROR collecting tests/build/test_build.py __________________
2026-01-07T05:36:04.8296810Z ImportError while importing test module '/home/runner/work/requirements-driven-development/requirements-driven-development/tests/build/test_build.py'.
2026-01-07T05:36:04.8297573Z Hint: make sure your test modules/packages have valid Python names.
2026-01-07T05:36:04.8297905Z Traceback:
2026-01-07T05:36:04.8298306Z /opt/hostedtoolcache/Python/3.9.25/x64/lib/python3.9/importlib/__init__.py:127: in import_module
2026-01-07T05:36:04.8298838Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-01-07T05:36:04.8299177Z tests/build/test_build.py:17: in <module>
2026-01-07T05:36:04.8299421Z     import build
2026-01-07T05:36:04.8299642Z E   ModuleNotFoundError: No module named 'build'
2026-01-07T05:36:04.8299965Z =========================== short test summary info ============================
2026-01-07T05:36:04.8300265Z ERROR tests/build/test_build.py
2026-01-07T05:36:04.8300798Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
2026-01-07T05:36:04.8301908Z =============================== 1 error in 0.22s ===============================
2026-01-07T05:36:04.8562961Z [0;31m✗[0m Build tests failed
2026-01-07T05:36:05.1389664Z ============================= test session starts ==============================
2026-01-07T05:36:05.1390940Z platform linux -- Python 3.9.25, pytest-8.4.2, pluggy-1.6.0 -- /home/runner/work/requirements-driven-development/requirements-driven-development/.venv/bin/python
2026-01-07T05:36:05.1391765Z cachedir: .pytest_cache
2026-01-07T05:36:05.1392279Z rootdir: /home/runner/work/requirements-driven-development/requirements-driven-development
2026-01-07T05:36:05.1392927Z plugins: timeout-2.4.0, cov-7.0.0, xdist-3.8.0, mock-3.15.1
2026-01-07T05:36:05.3681694Z collecting ... collected 0 items / 1 error
2026-01-07T05:36:05.3682084Z 
2026-01-07T05:36:05.3682272Z ==================================== ERRORS ====================================
2026-01-07T05:36:05.3682941Z ________________ ERROR collecting tests/install/test_install.py ________________
2026-01-07T05:36:05.3684338Z ImportError while importing test module '/home/runner/work/requirements-driven-development/requirements-driven-development/tests/install/test_install.py'.
2026-01-07T05:36:05.3685569Z Hint: make sure your test modules/packages have valid Python names.
2026-01-07T05:36:05.3686069Z Traceback:
2026-01-07T05:36:05.3687163Z /opt/hostedtoolcache/Python/3.9.25/x64/lib/python3.9/importlib/__init__.py:127: in import_module
2026-01-07T05:36:05.3688023Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-01-07T05:36:05.3688551Z tests/install/test_install.py:16: in <module>
2026-01-07T05:36:05.3688970Z     import install
2026-01-07T05:36:05.3689330Z E   ModuleNotFoundError: No module named 'install'
2026-01-07T05:36:05.3689904Z =========================== short test summary info ============================
2026-01-07T05:36:05.3690394Z ERROR tests/install/test_install.py
2026-01-07T05:36:05.3691148Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
2026-01-07T05:36:05.3691773Z =============================== 1 error in 0.22s ===============================
2026-01-07T05:36:05.3966033Z [0;31m✗[0m Install tests failed
2026-01-07T05:36:05.6901787Z ============================= test session starts ==============================
2026-01-07T05:36:05.6902859Z platform linux -- Python 3.9.25, pytest-8.4.2, pluggy-1.6.0 -- /home/runner/work/requirements-driven-development/requirements-driven-development/.venv/bin/python
2026-01-07T05:36:05.6903735Z cachedir: .pytest_cache
2026-01-07T05:36:05.6904281Z rootdir: /home/runner/work/requirements-driven-development/requirements-driven-development
2026-01-07T05:36:05.6904973Z plugins: timeout-2.4.0, cov-7.0.0, xdist-3.8.0, mock-3.15.1
2026-01-07T05:36:05.8242039Z collecting ... collected 73 items
2026-01-07T05:36:05.8242393Z 
2026-01-07T05:36:05.8258666Z tests/rdd-framework/actions/test_execution_actions.py::TestExecutionModeManagement::test_set_execution_mode_valid_modes PASSED [  1%]
2026-01-07T05:36:05.8271526Z tests/rdd-framework/actions/test_execution_actions.py::TestExecutionModeManagement::test_set_execution_mode_invalid_mode PASSED [  2%]
2026-01-07T05:36:05.8284085Z tests/rdd-framework/actions/test_execution_actions.py::TestImplementationTracking::test_implementation_completed_on_sets_flag PASSED [  4%]
2026-01-07T05:36:05.8297000Z tests/rdd-framework/actions/test_execution_actions.py::TestImplementationTracking::test_implementation_completed_off_unsets_flag PASSED [  5%]
2026-01-07T05:36:05.8309706Z tests/rdd-framework/actions/test_execution_actions.py::TestExecutionTracking::test_set_executed_on_sets_flag PASSED [  6%]
2026-01-07T05:36:05.8321896Z tests/rdd-framework/actions/test_misc_actions.py::TestFileListingGeneration::test_files_list_csv_refresh_creates_csv PASSED [  8%]
2026-01-07T05:36:05.8334143Z tests/rdd-framework/actions/test_misc_actions.py::TestFileListingGeneration::test_files_list_csv_preserves_descriptions PASSED [  9%]
2026-01-07T05:36:05.8346212Z tests/rdd-framework/actions/test_misc_actions.py::TestFileListingGeneration::test_files_list_csv_adds_new_files PASSED [ 10%]
2026-01-07T05:36:05.8358834Z tests/rdd-framework/actions/test_misc_actions.py::TestCsvDescriptionUpdate::test_set_description_updates_entry PASSED [ 12%]
2026-01-07T05:36:05.8371226Z tests/rdd-framework/actions/test_modification_actions.py::TestModificationCreation::test_create_modification_sequential_ids PASSED [ 13%]
2026-01-07T05:36:05.8383709Z tests/rdd-framework/actions/test_modification_actions.py::TestModificationCreation::test_create_modification_requires_implementation_completed PASSED [ 15%]
2026-01-07T05:36:05.8398362Z tests/rdd-framework/actions/test_modification_actions.py::TestModificationCreation::test_create_modification_enforces_single_active PASSED [ 16%]
2026-01-07T05:36:05.8411267Z tests/rdd-framework/actions/test_modification_actions.py::TestModificationCompletion::test_complete_modification_updates_log PASSED [ 17%]
2026-01-07T05:36:05.8424289Z tests/rdd-framework/actions/test_modification_actions.py::TestModificationCompletion::test_complete_modification_resets_current_id PASSED [ 19%]
2026-01-07T05:36:05.8801342Z tests/rdd-framework/actions/test_prompt_actions.py::TestPromptCreate::test_create_prompt_with_auto_id PASSED [ 20%]
2026-01-07T05:36:05.8822521Z tests/rdd-framework/actions/test_prompt_actions.py::TestPromptCreate::test_create_prompt_enforces_single_active PASSED [ 21%]
2026-01-07T05:36:05.8871686Z tests/rdd-framework/actions/test_prompt_actions.py::TestPromptCreate::test_create_prompt_sanitizes_title_for_folder PASSED [ 23%]
2026-01-07T05:36:05.8884689Z tests/rdd-framework/actions/test_prompt_actions.py::TestPromptSetState::test_set_state_to_completed PASSED [ 24%]
2026-01-07T05:36:05.8897300Z tests/rdd-framework/actions/test_prompt_actions.py::TestPromptSetState::test_set_state_enforces_single_active PASSED [ 26%]
2026-01-07T05:36:05.8909785Z tests/rdd-framework/actions/test_prompt_actions.py::TestPromptSetState::test_set_state_allows_bidirectional_transition PASSED [ 27%]
2026-01-07T05:36:05.8922215Z tests/rdd-framework/actions/test_prompt_actions.py::TestPromptSetState::test_set_state_defaults_to_active_prompt PASSED [ 28%]
2026-01-07T05:36:05.8948930Z tests/rdd-framework/actions/test_prompt_actions.py::TestPromptSetState::test_set_state_validates_state_parameter PASSED [ 30%]
2026-01-07T05:36:05.8961589Z tests/rdd-framework/actions/test_prompt_actions.py::TestPromptComplete::test_complete_prompt_updates_state PASSED [ 31%]
2026-01-07T05:36:05.8973776Z tests/rdd-framework/actions/test_prompt_actions.py::TestPromptComplete::test_complete_prompt_with_git_disabled PASSED [ 32%]
2026-01-07T05:36:05.8985917Z tests/rdd-framework/actions/test_prompt_actions.py::TestPromptComplete::test_complete_prompt_with_git_enabled PASSED [ 34%]
2026-01-07T05:36:05.8998089Z tests/rdd-framework/actions/test_prompt_actions.py::TestPromptComplete::test_complete_prompt_handles_git_failure_gracefully PASSED [ 35%]
2026-01-07T05:36:05.9010333Z tests/rdd-framework/actions/test_prompt_actions.py::TestPromptListActions::test_find_active_prompt PASSED [ 36%]
2026-01-07T05:36:05.9025362Z tests/rdd-framework/actions/test_prompt_actions.py::TestPromptValidation::test_validate_prompt_id_format PASSED [ 38%]
2026-01-07T05:36:05.9205064Z tests/rdd-framework/actions/test_prompt_actions.py::TestPromptValidation::test_parse_params_from_argv FAILED [ 39%]
2026-01-07T05:36:05.9226695Z tests/rdd-framework/actions/test_prompt_actions.py::TestPromptFolderCreation::test_ensure_prompt_workdir_artifacts PASSED [ 41%]
2026-01-07T05:36:05.9239240Z tests/rdd-framework/actions/test_requirement_actions.py::TestRequirementCreation::test_create_ur_with_validation PASSED [ 42%]
2026-01-07T05:36:05.9251554Z tests/rdd-framework/actions/test_requirement_actions.py::TestRequirementCreation::test_create_tr_with_validation PASSED [ 43%]
2026-01-07T05:36:05.9264317Z tests/rdd-framework/actions/test_requirement_actions.py::TestRequirementCreation::test_create_requirement_bypasses_validation PASSED [ 45%]
2026-01-07T05:36:05.9277260Z tests/rdd-framework/actions/test_requirement_actions.py::TestRequirementCreation::test_create_requirement_sequential_ids PASSED [ 46%]
2026-01-07T05:36:05.9289908Z tests/rdd-framework/actions/test_requirement_actions.py::TestRequirementModification::test_modify_ur_preserves_format PASSED [ 47%]
2026-01-07T05:36:05.9302731Z tests/rdd-framework/actions/test_requirement_actions.py::TestRequirementModification::test_modify_tr_preserves_format PASSED [ 49%]
2026-01-07T05:36:05.9315020Z tests/rdd-framework/actions/test_requirement_actions.py::TestRequirementModification::test_modify_nonexistent_requirement_fails PASSED [ 50%]
2026-01-07T05:36:05.9327424Z tests/rdd-framework/actions/test_requirement_actions.py::TestRequirementDeletion::test_delete_ur_marks_as_deleted PASSED [ 52%]
2026-01-07T05:36:05.9339633Z tests/rdd-framework/actions/test_requirement_actions.py::TestRequirementDeletion::test_delete_tr_marks_as_deleted PASSED [ 53%]
2026-01-07T05:36:05.9351978Z tests/rdd-framework/actions/test_requirement_actions.py::TestRequirementDeletion::test_delete_nonexistent_requirement_fails PASSED [ 54%]
2026-01-07T05:36:05.9364346Z tests/rdd-framework/actions/test_requirement_actions.py::TestRequirementValidation::test_validation_requires_shall PASSED [ 56%]
2026-01-07T05:36:05.9377610Z tests/rdd-framework/actions/test_requirement_actions.py::TestRequirementValidation::test_validation_checks_length PASSED [ 57%]
2026-01-07T05:36:05.9389761Z tests/rdd-framework/actions/test_workdir_actions.py::TestWorkdirInitialization::test_workdir_new_setup_creates_structure PASSED [ 58%]
2026-01-07T05:36:05.9401776Z tests/rdd-framework/actions/test_workdir_actions.py::TestIterationArchiving::test_archive_creates_proper_folder_structure PASSED [ 60%]
2026-01-07T05:36:05.9415532Z tests/rdd-framework/actions/test_workdir_actions.py::TestIterationArchiving::test_archive_preserves_all_files PASSED [ 61%]
2026-01-07T05:36:05.9427156Z tests/rdd-framework/actions/test_workdir_actions.py::TestIterationArchiving::test_archive_prevents_when_active_prompt_exists PASSED [ 63%]
2026-01-07T05:36:05.9438634Z tests/rdd-framework/actions/test_workdir_actions.py::TestWorkdirClearing::test_clear_removes_prompt_folders PASSED [ 64%]
2026-01-07T05:36:05.9450915Z tests/rdd-framework/actions/test_workdir_actions.py::TestWorkdirClearing::test_clear_preserves_registry_files PASSED [ 65%]
2026-01-07T05:36:05.9462733Z tests/rdd-framework/actions/test_workflow_actions.py::TestQuestionnaireActions::test_questionnaire_check_complete_all_answered PASSED [ 67%]
2026-01-07T05:36:05.9474199Z tests/rdd-framework/actions/test_workflow_actions.py::TestQuestionnaireActions::test_questionnaire_check_complete_partial PASSED [ 68%]
2026-01-07T05:36:05.9485763Z tests/rdd-framework/actions/test_workflow_actions.py::TestQuestionnaireActions::test_questionnaire_delete_resets_flags PASSED [ 69%]
2026-01-07T05:36:05.9497069Z tests/rdd-framework/actions/test_workflow_actions.py::TestPlanActions::test_plan_generated_on_sets_flag PASSED [ 71%]
2026-01-07T05:36:05.9508386Z tests/rdd-framework/actions/test_workflow_actions.py::TestPlanActions::test_plan_generated_off_unsets_flag PASSED [ 72%]
2026-01-07T05:36:05.9519777Z tests/rdd-framework/actions/test_workflow_actions.py::TestPlanActions::test_plan_delete_removes_file_and_resets_flag PASSED [ 73%]
2026-01-07T05:36:05.9531185Z tests/rdd-framework/actions/test_workflow_actions.py::TestAnalysisActions::test_analysis_generated_on_sets_flag PASSED [ 75%]
2026-01-07T05:36:05.9543445Z tests/rdd-framework/actions/test_workflow_actions.py::TestAnalysisActions::test_analysis_delete_removes_file_and_resets_flag PASSED [ 76%]
2026-01-07T05:36:05.9557617Z tests/rdd-framework/config/test_manifest_validation.py::TestManifestValidation::test_manifest_exists_and_valid_json PASSED [ 78%]
2026-01-07T05:36:05.9571299Z tests/rdd-framework/config/test_manifest_validation.py::TestManifestValidation::test_manifest_has_framework_version PASSED [ 79%]
2026-01-07T05:36:05.9627426Z tests/rdd-framework/config/test_manifest_validation.py::TestManifestValidation::test_manifest_has_required_paths FAILED [ 80%]
2026-01-07T05:36:05.9639179Z tests/rdd-framework/config/test_manifest_validation.py::TestManifestValidation::test_manifest_required_paths_exist PASSED [ 82%]
2026-01-07T05:36:05.9690862Z tests/rdd-framework/config/test_manifest_validation.py::TestManifestValidation::test_manifest_has_prompt_snippets FAILED [ 83%]
2026-01-07T05:36:05.9739608Z tests/rdd-framework/config/test_manifest_validation.py::TestManifestValidation::test_manifest_prompt_snippet_files_exist FAILED [ 84%]
2026-01-07T05:36:05.9751996Z tests/rdd-framework/config/test_manifest_validation.py::TestConfigStructureValidation::test_instance_config_structure PASSED [ 86%]
2026-01-07T05:36:06.0389928Z tests/rdd-framework/config/test_manifest_validation.py::TestConfigStructureValidation::test_technical_design_form_structure FAILED [ 87%]
2026-01-07T05:36:06.1470827Z tests/rdd-framework/integration/test_iteration_archive.py::TestIterationArchiving::test_archive_creates_proper_structure FAILED [ 89%]
2026-01-07T05:36:06.1885194Z tests/rdd-framework/integration/test_prompt_lifecycle.py::TestCompletePromptWorkflow::test_full_prompt_lifecycle FAILED [ 90%]
2026-01-07T05:36:06.2308825Z tests/rdd-framework/integration/test_prompt_lifecycle.py::TestCompletePromptWorkflow::test_create_multiple_prompts_enforces_single_active FAILED [ 91%]
2026-01-07T05:36:06.2728780Z tests/rdd-framework/integration/test_prompt_lifecycle.py::TestModificationWorkflow::test_modification_lifecycle FAILED [ 93%]
2026-01-07T05:36:06.3153988Z tests/rdd-framework/integration/test_prompt_lifecycle.py::TestStateTransitions::test_bidirectional_state_transitions FAILED [ 94%]
2026-01-07T05:36:06.3597235Z tests/rdd-framework/integration/test_requirement_workflows.py::TestRequirementCRUDCycle::test_create_modify_delete_ur FAILED [ 95%]
2026-01-07T05:36:06.4049494Z tests/rdd-framework/integration/test_requirement_workflows.py::TestRequirementCRUDCycle::test_create_modify_delete_tr FAILED [ 97%]
2026-01-07T05:36:06.5216100Z tests/rdd-framework/integration/test_requirement_workflows.py::TestRequirementIDSequencing::test_sequential_ur_ids FAILED [ 98%]
2026-01-07T05:36:06.7429477Z tests/rdd-framework/integration/test_requirement_workflows.py::TestRequirementValidation::test_validation_bypass PASSED [100%]
2026-01-07T05:36:06.7430415Z 
2026-01-07T05:36:06.7431039Z =================================== FAILURES ===================================
2026-01-07T05:36:06.7431788Z _______________ TestPromptValidation.test_parse_params_from_argv _______________
2026-01-07T05:36:06.7432670Z tests/rdd-framework/actions/test_prompt_actions.py:239: in test_parse_params_from_argv
2026-01-07T05:36:06.7433229Z     assert "title " in params  # Key includes space
2026-01-07T05:36:06.7433665Z E   AssertionError: assert 'title ' in {'state': 'active', 'title': ' Test Value'}
2026-01-07T05:36:06.7434201Z ___________ TestManifestValidation.test_manifest_has_required_paths ____________
2026-01-07T05:36:06.7434814Z tests/rdd-framework/config/test_manifest_validation.py:63: in test_manifest_has_required_paths
2026-01-07T05:36:06.7435421Z     assert "rddInstance" in data, "Manifest must have 'rddInstance' key"
2026-01-07T05:36:06.7435848Z E   AssertionError: Manifest must have 'rddInstance' key
2026-01-07T05:36:06.7441280Z E   assert 'rddInstance' in {'canonicalRoots': {'frameworkRoot': '.rdd', 'instanceRoot': '.rdd-instance'}, 'components': [{'component-id': 'framework', 'description': 'Framework static assets: conventions, docs, prompts, scripts, config.', 'required': True, 'root': '.rdd'}, {'component-id': 'instance', 'description': 'Repo-specific configuration, requirements, specifications, workdir, archive.', 'required': True, 'root': '.rdd-instance'}], 'framework': {'description': 'Requirements-Driven Development framework installed into a repository; framework assets live under .rdd and repo-specific state and documentation live under .rdd-instance.', 'name': 'RDD Framework', 'runtime': {'language': 'python', 'pythonCommand': 'python'}, 'supportedPlatforms': ['windows', 'linux'], ...}, 'promptSnippets': [{'prompt-snippet-key': '[[[CONSISTENCY]]]', 'prompt-snippet-path': '.rdd/prompt-snippets/check-consistency.prompt.md'}, {'prompt-snippet-key': '[[[FOLDER_STRUCTURE_UPDATE]]]', 'prompt-snippet-path': '.rdd/prompt-snippets/folder-structure.update.md'}, {'prompt-snippet-key': '[[[ROLE_SOLUTION_ARCHITECT]]]', 'prompt-snippet-path': '.rdd/prompt-snippets/role.solution-architect.md'}, {'prompt-snippet-key': '[[[ROLE_SOFTWARE_DEVELOPER]]]', 'prompt-snippet-path': '.rdd/prompt-snippets/role.sotware-developer.md'}], ...}
2026-01-07T05:36:06.7446051Z ___________ TestManifestValidation.test_manifest_has_prompt_snippets ___________
2026-01-07T05:36:06.7446611Z tests/rdd-framework/config/test_manifest_validation.py:85: in test_manifest_has_prompt_snippets
2026-01-07T05:36:06.7447136Z     assert isinstance(snippets, dict), "promptSnippets must be an object"
2026-01-07T05:36:06.7447523Z E   AssertionError: promptSnippets must be an object
2026-01-07T05:36:06.7447791Z E   assert False
2026-01-07T05:36:06.7449593Z E    +  where False = isinstance([{'prompt-snippet-key': '[[[CONSISTENCY]]]', 'prompt-snippet-path': '.rdd/prompt-snippets/check-consistency.prompt.md'}, {'prompt-snippet-key': '[[[FOLDER_STRUCTURE_UPDATE]]]', 'prompt-snippet-path': '.rdd/prompt-snippets/folder-structure.update.md'}, {'prompt-snippet-key': '[[[ROLE_SOLUTION_ARCHITECT]]]', 'prompt-snippet-path': '.rdd/prompt-snippets/role.solution-architect.md'}, {'prompt-snippet-key': '[[[ROLE_SOFTWARE_DEVELOPER]]]', 'prompt-snippet-path': '.rdd/prompt-snippets/role.sotware-developer.md'}], dict)
2026-01-07T05:36:06.7451548Z _______ TestManifestValidation.test_manifest_prompt_snippet_files_exist ________
2026-01-07T05:36:06.7452132Z tests/rdd-framework/config/test_manifest_validation.py:102: in test_manifest_prompt_snippet_files_exist
2026-01-07T05:36:06.7452596Z     for key, rel_path in snippets.items():
2026-01-07T05:36:06.7452908Z E   AttributeError: 'list' object has no attribute 'items'
2026-01-07T05:36:06.7453322Z ______ TestConfigStructureValidation.test_technical_design_form_structure ______
2026-01-07T05:36:06.7453891Z tests/rdd-framework/config/test_manifest_validation.py:121: in test_technical_design_form_structure
2026-01-07T05:36:06.7454327Z     data = json.load(f)
2026-01-07T05:36:06.7454653Z /opt/hostedtoolcache/Python/3.9.25/x64/lib/python3.9/json/__init__.py:293: in load
2026-01-07T05:36:06.7455035Z     return loads(fp.read(),
2026-01-07T05:36:06.7455396Z /opt/hostedtoolcache/Python/3.9.25/x64/lib/python3.9/json/__init__.py:346: in loads
2026-01-07T05:36:06.7455779Z     return _default_decoder.decode(s)
2026-01-07T05:36:06.7456153Z /opt/hostedtoolcache/Python/3.9.25/x64/lib/python3.9/json/decoder.py:337: in decode
2026-01-07T05:36:06.7456545Z     obj, end = self.raw_decode(s, idx=_w(s, 0).end())
2026-01-07T05:36:06.7456955Z /opt/hostedtoolcache/Python/3.9.25/x64/lib/python3.9/json/decoder.py:355: in raw_decode
2026-01-07T05:36:06.7457424Z     raise JSONDecodeError("Expecting value", s, err.value) from None
2026-01-07T05:36:06.7457858Z E   json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
2026-01-07T05:36:06.7458331Z _________ TestIterationArchiving.test_archive_creates_proper_structure _________
2026-01-07T05:36:06.7458885Z tests/rdd-framework/integration/test_iteration_archive.py:78: in test_archive_creates_proper_structure
2026-01-07T05:36:06.7459464Z     assert expected_archive.exists(), f"Archive folder not found: {expected_archive}"
2026-01-07T05:36:06.7460208Z E   AssertionError: Archive folder not found: /tmp/pytest-of-runner/pytest-0/test_archive_creates_proper_st0/.rdd-instance-test/archive/ITR-TEST-001_Test Iteration
2026-01-07T05:36:06.7460927Z E   assert False
2026-01-07T05:36:06.7461120Z E    +  where False = exists()
2026-01-07T05:36:06.7461691Z E    +    where exists = PosixPath('/tmp/pytest-of-runner/pytest-0/test_archive_creates_proper_st0/.rdd-instance-test/archive/ITR-TEST-001_Test Iteration').exists
2026-01-07T05:36:06.7462399Z ____________ TestCompletePromptWorkflow.test_full_prompt_lifecycle _____________
2026-01-07T05:36:06.7463048Z tests/rdd-framework/integration/test_prompt_lifecycle.py:55: in test_full_prompt_lifecycle
2026-01-07T05:36:06.7463567Z     assert result.returncode == 0, f"prompt_create failed: {result.stderr}"
2026-01-07T05:36:06.7464529Z E   AssertionError: prompt_create failed: ERROR: Work iteration registry not found: /home/runner/work/requirements-driven-development/requirements-driven-development/.rdd-instance/workdir/work-iteration-registry.json
2026-01-07T05:36:06.7465342Z E     
2026-01-07T05:36:06.7465499Z E   assert 1 == 0
2026-01-07T05:36:06.7467279Z E    +  where 1 = CompletedProcess(args=['/home/runner/work/requirements-driven-development/requirements-driven-development/.venv/bin/python', '/home/runner/work/requirements-driven-development/requirements-driven-development/.rdd/src/actions/prompt_create.py', 'title=Integration Test Prompt'], returncode=1, stdout='', stderr='ERROR: Work iteration registry not found: /home/runner/work/requirements-driven-development/requirements-driven-development/.rdd-instance/workdir/work-iteration-registry.json
').returncode
2026-01-07T05:36:06.7469247Z _ TestCompletePromptWorkflow.test_create_multiple_prompts_enforces_single_active _
2026-01-07T05:36:06.7469873Z tests/rdd-framework/integration/test_prompt_lifecycle.py:208: in test_create_multiple_prompts_enforces_single_active
2026-01-07T05:36:06.7470475Z     assert result1.returncode == 0
2026-01-07T05:36:06.7470973Z E   AssertionError: assert 1 == 0
2026-01-07T05:36:06.7472773Z E    +  where 1 = CompletedProcess(args=['/home/runner/work/requirements-driven-development/requirements-driven-development/.venv/bin/python', '/home/runner/work/requirements-driven-development/requirements-driven-development/.rdd/src/actions/prompt_create.py', 'title=First Prompt'], returncode=1, stdout='', stderr='ERROR: Work iteration registry not found: /home/runner/work/requirements-driven-development/requirements-driven-development/.rdd-instance/workdir/work-iteration-registry.json
').returncode
2026-01-07T05:36:06.7474678Z _____________ TestModificationWorkflow.test_modification_lifecycle _____________
2026-01-07T05:36:06.7475207Z tests/rdd-framework/integration/test_prompt_lifecycle.py:244: in test_modification_lifecycle
2026-01-07T05:36:06.7475629Z     assert result.returncode == 0
2026-01-07T05:36:06.7475853Z E   AssertionError: assert 1 == 0
2026-01-07T05:36:06.7477632Z E    +  where 1 = CompletedProcess(args=['/home/runner/work/requirements-driven-development/requirements-driven-development/.venv/bin/python', '/home/runner/work/requirements-driven-development/requirements-driven-development/.rdd/src/actions/prompt_create.py', 'title=Test Prompt'], returncode=1, stdout='', stderr='ERROR: Work iteration registry not found: /home/runner/work/requirements-driven-development/requirements-driven-development/.rdd-instance/workdir/work-iteration-registry.json
').returncode
2026-01-07T05:36:06.7479521Z __________ TestStateTransitions.test_bidirectional_state_transitions ___________
2026-01-07T05:36:06.7480082Z tests/rdd-framework/integration/test_prompt_lifecycle.py:301: in test_bidirectional_state_transitions
2026-01-07T05:36:06.7480713Z     assert result.returncode == 0
2026-01-07T05:36:06.7480973Z E   AssertionError: assert 1 == 0
2026-01-07T05:36:06.7482754Z E    +  where 1 = CompletedProcess(args=['/home/runner/work/requirements-driven-development/requirements-driven-development/.venv/bin/python', '/home/runner/work/requirements-driven-development/requirements-driven-development/.rdd/src/actions/prompt_create.py', 'title=Test Prompt'], returncode=1, stdout='', stderr='ERROR: Work iteration registry not found: /home/runner/work/requirements-driven-development/requirements-driven-development/.rdd-instance/workdir/work-iteration-registry.json
').returncode
2026-01-07T05:36:06.7484640Z ____________ TestRequirementCRUDCycle.test_create_modify_delete_ur _____________
2026-01-07T05:36:06.7485177Z tests/rdd-framework/integration/test_requirement_workflows.py:54: in test_create_modify_delete_ur
2026-01-07T05:36:06.7485759Z     assert "[UR-0001]" in content
2026-01-07T05:36:06.7486210Z E   AssertionError: assert '[UR-0001]' in '## Product Name

Test Product

## User Requirements

'
2026-01-07T05:36:06.7486823Z ____________ TestRequirementCRUDCycle.test_create_modify_delete_tr _____________
2026-01-07T05:36:06.7487373Z tests/rdd-framework/integration/test_requirement_workflows.py:111: in test_create_modify_delete_tr
2026-01-07T05:36:06.7487803Z     assert "[TR-0001]" in content
2026-01-07T05:36:06.7488171Z E   AssertionError: assert '[TR-0001]' in '## Product Name

Test Product

## User Requirements

'
2026-01-07T05:36:06.7488677Z ______________ TestRequirementIDSequencing.test_sequential_ur_ids ______________
2026-01-07T05:36:06.7489189Z tests/rdd-framework/integration/test_requirement_workflows.py:156: in test_sequential_ur_ids
2026-01-07T05:36:06.7489597Z     assert "[UR-0001]" in content
2026-01-07T05:36:06.7489968Z E   AssertionError: assert '[UR-0001]' in '## Product Name

Test Product

## User Requirements

'
2026-01-07T05:36:06.7490385Z ================================ tests coverage ================================
2026-01-07T05:36:06.7490888Z _______________ coverage: platform linux, python 3.9.25-final-0 ________________
2026-01-07T05:36:06.7491154Z 
2026-01-07T05:36:06.7491266Z Name                                                            Stmts   Miss  Cover
2026-01-07T05:36:06.7491719Z -----------------------------------------------------------------------------------
2026-01-07T05:36:06.7492135Z .rdd/src/actions/prompt_create.py                                 116     79    32%
2026-01-07T05:36:06.7492567Z .rdd/src/actions/prompt_set_state.py                               86     67    22%
2026-01-07T05:36:06.7493050Z tests/rdd-framework/actions/test_execution_actions.py              14      0   100%
2026-01-07T05:36:06.7493524Z tests/rdd-framework/actions/test_misc_actions.py                   11      0   100%
2026-01-07T05:36:06.7494014Z tests/rdd-framework/actions/test_modification_actions.py           13      0   100%
2026-01-07T05:36:06.7494517Z tests/rdd-framework/actions/test_prompt_actions.py                114      4    96%
2026-01-07T05:36:06.7495010Z tests/rdd-framework/actions/test_requirement_actions.py            32      0   100%
2026-01-07T05:36:06.7495497Z tests/rdd-framework/actions/test_workdir_actions.py                16      0   100%
2026-01-07T05:36:06.7495974Z tests/rdd-framework/actions/test_workflow_actions.py               24      0   100%
2026-01-07T05:36:06.7496461Z tests/rdd-framework/config/test_manifest_validation.py             59      9    85%
2026-01-07T05:36:06.7496912Z tests/rdd-framework/conftest.py                                    84     39    54%
2026-01-07T05:36:06.7497376Z tests/rdd-framework/integration/test_iteration_archive.py          32      2    94%
2026-01-07T05:36:06.7497905Z tests/rdd-framework/integration/test_prompt_lifecycle.py          116     66    43%
2026-01-07T05:36:06.7498392Z tests/rdd-framework/integration/test_requirement_workflows.py      67     12    82%
2026-01-07T05:36:06.7498812Z -----------------------------------------------------------------------------------
2026-01-07T05:36:06.7499124Z TOTAL                                                             784    278    65%
2026-01-07T05:36:06.7499409Z Coverage XML written to file coverage.xml
2026-01-07T05:36:06.7499695Z =========================== short test summary info ============================
2026-01-07T05:36:06.7500467Z FAILED tests/rdd-framework/actions/test_prompt_actions.py::TestPromptValidation::test_parse_params_from_argv - AssertionError: assert 'title ' in {'state': 'active', 'title': ' Test Value'}
2026-01-07T05:36:06.7501709Z FAILED tests/rdd-framework/config/test_manifest_validation.py::TestManifestValidation::test_manifest_has_required_paths - AssertionError: Manifest must have 'rddInstance' key
2026-01-07T05:36:06.7506000Z assert 'rddInstance' in {'canonicalRoots': {'frameworkRoot': '.rdd', 'instanceRoot': '.rdd-instance'}, 'components': [{'component-id': 'framework', 'description': 'Framework static assets: conventions, docs, prompts, scripts, config.', 'required': True, 'root': '.rdd'}, {'component-id': 'instance', 'description': 'Repo-specific configuration, requirements, specifications, workdir, archive.', 'required': True, 'root': '.rdd-instance'}], 'framework': {'description': 'Requirements-Driven Development framework installed into a repository; framework assets live under .rdd and repo-specific state and documentation live under .rdd-instance.', 'name': 'RDD Framework', 'runtime': {'language': 'python', 'pythonCommand': 'python'}, 'supportedPlatforms': ['windows', 'linux'], ...}, 'promptSnippets': [{'prompt-snippet-key': '[[[CONSISTENCY]]]', 'prompt-snippet-path': '.rdd/prompt-snippets/check-consistency.prompt.md'}, {'prompt-snippet-key': '[[[FOLDER_STRUCTURE_UPDATE]]]', 'prompt-snippet-path': '.rdd/prompt-snippets/folder-structure.update.md'}, {'prompt-snippet-key': '[[[ROLE_SOLUTION_ARCHITECT]]]', 'prompt-snippet-path': '.rdd/prompt-snippets/role.solution-architect.md'}, {'prompt-snippet-key': '[[[ROLE_SOFTWARE_DEVELOPER]]]', 'prompt-snippet-path': '.rdd/prompt-snippets/role.sotware-developer.md'}], ...}
2026-01-07T05:36:06.7510707Z FAILED tests/rdd-framework/config/test_manifest_validation.py::TestManifestValidation::test_manifest_has_prompt_snippets - AssertionError: promptSnippets must be an object
2026-01-07T05:36:06.7511629Z assert False
2026-01-07T05:36:06.7513290Z  +  where False = isinstance([{'prompt-snippet-key': '[[[CONSISTENCY]]]', 'prompt-snippet-path': '.rdd/prompt-snippets/check-consistency.prompt.md'}, {'prompt-snippet-key': '[[[FOLDER_STRUCTURE_UPDATE]]]', 'prompt-snippet-path': '.rdd/prompt-snippets/folder-structure.update.md'}, {'prompt-snippet-key': '[[[ROLE_SOLUTION_ARCHITECT]]]', 'prompt-snippet-path': '.rdd/prompt-snippets/role.solution-architect.md'}, {'prompt-snippet-key': '[[[ROLE_SOFTWARE_DEVELOPER]]]', 'prompt-snippet-path': '.rdd/prompt-snippets/role.sotware-developer.md'}], dict)
2026-01-07T05:36:06.7515465Z FAILED tests/rdd-framework/config/test_manifest_validation.py::TestManifestValidation::test_manifest_prompt_snippet_files_exist - AttributeError: 'list' object has no attribute 'items'
2026-01-07T05:36:06.7516705Z FAILED tests/rdd-framework/config/test_manifest_validation.py::TestConfigStructureValidation::test_technical_design_form_structure - json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
2026-01-07T05:36:06.7518281Z FAILED tests/rdd-framework/integration/test_iteration_archive.py::TestIterationArchiving::test_archive_creates_proper_structure - AssertionError: Archive folder not found: /tmp/pytest-of-runner/pytest-0/test_archive_creates_proper_st0/.rdd-instance-test/archive/ITR-TEST-001_Test Iteration
2026-01-07T05:36:06.7519292Z assert False
2026-01-07T05:36:06.7519468Z  +  where False = exists()
2026-01-07T05:36:06.7520038Z  +    where exists = PosixPath('/tmp/pytest-of-runner/pytest-0/test_archive_creates_proper_st0/.rdd-instance-test/archive/ITR-TEST-001_Test Iteration').exists
2026-01-07T05:36:06.7521878Z FAILED tests/rdd-framework/integration/test_prompt_lifecycle.py::TestCompletePromptWorkflow::test_full_prompt_lifecycle - AssertionError: prompt_create failed: ERROR: Work iteration registry not found: /home/runner/work/requirements-driven-development/requirements-driven-development/.rdd-instance/workdir/work-iteration-registry.json
2026-01-07T05:36:06.7523086Z   
2026-01-07T05:36:06.7523243Z assert 1 == 0
2026-01-07T05:36:06.7525012Z  +  where 1 = CompletedProcess(args=['/home/runner/work/requirements-driven-development/requirements-driven-development/.venv/bin/python', '/home/runner/work/requirements-driven-development/requirements-driven-development/.rdd/src/actions/prompt_create.py', 'title=Integration Test Prompt'], returncode=1, stdout='', stderr='ERROR: Work iteration registry not found: /home/runner/work/requirements-driven-development/requirements-driven-development/.rdd-instance/workdir/work-iteration-registry.json
').returncode
2026-01-07T05:36:06.7527282Z FAILED tests/rdd-framework/integration/test_prompt_lifecycle.py::TestCompletePromptWorkflow::test_create_multiple_prompts_enforces_single_active - AssertionError: assert 1 == 0
2026-01-07T05:36:06.7529679Z  +  where 1 = CompletedProcess(args=['/home/runner/work/requirements-driven-development/requirements-driven-development/.venv/bin/python', '/home/runner/work/requirements-driven-development/requirements-driven-development/.rdd/src/actions/prompt_create.py', 'title=First Prompt'], returncode=1, stdout='', stderr='ERROR: Work iteration registry not found: /home/runner/work/requirements-driven-development/requirements-driven-development/.rdd-instance/workdir/work-iteration-registry.json
').returncode
2026-01-07T05:36:06.7531946Z FAILED tests/rdd-framework/integration/test_prompt_lifecycle.py::TestModificationWorkflow::test_modification_lifecycle - AssertionError: assert 1 == 0
2026-01-07T05:36:06.7534098Z  +  where 1 = CompletedProcess(args=['/home/runner/work/requirements-driven-development/requirements-driven-development/.venv/bin/python', '/home/runner/work/requirements-driven-development/requirements-driven-development/.rdd/src/actions/prompt_create.py', 'title=Test Prompt'], returncode=1, stdout='', stderr='ERROR: Work iteration registry not found: /home/runner/work/requirements-driven-development/requirements-driven-development/.rdd-instance/workdir/work-iteration-registry.json
').returncode
2026-01-07T05:36:06.7833963Z FAILED tests/rdd-framework/integration/test_prompt_lifecycle.py::TestStateTransitions::test_bidirectional_state_transitions - AssertionError: assert 1 == 0
2026-01-07T05:36:06.7836920Z  +  where 1 = CompletedProcess(args=['/home/runner/work/requirements-driven-development/requirements-driven-development/.venv/bin/python', '/home/runner/work/requirements-driven-development/requirements-driven-development/.rdd/src/actions/prompt_create.py', 'title=Test Prompt'], returncode=1, stdout='', stderr='ERROR: Work iteration registry not found: /home/runner/work/requirements-driven-development/requirements-driven-development/.rdd-instance/workdir/work-iteration-registry.json
').returncode
2026-01-07T05:36:06.7839935Z FAILED tests/rdd-framework/integration/test_requirement_workflows.py::TestRequirementCRUDCycle::test_create_modify_delete_ur - AssertionError: assert '[UR-0001]' in '## Product Name

Test Product

## User Requirements

'
2026-01-07T05:36:06.7842042Z FAILED tests/rdd-framework/integration/test_requirement_workflows.py::TestRequirementCRUDCycle::test_create_modify_delete_tr - AssertionError: assert '[TR-0001]' in '## Product Name

Test Product

## User Requirements

'
2026-01-07T05:36:06.7843787Z FAILED tests/rdd-framework/integration/test_requirement_workflows.py::TestRequirementIDSequencing::test_sequential_ur_ids - AssertionError: assert '[UR-0001]' in '## Product Name

Test Product

## User Requirements

'
2026-01-07T05:36:06.7844728Z ======================== 13 failed, 60 passed in 1.07s =========================
2026-01-07T05:36:06.8183444Z [0;31m✗[0m RDD framework tests failed
2026-01-07T05:36:06.8183854Z [0;31m✗[0m Some tests failed
2026-01-07T05:36:06.8184305Z 
2026-01-07T05:36:06.8184466Z ============================================================
2026-01-07T05:36:06.8184810Z   RDD Framework Test Runner (Linux/macOS)
2026-01-07T05:36:06.8185079Z ============================================================
2026-01-07T05:36:06.8185256Z 
2026-01-07T05:36:06.8185453Z [0;34mℹ[0m Checking prerequisites...
2026-01-07T05:36:06.8185746Z [0;32m✓[0m Python found: 3.9.25
2026-01-07T05:36:06.8186033Z [0;32m✓[0m Virtual environment found
2026-01-07T05:36:06.8186302Z [0;32m✓[0m pytest 8.4.2
2026-01-07T05:36:06.8186447Z 
2026-01-07T05:36:06.8186451Z 
2026-01-07T05:36:06.8186536Z ============================================================
2026-01-07T05:36:06.8186782Z   Running Tests
2026-01-07T05:36:06.8186963Z ============================================================
2026-01-07T05:36:06.8187125Z 
2026-01-07T05:36:06.8187251Z [0;34m[1/3][0m Running Build tests
2026-01-07T05:36:06.8187740Z 
2026-01-07T05:36:06.8187863Z [0;34m[2/3][0m Running Install tests
2026-01-07T05:36:06.8188026Z 
2026-01-07T05:36:06.8188157Z [0;34m[3/3][0m Running RDD framework tests
2026-01-07T05:36:06.8188332Z 
2026-01-07T05:36:06.8188336Z 
2026-01-07T05:36:06.8188422Z ============================================================
2026-01-07T05:36:06.8188650Z   Test Summary
2026-01-07T05:36:06.8188834Z ============================================================
2026-01-07T05:36:06.8188992Z 
2026-01-07T05:36:06.8189066Z Total test suites: 3
2026-01-07T05:36:06.8189277Z [0;32mPassed: 0[0m
2026-01-07T05:36:06.8189474Z [0;31mFailed: 3[0m
2026-01-07T05:36:06.8189587Z 
2026-01-07T05:36:06.8264503Z ##[error]Process completed with exit code 1.
2026-01-07T05:36:06.8403329Z ##[group]Run codecov/codecov-action@v4
2026-01-07T05:36:06.8403600Z with:
2026-01-07T05:36:06.8403769Z   file: ./coverage.xml
2026-01-07T05:36:06.8403964Z   flags: python
2026-01-07T05:36:06.8404143Z   name: python-coverage
2026-01-07T05:36:06.8404355Z env:
2026-01-07T05:36:06.8404576Z   pythonLocation: /opt/hostedtoolcache/Python/3.9.25/x64
2026-01-07T05:36:06.8404959Z   PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.9.25/x64/lib/pkgconfig
2026-01-07T05:36:06.8405334Z   Python_ROOT_DIR: /opt/hostedtoolcache/Python/3.9.25/x64
2026-01-07T05:36:06.8405664Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.9.25/x64
2026-01-07T05:36:06.8405995Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.9.25/x64
2026-01-07T05:36:06.8406326Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.9.25/x64/lib
2026-01-07T05:36:06.8406612Z ##[endgroup]
2026-01-07T05:36:06.9251752Z eventName: pull_request
2026-01-07T05:36:06.9252968Z baseRef: h111359:dev | headRef: h111359:20251130-v120
2026-01-07T05:36:06.9261214Z ==> linux OS detected
2026-01-07T05:36:07.1255384Z https://cli.codecov.io/latest/linux/codecov.SHA256SUM
2026-01-07T05:36:07.1872540Z gpg: directory '/home/runner/.gnupg' created
2026-01-07T05:36:07.1877364Z gpg: keybox '/home/runner/.gnupg/pubring.kbx' created
2026-01-07T05:36:07.1899661Z gpg: /home/runner/.gnupg/trustdb.gpg: trustdb created
2026-01-07T05:36:07.1900866Z gpg: key 806BB28AED779869: public key "Codecov Uploader (Codecov Uploader Verification Key) <security@codecov.io>" imported
2026-01-07T05:36:07.2047691Z gpg: Total number processed: 1
2026-01-07T05:36:07.2048313Z gpg:               imported: 1
2026-01-07T05:36:07.2114454Z gpg: Signature made Fri Dec  5 15:31:48 2025 UTC
2026-01-07T05:36:07.2115242Z gpg:                using RSA key 27034E7FDB850E0BBC2C62FF806BB28AED779869
2026-01-07T05:36:07.2118251Z gpg: Good signature from "Codecov Uploader (Codecov Uploader Verification Key) <security@codecov.io>" [unknown]
2026-01-07T05:36:07.2119294Z gpg: WARNING: This key is not certified with a trusted signature!
2026-01-07T05:36:07.2119968Z gpg:          There is no indication that the signature belongs to the owner.
2026-01-07T05:36:07.2120859Z Primary key fingerprint: 2703 4E7F DB85 0E0B BC2C  62FF 806B B28A ED77 9869
2026-01-07T05:36:07.2376217Z ==> Uploader SHASUM verified (fd34214e2b2c738e48e3ac90b2c23ec4e975d0e9aee51f2cebe81b5704af3f6c  codecov)
2026-01-07T05:36:07.2377239Z ==> Running version latest
2026-01-07T05:36:07.3097365Z Could not pull latest version information: SyntaxError: Unexpected token '<', "<!DOCTYPE "... is not valid JSON
2026-01-07T05:36:07.3099231Z ==> Running git config --global --add safe.directory /home/runner/work/requirements-driven-development/requirements-driven-development
2026-01-07T05:36:07.3195682Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/requirements-driven-development/requirements-driven-development
2026-01-07T05:36:07.3246782Z ==> Running command '/home/runner/work/_actions/codecov/codecov-action/v4/dist/codecov create-commit'
2026-01-07T05:36:07.3249647Z [command]/home/runner/work/_actions/codecov/codecov-action/v4/dist/codecov create-commit --git-service github -C 3c74563356a143f3290d599d7a2bb1b644da720f
2026-01-07T05:36:07.6786562Z info - 2026-01-07 05:36:07,678 -- ci service found: github-actions
2026-01-07T05:36:07.6879551Z warning - 2026-01-07 05:36:07,687 -- No config file could be found. Ignoring config.
2026-01-07T05:36:07.7191760Z warning - 2026-01-07 05:36:07,718 -- Branch `20251130-v120` is protected but no token was provided
2026-01-07T05:36:07.7194130Z warning - 2026-01-07 05:36:07,718 -- For information on Codecov upload tokens, see https://docs.codecov.com/docs/codecov-tokens
2026-01-07T05:36:08.0106409Z info - 2026-01-07 05:36:08,010 -- Process Commit creating complete
2026-01-07T05:36:08.0107318Z error - 2026-01-07 05:36:08,010 -- Commit creating failed: {"message":"Token required - not valid tokenless upload"}
2026-01-07T05:36:08.1001549Z ==> Running command '/home/runner/work/_actions/codecov/codecov-action/v4/dist/codecov create-report'
2026-01-07T05:36:08.1003967Z [command]/home/runner/work/_actions/codecov/codecov-action/v4/dist/codecov create-report --git-service github -C 3c74563356a143f3290d599d7a2bb1b644da720f
2026-01-07T05:36:08.4533843Z info - 2026-01-07 05:36:08,452 -- ci service found: github-actions
2026-01-07T05:36:08.4626995Z warning - 2026-01-07 05:36:08,462 -- No config file could be found. Ignoring config.
2026-01-07T05:36:08.6463879Z info - 2026-01-07 05:36:08,645 -- Process Report creating complete
2026-01-07T05:36:08.6468615Z error - 2026-01-07 05:36:08,646 -- Report creating failed: {"message":"Token required - not valid tokenless upload"}
2026-01-07T05:36:08.7231750Z ==> Running command '/home/runner/work/_actions/codecov/codecov-action/v4/dist/codecov do-upload'
2026-01-07T05:36:08.7234293Z [command]/home/runner/work/_actions/codecov/codecov-action/v4/dist/codecov do-upload -f ./coverage.xml -F python --git-service github -n python-coverage -C 3c74563356a143f3290d599d7a2bb1b644da720f
2026-01-07T05:36:09.0767715Z info - 2026-01-07 05:36:09,076 -- ci service found: github-actions
2026-01-07T05:36:09.0859803Z warning - 2026-01-07 05:36:09,085 -- No config file could be found. Ignoring config.
2026-01-07T05:36:09.1192283Z warning - 2026-01-07 05:36:09,118 -- xcrun is not installed or can't be found.
2026-01-07T05:36:09.1781088Z warning - 2026-01-07 05:36:09,177 -- No gcov data found.
2026-01-07T05:36:09.1784860Z warning - 2026-01-07 05:36:09,178 -- coverage.py is not installed or can't be found.
2026-01-07T05:36:09.2631503Z info - 2026-01-07 05:36:09,262 -- Found 1 coverage files to report
2026-01-07T05:36:09.2632339Z info - 2026-01-07 05:36:09,262 -- > /home/runner/work/requirements-driven-development/requirements-driven-development/coverage.xml
2026-01-07T05:36:09.4215807Z info - 2026-01-07 05:36:09,421 -- Process Upload complete
2026-01-07T05:36:09.4216581Z error - 2026-01-07 05:36:09,421 -- Upload failed: {"message":"Token required - not valid tokenless upload"}
2026-01-07T05:36:09.5145023Z Post job cleanup.
2026-01-07T05:36:09.6117362Z [command]/usr/bin/git version
2026-01-07T05:36:09.6159661Z git version 2.52.0
2026-01-07T05:36:09.6199672Z Copying '/home/runner/.gitconfig' to '/home/runner/work/_temp/48fc020b-fe0e-4fd4-8650-b1ba8471bf64/.gitconfig'
2026-01-07T05:36:09.6218189Z Temporarily overriding HOME='/home/runner/work/_temp/48fc020b-fe0e-4fd4-8650-b1ba8471bf64' before making global git config changes
2026-01-07T05:36:09.6219461Z Adding repository directory to the temporary git global config as a safe directory
2026-01-07T05:36:09.6225283Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/requirements-driven-development/requirements-driven-development
2026-01-07T05:36:09.6262013Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-01-07T05:36:09.6295190Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-01-07T05:36:09.6534175Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-01-07T05:36:09.6557189Z http.https://github.com/.extraheader
2026-01-07T05:36:09.6570412Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
2026-01-07T05:36:09.6602745Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'http\.https\:\/\/github\.com\/\.extraheader' && git config --local --unset-all 'http.https://github.com/.extraheader' || :"
2026-01-07T05:36:09.6835037Z [command]/usr/bin/git config --local --name-only --get-regexp ^includeIf\.gitdir:
2026-01-07T05:36:09.6867613Z [command]/usr/bin/git submodule foreach --recursive git config --local --show-origin --name-only --get-regexp remote.origin.url
2026-01-07T05:36:09.7220190Z Cleaning up orphan processes
%%ENDPROMPT

%%PROMPT P-011 "Test troubleshoot"
TBD
%%ENDPROMPT

%%PROMPT P-012 "Tests Troubleshoot 2"
Windows tests were successful. But Linux test failed. This is the Linux test log from pull request to merge to DEV branch (executing .github/workflows/tests.yml). Find the issues and fix them. Test before completion and ensure you have resolved the issues:


Run source .venv/bin/activate
  source .venv/bin/activate
  pytest tests/python/ --cov=.rdd/src --cov=scripts --cov-report=xml --cov-report=term
  shell: /usr/bin/bash -e {0}
  env:
    pythonLocation: /opt/hostedtoolcache/Python/3.9.25/x64
    PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.9.25/x64/lib/pkgconfig
    Python_ROOT_DIR: /opt/hostedtoolcache/Python/3.9.25/x64
    Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.9.25/x64
    Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.9.25/x64
    LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.9.25/x64/lib
ERROR: file or directory not found: tests/python/
============================= test session starts ==============================

platform linux -- Python 3.9.25, pytest-8.4.2, pluggy-1.6.0
rootdir: /home/runner/work/requirements-driven-development/requirements-driven-development
plugins: timeout-2.4.0, cov-7.0.0, xdist-3.8.0, mock-3.15.1
collected 0 items

============================ no tests ran in 0.02s =============================
Error: Process completed with exit code 4.
%%ENDPROMPT
