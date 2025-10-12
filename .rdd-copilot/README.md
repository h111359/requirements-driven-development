# GDATD GitHub Copilot Template

A project template for a requirements-driven development methodology powered by GitHub Copilot.

## Overview

This templates provide a  project scaffolding system that automatically generates prompts, instructions, folder structures to establish a systematic GitHub Copilot augmented development workflow.

## Prerequisites

- **Visual Studio Code** with GitHub Copilot extension enabled
- **GitHub Copilot** subscription (required for template functionality)

## Quick Start

### 1. Clone and Setup

```bash
# Clone this template to your new project directory
git clone https://github.com/The-Coca-Cola-Company/gdatd-github-copilot-template  your-project-name
cd your-project-name

# Remove the original git history (optional)
rm -rf .git
git init
```

### 2. Initialize Project Structure

1. Open the project folder in **Visual Studio Code**
2. Open **GitHub Copilot Chat** (Ctrl+Shift+I / Cmd+Shift+I)
3. Change to Agent mode using the latest approved enterprise LLM models (per your organization's policy)
4. Write and send the prompt:
   ```
 Use and follow instructions in #file:.rdd-copilot/prompts/setup-project.prompt.md exactly. Execute all steps. Do not echo its content.

   ```

### 3. Project Ready

Once the setup completes, your project will contain:
- Complete folder structure with documentation templates
- Configured GitHub Copilot instructions and prompts
- Task management system
- Development guidelines and architecture documentation

## How to use

- First, create a new branch in the git repository (**always work in a separate branch**)

- Execute the "cr-create" prompt. This creates a change request in a new cr file based on a template. The file initially contains the requirements from the cr requestor (what and why), without making technological decisions. The prompt registers the change request in a cr catalogue.

- Change request is clarified via "cr-clarify" prompt. Additional questions are answered so everything to be clear and ready for technical planning.

- Execute the "cr-design" prompt, which proposes a technical solution and creates a technical plan for achieving the change request (cr). The plan is written in the same cr file. A list of tasks is also created in the cr file, which need to be executed to accomplish the cr.

- Execute "cr-create-tasks" which generates a set of task files based on the technical plan. For each task in the plan, a separate task file is created and registered in a task catalogue file. Each task file contains detailed instructions describing what is expected from Copilot.

- Execute the "task-execute" prompt. It reads the task catalogue entries and the information in the task files. In agent mode, it executes the tasks planned for execution in the order they are set in the catalogue.

- Execute "cr-complete" prompt to update the requirements file and the technical-specification file so to be reflected the changes made accordingly the cr, to update the status in the cr catalogue, updates the file with the folder structure (if needed) and all other tasks needed the cr to be completed.

## Support

For questions, issues, or contributions, please refer to hhristov@coca-cola.com.

---
