# **Concepts Definitions Document**


## **1. Purpose of the current document**

This concepts file describes the ideas, terms and general conceptual description for the RDD Framework. 

## **2. Product Name**

RDD Framework

## **3. Product Overview**

The the product is a system that seves to be installed the RDD framework in a software code repository (with or without git versioning).

The RDD framework aims to standardize execution of user defined tasks to GitHub copilot in form of prompts, maintain full traceability of prompt history, and provide a simplified developer experience through a unified execution model and a web-based interface. 

The framework enables:

* Persistent storage of prompts,
* Automated maintenance of requirements and technical specifications,
* A unified execution command (`execute command`),
* Web-based configuration and prompt management,
* Multi-platform support on Windows and Linux.

## **4. Definitions, Acronyms, and Abbreviations**

* **RDD** – Requirements-Driven Development
* **System** - A repository with scripts for test, build and release preparation of an installation of RDD framework
* **Framework** - In the context of the current document and code repository - the set of files and principles for realization of RDD development
* **Prompt** – A developer-issued instruction for the copilot
* **Technical Design** – Structured JSON defining architectural decisions
* **Questionnaire** – A set of questions generated to clarify missing or ambiguous information
* **execute command** - A github prompt, which is the only prompt exexuted in GitHub Copilot chat window and which includes instructions how the copilot to understant the needed context and actions.

## **5. Design principles**

- [DP-001] **Prompt Persistence & Traceability** – Prompts must be authored in a Web UI and saved in Markdown files rather than typed directly into the copilot chat, ensuring a permanent and auditable history of all executed prompts.

- [DP-002] **Automated Requirements Management** – The framework must maintain a requirements file and automatically update it after each prompt execution. During each execution, the framework must also load and apply the existing requirements.

- [DP-003] **Simplicity of Interaction** – A single command, `execute`, is used to initiate all copilot operations. The command operates based on github prompt defined as `.github/prompts/rdd.execute.prompt.md` which is instructed to further read the rest of the context defined in framework files.

- [DP-004] for developer Convenience a browser-based UI must support all user interactions except the actual execution of the `execute command`.

- [DP-005] **Multi-Platform Support** – The framework must operate on both Windows and Linux, with all core functionality implemented in Python.

- [DP-006] Prompts shall call scripts for actions rather than implementing logic directly


## **6. Concepts**

- [CON-001] **Prompt Execution Model**

A dedicated file, **`work-iteration-prompt.md`**, must exist under the `.rdd-docs` directory. It stores the currently active prompt. At any given moment, the file must contain exactly one prompt, and its full content must be used when executing the `execute` command. This file is the sole definition of the task to be executed together with the system-level `rdd.execute` prompt.


- [CON-002] **Execute Command Specification**

The `execute` command must perform the following operations in order:

1. Read the current prompt from `work-iteration-prompt.md`.
2. Create a file (named here implementation file) for storing the prompt, the analysis, plans, and other information for execution of the prompt in `.rdd-docs/workspace` and as first content copy the prompt text into it.
3. Read the requirements, technical design, and technical specification files.
4. Optionally read additional repository files if needed to clarify context.
5. If context remains incomplete or ambiguous, generate a questionnaire requiring developer input.
6. Produce a detailed implementation plan and write it down in the implementation file.
7. Execute the implementation plan.
8. Update requirements and technical specification files based on actual changes performed.
9. Mark the current prompt as completed.


- [CON-003] **Web User Interface**

The framework must provide a web-based UI hosted on a local web server and opened automatically in the user's default browser. The portal consists of several functional pages.

* Prompt Management Page
* Technical Specification Page
* File & Folder Structure Page
* Requirements Page
* Version Control & Workspace Management Page
* Administration Page

- [CON-004] **Prompt Management Page**

This page allows creating and editing prompts through the browser instead of editing Markdown files manually. Functionality includes:

* Loading the current content of `work-iteration-prompt.md` and allowing in-place editing.
* Saving edits back to the `work-iteration-prompt.md` file where the GitHub copilot will read the prompt definition when execute command is triggered in VS Code.
* Displaying any questionnaire generated during prompt execution and providing an interface to respond to questions.
* Displaying the implementation plan once generated.

- [CON-005] **Technical Specification Page**

Technical design must be separated from the requirements document and stored in several dedicated files.


- [CON-006] **File & Folder Structure Page**

* Visualize the project’s folder structure.
* Allow controlled updates to the folder structure through the UI.


- [CON-007] **Requirements Page**

* Generate a prompt for adding a new requirement.
* Reverse-engineer requirements from the existing project state.


- [CON-008] **Version Control & Workspace Management Page**

The system must support:

* Creating branches
* Updating from the default branch
* Committing changes
* Switching to the default branch
* Merging branches
* Archiving the workspace
* Loading an archived workspace

- [CON-009] **Administration Page**

* Provide configuration and administrative settings for the framework.


[CON-010] **Technical Design**

* Technical design is stored in a structured JSON document.
* A corresponding **design configuration JSON** defines the structure, available options, and default answers.
* The UI must allow users to populate or modify the JSON design using a form generated from the design configuration.
* Each item in the design JSON may:

  * Offer predefined answer options,
  * Allow multiple selections,
  * Allow free-text input when other choises could be taken from the user.
* Conditional/hierarchical logic must be supported—for example, questions that appear only when a certain answer is selected.
* A “Set Default Answers” option must allow users to quickly fill unanswered fields with their default values.


[CON-011] **Prompts Folder**

A folder named `.rdd/prompts` must store predefined prompt files (`.md`). Any such file can be loaded entirely into `work-iteration-prompt.md` for execution. These prompts act as reusable automation units—such as:

* Requirement revision prompts
* Folder structure synchronization prompts
* Questionnaire generation prompts

Over time, this library of predefined prompts will expand the framework’s capabilities.


[CON-012] **Operation Modes**

During installation, the user should be able to choose from three operational modes. After the installation the mode shall be able to be changed via the Web UI. The framework supports three git operational modes, configured via the `gitMode` field in `.rdd-docs/config.json`:

1. **`noGit`** - No Git Operations
   - No git commands executed
   - Version control features disabled in Web UI and CLI
   - Suitable for non-git projects or pure experimentation
   - Workspace management (archive, backup) still functional using filesystem operations

2. **`localGit`** - Local Git Only
   - Git commands executed for local operations: commit, branch, merge, status
   - No remote operations: fetch, push, pull skipped
   - Equivalent to previous `localOnly: true` configuration
   - Suitable for local-only repositories or offline development

3. **`remoteGit`** - Full Git with Remote (default)
   - All git operations enabled: local and remote
   - Fetch, push, pull executed during sync and wrap-up workflows
   - Suitable for standard GitHub-backed repositories

**Mode Selection**:
- User prompted during installation to select mode
- Mode stored in `config.json` and respected by all workflows
- Can be changed later via Web UI Administration page or `python .rdd/scripts/rdd.py config set gitMode <mode>`