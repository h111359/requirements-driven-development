## Definitions

- [WI-REGISTRY] is the file `.rdd-instance/workdir/work-iteration-registry.json`

## Instructions - Follow these steps exactly:  

1. **Read the registry**: Open and read the [WI-REGISTRY] file.
2. **Identify the mode**: Get the value of the attribute "mode" from the [WI-REGISTRY] file. Based on its value, proceed as follows:
    - If the "mode" is "prompt", follow the instructions in `.rdd/prompt-templates/execute-work-iteration.prompt.md`.
    - Else If the "mode" is "task", follow the instructions in `.rdd/prompt-templates/execute-task.prompt.md`.
    - Else: Stop and inform the user that the mode is unrecognized.