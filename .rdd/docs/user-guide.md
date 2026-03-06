# RDD Framework User Guide

## What is RDD?

Requirements-Driven Development (RDD) is a framework that helps you develop software with AI assistance (like GitHub Copilot) while keeping your requirements and documentation in sync with your code. Think of it as a structured workflow that guides you through clarifying what you want to build, planning how to build it, and documenting what you built.

## Understanding the Web Interface

The Web Interface has main sections accessible from the navigation bar:

### Active Prompt
Your current work item — the single prompt in [.rdd-instance/workdir/work-iteration-registry.json](.rdd-instance/workdir/work-iteration-registry.json) with state `active`. 

First step is to be created a new iteration. When an iteration is created - use this page to create a new prompt (it becomes the active prompt), author the prompt text and instructions, answer generated clarification questions (questionnaire), review and edit implementation plans, manage modifications, and track execution progress.

When the work on the iteration is completed and all active prompts are closed, archive the iteration and start over with a new one.


What each term means:

- **Questionnaire**: A set of clarification questions generated during Clarify mode. Questions are presented as an interactive form (stored alongside the prompt) so you can provide exact answers that guide implementation and avoid redundant queries.

The step inspects the prompt, current requirements, and repository context to surface ambiguities and produce the questionnaire.

- **Analyze**: Makes extended review of the prompt, searches for best practices, proposes a new prompt text.

- **Plan**: A step-by-step implementation plan produced in Plan mode. The plan is saved with the prompt and can be reviewed, edited, or approved before implementation begins.

- **Implementation**: The execution step that applies changes (code and files) based on the prompt, questionnaire answers, and approved plan. Implementation outputs (logs, `implementation.md`) are stored in the prompt work folder.

- **Modification**: A lightweight workflow for small fixes to a completed prompt. Modifications skip questionnaire and planning and go directly to implementation; each modification is tracked in `modification-<ID>.md` and recorded in the prompt's `modifications-log.json`.

### Prompt History
Browse the prompts in the current iteration and explore prompts statuses (active or completed) and the steps of their execution. Click any prompt to view its details.

### Technical Design

The Technical Design page enables you to record architectural decisions through a comprehensive questionnaire covering 33 categories of technical choices.

**Key Features:**
- **Dynamic questionnaire**: 490+ questions organized into categories and groups
- **Smart navigation**: Left sidebar shows categories with answered/total counts
- **Search and filter**: Find questions by text, filter by type (radio/multiselect/text) or status (answered/unanswered)
- **Conditional questions**: Questions appear based on previous answers (e.g., cloud-specific questions only show when you select a cloud deployment model)
- **Immediate save**: Answers save automatically when you make a selection
- **Optional**: Technical Design is not required; skip sections that don't apply to your project

**Usage:**
1. Select a category from the sidebar (e.g., "Project scale", "Cloud Strategy", "Frontend")
2. Expand groups within the category to see questions
3. Answer questions using radio buttons, checkboxes, or text inputs
4. Use search to quickly find specific topics
5. Filter by "Unanswered" to see what's left to complete
6. Clear answers if decisions change using the "Clear Answer" button

**Categories include:**
- Project fundamentals: Scale, Product Type, Criticality, Lifetime, Enterprise Constraints
- Infrastructure: Cloud Strategy, Compute, Networking, Disaster Recovery
- Application stack: Frontend, Backend, Mobile, Data Analytics, AI/ML
- Operations: CI/CD, DevOps, Observability, Monitoring, Logging
- Governance: Security, Compliance, Support SLAs, Data Lifecycle

**Technical Design and RDD Execution:**
- When you run prompts in clarify/analyze/plan/implement modes, the copilot reads your technical design decisions
- Clarify mode avoids asking questions already answered in Technical Design
- Analyze and Plan modes align recommendations with your recorded choices
- Implement mode ensures code complies with architectural constraints

**Storage:**
- Answers are stored in `.rdd-instance/specifications/technical-design.json`
- Only answered questions are saved (sparse storage)
- Each answer includes a timestamp
- The schema defining all questions is in `.rdd/config/technical-design-schema.json`

**Best Practices:**
- Answer foundational questions first (Project Scale, Cloud Strategy, Enterprise Constraints)
- Review and update Technical Design when project requirements or constraints change
- Don't feel obligated to answer every question—focus on what's relevant to your project

### Requirements

View and edit the project's authoritative requirements in [.rdd-instance/specifications/requirements.md](.rdd-instance/specifications/requirements.md). This file contains the user and technical requirements the framework loads during prompt execution to check constraints and avoid redundant clarification questions. Use this page to review requirements, edit name, overview and definition parts, and save changes — updates are persisted to the requirements file and are considered by subsequent Analyze and Execute operations. The requirements document follows the formatting conventions in [.rdd/conventions/requirements.convention.md](.rdd/conventions/requirements.convention.md).

Caution!!!: Avoid editing the User Requirements and Technical Requirements parts. Despite possible, it is better they to be maintained by the copilot based on prompt requests.

### Config
Manage instance-level settings and runtime options for this RDD installation. The Config page displays and edits `.rdd-instance/config/instance-config.json` (for example the `git-enabled` flag that controls optional git integration during prompt completion). Use the provided toggles and save button to persist changes; saved settings are applied by the Web UI and influence behaviors such as automatic git commits on archive or prompt completion. Note: some configuration changes may require restarting the web server to take full effect.

### Help

The current document.


## Common Workflows

### Workflow 1: Creating and Executing Your First Prompt

**Step 1: Setup RDD**
1. Click the "Config" tab
2. Chose if git functionality should be on or off

**Step 1: Create Work Iteration"**
1. Click the "Active Prompt" tab
2. Click "Create Work Iteration" button
3. Fulfill the iteration name in the dialog appeared and click "Create Work Iteration" button
4. Two new buttons appear - "Create New Prompt" and "Archive Iteration"

**Step 3: Create New Prompt**
1. Click the "Active Prompt" tab if you are not in it
2. If no active prompt exists, the button "Create New Prompt" will be present. Click it.
3. Enter a short descriptive title (e.g., "Add user login feature")
4. State should stay "Active"
5. Click "Create Prompt"

**Step 4: Write Your Prompt**
1. If not selected - click "Prompt" button
2. Write clear instructions for what you want to build. Be specific about the functionality you need
3. Optionaly you can use "Insert Snippet" button to add predefined prompt snippets to your prompt

**Step 5: Execution Mode Clarify** (Optional)
1. In the execution mode selector, click "Clarify"
2. This tells the system you want clarifying questions before implementation
3. Click on button "Copy Cmd" which will add an execute command in your clipboard
4. Open VS Code in your repository
5. Open a new GitHub Copilot Chat
6. Paste the execute command storred in your clipboard
7. Copilot will read your prompt and generate clarification questions
1. Return to the Web Interface (and refresh the page)
2. Click the "Questionnaire" tab
3. Review and answer each question

**Step 6: Execution Mode Analyze** (Optional)
1. Change execution mode selector to "Analyze"
2. This tells the system you want analysis to be created before implementation
3. Click on button "Copy Cmd" which will add an execute command in your clipboard
4. Open VS Code in your repository
5. Open a new GitHub Copilot Chat
6. Paste the execute command storred in your clipboard
7. Copilot will read your prompt and questionnaire if created and will generate analysis file for you
8. Read the analysis and modify your prompt if needed

**Step 7: Execution Mode Plan** (Optional)
1. Change execution mode selector to "Plan"
2. This tells the system you want an execution plan to be created before implementation
3. Click on button "Copy Cmd" which will add an execute command in your clipboard
4. Open VS Code in your repository
5. Open a new GitHub Copilot Chat
6. Paste the execute command storred in your clipboard
7. Copilot will read your prompt and questionnaire if created and will generate a plan file for you
8. Read the plan in the Web UI and modify it if needed

**Step 8: Execution Mode Implement**
1. Change execution mode selector to "Implement"
2. This tells the system you want to run the implementation
3. Click on button "Copy Cmd" which will add an execute command in your clipboard
4. Open VS Code in your repository
5. Open a new GitHub Copilot Chat
6. Paste the execute command storred in your clipboard
7. Copilot will read your prompt, questionnaire and plan if created and will follow the instructions. While working - it will create implementation file
8. Review the changes Copilot has made. Read the implementation file. Test the result yourself

**Step 8: Execution Mode Modify** (Optional)
1. In case you are satisfied with the result but want just small modification - click on "Create Modification" button (it is activated after the implementation is completed)
2. In the modal explain the modification needed
3. Change execution mode selector to "Modify"
4. Click on button "Copy Cmd" which will add an execute command in your clipboard
5. Open VS Code in your repository
6. Open a new GitHub Copilot Chat
7. Paste the execute command storred in your clipboard
8. Copilot will read your modification text, the prompt, questionnaire and plan if created and will follow the instructions. While working - it will create modification implementation file
9. Review the changes Copilot has made. Read the modiication implementation file. Test the result yourself
10. If needed - create a new modification


**Step 8: Complete the Prompt**
1. After you have completed the implementation and optionnaly modifications - click "Complete" button
2. In case git is activated, RDD will commit the chages
3. The "Active Prompt" page chanes to "no active prompt" mode and you can press "Create New Prompt" button


## File Organization

RDD uses two main folders in your repository:

### .rdd Folder
Contains the framework itself (scripts, conventions, documentation). These files are updated when you upgrade RDD to a new version.

### .rdd-instance Folder
Contains YOUR project's data:
- **specifications/**: Your requirements and technical design
- **workdir/**: Active work in progress
- **archive/**: Completed work iterations

You'll mostly interact with files in `.rdd-instance` through the Web Interface.

## Tips for Success

**Write Clear Prompts**: Be specific about what you want. Instead of "improve performance," write "optimize the search function to handle 10,000 records without lag."

**Use Clarify Mode**: Answer the clarification questions thoughtfully. This helps Copilot understand exactly what you need.

**Review Plans**: In complex implementations, use Plan mode to see what Copilot intends to do before it makes changes.

**Small Iterations**: Break large features into multiple smaller prompts. It's easier to review and verify smaller changes.

**Complete Promptly**: Complete prompts soon after implementation. This keeps your work history accurate and requirements up-to-date.

## Troubleshooting

**Web interface won't start**
- Ensure Python 3.7+ is installed and accessible via `python` command
- Check if port 8080 is available (close other applications using it)
- Look for error messages in the console

**No active prompt showing**
- Create a new prompt using "Create New Prompt" button
- Only one prompt can be active at a time

**Can't complete prompt**
- Refresh the page
- Execute the prompt at least once before completing
- Check that you're not in an execution mode (set to "No Action" first)

**Modifications won't create**
- Complete the main prompt implementation first
- Ensure the prompt shows "Implementation Completed"

**How do I assign GitHub Issue #1 to Copilot?**
- Open the issue in GitHub (for example: issue #1)
- In the right sidebar, click **Assignees**
- Select **Copilot** as the assignee
- If Copilot is not listed, ask a repository admin to enable Copilot coding agent access for the repository/org and verify you have permission to assign issues

