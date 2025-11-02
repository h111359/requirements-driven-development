# Role:

You should execute the plan in the CR according to the technical specification and the business requirements. 

# Context:

C01: In workspace `.rdd-docs/workspace/` are stored files related to the current branch planning and execution. The file implementation-plan.md contains the implementation plan to be executed.

# Rules:

R01: Use the standardized confirmation format for every critical action: `**Please confirm to proceed: (Y/N)**`.

# Steps:

S01: Display the banner:
```
─── RDD-COPILOT ───
 Prompt: CR Implement
───────────────────
```

S02: Based on the `.rdd-docs/workspace/implementation-plan.md` update `.rdd-docs/workspace/journal.md` by creating a series of prompts which should be executed sequentially and which should define in very details the needed outcome. In prompts refer to `.rdd-docs/workspace/implementation-plan.md`, if needed, mentioning the exact place in the implementation plan file to be found the information. Also refer to other files in .rdd-docs/ folder and subfolders if needed. Follow the format in the `.rdd-docs/workspace/journal.md`. You can reuse the promts where <PROMPT-PLACEHOLDER> is the only entry and you can create new prompts continuing the sequence. **Do not change existing prompts**.

