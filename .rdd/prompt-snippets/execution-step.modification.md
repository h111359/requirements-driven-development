## Definitions

See the definitions in `.rdd/prompt-snippets/execution.md`



## Execution Step Instructions for Modification Mode

1. Read [CURRENT-MODIFICATION-ID] from [WI-REGISTRY]

2. Verify that [CURRENT-MODIFICATION-ID] is not null. If it is null, report error and stop.

3. Read the modification description from [MODIFICATION-FILE]

4. Execute the modification instructions exactly as described in [MODIFICATION-FILE]. Along with the execution, add continuously information for the implementation details in [MODIFICATION-IMPLEMENTATION] on each step. Especially take care of adding the commands you run in a terminal! Do not log the content of the changed files.

5. Update `.rdd-instance/specifications/requirements.md` following the instructions in `.rdd/conventions/requirements.convention.md` to reflect precisely the changes from the modification (if not reflected already).



## Rules

- Modifications are meant for small corrections after the main implementation is completed
- If the change is complex or requires significant restructuring, recommend creating a new prompt instead of a modification
- Follow the same requirements update conventions as regular implementation
- Be concise but thorough in logging to [MODIFICATION-IMPLEMENTATION]
- Execute the modification instructions exactly as if the user had entered them directly in the chat
- The modification description takes precedence over other context
