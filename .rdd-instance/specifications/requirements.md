## Product Name

RDD Framework

<!-- 
Migration Note: On January 4, 2026, requirement IDs were migrated from timestamp-based 
format (UR-YYYYMMDD-HHmm, TR-YYYYMMDD-HHmm) to sequential numeric format (UR-0001, TR-0001). 
Git history preserves original IDs for traceability.
-->



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

- [UR-0001] The framework shall define RDD (Requirement Driven Development) as a set of prompts, scripts, and workflows enabling a developer to use an LLM-based copilot for software development.

- [UR-0002] The framework shall maintain a library of predefined framework prompt snippets. The framework shall persist all composed prompts in a Markdown file authored through the Web UI to ensure full historical traceability.

- [UR-0003] The framework shall load, apply, and update `requirements file` automatically during each prompt execution.

- [UR-0004] The framework shall provide a web-based user interface for creating, editing, and managing prompts, questionnaires, implementation plans, technical specifications, file structure, requirements, and working directory control operations. The Web UI shall provide a modern, responsive interface optimized for desktop browsers, with clear navigation between pages, real-time feedback on operations, color-coded status indicators (success: green, error: red, warning: yellow, info: blue), and graceful error handling with user-friendly messages.

- [UR-0005] The framework shall provide a single prompt implementing the `execute command`, that initiates all copilot-related operations using the `active prompt`. 

- [UR-0006] The framework shall operate on both Windows and Linux.

- [UR-0007] The framework shall provide visualization and controlled modification of the `rdd instance` files through the Web UI.

- [UR-0008] The framework shall support reverse-engineering requirements from the existing product state.

- [UR-0009] The framework shall archive `working directory` content at the end of the current iteration for historical reference. The system shall create a dedicated archive directory during the work iteration archiving. Archives preserve the complete workdir folder state exactly as it existed before archiving.

- [UR-0010] Prompts shall call scripts for file and folder modifications or other deterministic actions rather than the copilot to implementing the logic.

- [UR-0011] The system shall clear the workdir folder after archiving by removing all files and subdirectories inside `working directory`.

- [UR-0012] The framework must maintain a `requirements file` and automatically update it after each prompt execution. During each execution, the framework must also load and apply the existing requirements.

- [UR-0013] The system documentation shall include Linux installation guidance for enabling the `python` command using the appropriate system package.

- [UR-0014] The framework shall provide CLI commands on top of the UI interface.

- [UR-0015] The system shall provide a Python-based test runner capable of executing all test types across platforms.

- [UR-0016] The system shall provide a functionality for creation of a JSON listing of the repository or workdir files via a dedicated command.

- [UR-0017] The Web UI shall provide a Prompt Management page enabling loading, editing, saving, questionnaire interaction, and plan review for the `active prompt`. 

- [UR-0018] The Web UI shall provide a Technical Specification page enabling editing of `technical-design` using a configuration-driven interactive form. 

- [UR-0019] The Web UI shall provide a File & Folder Structure page enabling visualization and controlled modification of the product's `files-and-folders`. 

- [UR-0020] When the `execute command` generates a questionnaire, the Web UI shall present the questionnaire with input fields and persist responses back to the questionnaire file.

- [UR-0021] The Web UI shall be able to display the `prompt-implementation-plan`, allow edits, and provide approval or regeneration options. 

- [UR-0022] The Web UI shall display technical design, requirements, and file structure content and allow controlled user edits.

- [UR-0023] The system shall check existing content in `requirements file`  before generating clarification questions to avoid redundant queries.

- [UR-0024] The `technical-design` configuration JSON shall support conditional and hierarchical logic, enabling form fields to appear or change behavior based on previously selected answers.

- [UR-0025] The Web UI shall provide a Technical Specification page for editing of `technical-design`. It shall provide a “Set Default Answers” function that automatically populates all unanswered design fields with their configured default values.

- [UR-0026] The framework shall provide smooth developer experience, minimizing technical overhead for requirement clarification

- [UR-0027] Error messages shall include specific problem description and suggested remediation steps

- [UR-0028] All destructive operations shall create backups before proceeding

- [UR-0029] Scripts shall validate prerequisites before executing operations

- [UR-0030] Scripts shall handle errors gracefully and provide recovery guidance

- [UR-0031] The Web UI and installers shall provide clear, color-coded feedback for success, error, warning, or informational messages to improve user comprehension.

- [UR-0032] Interactive menus used in CLI components shall support curses-based navigation with fallback to numeric input when curses is not available.

- [UR-0033] The test runner shall provide colored output indicating success, failure, and warnings to improve readability during test execution.

- [UR-0034] The installation process shall provide clear, user-friendly explanations of all required decisions and actions during installation.

- [UR-0035] All Web UI pages shall be optimized for desktop usage, offering clear navigation, real-time feedback on operations, and graceful handling of errors with informative messages.

- [UR-0036] [DELETED]

- [UR-0037] [DELETED]

- [UR-0038] [DELETED]

- [UR-0039] [DELETED]

- [UR-0040] The framework shall provide a mechanism to mark prompts as executed and track execution status in the work iteration registry.

- [UR-0041] The framework shall provide a prompt completion command that transitions prompts to completed state and optionally triggers git commit operations.

- [UR-0042] The Web UI shall display execution status for each prompt and provide a completion button that is enabled only for executed prompts in in-progress state.

- [UR-0043] The framework shall support optional git integration during prompt completion, controlled by a global configuration flag.

- [UR-0044] The framework shall provide easy-to-use launcher scripts for starting the Web UI on both Windows and Linux platforms without requiring manual terminal commands.

- [UR-0045] The Web UI launchers shall automatically open the default web browser when the server starts successfully.

- [UR-0046] The Web UI shall provide a shutdown button to allow users to stop the server without using terminal commands.

- [UR-0047] The framework shall support two prompt states: `active` and `completed`. The `active` state indicates a prompt is currently being worked on, while `completed` indicates finished work.

- [UR-0048] New prompts shall be created in `active` state by default.

- [UR-0049] The framework shall enforce that only one prompt can be in `active` state at any time, ensuring clear focus on current work.

- [UR-0050] The framework shall support creation of modifications for prompts that have completed implementation, enabling small corrections without requiring a new prompt.

- [UR-0051] Each modification shall be stored in a separate markdown file in the prompt folder with naming pattern modification-<ID>.md where ID is a sequential three-digit number.

- [UR-0052] The framework shall maintain a modifications-log.json file in each prompt folder that tracks metadata for all modifications including creation timestamp, status, and completion timestamp.

- [UR-0053] Modifications shall skip questionnaire and planning steps, going directly to implementation to provide a lightweight workflow for small corrections.

- [UR-0054] The framework shall enforce that only one modification can be active at a time per prompt, tracked via the current-modification-id field in the work iteration registry.

- [UR-0055] The Web UI shall display an "Add Modification" button in the active prompt page that is enabled only when implementation-completed is true.

- [UR-0056] The Web UI shall provide a modifications history section showing all modifications with their status, timestamps, and descriptions.

- [UR-0057] The framework shall provide a "modification" execution mode that executes the current modification and logs implementation details to a modification-specific implementation file.

- [UR-0058] The Web UI shall display the "Active Prompt" page as the default landing page when the web portal opens, with "Active Prompt" appearing as the leftmost navigation menu item.

- [UR-0059] The Web UI shall provide the "Create New Prompt" button on the Active Prompt page to enable quick prompt creation from the primary workspace.

- [UR-0060] The framework shall store questionnaire data in JSON format with structured fields for questions, options, pros/cons, recommendations, and user answers to enable programmatic parsing and interactive UI rendering.

- [UR-0061] The Web UI Active Prompt page shall display questionnaires as interactive forms with radio buttons for option selection, custom answer text inputs, and visual indicators for recommendations.

- [UR-0062] User answers to questionnaire questions shall be persisted immediately to the JSON file when selections are made, without requiring a manual save action.

- [UR-0063] The questionnaire form shall display pros and cons for each answer option, show recommended answers with rationale, and allow custom text answers when predefined options are insufficient.

- [UR-0064] The framework shall support both legacy markdown questionnaires (read-only display) and new JSON questionnaires (interactive forms) without requiring migration of historical data.

- [UR-0065] The Web UI questionnaire form shall automatically display the first unanswered question when loading, and shall automatically advance to the next unanswered question after saving an answer to improve workflow efficiency.

- [UR-0066] The Web UI questionnaire form shall use a two-column layout with context and question navigation on the left side and the current question details and answer options on the right side, enabling efficient navigation and better space utilization.

- [UR-0067] The Web UI Active Prompt page shall provide a "View Implementation" button for each modification in the Modifications tab that displays the modification's implementation log file in a read-only modal dialog with monospace font formatting.

- [UR-0068] The framework shall provide a plan mode that allows users to generate implementation plans without proceeding to execution, enabling plan review and approval.

- [UR-0069] The framework shall automatically disable plan mode after the plan generation completes.

- [UR-0070] The framework shall ensure that plan mode and analyze mode are mutually exclusive and cannot be enabled simultaneously for the same prompt.

- [UR-0071] The framework shall prevent enabling plan mode for prompts not in `active` state.

- [UR-0072] The framework shall provide a toggle mechanism to enable/disable plan mode for prompts through the Web UI.

- [UR-0073] The Web UI navigation menu shall remain fixed at the top of the viewport while scrolling, ensuring navigation tabs are always accessible to users. The navbar shall include a subtle bottom shadow to provide visual depth and indicate its floating state.

- [UR-0074] The Web UI shall display all radio button form controls with enhanced visibility through increased size, darker border colors, and interactive visual feedback states including hover, focus, and checked states to improve usability and accessibility across all pages and forms.

- [UR-0075] The Web UI Active Prompt page shall control tab visibility based on workflow state instead of displaying status badges, showing the Questionnaire tab only when questionnaire-generated is true, the Plan tab only when plan-generated is true, the Analysis tab only when analysis-generated is true, the Implementation tab only when implementation-completed is true, and the Modifications tab only when executed is true, while keeping only the Prompt tab always visible.

- [UR-0076] The Web UI Active Prompt page shall display visual indicators for prompt workflow state flags positioned directly above their corresponding execution mode buttons, with each execution mode showing relevant status icons (Clarify mode displaying questionnaire-generated and questionnaire-answered icons, Analyze mode displaying analysis-generated icon, Plan mode displaying plan-generated icon, Implement mode displaying implementation-completed and executed icons, and Modification mode displaying modifications-count and current-modification-id values), providing immediate visibility of the prompt's lifecycle state aligned with each mode's function.

- [UR-0087] [DELETED]

- [UR-0088] [DELETED]

- [UR-0089] The Web UI shall automatically save changes to prompt.md without requiring manual save button clicks, using a combination of debounced auto-save (after 2 seconds of typing inactivity) and immediate save on blur events.

- [UR-0090] The Web UI shall automatically save changes to prompt.md without requiring manual save button clicks, using a combination of debounced auto-save (after 2 seconds of typing inactivity) and immediate save on blur events.

- [UR-0091] The Web UI Workdir page shall display the work iteration registry in a comprehensive, human-readable format showing iteration metadata and a table of all prompts with their states, execution modes, and workflow flags, enabling quick status overview and navigation to individual prompts.








## Technical Requirements

- [TR-0001] The framework shall implement all automation functionality in Python using a domain-based command routing architecture and for the user interface shall use only vanilla JavaScript, HTML, CSS.

- [TR-0002] The framework shall use the `python` command (not `python3`) for executing all internal scripts to ensure cross-platform compatibility.

- [TR-0003] No database is used; all data is stored in Markdown or JSON files.

- [TR-0004] Archived workdirs are stored in `.rdd-instance/archive/`.

- [TR-0005] Prompt templates provided by the framework are stored in `.rdd/prompt-snippets`.

- [TR-0006] The framework shall use `.rdd-instance/specifications/` for storing technical design files. 

- [TR-0007] A technical design form JSON config file `.rdd/config/technical-design-form.json` shall define the content of Technical Specification page and should support definition of form elements with predefined options, multi-select fields, free-text values, conditional logic, and a default-answer mechanism. 

- [TR-0008] Web UI server shall be implemented using Python standard-library components (such as `http.server`) or equivalent, binding to `127.0.0.1` on an available port and automatically opening the user's default browser. 

- [TR-0009] The Web UI server shall expose REST-like JSON endpoints for reading, writing, and updating files in `.rdd-instance/` and for invoking RDD commands.

- [TR-0010] The Web UI server shall generate a session token on startup and require it for all operations to prevent unauthorized access. 

- [TR-0011] The system shall keep the currently installed framework version number in `.rdd/config/manifest.json` at JSONPath "framework.version" using semantic versioning (MAJOR.MINOR.PATCH).

- [TR-0012] The build script shall generate together with the zip file a SHA256 checksum file for each release archive and ensure compatibility with standard `sha256sum` verification tools.

- [TR-0013] The build script shall detect when build artifacts for the same version already exist and allow the user to stop, overwrite, or increment the patch version.

- [TR-0014] The build script shall substitute version placeholders (e.g., `{{VERSION}}`) in template files when constructing installation assets.

- [TR-0015] The system shall store all active workdir files in .rdd-instance/workdir/

- [TR-0016] The framework shall provide scripts for managing file listings: `.rdd/src/actions/files_list_csv_refresh.py` generates a CSV listing stored at `.rdd-instance/specifications/files-list.csv` and `.rdd/src/actions/files_list_csv_set_description.py` updates descriptions for specific files in the CSV.

- [TR-0017] The Web UI shall provide pages for managing prompts, technical specifications, folder structures, requirements, and version-control workflows, backed by the REST endpoints and reflecting the interaction model defined in the Product Requirements Specification.

- [TR-0018] `.rdd-instance/workdir/prompts-registry.md` shall contain completed prompts texts. All other operational state of the prompt is maintained in `.rdd-instance/workdir/work-iteration-registry.json`. The consistency between those two files will be maintained by the scripts in `.rdd/src/`.

- [TR-0019] The framework shall implement safety checks that prevent iteration creation unless the workdir is empty.

- [TR-0020] The framework shall archive each completed iteration in `.rdd-instance/archive/<iteration-id>_<iteration-name>/`.

- [TR-0021] All generated questions shall follow the question-formatting standards defined in `.rdd/conventions/questions-formatting.md`.

- [TR-0022] The framework shall support extracting and displaying repository file lists, technical design content, and requirements content through Web UI components for visualization and editing.

- [TR-0023] The test system shall be implemented entirely in Python using pytest for Python tests with optional coverage reporting.

- [TR-0024] The system shall maintain its test fixtures in a `tests/` directory using isolated temporary directories to prevent modification of product files during test execution.

- [TR-0025] The testing environment shall be created using a Python script that constructs and manages a dedicated virtual environment for testing.

- [TR-0026] All automation scripts shall be stored in the `.rdd/src/` directory.

- [TR-0027] CI/CD Testing: The system shall use GitHub Actions to run tests automatically on push and pull request events, executing only the Python test runner. For the purpose shall exist a file `.github/workflows/tests.yaml` 

- [TR-0028] The CI/CD pipeline shall include a GitHub Actions workflow file `.github/workflows/tests.yaml` configured to run on `pull_request` events targeting the `dev` branch and on manual `workflow_dispatch` triggers.

- [TR-0029] The `.github/workflows/tests.yaml` workflow shall define a job `all-tests-linux` that runs on `ubuntu-latest`, checks out the repository, installs Python 3.9 using `actions/setup-python@v5`, installs BATS, sets up the test environment by running `python .rdd/src/setup-test-env.py`, and executes all tests by running `python .rdd/src/run-tests.py`.

- [TR-0030] The `all-tests-linux` job in `.github/workflows/tests.yaml` shall generate a Python test coverage report by activating the `.venv` virtual environment, running `pytest tests/python/ --cov=.rdd/src --cov=scripts --cov-report=xml --cov-report=term`, and producing a `coverage.xml` file.

- [TR-0031] The `all-tests-linux` job in `.github/workflows/tests.yaml` shall upload the generated `coverage.xml` report using `codecov/codecov-action@v4` with appropriate flags and name metadata, and this upload step shall execute even when previous steps fail.

- [TR-0032] The `.github/workflows/tests.yaml` workflow shall define a job `all-tests-windows` that runs on `windows-latest`, checks out the repository, installs Python 3.9 using `actions/setup-python@v5`, installs the Pester module using PowerShell, sets up the test environment by running `python .rdd/src/setup-test-env.py`, and executes all tests by running `python .rdd/src/run-tests.py`.

- [TR-0033] The `.github/workflows/tests.yaml` workflow shall define a job `test-summary` that runs on `ubuntu-latest`, depends on the completion of `all-tests-linux` and `all-tests-windows`, executes regardless of their success or failure, and prints the final result status of both jobs to the workflow logs.

- [TR-0034] The test framework shall generate code coverage reports for Python code and report coverage metrics in CI/CD pipelines

- [TR-0035] Test runner scripts shall provide colored output (green for success, red for failure, yellow for warnings) to improve readability

- [TR-0036] The system documentation shall provide installation guidance for enabling the `python` command on Linux systems using distribution-appropriate packages such as `python-is-python3`.

- [TR-0037] The build process shall detect existing artifacts (ZIP and checksum files) for the current version before starting a build.

- [TR-0038] When existing build artifacts are detected, the build process shall prompt the user to stop, overwrite the artifacts, or increment the patch version.

- [TR-0039] An empty workdir folder `.rdd-instance/workdir` should exist at the start of each new work iteration

- [TR-0040] The system shall implement a build script that generates cross-platform release zip file following the naming convention `rdd-v{version}.zip`. Releases shall be built by the script `build/build.py`.

- [TR-0041] Build artifacts are generated in the `build/` directory.

- [TR-0042] Releases are distributed as a single cross-platform archive named `rdd-v{version}.zip`. The release zip file includes framework code, installation scripts, templates, and documentation.

- [TR-0043] The framework shall provide a deterministic script `.rdd/src/actions/prompt_create.py` that creates a new prompt by appending a `prompt-metadata` record to `.rdd-instance/workdir/work-iteration-registry.json` and ensuring a corresponding stub record exists in `.rdd-instance/workdir/prompts-registry.md` (creating the file if missing). The created prompt text record shall be a placeholder (e.g., `TBD`) until populated by other tooling.

- [TR-0044] The framework shall provide a deterministic script `.rdd/src/actions/prompt_add_to_registry.py` that reads the prompt.md file and any modification-XXX.md files from a prompt's workdir folder and updates the corresponding record in `.rdd-instance/workdir/prompts-registry.md` following the format defined in `.rdd/conventions/prompts-registry.convention.md`. Modifications shall be appended inline within the same prompt record using `### Modification XXX` markers. The script shall accept an optional `prompt-id=` parameter (defaulting to the active prompt if omitted). The prompt completion workflow in `.rdd/src/actions/prompt_complete.py` shall automatically invoke this script when setting a prompt to completed state.

- [TR-0045] The framework shall create a per-prompt working folder under `.rdd-instance/workdir/` named `<prompt-id>_<prompt-title>` and in it shall create an empty `prompt.md` file when a new prompt is created. Other files (plan.md, questionnaire.json, implementation.md) shall be created by their respective execution modes (plan, clarify, implement) when those modes execute.

- [TR-0046] The framework shall provide a deterministic script `.rdd/src/actions/prompt_set_state.py` that updates the `state` field of a prompt record in `.rdd-instance/workdir/work-iteration-registry.json`. The script shall accept `state=` (required, one of `active|completed`) and optional `prompt-id=` parameters. When `prompt-id=` is omitted, the script shall default to the currently active prompt (the one in `active` state). The script shall enforce the "single active prompt" invariant by failing with a clear error if attempting to set a prompt to `active` when another prompt is already in that state.
  
- [TR-0047] The framework shall provide a main CLI entry point at `.rdd/src/rdd.py` that implements domain-based command routing with support for `prompt` and `workdir` domains.

- [TR-0048] The CLI shall support three execution modes: interactive menu mode (no arguments), domain menu mode (single domain argument), and direct action execution mode (domain and action arguments).

- [TR-0049] The CLI shall provide interactive menus using the curses library for terminal-based navigation with arrow keys, Enter to select, and Q to quit.

- [TR-0050] The CLI shall implement a numeric fallback menu system that activates when curses is unavailable or fails, accepting numeric input (1-N) or 'q' to quit.

- [TR-0051] The CLI shall route domain actions to Python scripts in `.rdd/src/actions/` following the naming convention `<domain>_<action>.py` where action names use underscores instead of hyphens.

- [TR-0052] The framework shall provide wrapper scripts `.rdd/src/rdd.sh` (Linux/macOS) and `.rdd/src/rdd.bat` (Windows) that execute `rdd.py` using the `python` command and forward all arguments.

- [TR-0053] The CLI shall provide a `--help` flag that displays usage documentation including available domains, execution modes, and usage examples.

- [TR-0054] The framework shall provide a script `.rdd/src/actions/prompt_list.py` that displays all prompts from the work iteration registry in a formatted table showing prompt ID, title, state, and type.

- [TR-0055] All CLI error messages shall include both a specific problem description and suggested remediation steps.

- [TR-0056] All Python functions in the CLI implementation shall include comprehensive docstrings describing purpose, parameters, return values, and any exceptions raised.

- [TR-0057] [DELETED]

- [TR-0058] [DELETED]

- [TR-0059] [DELETED]

- [TR-0060] [DELETED]

- [TR-0061] The framework shall provide a web server implementation at `.rdd/src/web/server.py` that serves the web interface on localhost port 8080 (configurable via --port parameter) and automatically opens the default browser on startup.

- [TR-0062] The web server shall implement API endpoints including GET /api/token for session token retrieval, GET /api/registry for work iteration registry access, GET /api/file/{filepath} for reading files from .rdd-instance, POST /api/action for executing RDD actions, and POST /api/file/save for saving files to .rdd-instance.

- [TR-0063] The web interface shall be implemented using vanilla JavaScript, HTML, and Bootstrap 5 CSS framework, with all frontend assets located in `.rdd/src/web/static/` (app.js, style.css) and templates in `.rdd/src/web/templates/` (index.html).

- [TR-0064] The web interface shall provide a responsive navigation bar with sections for Active Prompt, Workdir, Technical Design, Requirements, and Help, with each section displaying relevant operations and status information with color-coded alerts (success: green, error: red, warning: yellow, info: blue).

- [TR-0065] The Prompts section shall display all prompts in a table showing ID, title, type, state, parent ID, and actions, with buttons for creating new prompts and setting prompt states via modal dialogs.

- [TR-0066] The Workdir section shall provide a button to create new work iterations via a modal dialog, archiving current iterations with confirmation dialog, displaying current iteration status including iteration ID, name, total prompts, and next prompt ID, and a file viewer with quick access buttons for common files (registry, requirements, technical design), a text editor for viewing and editing file contents, and save functionality.

- [TR-0067] [DELETED]

- [TR-0068] [DELETED]

- [TR-0069] The Prompts section shall provide an integrated prompt editor that displays Edit buttons for prompts in `active` state and View buttons for prompts in `completed` state.

- [TR-0070] The prompt editor shall replace the prompts list view with a tabbed interface containing tabs for prompt.md, plan.md, questionnaire.md, and implementation.md files, with a Back button to return to the prompts list.

- [TR-0071] The prompt editor shall load prompt files from the prompt's working folder (workdir/<prompt-id>_<prompt-title>/) and display their contents in monospace textareas within the appropriate tabs.

- [TR-0072] The prompt editor shall provide individual Save buttons for plan.md and questionnaire.md files that persist changes back to the file system when clicked, while prompt.md uses automatic save functionality.

- [TR-0073] The implementation.md file in the prompt editor shall be displayed as read-only in all cases.

- [TR-0074] The prompt editor shall enforce frontend soft enforcement of edit permissions by setting textareas to readonly and disabling save buttons when in view-only mode (for completed prompts).

- [UR-0077] The framework shall provide a toggle mechanism to enable/disable analyze mode for prompts through the Web UI.

- [UR-0078] The framework shall automatically disable analyze mode after each analyze execution completes.

- [UR-0079] The framework shall prevent enabling analyze mode for prompts not in `active` state.

- [TR-0075] [DELETED]

- [TR-0076] [DELETED]

- [TR-0077] [DELETED]

- [TR-0078] The Web UI shall display analyze mode toggles only for prompts in `active` state.

- [TR-0079] The Prompts section table in the Web UI shall include an "Analyze Mode" column with a toggle switch for `active` prompts and "N/A" for `completed` prompts.

- [TR-0080] [DELETED]

- [TR-0081] [DELETED]

- [TR-0082] [DELETED]

- [TR-0083] Each prompt object in the work iteration registry shall include an `executed` boolean field (default: false) to track execution status.

- [TR-0084] The framework shall provide a script `.rdd/src/actions/prompt_set_executed_on.py` that sets the executed flag for a specified prompt or the active prompt.

- [TR-0085] The framework shall provide a script .rdd/src/actions/prompt_complete.py that sets a prompt to completed state and conditionally executes git commit based on the git-enabled flag from .rdd-instance/config/instance-config.json

- [TR-0086] The prompt completion action shall handle git commit failures gracefully, logging warnings but proceeding with state changes when no repository changes exist.

- [TR-0087] The Web UI Prompts section table shall include an "Executed" column displaying a badge indicating whether each prompt has been executed (green "Yes" or gray "No").

- [TR-0088] The Web UI shall provide a "Complete" button in the Actions column for prompts in `active` state, enabled only when the prompt's executed flag is true, with a tooltip explaining the requirement.
- [TR-0089] Each prompt in work-iteration-registry.json shall have a `plan-enabled` boolean field with default value `false`.

- [TR-0090] The framework shall provide scripts `prompt_plan_on.py` and `prompt_plan_off.py` in `.rdd/src/actions/` for controlling plan mode.

- [TR-0091] The execution prompt logic shall read plan mode from the `plan-enabled` field in work-iteration-registry.json and execute only the plan generation step when enabled.

- [TR-0092] The Web UI shall display plan mode toggles only for prompts in `active` state.

- [TR-0093] The Prompts section table in the Web UI shall include a "Plan Mode" column with a toggle switch for `active` prompts and "N/A" for `completed` prompts.

- [TR-0094] [DELETED]

- [TR-0095] The plan execution step shall automatically invoke the prompt_plan_off.py script after completing the plan generation to disable the plan flag.

- [TR-0096] When enabling plan mode, the system shall automatically disable analyze mode if it is currently enabled, and vice versa, to enforce mutual exclusivity.

- [TR-0097] The framework shall provide launcher scripts `run.bat` for Windows and `run.sh` for Linux located in the `.rdd/` directory.

- [TR-0098] The launcher scripts shall execute `.rdd/src/web/server.py` using the `python` command with automatic browser opening enabled.

- [TR-0099] The launcher scripts shall display clear error messages and keep the console/terminal window open when errors occur to allow users to read the error information.

- [TR-0100] The Web UI server shall support automatic detection of available ports and use a fallback mechanism if the default port is occupied.

- [TR-0101] The Web UI shall implement a POST /api/shutdown endpoint that gracefully stops the web server when invoked.

- [TR-0102] The Linux launcher script `run.sh` shall include proper shebang (`#!/bin/bash`) and require executable permissions to be set before use.

- [TR-0103] The `prompt_set_state.py` script shall accept only `active` or `completed` as valid state values.

- [TR-0104] The framework shall allow bidirectional state transitions between `active` and `completed` states without restrictions.

- [TR-0105] The `prompt_create.py` script shall validate that no other prompt is in `active` state when creating a new prompt, and shall fail with a clear error message if validation fails.
- [TR-0106] The framework shall not distinguish between different types of prompts. All prompts shall be treated equally without type classification or parent-child relationships.
- [TR-0107] The framework shall provide Python action scripts modification_create.py, modification_list.py, and modification_complete.py in .rdd/src/actions/ for managing modifications.

- [TR-0108] The work-iteration-registry.json schema shall include current-modification-id and modifications-count fields for each prompt entry to track modification state.

- [TR-0109] The modifications-log.json file shall store an array of modification metadata objects with fields modification-id, created, status, and completed timestamps in ISO8601 format.

- [TR-0110] The modification_create.py script shall validate that implementation-completed is true before allowing modification creation and shall fail with a clear error message if validation fails.

- [TR-0111] The modification_create.py script shall increment the modifications-count field and set current-modification-id when creating a new modification.

- [TR-0112] The modification_complete.py script shall update the modifications-log.json with completion timestamp, set status to completed, and reset current-modification-id to null.

- [TR-0113] The execution prompt logic in .rdd/prompt-snippets/execution.md shall include a modification execution mode that follows instructions in .rdd/prompt-snippets/execution-step.modification.md.

- [TR-0114] The Web UI shall provide /api/modification/create and /api/modification/list endpoints that invoke the corresponding action scripts and return JSON responses.

- [TR-0115] The prompt_set_execution_mode.py script shall support "modification" as a valid execution mode value in addition to no-action, analyze, plan, and implement.

- [UR-0080] The Web UI shall allow users to edit the description of in-progress modifications directly from the modifications list.

- [UR-0081] The Web UI shall display an "Edit" button for modifications with status not equal to "completed" in the modifications history section.

- [TR-0116] The Web UI shall provide inline editing capability for modification descriptions using a textarea with Save and Cancel buttons.

- [TR-0117] The Web UI shall provide /api/modification/update endpoint that accepts modificationId and description parameters and updates the corresponding modification file.

- [TR-0118] The modification edit functionality shall validate that the description is not empty before allowing save operation.
- [TR-0119] Questionnaire JSON files shall follow the schema defined in `.rdd/conventions/questionnaire-json-schema.md` with root-level `context` and `questions` array fields.

- [TR-0120] Each question object in the JSON shall include: `id`, `question-text`, `options` array, `recommended-option`, `recommendation-rationale`, and `user-selection` object with `type` and `value` fields.

- [TR-0121] Question options shall be stored as an array of objects with `id`, `label`, `pros`, and `cons` fields for each option.

- [TR-0122] User selections shall be stored as an object with `type` field ("predefined", "custom", or null) and `value` field containing the selected option ID or custom text.

- [TR-0123] The Web UI shall render questionnaire forms using Bootstrap accordion components with individual panels for each question, displaying options as radio buttons with associated pros/cons text.

- [TR-0124] The questionnaire form shall implement immediate persistence using the existing `/api/file/save` endpoint, updating the entire JSON file when user selections change.

- [TR-0125] Custom answer text inputs shall use explicit save buttons rather than debounced auto-save to ensure users confirm their custom text submissions.

- [TR-0126] The clarify execution step in `.rdd/prompt-snippets/execution-step.clarify.md` shall generate questionnaire data in JSON format stored as `questionnaire.json` in the prompt's working folder.

- [TR-0127] [DELETED]

- [TR-0128] The Web UI Active Prompt page shall detect questionnaire file type (.json vs .md) and render interactive forms for JSON files while displaying markdown files as read-only text for legacy support.

- [TR-0129] The framework shall provide a script `.rdd/src/actions/files_list_csv_refresh.py` that generates a CSV listing of all repository files and stores it at `.rdd-instance/specifications/files-list.csv`, excluding directories beginning with `.` and directories named `venv`, and listing for each entry: `File Name` (file name), `Relative Path` (relative path from repository root), `Modification Time` (file modification timestamp in ISO8601 format), and `Description` (manually-maintained description field).

- [TR-0130] The `files_list_csv_refresh.py` script shall update the CSV file incrementally by adding new files with empty descriptions, updating modification times and clearing descriptions for modified files, removing deleted files, and preserving descriptions for unchanged files.

- [TR-0131] The framework shall provide a script `.rdd/src/actions/files_list_csv_set_description.py` that accepts `file-name=`, `relative-path=`, and `description=` parameters and updates the Description field for the matching entry in `.rdd-instance/specifications/files-list.csv`.

- [TR-0132] The files listing CSV shall use tab character as field delimiter and shall be stored with UTF-8 encoding to support international characters in file names and descriptions.
- [UR-0082] The Web UI shall provide a snippet insertion feature for the prompt editor that enables users to insert predefined prompt snippet keys through an autocomplete dropdown interface. The autocomplete shall trigger when user types '[[[' and display available snippets with preview content. The system shall validate snippet keys against manifest.json on save and warn about invalid keys.

- [UR-0083] The Web UI shall provide a Help tab that displays the user guide to assist users in understanding how to work with the RDD framework through the Web UI and VS Code.

- [UR-0084] The user guide shall focus on practical Web UI workflows without exposing technical implementation details, providing multiple short workflow examples for different development scenarios including creating prompts, using plan mode, working with modifications, and completing prompts.

- [UR-0085] The framework shall use sequential numeric requirement identifiers with category prefixes (UR, TR) and 4-digit zero-padding to ensure unique, compact, and easily referenceable requirement IDs.

- [UR-0086] The framework shall determine the next available requirement ID by scanning the existing requirements file to find the highest ID in each category, ensuring uniqueness without requiring separate state tracking.

- [TR-0133] The web server shall provide a GET /api/help/user-guide endpoint that reads `.rdd/docs/user-guide.md`, converts it to HTML using a Python-based markdown converter, and returns the rendered HTML in JSON format.

- [TR-0134] The Help tab shall be positioned after the Files tab in the Web UI navigation bar and shall automatically load and display the rendered user guide when accessed.

- [TR-0135] The user guide markdown rendering shall be performed server-side using a lightweight markdown-to-HTML converter implemented in Python without requiring external dependencies beyond the standard library.
- [TR-0136] The markdown-to-HTML converter shall escape special HTML characters (apostrophes, quotes, ampersands, angle brackets) exactly once to prevent XSS vulnerabilities while ensuring correct display without double-escaping (e.g., apostrophes shall render as ' not as &#x27;).

- [TR-0137] Radio button styles in `.rdd/src/web/static/style.css` shall define enhanced visibility CSS rules for `.form-check-input[type="radio"]` elements with increased size (1.25em width and height), thicker borders (2px), darker border colors (#495057), and comprehensive interactive state styling including hover (primary blue border with light background), focus (primary blue border with box-shadow), and checked (primary blue background with border and subtle shadow) states to ensure visibility and accessibility compliance.

- [TR-0138] The Web UI Active Prompt page shall implement tab visibility control through JavaScript by dynamically showing or hiding tab navigation items based on prompt workflow state flags (questionnaire-generated, plan-generated, analysis-generated, implementation-completed, executed), removing the previous status badge indicators, and ensuring that the currently active tab remains selected when tab visibility changes.

- [TR-0139] The framework shall provide a "clarify" execution mode that generates a questionnaire to clarify ambiguous or missing information in the active prompt.

- [TR-0140] The framework shall provide an "analyze" execution mode that generates an analysis.md file containing copilot review, best practices research, GitHub samples, proposals, and prompt modifications.

- [TR-0141] The framework shall track whether analysis has been generated for each prompt using an "analysis-generated" boolean flag in the work iteration registry, positioned after "plan-generated" and before "implementation-completed" for consistency.

- [TR-0142] The clarify and analyze modes shall automatically reset execution-mode to "no-action" after completion, following the same pattern as plan and implement modes.

- [TR-0143] The analyze mode shall NOT execute prompt_set_executed_on.py after completion, as analysis is documentation generation, not implementation execution.

- [TR-0144] The framework shall provide a script `.rdd/src/actions/prompt_analysis_generated_on.py` that sets the analysis-generated flag to true for the active or specified prompt in the work iteration registry.

- [TR-0145] The execution orchestration file `.rdd/prompt-snippets/execution.md` shall include both clarify and analyze modes, with clarify referencing `.rdd/prompt-snippets/execution-step.clarify.md` and analyze referencing `.rdd/prompt-snippets/execution-step.analyze.md`.

- [TR-0146] The Web UI Active Prompt page shall display an analysis-generated flag icon in the workflow status indicators and show an Analysis tab that becomes visible when analysis-generated is true.

- [TR-0147] The Web UI execution mode selector shall provide both "Clarify" and "Analyze" mode options, replacing the previous single "Analyze" mode which has been renamed to "Clarify".

- [TR-0148] The prompt snippet key [[[ANALYZE]]] shall be removed from the manifest.json promptSnippets array, as analyze is now an execution mode invoked via execution-mode setting, not a user-insertable prompt snippet.
- [TR-0149] The Web UI Active Prompt page shall display execution mode buttons with consistent visual styling, using secondary outline style for inactive buttons and primary solid background for the active button, with smooth transitions and hover effects to improve user interaction clarity.

- [TR-0150] The Web UI Active Prompt page shall order tabs in the logical execution workflow sequence: Prompt, Questionnaire, Analysis, Plan, Implementation, Modifications, enabling users to navigate through the prompt lifecycle in a natural progression.

- [TR-0151] The framework shall provide a script `.rdd/src/actions/questionnaire_check_complete.py` that validates whether all questions in a prompt's questionnaire.json have been answered by checking that each question's user-selection.type field is not null, and automatically sets the questionnaire-answered flag to true when all questions are answered or false otherwise.

- [TR-0152] The Web UI shall call the questionnaire validation script via the /api/action endpoint after each questionnaire answer is saved to automatically update the questionnaire-answered flag based on completion status.

- [TR-0153] The questionnaire validation script shall accept an optional prompt-id parameter and default to the active prompt when the parameter is omitted, following the same pattern as other prompt action scripts.

- [TR-0154] Requirement IDs shall follow the format <PREFIX>-<NUMBER> where PREFIX is UR or TR and NUMBER is a 4-digit zero-padded sequential integer (e.g., UR-0001, TR-0042).

- [TR-0155] The requirements convention file shall specify the requirement ID format, padding rules, and uniqueness guarantees to ensure consistent ID generation across all framework operations.

- [TR-0156] Requirement ID generation shall scan requirements.md using regex pattern `\[(UR|TR)-(\d{4})\]` to extract existing IDs and calculate the next available ID per category.

- [TR-0157] The framework shall provide deterministic Python scripts for requirement management (requirement_ur_create.py, requirement_ur_modify.py, requirement_ur_delete.py, requirement_tr_create.py, requirement_tr_modify.py, requirement_tr_delete.py) that enforce format consistency, prevent ID conflicts, and provide atomic file operations with validation.

- [TR-0158] The prompt.md editor shall implement auto-save using a 2-second debounce delay combined with immediate save on textarea blur events, with deduplication to prevent saving unchanged content.

- [TR-0159] The prompt.md editor shall display a dynamic status indicator showing the current save state (Editing, Saving, Saved, Error) instead of a manual save button.

- [TR-0160] The prompt.md auto-save shall run snippet validation asynchronously and display validation results (invalid snippet count) in the status indicator without blocking the save operation.

- [TR-0161] The prompt.md auto-save error state shall provide a manual retry option via a clickable link in the status indicator.

- [TR-0162] The framework shall provide a seed script at .rdd/src/actions/rdd-instance_seed.py that validates and initializes the RDD instance structure by creating missing folders and files based on manifest.json configuration

- [TR-0163] The seed script shall create folders recursively using mkdir -p semantics, ensuring all parent directories are created as needed

- [TR-0164] The seed script shall preserve existing files without modification, implementing idempotent behavior safe for repeated execution

- [TR-0165] The seed script shall validate JSON files after creation using JSON parsing and verify UTF-8 encoding for Markdown files

- [TR-0166] The seed script shall fail fast with specific error messages and exit code 1 when manifest.json is missing, malformed, or references non-existent convention files

- [TR-0167] The seed script shall support a --verbose flag for DEBUG level logging and provide summary output showing folder and file creation statistics

- [TR-0168] The web server startup sequence shall execute the seed script before starting the HTTP server and abort startup if seeding fails with non-zero exit code

- [TR-0169] The seed script shall complete initialization in under 100ms for typical cases where all required files and folders already exist

- [TR-0170] The framework shall store instance-level configuration in .rdd-instance/config/instance-config.json file containing a git-enabled boolean flag

- [TR-0171] The framework shall read the git-enabled setting from .rdd-instance/config/instance-config.json to determine whether to perform git operations during prompt completion

- [TR-0172] The framework shall validate the presence of .rdd-instance/config/ folder and instance-config.json file during manifest validation and provide clear error messages directing users to re-seed if missing















