# GDATD GitHub Copilot Template

A project template for a requirements-driven development methodology powered by GitHub Copilot.

## Overview

This templates provide a  project scaffolding system that automatically generates prompts, instructions, folder structures to establish a systematic GitHub Copilot augmented development workflow.

## Prerequisites

- **Visual Studio Code** with GitHub Copilot extension enabled
- **GitHub Copilot** subscription (required for template functionality)

## Quick Start

### 1. Download the code

- From `https://github.com/The-Coca-Cola-Company/gdatd-github-copilot-template` should be copied the folder `.rdd-copilot` in the root of your project folder. The current README.md file is optional - it is needed for initial instructions for the deploy and knowledge about rdd-copilot. 

### 2. Initialize Project Structure

1. Open the project folder in **Visual Studio Code**
2. Open **GitHub Copilot Chat** (Ctrl+Shift+I / Cmd+Shift+I)
3. Change to Agent mode 
4. Execute as prompt the file:.rdd-copilot/prompts/setup-project.prompt.md (in it is added exact instructions)

### 3. Project Ready

Once the setup completes, your project will contain:
- Complete folder structure with documentation templates
- Configured GitHub Copilot instructions and prompts
- Task management system
- Development guidelines and architecture documentation

## Concepts

rdd-copilot tool consists of several prompts, instructions and chatmodes in .github folder. For more clarity about .github folder - see https://code.visualstudio.com/docs/copilot/overview 

In addition is set a folder .rdd-docs, where the requirements, the technical specification and the folder structure will be documented and maintained.

Here also will be created files for each new change request and it will be populated with all details needed to be understood the business requirement, the technical aspects that should be obliged. In it will be created also a list of steps in form of prompts, which after being executed in sequence, should produce the expected from the change request result.

All the changes to a change request file and its results should be done in a separate git branch. Still the documents requirements.md, technical-specification.md and file-structure.md are common for all change requests, so their maintenance should happen in a separate branch. This functionality is planned to be developed in the future.


## 4. How to use

- Follow this sequence

### Step 01: 

Execute the prompt cr-create as it is and follow the instructions

```
/rdd-copilot.cr-create
```

### Step 02:

The `cr-clarify` prompt guides users through an iterative process to eliminate ambiguity in Change Requests (CRs). It helps clarify business and functional requirements by asking targeted questions, ensuring all goals, scope, constraints, dependencies, stakeholders, and success metrics are well-defined. The process starts by listing available CRs, then focuses on clarifying one selected CR until it is ready for technical design, without making implementation decisions.

Execute the prompt cr-clarify as it is and follow the instructions from the agent.

```
/rdd-copilot.cr-cclarify
```

### Step 03:

The `.github/prompts/rdd-copilot.cr-design.prompt.md` file provides a structured prompt for guiding users through the technical design phase of a Change Request (CR), helping to define architecture, implementation steps, dependencies, and acceptance criteria before development begins.

Execute the prompt cr-design as it is and follow the instructions

```
/rdd-copilot.cr-design
```

### Step 04:

The `.github/prompts/rdd-copilot.cr-implement.prompt.md` file provides a structured prompt to guide users through the implementation phase of a Change Request (CR), detailing development tasks, coding standards, and steps to ensure requirements are met.

Execute the prompt cr-implement as it is and follow the instructions from the agent.

```
/rdd-copilot.cr-implement
```

## Support

For questions, issues, or contributions, please refer to hhristov@coca-cola.com.



