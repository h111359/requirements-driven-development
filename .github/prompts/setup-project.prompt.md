# Project Setup Instructions

> Use these instructions with GitHub Copilot to automatically recreate the full project template from only the `.github` folder. This will restore all folders and files as described below, with exact content for each file.

## 1. Create `.vscode` folder and its contents

- Create folder: `.vscode`
- Create file: `.vscode/settings.json` with three color values for:
  - `titleBar.activeBackground`
  - `titleBar.inactiveBackground`
  - `statusBar.background`

**Choose the three colors arbitrarily, but ensure they are from the same theme (e.g., all pastel, all dark, all vibrant, etc.) so they look nice together.**

Example (replace with your own theme-matching colors):

```jsonc
{
  "workbench.colorCustomizations": {
    "titleBar.activeBackground": "#A3CEF1",
    "titleBar.inactiveBackground": "#5390D9",
    "statusBar.background": "#29335C"
  }
}
```

## 2. Create `.github` folder structure and prompt files

- Create folder: `.github/prompts` (if not exists)
- Create folder: `.github/instructions` (if not exists)

- Create file: `.github/prompts/task-creator.prompt.md`:

```markdown
# Task Creator Prompt 

## Purpose 

Guide the creation of new task files in `/docs/tasks` and ensure they are properly cataloged for execution. 

## Instructions 

1. **Receive Task Intention** 

  - You will be provided with a description or intention for a new task. 

  - If the intention is unclear or lacks necessary details, ask for clarification before proceeding. 


2. **Create Task File** 

  - Find the current date and time of the local machine to use in the filename. Write the date and time in the specified format as `YYYYMMDD-HHmm` as a response.
  - Create a new file in `docs/tasks` following the format: `T-YYYYMMDD-HHmm-short-description.task.md`. 

    - `YYYYMMDD`: Current date (year, month, day). 
    - `HHmm`: Current time (24-hour format, hours and minutes). 
    - `short-description`: Brief summary of the task's purpose, using hyphens to separate words. 

  - The task file must include: 

    - A clear and concise title. 
    - A detailed description of what needs to be done. 
    - Any specific requirements or constraints. 
    - Acceptance criteria to define when the task is considered complete. 

  - Ensure the task is actionable and can be completed independently. 

3. **Update Tasks Catalog**
- After creating the task file, update the `docs/tasks-catalog.md` file to include the new task with a status of `not-started`.

4. **Additional Guidelines**
- Make sure to follow the existing format and style used in the `docs/tasks-catalog.md` file.
- Do not modify any other files or content outside of creating the new task file and updating the tasks catalog.
- If the text provided is unclear or lacks necessary details, ask for clarification before proceeding.
```

- Create file: `.github/prompts/task-executor.prompt.md`:

```markdown
# Task Executor Prompt

## Purpose
Automate the process of checking for new tasks in `/docs/tasks`, updating `tasks-catalog.md`, and executing not-started tasks in chronological order.

## Instructions
   - Read the `docs/tasks-catalog.md` file to identify existing tasks and their statuses.
   - Ensure the table with the tasks is sorted by date and time from the filename.
   - Find the first by time task with status `not-started` and follow the next instructions for it.
   - Change its status to `in-progress` in `docs/tasks-catalog.md`.
   - Open the corresponding task file in `docs/tasks/`.
   - Read the task definition and follow the instructions to execute the task.
   - If the task description is unclear or lacks necessary details, ask for clarification before proceeding.
   - First create a detailed plan for completing the task and write it down at the end of the task definition file in a new section `## Execution Plan`.
   - Then start executing the task step-by-step, documenting each step in an execution log written in the same task file under new `## Execution Log` section. 
   - In this execution log section, write: 
     - Each step taken, including details, decisions, and references found. 
     - The flow of execution, status of tests, and any encountered issues or resolutions. 
     - Any additional information relevant to the execution. 
   - At the end of the task create tests to verify the task completion and document their results in a new section `## Test Results`. In this section, write: 
     - The tests created to verify the task completion. 
     - The results of each test (pass/fail) and any relevant details. 
   - If the task needs to be executed again, create a new log entry with a new timestamp in the same task file. 
   - Save the execution log in the same task file under the `## Execution Log` section. 
   - After completion, update status to `done` in `tasks-catalog.md`. 

   - Proceed to the next not-started task in chronological order. 

## Notes
- Only one task should be `in-progress` at a time.
- All actions must be logged in `tasks-catalog.md`.
- Task execution should follow the instructions in each task file.
```

- Create file: `.github/instructions/task-creator-instructions.instructions.md`:

```markdown
---
applyTo: '**/**/docs/tasks/T-*.task.md'
---

- **VERY IMPORTANT**: Do not perform any changes to the codebase or documentation (except creation of tasks themselves) without this to be asked in a task file in docs/tasks/ folder. You should only suggest changes if you are asked to do so in a task file. Read the instructions in /.github/instructions/task-creator-instructions.instructions.md carefully and follow them exactly.
```

- Create file: `.github/copilot-instructions.md`:

```markdown
# RULES

- Do not perform any changes to the codebase or documentation (except creation of tasks themselves) without this to be asked in a task file in docs/tasks/ folder. You should only suggest changes if you are asked to do so. 

- After each change update README.md files
- After each change update docs/requirements.md file
- After each change update docs/developer-guide.md file
- After each change update docs/user-guide.md file
- After each change update docs/architecture.md file    
- After each change update docs/folder-structure.md file

- Write clean, modular, and well-documented code to facilitate future maintenance and updates.


# INSTRUCTIONS

Refer to the following files and instructions for all requirements, rules, and structure:

- `docs/folder-structure.md`: File and folder structure specification
- `docs/requirements/functional.requirements.md`: Functional requirements
- `docs/requirements/technical.requirements.md`: Technical requirements and constraints
- `docs/developer-guide.md`: Developer instructions
- `docs/user-guide.md`: User instructions
- `docs/architecture.md`: Architecture and design
- `docs/tasks-catalog.md`: List of all tasks and their status
- `docs/tasks/`: All individual task files
- `.github/prompts/developer.prompt.md`: Main game development prompt
- `.github/prompts/task-executor.prompt.md`: Task execution automation prompt
```

## 3. Create `docs` folder and all subfolders/files

- Create folder: `docs`
- Create file: `docs/architecture.md`:

```markdown
# Architecture

> This is a template file. Replace with your project's architecture documentation.

## System Overview
- [Provide high-level description of the system]
- [Define main components and their interactions]
- [Specify system boundaries and interfaces]

## Architecture Patterns
- [Describe architectural patterns used (MVC, microservices, etc.)]
- [Explain design principles and patterns]
- [Document architectural decisions and rationale]

## Component Architecture
- [Detail major system components]
- [Define component responsibilities and interfaces]
- [Show component relationships and dependencies]

## Data Architecture
- [Describe data models and schemas]
- [Define data flow and storage patterns]
- [Specify data management strategies]

## Deployment Architecture
- [Define deployment topology]
- [Specify infrastructure components]
- [Document scaling and availability strategies]
```

- Create file: `docs/developer-guide.md`:

```markdown
# Developer Guide

> This is a template file. Replace with your project's developer guide.

## Getting Started
- [Prerequisites and setup instructions]
- [Installation and configuration steps]
- [First-time setup and validation]

## Development Environment
- [Required tools and IDEs]
- [Environment setup and configuration]
- [Local development workflow]

## Project Structure
See [docs/folder-structure.md](folder-structure.md) for a complete description of the file and folder organization.

## Coding Standards
- [Code style and formatting guidelines]
- [Naming conventions and best practices]
- [Documentation requirements]

## Testing
- [Testing framework and tools]
- [Test organization and structure]
- [Running and debugging tests]

## Build and Deployment
- [Build process and scripts]
- [Deployment procedures]
- [Environment-specific configurations]

## Contributing
- [Contributing guidelines and process]
- [Code review requirements]
- [Issue reporting and feature requests]
```

- Create file: `docs/folder-structure.md`:

```markdown
# File and Folder Structure

> This template provides a standard project structure for web applications.

## Project Root
- `README.md`: Project overview and setup instructions
- `.github/`: GitHub-specific files (workflows, templates, etc.)
- `docs/`: All project documentation

## src/
The main source code directory
- `assets/`: Static assets (images, fonts, data files, etc.)
- `components/`: Reusable UI components and modules
- `utils/`: Utility functions and helper modules

## docs/
Project documentation and planning
- `requirements/`: Requirements specification
  - `functional.requirements.md`: User and business requirements
  - `technical.requirements.md`: Technical constraints and requirements
- `architecture.md`: System architecture and design
- `developer-guide.md`: Development setup and guidelines
- `user-guide.md`: End-user documentation
- `folder-structure.md`: This file describing project organization
- `tasks/`: Individual task documentation (*.task.md files)
- `tasks-catalog.md`: Overview of all project tasks
- `task-execution-logs/`: Historical task execution records

## Customization
- Modify this structure based on your project's specific needs
- Add additional directories for frameworks, testing, build tools, etc.
- Maintain clear separation between source code, documentation, and configuration
```

- Create file: `docs/requirements/functional.requirements.md`:

```markdown
# Functional Requirements

> This is a template file. Replace with your project's functional requirements.

## User Requirements
- [List what the users need from this application]
- [Define user stories and use cases]
- [Specify target audience and user experience goals]

## Feature Requirements  
- [Define core features and functionality]
- [Specify user interactions and workflows]
- [Define success criteria and acceptance criteria]

## Business Requirements
- [List business objectives and goals]
- [Define scope and constraints]
- [Specify compliance and regulatory requirements]
```

- Create file: `docs/requirements/technical.requirements.md`:

```markdown
# Technical Requirements

> This is a template file. Replace with your project's technical requirements.

## Technology Stack
- [Specify programming languages, frameworks, and libraries]
- [Define browser/platform compatibility requirements]
- [List development tools and build systems]

## Performance Requirements
- [Define response time and throughput requirements]
- [Specify resource usage limits]
- [Set scalability requirements]

## Security Requirements
- [Define authentication and authorization requirements]
- [Specify data protection and privacy requirements]
- [List compliance requirements]

## Infrastructure Requirements
- [Define hosting and deployment requirements]
- [Specify database and storage requirements]
- [List third-party service dependencies]
```

- Create file: `docs/tasks/T-20250929-1854-template.task.md`:

```markdown
# Task Template: Project Setup

**Task ID**: T-YYYYMMDD-NNNN-project-setup  
**Created**: [Date]  
**Assigned**: [Developer Name]  
**Status**: not-started  

## Description
This is a template task file. Replace this content with your actual task details.

## Objectives
- [ ] Define what needs to be accomplished
- [ ] Break down the task into smaller, actionable items
- [ ] Set clear acceptance criteria

## Requirements
- List any prerequisites or dependencies
- Specify any constraints or limitations
- Define success criteria

## Implementation Plan
1. Step-by-step approach to complete the task
2. Include any design decisions or technical considerations
3. Identify potential risks or challenges

## Testing
- How will this task be validated?
- What tests need to be created or updated?
- Definition of "done"

## Notes
- Additional context or considerations
- Links to relevant documentation
- Dependencies on other tasks

## Status Updates
- [Date] - Task created
- [Date] - Status update or progress notes
```

- Create file: `docs/tasks-catalog.md`:

```markdown
# Tasks Catalog

> This is a template file. Replace with your project's task catalog.

## Overview
This file tracks all project tasks, their current status, and provides links to detailed task documentation.

## Active Tasks
| Task ID | Title | Status | Assigned | Due Date |
|---------|-------|--------|----------|----------|
| [Example] | [Task description] | [not-started/in-progress/completed] | [Developer] | [Date] |

## Completed Tasks
| Task ID | Title | Completed Date | Notes |
|---------|-------|----------------|-------|
| [Example] | [Task description] | [Date] | [Completion notes] |

## Task Status Guide
- **not-started**: Task has been identified but work has not begun
- **in-progress**: Task is currently being worked on
- **completed**: Task has been finished and verified
- **blocked**: Task cannot proceed due to dependencies or issues

## Task Management
- All detailed task documentation should be stored in `docs/tasks/`
- Use the format `T-YYYYMMDD-NNNN-short-description.task.md` for task files
- Update this catalog whenever task status changes
```

- Create file: `docs/user-guide.md`:

```markdown
# User Guide

> This is a template file. Replace with your project's user guide.

## Getting Started
- [How to access and start using the application]
- [Initial setup and configuration for users]
- [Overview of main features and capabilities]

## Basic Usage
- [Step-by-step instructions for common tasks]
- [User interface overview and navigation]
- [Core workflows and user journeys]

## Features
- [Detailed description of all features]
- [Use cases and examples]
- [Tips and best practices]

## Troubleshooting
- [Common issues and solutions]
- [Error messages and their meanings]
- [How to get help and support]

## Advanced Usage
- [Advanced features and configurations]
- [Customization options]
- [Integration with other tools]
```

## 3. Create `src` folder and subfolders (all empty)

- Create folder: `src`
- Create empty folders:
  - `src/assets`
  - `src/components`
  - `src/utils`

## 4. Create `README.md` file

- Create file: `README.md`. If the README.md file already exists, rename it to `README-SCATED.md` before creating the new one.

```markdown
# GitHub Copilot Template Project

This is a template repository designed to work with GitHub Copilot using a structured task-based workflow. The repository includes automated prompts and instructions that help you create, manage, and execute development tasks systematically.

## How It Works

This template uses a task-driven development approach where all changes to the codebase are managed through structured task files. Here's how to use it:

### 1. Creating Tasks

To create a new task, start your message to GitHub Copilot with `/task-creator` followed by your task description:

```
/task-creator Create a login page with username and password fields
```

GitHub Copilot will automatically:
- Generate a timestamped task file in `docs/tasks/` (format: `T-YYYYMMDD-HHmm-description.task.md`)
- Add the task to `docs/tasks-catalog.md` with status `not-started`
- Include detailed requirements, objectives, and acceptance criteria

### 2. Executing Tasks

To execute tasks, start your message with `/task-executor`:

```
Execute the next pending task
```

GitHub Copilot will:
- Find the oldest `not-started` task in chronological order
- Change its status to `in-progress` in `docs/tasks-catalog.md`
- Create an execution plan in the task file
- Execute the task step-by-step
- Log all actions in the task file under `## Execution Log`
- Create and run tests to verify completion
- Update status to `completed` when finished

### 3. Monitoring Progress

#### Files That Get Updated

During task execution, these files are automatically updated:

- **`docs/tasks-catalog.md`**: Task status tracking and overview
- **Task files in `docs/tasks/`**: Execution plans, logs, and test results
- **`README.md`**: Project documentation updates
- **`docs/requirements/functional.requirements.md`**: Feature requirements
- **`docs/requirements/technical.requirements.md`**: Technical specifications
- **`docs/developer-guide.md`**: Development instructions
- **`docs/user-guide.md`**: User documentation
- **`docs/architecture.md`**: System architecture
- **`docs/folder-structure.md`**: Project structure documentation

#### Tracking Your Work

1. **Task Overview**: Check `docs/tasks-catalog.md` for a complete list of all tasks and their current status
2. **Individual Tasks**: Review specific task files in `docs/tasks/` for detailed execution logs and results
3. **Project Status**: Monitor the documentation files listed above to see how your project evolves

### 4. Project Structure

```
├── .github/
│   ├── copilot-instructions.md     # GitHub Copilot behavior rules
│   ├── prompts/                    # Automated prompt files
│   └── instructions/               # Additional instruction files
├── .vscode/
│   └── settings.json              # VS Code customizations
├── docs/
│   ├── requirements/              # Project requirements
│   ├── tasks/                     # Individual task files
│   ├── tasks-catalog.md          # Task tracking and status
│   ├── architecture.md           # System architecture
│   ├── developer-guide.md        # Development guidelines
│   ├── user-guide.md             # User documentation
│   └── folder-structure.md       # Project structure guide
├── src/                          # Source code (initially empty)
│   ├── assets/                   # Static files
│   ├── components/               # Reusable components
│   └── utils/                    # Utility functions
└── README.md                     # This file
```

### 5. Best Practices

- **Be Specific**: When creating tasks, provide clear and detailed descriptions
- **One Task at a Time**: The system processes tasks sequentially for better tracking
- **Review Logs**: Check execution logs in task files to understand what was implemented
- **Update Documentation**: The system automatically updates documentation, but review for accuracy
- **Monitor Status**: Regularly check `docs/tasks-catalog.md` to track overall progress

### 6. Getting Started

1. **Create Your First Task**: Use `Task: [your description]` to create your initial development task
2. **Execute It**: Ask GitHub Copilot to execute the task
3. **Review Results**: Check the generated files and documentation
4. **Continue**: Create more tasks as needed for your project

This template ensures consistent development practices, comprehensive documentation, and full traceability of all changes made to your project.

```

---

**After running this prompt, your project will be fully restored to the template structure and contents.**
