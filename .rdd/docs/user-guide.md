# RDD Framework User Guide

## What is RDD?

Requirements-Driven Development (RDD) is a framework that helps you develop software with AI assistance (like GitHub Copilot) while keeping your requirements and documentation in sync with your code. Think of it as a structured workflow that guides you through clarifying what you want to build, planning how to build it, and documenting what you built.

## Getting Started

### Starting the Web Interface

After installing RDD in your repository, start the web interface:

**On Linux:**
```bash
./.rdd/run.sh
```

**On Windows:**
```cmd
.rdd\run.bat
```

Your browser will automatically open the RDD Web Interface. You can now manage your development workflow through this interface.

## Understanding the Web Interface

The Web Interface has main sections accessible from the navigation bar:

### Active Prompt
Your current work item. This is where you create new prompts, write instructions for what you want to build, answer clarification questions, review implementation plans, and track progress.

### Workdir
Manage your work iteration and view all prompts. You can create new iterations (work sessions), archive completed iterations, view iteration status, and browse all prompts (both active and completed) in the registry view. Click on any prompt to view its details.

### Files
Browse and edit files in your `.rdd-instance` folder, which contains your requirements, technical specifications, and work files.

## Common Workflows

### Workflow 1: Creating and Executing Your First Prompt

**Step 1: Create a New Prompt**
1. Click the "Active Prompt" tab
2. If no active prompt exists, click "Create New Prompt"
3. Enter a descriptive title (e.g., "Add user login feature")
4. Click "Create"

**Step 2: Write Your Prompt**
1. In the "Prompt" tab, write clear instructions for what you want to build
2. Be specific about the functionality you need
3. Click "Save Prompt" when done

**Step 3: Set Execution Mode to Analyze**
1. In the execution mode selector, click "Analyze"
2. This tells the system you want clarifying questions before implementation

**Step 4: Execute in VS Code**
1. Open VS Code in your repository
2. Open GitHub Copilot Chat
3. Type: `@workspace /rdd.execute`
4. Copilot will read your prompt and generate clarification questions

**Step 5: Answer Questions**
1. Return to the Web Interface
2. Click the "Questionnaire" tab
3. Review and answer each question
4. Click "Save Questionnaire" after answering

**Step 6: Set Execution Mode to Implement**
1. Change execution mode selector to "Implement"

**Step 7: Execute Implementation**
1. In VS Code Copilot Chat, type: `@workspace /rdd.execute`
2. Copilot will implement the feature based on your prompt and answers
3. Review the changes Copilot makes

**Step 8: Complete the Prompt**
1. After Copilot finishes, return to the Web Interface
2. Click "Complete" button
3. Your prompt becomes completed and appears in the Workdir registry view

### Workflow 2: Using Plan Mode

Sometimes you want to see a detailed implementation plan before actual coding begins.

**Step 1: Create a prompt as usual**

**Step 2: Set Execution Mode to Plan**
1. In the execution mode selector, click "Plan"

**Step 3: Execute in VS Code**
1. In Copilot Chat: `@workspace /rdd.execute`
2. Copilot generates a detailed step-by-step plan

**Step 4: Review the Plan**
1. In Web Interface, click "Plan" tab
2. Review each step of the proposed implementation
3. Edit the plan if needed and save

**Step 5: Proceed with Implementation**
1. Change execution mode to "Implement"
2. Execute again in VS Code: `@workspace /rdd.execute`
3. Copilot follows the plan you reviewed

### Workflow 3: Making Modifications

After completing a prompt, you might need to adjust or fix something. Use modifications instead of creating a new prompt.

**Step 1: Ensure Prompt is Implemented**
1. The original prompt must be completed first

**Step 2: Add a Modification**
1. In Active Prompt tab, click "Mod" button
2. Enter a description (e.g., "Fix validation error in login form")
3. Click "Create Modification"

**Step 3: Set Execution Mode to Modification**
1. In execution mode selector, click "Modification"

**Step 4: Execute the Modification**
1. In VS Code Copilot Chat: `@workspace /rdd.execute`
2. Copilot implements the modification

**Step 5: Complete Modification**
1. After Copilot finishes, click "Complete Modification" in the Modifications tab

**Step 6: Add More Modifications**
1. You can add multiple modifications to the same prompt
2. Each modification is tracked separately in the Modifications tab

## Understanding Execution Modes

The execution mode selector controls what happens when you run `@workspace /rdd.execute`:

- **No Action**: Nothing happens automatically - use this when you're still writing the prompt or working manually
- **Analyze**: Copilot generates clarification questions
- **Plan**: Copilot creates a detailed implementation plan
- **Implement**: Copilot writes the actual code
- **Modification**: Copilot implements the current modification

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

**Use Analyze Mode**: Answer the clarification questions thoughtfully. This helps Copilot understand exactly what you need.

**Review Plans**: In complex implementations, use Plan mode to see what Copilot intends to do before it makes changes.

**Small Iterations**: Break large features into multiple smaller prompts. It's easier to review and verify smaller changes.

**Complete Promptly**: Complete prompts soon after implementation. This keeps your work history accurate and requirements up-to-date.

## Troubleshooting

**Web interface won't start**
- Ensure Python 3.7+ is installed and accessible via `python` command
- Check if port 8080 is available (close other applications using it)
- Look for error messages in the console

**Copilot doesn't respond to @workspace /rdd.execute**
- Ensure you're in VS Code with the repository open
- Check that GitHub Copilot extension is installed and active
- Verify `.github/prompts/rdd.execute.prompt.md` exists in your repository

**No active prompt showing**
- Create a new prompt using "Create New Prompt" button
- Only one prompt can be active at a time

**Can't complete prompt**
- Execute the prompt at least once before completing
- Check that you're not in an execution mode (set to "No Action" first)

**Modifications won't create**
- Complete the main prompt implementation first
- Ensure the prompt shows "Implementation Completed"

## Next Steps

- Create your first prompt and try the complete workflow
- Explore the Workdir registry to see all prompts and their status
- Review and update requirements in the Files section
- Experiment with different execution modes

For more information and updates, visit: https://github.com/h111359/requirements-driven-development

