# Product Name

RDD Framework

# Product Overview

The product is a system that serves to be installed the RDD framework in a software code repository (with or without git versioning).

The RDD framework aims to standardize execution of user defined tasks to GitHub copilot in form of prompts, maintain full traceability of prompt history, and provide a simplified developer experience through a unified execution model and a web-based interface. 

The framework enables:

* Persistent storage of prompts,
* Automated maintenance of requirements and technical specifications,
* A unified execution command (`execute command`),
* Web-based configuration and prompt management,
* Multi-platform support on Windows and Linux.

# Definitions, Acronyms, and Abbreviations

* **RDD** – Requirements-Driven Development

* **System** - A repository with scripts for test, build and release preparation of an installation of RDD framework

* **Framework** - In the context of the current document and code repository - the set of files and principles for realization of RDD development

* **RDD instance** - A folder holding the RDD related files specific for the current product

* **Prompt** – A developer-issued instruction for the copilot

* **Technical Design** – Structured JSON defining architectural decisions

* **Questionnaire** – A set of questions generated to clarify missing or ambiguous information

* **execute command** - A github prompt, which is the only prompt executed in GitHub Copilot chat window and which includes instructions how the copilot to understand the needed context and actions.

* **active prompt** - The prompt in `.rdd-instance/workdir/work-iteration-registry.json` which is with status `planned` or `in-progress`. The framework allows only one prompt to be in some of those statuses and this prompt is considered to be the `active prompt`

* **requirements file** - The file `.rdd-instance/specifications/requirements.md` which contains user and technical requirements and is formatted accordingly `.rdd/conventions/requirements.convention.md`

* **working directory** - The framework shall maintain a working directory `.rdd-instance/workdir` for active development work files.

* **prompt-snippets** - Reusable prompt snippets or whole prompts stored in `.rdd/prompt-snippets/`.

* **technical-design** - A file providin technical specificationa and constraints in a structured JSON format located in `.rdd-instance/specifications/technical-design.json`

* **files-and-folders** - The product files and folders structure documented in `.rdd-instance/specifications/files-and-folders.md`

* **prompt-implementation-plan** - A file with the exact steps which the copilot should execute



# Functional Requirements

- [UR-001] The framework shall define RDD (Requirement Driven Development) as a set of prompts, scripts, and workflows enabling a developer to use an LLM-based copilot for software development.

- [UR-002] The framework shall maintain a library of predefined framework prompt parts. The framework shall persist all prompts as Markdown files authored through the Web UI to ensure full historical traceability.

- [UR-003] The framework shall load, apply, and update `requirements file` automatically during each prompt execution.

- [UR-004] The framework shall provide a web-based user interface for creating, editing, and managing prompts, questionnaires, implementation plans, technical specifications, file structure, requirements, and working directory control operations. The Web UI shall provide a modern, responsive interface optimized for desktop browsers, with clear navigation between pages, real-time feedback on operations, color-coded status indicators (success: green, error: red, warning: yellow, info: blue), and graceful error handling with user-friendly messages.

- [UR-005] The framework shall provide a single prompt implementing the `execute command`, that initiates all copilot-related operations using the `active prompt`. 

- [UR-006] The framework shall operate on both Windows and Linux.

- [UR-007] The framework shall provide visualization and controlled modification of the `rdd instance` files through the Web UI.

- [UR-008] The framework shall support reverse-engineering requirements from the existing product state.

- [UR-009] The framework shall archive `working directory` content at the end of the current iteration for historical reference. The system shall create a dedicated archive directory during the work iteration archiving.

- [UR-010] Prompts shall call scripts for file and folder modifications or other deterministic actions rather than the copilot to implementing the logic.

- [UR-011] The system shall clear the workdir folder after archiving by removing all files and subdirectories inside `working directory`.

- [UR-012] The framework must maintain a `requirements file` and automatically update it after each prompt execution. During each execution, the framework must also load and apply the existing requirements.

- [UR-013] The system documentation shall include Linux installation guidance for enabling the `python` command using the appropriate system package.

- [UR-014] The framework shall provide CLI commands on top of the UI interface.

- [UR-015] The system shall provide a Python-based test runner capable of executing all test types across platforms without requiring third-party shell testing frameworks.

- [UR-016] The system shall provide a functionality for creation of a JSON listing of the repository or workdir files via a dedicated command.

- [UR-017] The Web UI shall provide a Prompt Management page enabling loading, editing, saving, questionnaire interaction, and plan review for the `active prompt`. 

- [UR-018] The Web UI shall provide a Technical Specification page enabling editing of `technical-design` using a configuration-driven interactive form. 

- [UR-019] The Web UI shall provide a File & Folder Structure page enabling visualization and controlled modification of the product's `files-and-folders`. 

- [UR-020] When the `execute command` generates a questionnaire, the Web UI shall present the questionnaire with input fields and persist responses back to the questionnaire file.

- [UR-021] The Web UI shall be able to display the `prompt-implementation-plan`, allow edits, and provide approval or regeneration options. 

- [UR-022] The Web UI shall display technical design, requirements, and file structure content and allow controlled user edits.

- [UR-023] The system shall check existing content in `requirements file`  before generating clarification questions to avoid redundant queries.

- [UR-024] The `technical-design` configuration JSON shall support conditional and hierarchical logic, enabling form fields to appear or change behavior based on previously selected answers.

- [UR-025] The Web UI should provide a Technical Specification page for editing of `technical-design`. It shall provide a “Set Default Answers” function that automatically populates all unanswered design fields with their configured default values.

- [UR-026] The framework shall provide smooth developer experience, minimizing technical overhead for requirement clarification

- [UR-027] Error messages shall include specific problem description and suggested remediation steps

- [UR-028] All destructive operations shall create backups before proceeding

- [UR-029] Scripts shall validate prerequisites before executing operations

- [UR-030] Scripts shall handle errors gracefully and provide recovery guidance

- [UR-031] The Web UI and installers shall provide clear, color-coded feedback for success, error, warning, or informational messages to improve user comprehension.

- [UR-032] Interactive menus used in CLI components shall support curses-based navigation with fallback to numeric input when curses is not available.

- [UR-033] The test runner shall provide colored output indicating success, failure, and warnings to improve readability during test execution.

- [UR-034] The installation process shall provide clear, user-friendly explanations of all required decisions and actions during installation.

- [UR-035] All Web UI pages shall be optimized for desktop usage, offering clear navigation, real-time feedback on operations, and graceful handling of errors with informative messages.




# Technical Requirements

- [TR-001] The framework shall implement all automation functionality in Python using a domain-based command routing architecture and for the user interface shall use only vanilla JavaScript, HTML, CSS.

- [TR-002] The framework shall use the `python` command (not `python3`) for executing all internal scripts to ensure cross-platform compatibility.

- [TR-003] No database is used; all data is stored in Markdown, JSON, or JSONL files.

- [TR-004] Archived workdirs are stored in `.rdd-instance/archive/`.

- [TR-005] Prompt templates provided by the framework are stored in `.rdd/prompt-snippets`.

- [TR-006] The framework shall use `.rdd-instance/specifications/` for storing technical design files. 

- [TR-007] A technical design form JSON config file `.rdd/config/technical-design-form.json` shall define the content of Technical Specification page and should support definition of form elements with predefined options, multi-select fields, free-text values, conditional logic, and a default-answer mechanism. 

- [TR-008] Web UI server shall be implemented using Python standard-library components (such as `http.server`) or equivalent, binding to `127.0.0.1` on an available port and automatically opening the user's default browser. 

- [TR-009] The Web UI server shall expose REST-like JSON endpoints for reading, writing, and updating files in `.rdd-instance/` and for invoking RDD commands.

- [TR-010] The Web UI server shall generate a session token on startup and require it for all operations to prevent unauthorized access. 

- [TR-011] [DELETED]

- [TR-012] The installer shall be implemented as a Python script that automates installation steps, including copying framework files, and updating `.gitignore`.

- [TR-013] The installer shall validate prerequisites including Python availability, Git availability when the configured mode requires it, and validity of the installation target directory.

- [TR-014] The installer shall support selecting the installation target directory via a Tkinter folder browser with fallback to manual text entry when GUI mode is unavailable.

- [TR-015] The installer shall warn users when an existing RDD installation is detected and list the files that will be overwritten or preserved.

- [TR-016] The installer shall archive all the files from the existing RDD version folders into `.rdd-instance/archive/replaced_version_files_<timestamp>/` during upgrades. This includes at least folders `.github`, `.rdd`, `.rdd-instance`, `.vscode` (if exists)

- [TR-017] The system shall store the currently installed framework version in `.rdd/config/manifest.json` key "framework.version" using semantic versioning (MAJOR.MINOR.PATCH).

- [TR-018] The system shall implement a build script (`build/build.py`) that generates cross-platform release zip file following the naming convention `rdd-v{version}.zip`.

- [TR-019] The build script shall generate together with the zip file a SHA256 checksum file for each release archive and ensure compatibility with standard `sha256sum` verification tools.

- [TR-020] The build script shall detect when build artifacts for the same version already exist and allow the user to stop, overwrite, or increment the patch version.

- [TR-021] The build script shall substitute version placeholders (e.g., `{{VERSION}}`) in template files when constructing installation assets.

- [TR-022] The system shall store all active workdir files in .rdd-instance/workdir/

- [TR-023] The framework shall provide a command to generate a JSON listing of repository or workdir files and store it at `.rdd-instance/workdir/files-list.json`, excluding directories beginning with `.` and directories named `venv`, and listing for each entry: `type` (file type - like 'txt', 'md', 'csv', 'xlsx', 'pdf', 'json', 'py', 'html', 'js', 'css' and others), `name` (file name), `relpath` (relative path), and `mtime` (modification time) in ISO8601 UTC format.

- [TR-025] The Web UI shall provide pages for managing prompts, technical specifications, folder structures, requirements, and version-control workflows, backed by the REST endpoints and reflecting the interaction model defined in the Product Requirements Specification.

- [TR-026] `.rdd-instance/workdir/prompts-registry.md` shall contain prompts texts. All other operational state of the prompt is maintained in `.rdd-instance/workdir/work-iteration-registry.json`. The consistency between those two files will be maintained by the scripts in `.rdd/src/`.

- [TR-027] The framework shall implement safety checks that prevent iteration creation unless the workdir is empty.

- [TR-028] The framework shall archive each completed iteration in `.rdd-instance/archive/<iteration-name>/`.

- [TR-029] All generated questions shall follow the question-formatting standards defined in `.rdd/conventions/questions-formatting.md`.

- [TR-030] The framework shall provide utility functions for reading and updating configuration values, including but not limited to `get_rdd_config`, `set_rdd_config`, and configuration-path helpers.

- [TR-031] The framework shall support extracting and displaying repository file lists, technical design content, and requirements content through Web UI components for visualization and editing.

- [TR-032] The test system shall be implemented entirely in Python using pytest for Python tests with optional coverage reporting, and shall avoid dependencies on shell-based test frameworks.

- [TR-033] The system shall maintain its test fixtures in a `tests/` directory using isolated temporary directories to prevent modification of product files during test execution.

- [TR-034] The testing environment shall be created using a Python script that constructs and manages a dedicated virtual environment for testing.

- [TR-035] The test environment shall install dependencies listed in `tests/requirements.txt` and execute builds and installation tests in isolation from the developer’s system environment.

- [TR-036] All automation scripts shall be stored in the `.rdd/src/` directory.

- [TR-037] [DELETED]

- [TR-038] CI/CD Testing: The system shall use GitHub Actions to run tests automatically on push and pull request events, executing only the Python test runner. For the purpose shall exist a file `.github/workflows/tests.yaml` 

- [TR-039] The CI/CD pipeline shall include a GitHub Actions workflow file `.github/workflows/tests.yaml` configured to run on `pull_request` events targeting the `dev` branch and on manual `workflow_dispatch` triggers.

- [TR-040] The `.github/workflows/tests.yaml` workflow shall define a job `all-tests-linux` that runs on `ubuntu-latest`, checks out the repository, installs Python 3.9 using `actions/setup-python@v5`, installs BATS, sets up the test environment by running `python .rdd/src/setup-test-env.py`, and executes all tests by running `python .rdd/src/run-tests.py`.

- [TR-041] The `all-tests-linux` job in `.github/workflows/tests.yaml` shall generate a Python test coverage report by activating the `.venv` virtual environment, running `pytest tests/python/ --cov=.rdd/src --cov=scripts --cov-report=xml --cov-report=term`, and producing a `coverage.xml` file.

- [TR-042] The `all-tests-linux` job in `.github/workflows/tests.yaml` shall upload the generated `coverage.xml` report using `codecov/codecov-action@v4` with appropriate flags and name metadata, and this upload step shall execute even when previous steps fail.

- [TR-043] The `.github/workflows/tests.yaml` workflow shall define a job `all-tests-windows` that runs on `windows-latest`, checks out the repository, installs Python 3.9 using `actions/setup-python@v5`, installs the Pester module using PowerShell, sets up the test environment by running `python .rdd/src/setup-test-env.py`, and executes all tests by running `python .rdd/src/run-tests.py`.

- [TR-044] The `.github/workflows/tests.yaml` workflow shall define a job `test-summary` that runs on `ubuntu-latest`, depends on the completion of `all-tests-linux` and `all-tests-windows`, executes regardless of their success or failure, and prints the final result status of both jobs to the workflow logs.

- [TR-045] The test framework shall generate code coverage reports for Python code and report coverage metrics in CI/CD pipelines

- [TR-046] Test runner scripts shall provide colored output (green for success, red for failure, yellow for warnings) to improve readability

- [TR-047] [DELETED]

- [TR-048] The system documentation shall provide installation guidance for enabling the `python` command on Linux systems using distribution-appropriate packages such as `python-is-python3`.

- [TR-049] Release archives shall include framework directories, GitHub Copilot prompt templates, VS Code settings templates, the README, LICENSE, and the Python installer script.

- [TR-050] The framework shall include cross-platform installation louncher scripts (`install.sh` for Linux/macOS and `install.bat` for Windows) that check for Python availability and execute the Python installer.

- [TR-051] [DELETED]

- [TR-052] During upgrades, the installer shall detect obsolete files from previous RDD versions and archive them in `.rdd-instance/archive/installation_<version>/`.

- [TR-053] The installer shall inform the user when obsolete files are archived.

- [TR-054] The build process shall detect existing artifacts (ZIP and checksum files) for the current version before starting a build.

- [TR-055] When existing build artifacts are detected, the build process shall prompt the user to stop, overwrite the artifacts, or increment the patch version.

- [TR-056] An empty workdir folder `.rdd-instance/workdir` should exist at the start of each new work iteration

- [TR-057] During work itteration, files are freely added or modified within the workdir folder.

- [TR-058] At completion, the entire workdir folder is archived as a full snapshot of its final state.

- [TR-059] After archiving, the workdir folder is fully cleaned by removing all files and folders in it.

- [TR-060] Archives preserve the complete workdir folder state exactly as it existed before archiving.

- [TR-061] Releases are built using the script `build/build.py`.

- [TR-062] Build artifacts are generated in the `build/` directory.

- [TR-063] Releases are distributed as a single cross-platform archive named `rdd-v{version}.zip`. The release zip file includes framework code, installation scripts, templates, and documentation.