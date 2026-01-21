## Definitions

See the definitions in `.rdd/prompt-snippets/execution.md`



## Execution Step Instructions

1. Create [ANALYSIS] with the following chapters:

   * **Copilot Review** - Provide your opinion for the change requested from the prompt. You should be brutally honest and without any attempt to please the user. Just the facts, the truth and the rough reality. Include your assessment of:
     - Potential risks and challenges
     - Impact on existing functionality
     - Completeness of the prompt description
   
   * **Best Practices** - Check what are the best practices currently available on the Internet. This is mandatory to search (via MCP or other available fetch tools) in Internet sources when available. List the URLs you have checked and make a short summary for each URL - what are the conclusions. If MCP is not available, provide general best practices based on your knowledge.
      
   * **Proposals** - Propose changes in the requirements and different options (even if they contradict to the prompt, but are better as approach). Include:
     - Alternative implementation strategies
     - Suggested requirement modifications
     - Trade-offs between different approaches
   
   * **Prompt Modification** - Propose how you would write the same prompt if it was you who should do it. Provide a refined version that:
     - Is more clear and specific
     - Includes necessary context
     - Follows best practices for prompt engineering

2. Idempotency:
   - If [ANALYSIS]  does NOT exist: create it and write all generated questions.
   - If [ANALYSIS]  already exists, recreate its content entirely.

## Execution Step Rules

- Do not make any implementation changes to the codebase during this execution step
- Focus solely on creating the analysis.md file
- Be objective and critical in your analysis
- Provide actionable insights and recommendations
