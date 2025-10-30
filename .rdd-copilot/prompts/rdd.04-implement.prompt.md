# Role:

You should execute the plan in the CR according to the technical specification and the business requirements. 

# Context:

C01: The CR is presently in designed state (filename suffix contains `designed`). You will read the CR file to obtain the implementation plan, the business requirements, and the technical specification.

C02: Edge Handling Expectations:
- Partial deliveries or missing artifacts must be surfaced before completion.
- Failing tests require either remediation (re-run after fix) or deferral + follow-up CR suggestion (do not mark completed with red tests).
- Any ambiguity in an implementation step requires a clarification prompt using the standardized confirmation format.

# Rules:

R01: Use the standardized confirmation format for every critical action: `**Please confirm to proceed: (Y/N)**`.

R02: When multiple resolution options exist (e.g., handling failing tests), present them using the standardized ASCII Options box.

R03: Do not alter, reorder, or skip implementation steps unless the CR file explicitly marks a step Deferred; ask for confirmation before deferral.

R04: On any failure: stop further execution, log failure, present recovery options (retry, manual fix, defer) via Options box.

R05: Never proceed if branch switch is impossible; inform user and stop.

R06: If a required artifact referenced by a step is missing, mark step as BLOCKED, and request user direction.

R07: Use clear outcome statuses: SUCCESS | FAILURE | DEFERRED | BLOCKED.

R08: Do not push to remote unless explicitly instructed; local repository operations only.

# Steps:

S01: Display the banner:
```
─── RDD-COPILOT ───
 Prompt: CR Implement
 Description:
 > Execute, validate, and finalize implementation
   steps for a designed CR; update docs, log actions,
   and transition the CR to completed state.
───────────────────
```

S02: Ask the user to verify they are in the correct git branch according to the CR they want to design. 

S03: Check which is the current git branch. If the branch is with format `cr/<cr-id>-<cr-name>`. Recognize the corresponding CR file name as `cr-<cr-id>-<cr-name>-clarified.cr.md`. If not in such branch, inform the user and stop (do not proceed to design loop). 

S04: Open and read the corresponding CR file. Read also the file `.rdd-docs/technical-specification.md` to understand the technical specifications existing before the CR initiation.

S06: If everything is clear - proceed to execute the implementation plan. In case you need clarification - ask the user. Record the answers of the users or independent additional instructions in the "Implementation" section of the CR file immediately after receiveing the user input. All the user inputs must be recorded in the "Implementation" section of the CR file and treated as addition to the specifications. **do not miss any user input - all must be recorded in the CR file**. The user input should be recorded in the order it is received. Each time read again the CR and add the latest input after the last line of implementation section. Keep an empty line between different user ansers. Do not ask the user or stop after every step. Work continuously untill you complete everything.

S07: After implementation - test the result. It should fully comply with the acceptance criteria in the CR file and its whole content. If you find any deviation - repeat step S06 to fix it. Do it alone - do not ask the user for help in fixing issues. Only if you are blocked - ask the user for help. Perform all the actions by yourself - you don't need youe confirmation to do the implementation and testing. Only ask for confirmation when you are blocked or when you need clarification on what to do.

S08: If no more changes are needed, ask for confirmation the user and rename CR file from `...-designed.cr.md` to `...-completed.cr.md`. Verify existence of new filename; log rename action.

S09: Offer local git commit (`completion CR: <cr-id>-<cr-name>`). Confirm before committing. Do not push.


