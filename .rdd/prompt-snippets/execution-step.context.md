## Execution Step Name

Context Gathering

## Execution Step Definitions

- [WI-REGISTRY] is the file `.rdd-instance/workdir/work-iteration-registry.json`

- [PROMPT-ID] is the value of the attribute "PROMPT-ID" in the file `.rdd-instance/workdir/work-iteration-registry.json`

- [CONTEXT-ANALYSIS-FILE] is a file, containing the context information needed for proper execution of the current work. The file location is in folder `.rdd-instance/workdir/`. The file name convention is `[PROMPT-ID]-context-analysis.md`, where [PROMPT-ID] should be replaced with the respective [PROMPT-ID] value.

- [PROMPT-TEXT] is the content of the file `.rdd-instance/workdir/work-iteration-prompt.md`


## Execution Step Instructions

- Create [CONTEXT-ANALYSIS-FILE] (if it does not exist; otherwise reuse the existing file).

- The `specifications` object in `.rdd-instance/config.json` contains a list of possible specifications. Each specification has an "enabled" attribute which can be "true" or "false". Determine which specifications have the "enabled" attribute set to "true". For these specifications, find their "path" attribute whose value is the file that contains the respective specification. Add (or update) in the [CONTEXT-ANALYSIS-FILE] a short summary for each enabled specification with the relevant information needed to execute the prompt [PROMPT-TEXT].

- For each file referred to in [PROMPT-TEXT], read that file and add (or update) in the [CONTEXT-ANALYSIS-FILE] a short summary of relevant information for executing the prompt [PROMPT-TEXT].

- Read the file descriptions in `.rdd-instance/specifications/files-and-folders.md` and, for each file whose description is related to [PROMPT-TEXT], read that file and add (or update) in the [CONTEXT-ANALYSIS-FILE] a short summary of relevant information for executing the prompt [PROMPT-TEXT].

- After you finish generating or updating the content of [CONTEXT-ANALYSIS-FILE]:
    * set the attribute "context.state" in [WI-REGISTRY] to "done"
    * set the attribute "context.file" to the relative path of [CONTEXT-ANALYSIS-FILE]
    * set the "clarity.state" attribute in [WI-REGISTRY] to "ready-to-start"

## Execution Step Rules

- Write the summary in a concise and clear style without omission of information

