## Definitions

See the definitions in `.rdd/prompt-snippets/execution.md`



## Execution Step Instructions

1. Execute the instructions in [ACTIVE-PROMPT]. Along with the execution add continuously information for the implementation details in [IMPLEMENTATION] on each step. Especially take care of adding the commands you run in a terminal! Do not log the content of the changed files. In [IMPLEMENTATION] add also what you have found relevant in [TECHNICAL-DESIGN], [REQUIREMENTS] and [FILES-AND-FOLDERS] and explicitely say in which cases the [ACTIVE-PROMPT] took precedence and will overwrite.

2.  Update `.rdd-instance/specifications/requirements.md` following the instructions in `.rdd/conventions/requirements.convention.md` so to reflect precisely the changes from the prompt (if not reflected already). If reflected - do not duplicate.



## Rules

- Execute the instructions in the prompt exactly as if the user had entered them directly in the chat.     

- Follow all instructions in the prompt carefully. The instructions in the prompt take precedence over the context. 



## Examples: Managing Requirements During Implementation

**IMPORTANT**: Never edit requirements.md directly. Always use requirement scripts.

**Creating new requirements:**

```bash
# Add new user requirement
python .rdd/src/actions/requirement_ur_create.py text="The system shall provide export to PDF format"

# Add new technical requirement
python .rdd/src/actions/requirement_tr_create.py text="The export module shall use the reportlab library"
```

**Modifying existing requirements:**

```bash
# Update user requirement
python .rdd/src/actions/requirement_ur_modify.py id="UR-0042" text="The system shall export data in CSV and JSON formats"

# Update technical requirement  
python .rdd/src/actions/requirement_tr_modify.py id="TR-0015" text="The framework shall use Python 3.11 or higher"
```

**Deleting requirements:**

```bash
# Mark user requirement as deleted
python .rdd/src/actions/requirement_ur_delete.py id="UR-0088"

# Mark technical requirement as deleted
python .rdd/src/actions/requirement_tr_delete.py id="TR-0052"
```

**Skipping validation (special cases only):**

```bash
# Create requirement without validation
python .rdd/src/actions/requirement_ur_create.py text="See section 5.2 of external specification" validation=none
```

**Documenting requirement changes in implementation.md:**

After running requirement scripts, document in your implementation file:
- Which requirements were added/modified/deleted
- Why the changes were made
- How they relate to the prompt objectives






 

