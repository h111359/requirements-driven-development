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

* **active prompt** - The prompt in `.rdd-instance/workdir/work-iteration-registry.json` which is with state `planned` or `in-progress`. The framework allows only one prompt to be in some of those states and this prompt is considered to be the `active prompt`

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

- [TR-20251224-0925] `.rdd-instance/workdir/prompts-registry.md` shall contain prompts texts. All other operational state of the prompt is maintained in `.rdd-instance/workdir/work-iteration-registry.json`. The consistency between those two files will be maintained by the scripts in `.rdd/src/`.

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