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

* **Prompt** – A developer-issued instruction for the copilot

* **Technical Design** – Structured JSON defining architectural decisions

* **Questionnaire** – A set of questions generated to clarify missing or ambiguous information

* **execute command** - A github prompt, which is the only prompt executed in GitHub Copilot chat window and which includes instructions how the copilot to understand the needed context and actions.

* **active prompt** - The prompt in `.rdd-instance/workdir/work-iteration-registry.json` which is with status `planned` or `in-progress`. The framework allows only one prompt to be in some of those statuses and this prompt is considered to be the `active prompt`


# General Functionalities

- [GF-001] The framework shall define RDD (Requirement Driven Development) as a set of prompts, scripts, and workflows enabling a developer to use an LLM-based copilot for software development.

- [GF-002] The framework shall persist all prompts as Markdown files authored through the Web UI to ensure full historical traceability.

- [GF-003] The framework shall maintain a workdir directory (.rdd-instance/workdir/) for active development work on enhancements and fixes.

- [GF-004] The framework shall archive completed workdir content for historical reference.

- [GF-005] The framework shall support update of `.rdd-instance/specifications/requirements.md` file according the `execute command` work.

- [GF-006] The framework shall load, apply, and update requirements automatically during each prompt execution.

- [GF-007] The framework shall maintain and update the technical design and technical specification in dedicated files as part of prompt execution workflows.

- [GF-008] The framework shall provide a web-based user interface for creating, editing, and managing prompts, questionnaires, implementation plans, technical specifications, file structure, requirements, and workdir/version control operations.

- [GF-009] The framework shall require that all prompts are authored through the Web UI and stored in a Markdown file, preventing ad-hoc prompt text in copilot chat from being treated as canonical input.

- [GF-010] The framework shall provide a structured workflow for clarifying requirements through iterative questioning based on a clarity taxonomy.

- [GF-011] The framework shall provide a single command, `execute`, that initiates all copilot-related operations using the `active prompt`. 

- [GF-012] [DELETED]

- [GF-013] The framework shall provide all user interactions, except command execution, through a browser-based user interface rather than terminal menus.

- [GF-014] The framework shall operate on both Windows and Linux.

- [GF-015] The framework shall allow visualization and controlled modification of the project folder structure through the Web UI.

- [GF-016] The framework shall support adding new requirements and reverse-engineering requirements from the existing project state.

- [GF-017] The framework shall support git branch creation, updates from the default branch, commits, merges, workdir archiving, and workdir loading through the Web UI.

- [GF-018] The framework shall provide configuration and administrative options through a dedicated administration interface in the Web UI.

- [GF-019] The framework shall maintain a library of predefined framework prompts in the .rdd/prompt-templates directory and allow loading any such prompt into the `active prompt` file.

- [GF-020] The framework shall support operation in three modes—No Git, Local Git Only, and Local Git plus Remote GitHub—and enforce the selected mode across all related operations.


# Functional Requirements

- [FR-001] The system shall store all active workdir files in .rdd-instance/workdir/

- [FR-002] `.rdd-instance/workdir/prompts-registry.md` shall contain prompts texts. All other operational state of the prompt is maintained in `.rdd-instance/workdir/work-iteration-registry.json`. The consistency between those two files will be maintained by the scripts in `.rdd/scripts/`.

- [FR-005] All generated questions shall follow the question-formatting standards defined in `.rdd/conventions/questions-formatting.md`.

- [FR-018] The system shall create a dedicated archive directory during the work iteration archiving.

- [FR-019] [DELETED]

- [FR-021] The system shall preserve workdir folder files during archiving by copying them instead of moving them until a final clearing action is triggered.

- [FR-024] After wrap-up synchronization, the system shall ensure `.rdd-instance/specifications/requirements.md` accurately reflects the committed state of the default branch.

- [FR-025] The system shall clear the workdir folder after archiving by removing all files and subdirectories inside `.rdd-instance/workdir/`.

- [FR-026] [TO-BE-REUSED]

- [FR-027] [TO-BE-REUSED]

- [FR-028] The system documentation shall include Linux installation guidance for enabling the `python` command using the appropriate system package.

- [FR-029] The system shall provide a build script that produces cross-platform release archives containing framework files, templates, documentation, and installation scripts.

- [FR-030] Release archives shall include all relevant framework directories, configuration templates, installation scripts, and documentation required for correct setup.

- [FR-031] The system shall include a Python-based installer that automates installation tasks including copying files, merging template settings, and updating .gitignore.

- [FR-032] The installer shall verify prerequisites including Python availability, Git availability (when applicable to mode), and the validity of the installation target.

- [FR-033] The installer shall remove obsolete RDD prompt files from `.github/prompts/` prior to deploying updated prompt templates.

- [FR-035] [DELETED]

- [FR-037] The framework shall provide CLI commands on top of the UI interface.

- [FR-040] [DELETED].

- [FR-041] The build process shall copy template files (requirements.md, files-and-folders.md, technical-design.json) to `.rdd-instance/` during installation.

- [FR-042] The work-iteration creation workflow shall validate presence of required seed templates and notify the user if they are missing.

- [FR-044] [DELETED]

- [FR-045] The framework shall depend on Python-based installation, and using shell-based or PowerShell-based scripts to run the Python-based installer.

- [FR-046] The system shall provide a Python-based test runner capable of executing all test types across platforms without requiring third-party shell testing frameworks.

- [FR-047] [DELETED]

- [FR-049] The system shall provide a functionality for creation of a JSON listing of the repository or workdir files via a dedicated command, storing the output in `.rdd-instance/workdir/files-list.json`.

- [FR-050] The system shall treat `.rdd/prompt-templates/` as a storage location for reusable prompt templates, `.rdd/prompt-snippets/` as a storage location for reusable prompt snippets and `.github/prompts/` containing a single GitHub Copilot default prompt file named `rdd.execute.prompt.md` which defines the referred in this requirements document `execute command`.

- [FR-051] The `execute command` shall follow an ordered workflow including reading the `active prompt`, generating implementation artifacts, loading documentation, resolving missing context through questionnaires, producing plans, executing those plans, updating documentation, and marking the prompt as completed.

- [FR-052] The Web UI shall provide a Prompt Management page enabling loading, editing, saving, questionnaire interaction, and plan review for the `active prompt`. 

- [FR-053] The Web UI shall provide a Technical Specification page enabling editing of structured technical design JSON `.rdd-instance/specifications/technical-design.json` using a configuration-driven interactive form. 

- [FR-054] The Web UI shall provide a File & Folder Structure page enabling visualization and controlled modification of the project's directory structure documented in `.rdd-instance/specifications/files-and-folders.md`. 

- [FR-055] The Web UI shall provide a Requirements page enabling generation of requirement-creation prompts and reverse engineering of requirements in `.rdd-instance/specifications/requirements.md` from project files. 

- [FR-056] The Web UI shall provide a Version Control & workdir Management page enabling git branch operations, commits, merges, workdir archiving, and workdir loading. 

- [FR-057] [DELETED]

- [FR-058] The Web UI shall provide access to predefined prompt files stored in `.rdd/prompt-templates/`, enabling users to load such prompts into the `active prompt` for execution. 

- [FR-059] When the `execute command` generates a questionnaire, the Web UI shall present the questionnaire with input fields and persist responses back to the questionnaire file.

- [FR-060] After the `execute command` generates an implementation plan, the Web UI shall display the plan, allow edits, and provide approval or regeneration options. 


- [FR-061] The Web UI shall display technical design, requirements, and file structure content retrieved from their respective JSON or Markdown sources and allow controlled user edits.

- [FR-062] The Web UI shall present implementation plans produced by the `execute  command`, allow editing of these plans, and support approval or regeneration when appropriate.

- [FR-063] The installer shall request user confirmation before performing operations that overwrite existing framework files.

- [FR-064] The installer shall provide a clear explanation of planned actions—including file copying, settings merging, and `.gitignore` updates—before making changes to the target directory.

- [FR-065] The installer shall detect existing RDD installations and display a summary of files and directories that will be overwritten or preserved.

- [FR-066] The installer shall allow the user to select between a GUI folder browser and manual path entry when choosing an installation target directory.

- [FR-067] [DELETED]

- [FR-068] The system shall check existing content in `requirements.md`  before generating clarification questions to avoid redundant queries.

- [FR-069] [DELETED]

- [FR-070] Technical design content shall be strictly separated from requirements and shall not be embedded directly within `requirements.md`, but instead stored exclusively in dedicated technical specification files under `.rdd-instance/specifications/`.

- [FR-071] The technical design configuration JSON shall support conditional and hierarchical logic, enabling form fields to appear or change behavior based on previously selected answers.

- [FR-072] The Technical Specification page shall provide a “Set Default Answers” function that automatically populates all unanswered design fields with their configured default values.


# Non-Functional Requirements

- [NFR-001] The framework shall provide smooth developer experience, minimizing technical overhead for requirement clarification

- [NFR-002] Error messages shall include specific problem description and suggested remediation steps

- [NFR-003] New files shall be generated from templates in `.rdd/templates/` for consistency

- [NFR-004] All destructive operations shall create backups before proceeding

- [NFR-005] Scripts shall validate prerequisites before executing operations

- [NFR-006] Scripts shall handle errors gracefully and provide recovery guidance

- [NFR-007] CLI Interactive menus shall provide visual feedback with arrow key navigation, clear selection indicators using Unicode box drawing characters (╔═╗╚╝║╠╣), bold and reverse video for highlighted items, and support for both curses-based and numeric fallback input methods

- [NFR-008] The installation process shall be straightforward and consistent across platforms, using only Python (install.py) 

- [NFR-009] The installation process shall provide clear explanations of the required decisions and actions taken from the system while running the installer from the command line

- [NFR-010] The Web UI shall provide a modern, responsive interface optimized for desktop browsers, with clear navigation between pages, real-time feedback on operations, color-coded status indicators (success: green, error: red, warning: yellow, info: blue), and graceful error handling with user-friendly messages.

- [NFR-011] The framework’s VS Code integration shall recommend RDD prompt file of `execute command` using the `chat.promptFilesRecommendations` setting for improved discoverability.

- [NFR-012] The framework’s VS Code integration shall configure terminal auto-approval for `.rdd/scripts/` using the `chat.tools.terminal.autoApprove` setting.

- [NFR-013] The framework’s VS Code integration shall associate all `*.jsonl` files with the `jsonlines` language for improved editing experience.

- [NFR-014] The Web UI and installers shall provide clear, color-coded feedback for success, error, warning, or informational messages to improve user comprehension.

- [NFR-015] Interactive menus used in CLI components shall support curses-based navigation with fallback to numeric input when curses is not available.

- [NFR-016] The test runner shall provide colored output indicating success, failure, and warnings to improve readability during test execution.

- [NFR-017] The installation process shall provide clear, user-friendly explanations of all required decisions and actions during installation.

- [NFR-018] All Web UI pages shall be optimized for desktop usage, offering clear navigation, real-time feedback on operations, and graceful handling of errors with informative messages.

- [NFR-019] All destructive operations (workdir clearing, iteration completion, overwriting files during installation) shall present warnings to the user before proceeding.



# Design principles

- [DP-001] Prompts must be authored in a Web UI and saved in Markdown files rather than typed directly into the copilot chat, ensuring a permanent and auditable history of all executed prompts.

- [DP-002] The framework must maintain a requirements file and automatically update it after each prompt execution. During each execution, the framework must also load and apply the existing requirements.

- [DP-003] A single command, `execute`, is used to initiate all copilot operations. The command operates based on github prompt defined as `.github/prompts/rdd.execute.prompt.md` which is instructed to further read the rest of the context defined in framework files.

- [DP-004] for developer Convenience a browser-based UI must support all user interactions except the actual execution of the `execute command`.

- [DP-005] The framework must operate on both Windows and Linux, with functionality implemented primerely in Python, vanilla JavaScript, HTML, CSS.

- [DP-006] Prompts shall call scripts for actions rather than implementing logic directly

- [DP-007] Prompt templates provided by the framework and user are stored in `.rdd/prompt-templates`.

- [DP-008] GitHub-specific Copilot prompt integrations reside in `.github/prompts/`.

- [DP-009] Archived workdirs are stored in `.rdd-instance/archive/`.

- [DP-010] No database is used; all data is stored in Markdown, JSON, or JSONL files.




# Technical Requirements

- [TR-001] The framework shall implement all automation functionality in Python using a domain-based command routing architecture.

- [TR-002] The framework shall use the `python` command (not `python3`) for executing all internal scripts to ensure cross-platform compatibility.

- [TR-003] [TO-BE-REUSED]

- [TR-005] [DELETED].

- [TR-006] The framework shall use `.rdd-instance/specifications/` for storing technical design files. 

- [TR-007] A technical design form JSON config file `.rdd/config/technical-design-form.json` shall define the content of Technical Specification page and should support definition of form elements with predefined options, multi-select fields, free-text values, conditional logic, and a default-answer mechanism. 

- [TR-008] Web UI server shall be implemented using Python standard-library components (such as `http.server`) or equivalent, binding to `127.0.0.1` on an available port and automatically opening the user's default browser. 

- [TR-009] The Web UI server shall expose REST-like JSON endpoints for reading, writing, and updating files in `.rdd-instance/` and for invoking RDD commands.

- [TR-010] The Web UI server shall generate a session token on startup and require it for all operations to prevent unauthorized access. 

- [TR-011] The template files which shall serve to be seeded the .rdd-instance folder (configuration templates, requirements template, technical specification templates) during the installation should be stored in the `.rdd/templates/` directory and the installation script should copy them to the respective locations under `.rdd-instance/` during installation.

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

- [TR-022] [DELETED]

- [TR-023] The framework shall provide a command to generate a JSON listing of repository or workdir files and store it at `.rdd-instance/workdir/files-list.json`, excluding directories beginning with `.` and directories named `venv`, and listing for each entry: `type` (file type - like 'txt', 'md', 'csv', 'xlsx', 'pdf', 'json', 'py', 'html', 'js', 'css' and others), `name` (file name), `relpath` (relative path), and `mtime` (modification time) in ISO8601 UTC format.

- [TR-025] The Web UI shall provide pages for managing prompts, technical specifications, folder structures, requirements, and version-control workflows, backed by the REST endpoints and reflecting the interaction model defined in the Product Requirements Specification.

- [TR-026] [DELETED]

- [TR-027] The framework shall implement safety checks that prevent iteration creation unless the workdir is empty.

- [TR-028] The framework shall archive each completed iteration in `.rdd-instance/archive/<iteration-name>/`.

- [TR-029] [DELETED]

- [TR-030] The framework shall provide utility functions for reading and updating configuration values, including but not limited to `get_rdd_config`, `set_rdd_config`, and configuration-path helpers.

- [TR-031] The framework shall support extracting and displaying repository file lists, technical design content, and requirements content through Web UI components for visualization and editing.

- [TR-032] The test system shall be implemented entirely in Python using pytest for Python tests with optional coverage reporting, and shall avoid dependencies on shell-based test frameworks.

- [TR-033] The system shall maintain its test fixtures in a `tests/` directory using isolated temporary directories to prevent modification of project files during test execution.

- [TR-034] The testing environment shall be created using a Python script that constructs and manages a dedicated virtual environment for testing.

- [TR-035] The test environment shall install dependencies listed in `tests/requirements.txt` and execute builds and installation tests in isolation from the developer’s system environment.

- [TR-036] All automation scripts shall be stored in the `.rdd/scripts/` directory.

- [TR-037] The framework shall use `.rdd/prompt-templates/` for framework templates and user-created prompts. The Web UI shall look in `.rdd/prompt-templates/` for loading prompt templates.

- [TR-038] CI/CD Testing: The system shall use GitHub Actions to run tests automatically on push and pull request events, executing only the Python test runner. For the purpose shall exist a file `.github/workflows/tests.yaml` 

- [TR-039] The CI/CD pipeline shall include a GitHub Actions workflow file `.github/workflows/tests.yaml` configured to run on `pull_request` events targeting the `dev` branch and on manual `workflow_dispatch` triggers.

- [TR-040] The `.github/workflows/tests.yaml` workflow shall define a job `all-tests-linux` that runs on `ubuntu-latest`, checks out the repository, installs Python 3.9 using `actions/setup-python@v5`, installs BATS, sets up the test environment by running `python .rdd/scripts/setup-test-env.py`, and executes all tests by running `python .rdd/scripts/run-tests.py`.

- [TR-041] The `all-tests-linux` job in `.github/workflows/tests.yaml` shall generate a Python test coverage report by activating the `.venv` virtual environment, running `pytest tests/python/ --cov=.rdd/scripts --cov=scripts --cov-report=xml --cov-report=term`, and producing a `coverage.xml` file.

- [TR-042] The `all-tests-linux` job in `.github/workflows/tests.yaml` shall upload the generated `coverage.xml` report using `codecov/codecov-action@v4` with appropriate flags and name metadata, and this upload step shall execute even when previous steps fail.

- [TR-043] The `.github/workflows/tests.yaml` workflow shall define a job `all-tests-windows` that runs on `windows-latest`, checks out the repository, installs Python 3.9 using `actions/setup-python@v5`, installs the Pester module using PowerShell, sets up the test environment by running `python .rdd/scripts/setup-test-env.py`, and executes all tests by running `python .rdd/scripts/run-tests.py`.

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