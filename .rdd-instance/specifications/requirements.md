## Product Name

RDD Framework



## Product Overview

The product is a system that serves to be installed the RDD framework in a software code repository (with or without git versioning).

The RDD framework aims to standardize execution of user defined tasks to GitHub copilot in form of prompts, maintain full traceability of prompt history, and provide a simplified developer experience through a unified execution model and a web-based interface. 

The framework enables:

* Persistent storage of prompts,
* Automated maintenance of requirements and technical specifications,
* A unified execution command (`execute command`),
* Web-based configuration and prompt management,
* Multi-platform support on Windows and Linux.



## Definitions

* **RDD** – Requirements-Driven Development

* **System** - A repository with scripts for test, build and release preparation of an installation of RDD framework

* **Framework** - In the context of the current document and code repository - the set of files and principles for realization of RDD development

* **RDD instance** - A folder holding the RDD related files specific for the current product

* **Prompt** – A developer-issued instruction for the copilot

* **Technical Design** – Structured JSON defining architectural decisions

* **Questionnaire** – A set of questions generated to clarify missing or ambiguous information

* **execute command** - A github prompt, which is the only prompt executed in GitHub Copilot chat window and which includes instructions how the copilot to understand the needed context and actions.

* **active prompt** - The prompt in `.rdd-instance/workdir/work-iteration-registry.json` which is with state `active`. The framework allows only one prompt to be in this state and this prompt is considered to be the `active prompt`

* **requirements file** - The file `.rdd-instance/specifications/requirements.md` which contains user and technical requirements and is formatted accordingly `.rdd/conventions/requirements.convention.md`

* **working directory** - The framework shall maintain a working directory `.rdd-instance/workdir` for active development work files.

* **prompt-snippets** - Reusable prompt snippets or whole prompts stored in `.rdd/prompt-snippets/`.

* **technical-design** - A file providin technical specificationa and constraints in a structured JSON format located in `.rdd-instance/specifications/technical-design.json`

* **files-and-folders** - The product files and folders structure documented in `.rdd-instance/specifications/files-and-folders.md`

* **prompt-implementation-plan** - A file with the exact steps which the copilot should execute. This is the per-prompt plan artifact stored as plan.md



## User Requirements

- [UR-20251224-0901] The framework shall define RDD (Requirement Driven Development) as a set of prompts, scripts, and workflows enabling a developer to use an LLM-based copilot for software development.

- [UR-20251224-0902] The framework shall maintain a library of predefined framework prompt snippets. The framework shall persist all composed prompts in a Markdown file authored through the Web UI to ensure full historical traceability.

- [UR-20251224-0903] The framework shall load, apply, and update `requirements file` automatically during each prompt execution.

- [UR-20251224-0904] The framework shall provide a web-based user interface for creating, editing, and managing prompts, questionnaires, implementation plans, technical specifications, file structure, requirements, and working directory control operations. The Web UI shall provide a modern, responsive interface optimized for desktop browsers, with clear navigation between pages, real-time feedback on operations, color-coded status indicators (success: green, error: red, warning: yellow, info: blue), and graceful error handling with user-friendly messages.

- [UR-20251224-0905] The framework shall provide a single prompt implementing the `execute command`, that initiates all copilot-related operations using the `active prompt`. 

- [UR-20251224-0906] The framework shall operate on both Windows and Linux.

- [UR-20251224-0907] The framework shall provide visualization and controlled modification of the `rdd instance` files through the Web UI.

- [UR-20251224-0908] The framework shall support reverse-engineering requirements from the existing product state.

- [UR-20251224-0909] The framework shall archive `working directory` content at the end of the current iteration for historical reference. The system shall create a dedicated archive directory during the work iteration archiving. Archives preserve the complete workdir folder state exactly as it existed before archiving.

- [UR-20251224-0910] Prompts shall call scripts for file and folder modifications or other deterministic actions rather than the copilot to implementing the logic.

- [UR-20251224-0911] The system shall clear the workdir folder after archiving by removing all files and subdirectories inside `working directory`.

- [UR-20251224-0912] The framework must maintain a `requirements file` and automatically update it after each prompt execution. During each execution, the framework must also load and apply the existing requirements.

- [UR-20251224-0913] The system documentation shall include Linux installation guidance for enabling the `python` command using the appropriate system package.

- [UR-20251224-0914] The framework shall provide CLI commands on top of the UI interface.

- [UR-20251224-0915] The system shall provide a Python-based test runner capable of executing all test types across platforms.

- [UR-20251224-0916] The system shall provide a functionality for creation of a JSON listing of the repository or workdir files via a dedicated command.

- [UR-20251224-0917] The Web UI shall provide a Prompt Management page enabling loading, editing, saving, questionnaire interaction, and plan review for the `active prompt`. 

- [UR-20251224-0918] The Web UI shall provide a Technical Specification page enabling editing of `technical-design` using a configuration-driven interactive form. 

- [UR-20251224-0919] The Web UI shall provide a File & Folder Structure page enabling visualization and controlled modification of the product's `files-and-folders`. 

- [UR-20251224-0920] When the `execute command` generates a questionnaire, the Web UI shall present the questionnaire with input fields and persist responses back to the questionnaire file.

- [UR-20251224-0921] The Web UI shall be able to display the `prompt-implementation-plan`, allow edits, and provide approval or regeneration options. 

- [UR-20251224-0922] The Web UI shall display technical design, requirements, and file structure content and allow controlled user edits.

- [UR-20251224-0923] The system shall check existing content in `requirements file`  before generating clarification questions to avoid redundant queries.

- [UR-20251224-0924] The `technical-design` configuration JSON shall support conditional and hierarchical logic, enabling form fields to appear or change behavior based on previously selected answers.

- [UR-20251224-0925] The Web UI shall provide a Technical Specification page for editing of `technical-design`. It shall provide a “Set Default Answers” function that automatically populates all unanswered design fields with their configured default values.

- [UR-20251224-0926] The framework shall provide smooth developer experience, minimizing technical overhead for requirement clarification

- [UR-20251224-0927] Error messages shall include specific problem description and suggested remediation steps

- [UR-20251224-0928] All destructive operations shall create backups before proceeding

- [UR-20251224-0929] Scripts shall validate prerequisites before executing operations

- [UR-20251224-0930] Scripts shall handle errors gracefully and provide recovery guidance

- [UR-20251224-0931] The Web UI and installers shall provide clear, color-coded feedback for success, error, warning, or informational messages to improve user comprehension.

- [UR-20251224-0932] Interactive menus used in CLI components shall support curses-based navigation with fallback to numeric input when curses is not available.

- [UR-20251224-0933] The test runner shall provide colored output indicating success, failure, and warnings to improve readability during test execution.

- [UR-20251224-0934] The installation process shall provide clear, user-friendly explanations of all required decisions and actions during installation.

- [UR-20251224-0935] All Web UI pages shall be optimized for desktop usage, offering clear navigation, real-time feedback on operations, and graceful handling of errors with informative messages.

- [UR-20251229-1841] [DELETED]

- [UR-20251229-1842] [DELETED]

- [UR-20251229-1843] [DELETED]

- [UR-20251229-1844] [DELETED]

- [UR-20251231-0100] The framework shall provide a mechanism to mark prompts as executed and track execution status in the work iteration registry.

- [UR-20251231-0101] The framework shall provide a prompt completion command that transitions prompts to completed state and optionally triggers git commit operations.

- [UR-20251231-0102] The Web UI shall display execution status for each prompt and provide a completion button that is enabled only for executed prompts in in-progress state.

- [UR-20251231-0103] The framework shall support optional git integration during prompt completion, controlled by a global configuration flag.

- [UR-20251231-1600] The framework shall provide easy-to-use launcher scripts for starting the Web UI on both Windows and Linux platforms without requiring manual terminal commands.

- [UR-20251231-1601] The Web UI launchers shall automatically open the default web browser when the server starts successfully.

- [UR-20251231-1602] The Web UI shall provide a shutdown button to allow users to stop the server without using terminal commands.

- [UR-20251231-0700] The framework shall support two prompt states: `active` and `completed`. The `active` state indicates a prompt is currently being worked on, while `completed` indicates finished work.

- [UR-20251231-0701] New prompts shall be created in `active` state by default.

- [UR-20251231-0702] The framework shall enforce that only one prompt can be in `active` state at any time, ensuring clear focus on current work.



## Technical Requirements

- [TR-20251224-0901] The framework shall implement all automation functionality in Python using a domain-based command routing architecture and for the user interface shall use only vanilla JavaScript, HTML, CSS.

- [TR-20251224-0902] The framework shall use the `python` command (not `python3`) for executing all internal scripts to ensure cross-platform compatibility.

- [TR-20251224-0903] No database is used; all data is stored in Markdown or JSON files.

- [TR-20251224-0904] Archived workdirs are stored in `.rdd-instance/archive/`.

- [TR-20251224-0905] Prompt templates provided by the framework are stored in `.rdd/prompt-snippets`.

- [TR-20251224-0906] The framework shall use `.rdd-instance/specifications/` for storing technical design files. 

- [TR-20251224-0907] A technical design form JSON config file `.rdd/config/technical-design-form.json` shall define the content of Technical Specification page and should support definition of form elements with predefined options, multi-select fields, free-text values, conditional logic, and a default-answer mechanism. 

- [TR-20251224-0908] Web UI server shall be implemented using Python standard-library components (such as `http.server`) or equivalent, binding to `127.0.0.1` on an available port and automatically opening the user's default browser. 

- [TR-20251224-0909] The Web UI server shall expose REST-like JSON endpoints for reading, writing, and updating files in `.rdd-instance/` and for invoking RDD commands.

- [TR-20251224-0910] The Web UI server shall generate a session token on startup and require it for all operations to prevent unauthorized access. 

- [TR-20251224-0917] The system shall keep the currently installed framework version number in `.rdd/config/manifest.json` at JSONPath "framework.version" using semantic versioning (MAJOR.MINOR.PATCH).

- [TR-20251224-0919] The build script shall generate together with the zip file a SHA256 checksum file for each release archive and ensure compatibility with standard `sha256sum` verification tools.

- [TR-20251224-0920] The build script shall detect when build artifacts for the same version already exist and allow the user to stop, overwrite, or increment the patch version.

- [TR-20251224-0921] The build script shall substitute version placeholders (e.g., `{{VERSION}}`) in template files when constructing installation assets.

- [TR-20251224-0922] The system shall store all active workdir files in .rdd-instance/workdir/

- [TR-20251224-0923] The framework shall provide a command to generate a JSON listing of repository or workdir files and store it at `.rdd-instance/workdir/files-list.json`, excluding directories beginning with `.` and directories named `venv`, and listing for each entry: `type` (file type - like 'txt', 'md', 'csv', 'xlsx', 'pdf', 'json', 'py', 'html', 'js', 'css' and others), `name` (file name), `relpath` (relative path), and `mtime` (modification time) in ISO8601 UTC format.

- [TR-20251224-0924] The Web UI shall provide pages for managing prompts, technical specifications, folder structures, requirements, and version-control workflows, backed by the REST endpoints and reflecting the interaction model defined in the Product Requirements Specification.

- [TR-20251224-0925] `.rdd-instance/workdir/prompts-registry.md` shall contain completed prompts texts. All other operational state of the prompt is maintained in `.rdd-instance/workdir/work-iteration-registry.json`. The consistency between those two files will be maintained by the scripts in `.rdd/src/`.

- [TR-20251224-0926] The framework shall implement safety checks that prevent iteration creation unless the workdir is empty.

- [TR-20251224-0927] The framework shall archive each completed iteration in `.rdd-instance/archive/<iteration-id>_<iteration-name>/`.

- [TR-20251224-0928] All generated questions shall follow the question-formatting standards defined in `.rdd/conventions/questions-formatting.md`.

- [TR-20251224-0931] The framework shall support extracting and displaying repository file lists, technical design content, and requirements content through Web UI components for visualization and editing.

- [TR-20251224-0932] The test system shall be implemented entirely in Python using pytest for Python tests with optional coverage reporting.

- [TR-20251224-0933] The system shall maintain its test fixtures in a `tests/` directory using isolated temporary directories to prevent modification of product files during test execution.

- [TR-20251224-0934] The testing environment shall be created using a Python script that constructs and manages a dedicated virtual environment for testing.

- [TR-20251224-0936] All automation scripts shall be stored in the `.rdd/src/` directory.

- [TR-20251224-0938] CI/CD Testing: The system shall use GitHub Actions to run tests automatically on push and pull request events, executing only the Python test runner. For the purpose shall exist a file `.github/workflows/tests.yaml` 

- [TR-20251224-0939] The CI/CD pipeline shall include a GitHub Actions workflow file `.github/workflows/tests.yaml` configured to run on `pull_request` events targeting the `dev` branch and on manual `workflow_dispatch` triggers.

- [TR-20251224-0940] The `.github/workflows/tests.yaml` workflow shall define a job `all-tests-linux` that runs on `ubuntu-latest`, checks out the repository, installs Python 3.9 using `actions/setup-python@v5`, installs BATS, sets up the test environment by running `python .rdd/src/setup-test-env.py`, and executes all tests by running `python .rdd/src/run-tests.py`.

- [TR-20251224-0941] The `all-tests-linux` job in `.github/workflows/tests.yaml` shall generate a Python test coverage report by activating the `.venv` virtual environment, running `pytest tests/python/ --cov=.rdd/src --cov=scripts --cov-report=xml --cov-report=term`, and producing a `coverage.xml` file.

- [TR-20251224-0942] The `all-tests-linux` job in `.github/workflows/tests.yaml` shall upload the generated `coverage.xml` report using `codecov/codecov-action@v4` with appropriate flags and name metadata, and this upload step shall execute even when previous steps fail.

- [TR-20251224-0943] The `.github/workflows/tests.yaml` workflow shall define a job `all-tests-windows` that runs on `windows-latest`, checks out the repository, installs Python 3.9 using `actions/setup-python@v5`, installs the Pester module using PowerShell, sets up the test environment by running `python .rdd/src/setup-test-env.py`, and executes all tests by running `python .rdd/src/run-tests.py`.

- [TR-20251224-0944] The `.github/workflows/tests.yaml` workflow shall define a job `test-summary` that runs on `ubuntu-latest`, depends on the completion of `all-tests-linux` and `all-tests-windows`, executes regardless of their success or failure, and prints the final result status of both jobs to the workflow logs.

- [TR-20251224-0945] The test framework shall generate code coverage reports for Python code and report coverage metrics in CI/CD pipelines

- [TR-20251224-0946] Test runner scripts shall provide colored output (green for success, red for failure, yellow for warnings) to improve readability

- [TR-20251224-0948] The system documentation shall provide installation guidance for enabling the `python` command on Linux systems using distribution-appropriate packages such as `python-is-python3`.

- [TR-20251224-0954] The build process shall detect existing artifacts (ZIP and checksum files) for the current version before starting a build.

- [TR-20251224-0955] When existing build artifacts are detected, the build process shall prompt the user to stop, overwrite the artifacts, or increment the patch version.

- [TR-20251224-0956] An empty workdir folder `.rdd-instance/workdir` should exist at the start of each new work iteration

- [TR-20251224-0957] The system shall implement a build script that generates cross-platform release zip file following the naming convention `rdd-v{version}.zip`. Releases shall be built by the script `build/build.py`.

- [TR-20251224-0958] Build artifacts are generated in the `build/` directory.

- [TR-20251224-0959] Releases are distributed as a single cross-platform archive named `rdd-v{version}.zip`. The release zip file includes framework code, installation scripts, templates, and documentation.

- [TR-20251225-0350] The framework shall provide a deterministic script `.rdd/src/actions/prompt_create.py` that creates a new prompt by appending a `prompt-metadata` record to `.rdd-instance/workdir/work-iteration-registry.json` and ensuring a corresponding stub record exists in `.rdd-instance/workdir/prompts-registry.md` (creating the file if missing). The created prompt text record shall be a placeholder (e.g., `TBD`) until populated by other tooling.

- [TR-20251228-1537] The framework shall create a per-prompt working folder under `.rdd-instance/workdir/` named `<prompt-id>_<prompt-title>` and in it shall create empty files `prompt.md`, `plan.md`, and `implementation.md` when a new prompt is created.

- [TR-20251228-1727] The framework shall provide a deterministic script `.rdd/src/actions/prompt_set_state.py` that updates the `state` field of a prompt record in `.rdd-instance/workdir/work-iteration-registry.json`. The script shall accept `state=` (required, one of `active|completed`) and optional `prompt-id=` parameters. When `prompt-id=` is omitted, the script shall default to the currently active prompt (the one in `active` state). The script shall enforce the "single active prompt" invariant by failing with a clear error if attempting to set a prompt to `active` when another prompt is already in that state.
  
- [TR-20251229-1352] The framework shall provide a main CLI entry point at `.rdd/src/rdd.py` that implements domain-based command routing with support for `prompt` and `workdir` domains.

- [TR-20251229-1353] The CLI shall support three execution modes: interactive menu mode (no arguments), domain menu mode (single domain argument), and direct action execution mode (domain and action arguments).

- [TR-20251229-1354] The CLI shall provide interactive menus using the curses library for terminal-based navigation with arrow keys, Enter to select, and Q to quit.

- [TR-20251229-1355] The CLI shall implement a numeric fallback menu system that activates when curses is unavailable or fails, accepting numeric input (1-N) or 'q' to quit.

- [TR-20251229-1356] The CLI shall route domain actions to Python scripts in `.rdd/src/actions/` following the naming convention `<domain>_<action>.py` where action names use underscores instead of hyphens.

- [TR-20251229-1357] The framework shall provide wrapper scripts `.rdd/src/rdd.sh` (Linux/macOS) and `.rdd/src/rdd.bat` (Windows) that execute `rdd.py` using the `python` command and forward all arguments.

- [TR-20251229-1358] The CLI shall provide a `--help` flag that displays usage documentation including available domains, execution modes, and usage examples.

- [TR-20251229-1359] The framework shall provide a script `.rdd/src/actions/prompt_list.py` that displays all prompts from the work iteration registry in a formatted table showing prompt ID, title, state, and type.

- [TR-20251229-1360] All CLI error messages shall include both a specific problem description and suggested remediation steps.

- [TR-20251229-1361] All Python functions in the CLI implementation shall include comprehensive docstrings describing purpose, parameters, return values, and any exceptions raised.

- [TR-20251229-1841] [DELETED]

- [TR-20251229-1842] [DELETED]

- [TR-20251229-1843] [DELETED]

- [TR-20251229-1844] [DELETED]

- [TR-20251230-1430] The framework shall provide a web server implementation at `.rdd/src/web/server.py` that serves the web interface on localhost port 8080 (configurable via --port parameter) and automatically opens the default browser on startup.

- [TR-20251230-1431] The web server shall implement API endpoints including GET /api/token for session token retrieval, GET /api/registry for work iteration registry access, GET /api/file/{filepath} for reading files from .rdd-instance, POST /api/action for executing RDD actions, and POST /api/file/save for saving files to .rdd-instance.

- [TR-20251230-1432] The web interface shall be implemented using vanilla JavaScript, HTML, and Bootstrap 5 CSS framework, with all frontend assets located in `.rdd/src/web/static/` (app.js, style.css) and templates in `.rdd/src/web/templates/` (index.html).

- [TR-20251230-1433] The web interface shall provide a responsive navigation bar with sections for Prompts, Workdir, Git, and Files, each section displaying relevant operations and status information with color-coded alerts (success: green, error: red, warning: yellow, info: blue).

- [TR-20251230-1434] The Prompts section shall display all prompts in a table showing ID, title, type, state, parent ID, and actions, with buttons for creating new prompts and setting prompt states via modal dialogs.

- [TR-20251230-1435] The Workdir section shall provide forms for creating new work iterations with iteration name input, archiving current iterations with confirmation dialog, and displaying current iteration status including iteration ID, name, total prompts, and next prompt ID.

- [TR-20251230-1436] [DELETED]

- [TR-20251230-1437] The Files section shall provide a file browser with path input field, quick access buttons for common files (registry, requirements, technical design), a text editor for viewing and editing file contents, and save functionality.

- [TR-20251230-1438] The Prompts section shall provide an integrated prompt editor that displays Edit buttons for prompts in `active` state and View buttons for prompts in `completed` state.

- [TR-20251230-1439] The prompt editor shall replace the prompts list view with a tabbed interface containing tabs for prompt.md, plan.md, questionnaire.md, and implementation.md files, with a Back button to return to the prompts list.

- [TR-20251230-1440] The prompt editor shall load prompt files from the prompt's working folder (workdir/<prompt-id>_<prompt-title>/) and display their contents in monospace textareas within the appropriate tabs.

- [TR-20251230-1441] The prompt editor shall provide individual Save buttons for prompt.md, plan.md, and questionnaire.md files that persist changes back to the file system when clicked.

- [TR-20251230-1442] The implementation.md file in the prompt editor shall be displayed as read-only in all cases.

- [TR-20251230-1443] The prompt editor shall enforce frontend soft enforcement of edit permissions by setting textareas to readonly and disabling save buttons when in view-only mode (for completed prompts).

- [UR-20251230-2001] The framework shall provide a toggle mechanism to enable/disable analyze mode for prompts through the Web UI.

- [UR-20251230-2002] The framework shall automatically disable analyze mode after each analyze execution completes.

- [UR-20251230-2003] The framework shall prevent enabling analyze mode for prompts not in `active` state.

- [TR-20251230-2004] Each prompt in work-iteration-registry.json shall have an `analyze-enabled` boolean field with default value `false`.

- [TR-20251230-2005] The framework shall provide scripts `prompt_analyze_on.py` and `prompt_analyze_off.py` in `.rdd/src/actions/` for controlling analyze mode.

- [TR-20251230-2006] The execution prompt logic shall read analyze mode from the `analyze-enabled` field in work-iteration-registry.json rather than from chat modifiers.

- [TR-20251230-2007] The Web UI shall display analyze mode toggles only for prompts in `active` state.

- [TR-20251230-2008] The Prompts section table in the Web UI shall include an "Analyze Mode" column with a toggle switch for `active` prompts and "N/A" for `completed` prompts.

- [TR-20251230-2009] The CLI prompt domain menu shall include "analyze-on" and "analyze-off" actions that route to the prompt_analyze_on.py and prompt_analyze_off.py scripts.

- [TR-20251230-2010] The analyze execution step shall automatically invoke the prompt_analyze_off.py script after completing the analyze execution to disable the analyze flag.

- [TR-20251231-0100] The work iteration registry shall include a root-level boolean field `git-enabled` (default: false) to control git operations during prompt completion.

- [TR-20251231-0101] Each prompt object in the work iteration registry shall include an `executed` boolean field (default: false) to track execution status.

- [TR-20251231-0102] The framework shall provide a script `.rdd/src/actions/prompt_set_executed_on.py` that sets the executed flag for a specified prompt or the active prompt.

- [TR-20251231-0103] The framework shall provide a script `.rdd/src/actions/prompt_complete.py` that sets a prompt to completed state and conditionally executes git commit based on the git-enabled flag.

- [TR-20251231-0104] The prompt completion action shall handle git commit failures gracefully, logging warnings but proceeding with state changes when no repository changes exist.

- [TR-20251231-0105] The Web UI Prompts section table shall include an "Executed" column displaying a badge indicating whether each prompt has been executed (green "Yes" or gray "No").

- [TR-20251231-0106] The Web UI shall provide a "Complete" button in the Actions column for prompts in `active` state, enabled only when the prompt's executed flag is true, with a tooltip explaining the requirement.



## Plan Mode Requirements

- [UR-20251231-0200] The framework shall provide a plan mode that allows users to generate implementation plans without proceeding to execution, enabling plan review and approval.

- [UR-20251231-0201] The framework shall automatically disable plan mode after the plan generation completes.

- [UR-20251231-0202] The framework shall ensure that plan mode and analyze mode are mutually exclusive and cannot be enabled simultaneously for the same prompt.

- [UR-20251231-0203] The framework shall prevent enabling plan mode for prompts not in `active` state.

- [UR-20251231-0204] The framework shall provide a toggle mechanism to enable/disable plan mode for prompts through the Web UI.

- [TR-20251231-0200] Each prompt in work-iteration-registry.json shall have a `plan-enabled` boolean field with default value `false`.

- [TR-20251231-0201] The framework shall provide scripts `prompt_plan_on.py` and `prompt_plan_off.py` in `.rdd/src/actions/` for controlling plan mode.

- [TR-20251231-0202] The execution prompt logic shall read plan mode from the `plan-enabled` field in work-iteration-registry.json and execute only the plan generation step when enabled.

- [TR-20251231-0203] The Web UI shall display plan mode toggles only for prompts in `active` state.

- [TR-20251231-0204] The Prompts section table in the Web UI shall include a "Plan Mode" column with a toggle switch for `active` prompts and "N/A" for `completed` prompts.

- [TR-20251231-0205] The CLI prompt domain menu shall include "plan-on" and "plan-off" actions that route to the prompt_plan_on.py and prompt_plan_off.py scripts.

- [TR-20251231-0206] The plan execution step shall automatically invoke the prompt_plan_off.py script after completing the plan generation to disable the plan flag.

- [TR-20251231-0207] When enabling plan mode, the system shall automatically disable analyze mode if it is currently enabled, and vice versa, to enforce mutual exclusivity.

- [TR-20251231-1600] The framework shall provide launcher scripts `run.bat` for Windows and `run.sh` for Linux located in the `.rdd/` directory.

- [TR-20251231-1601] The launcher scripts shall execute `.rdd/src/web/server.py` using the `python` command with automatic browser opening enabled.

- [TR-20251231-1602] The launcher scripts shall display clear error messages and keep the console/terminal window open when errors occur to allow users to read the error information.

- [TR-20251231-1603] The Web UI server shall support automatic detection of available ports and use a fallback mechanism if the default port is occupied.

- [TR-20251231-1604] The Web UI shall implement a POST /api/shutdown endpoint that gracefully stops the web server when invoked.

- [TR-20251231-1605] The Linux launcher script `run.sh` shall include proper shebang (`#!/bin/bash`) and require executable permissions to be set before use.

- [TR-20251231-0700] The `prompt_set_state.py` script shall accept only `active` or `completed` as valid state values.

- [TR-20251231-0701] The framework shall allow bidirectional state transitions between `active` and `completed` states without restrictions.

- [TR-20251231-0702] The `prompt_create.py` script shall validate that no other prompt is in `active` state when creating a new prompt, and shall fail with a clear error message if validation fails.
