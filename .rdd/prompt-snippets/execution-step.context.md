## Execution Step Name

Context Gathering

## Execution Step Definitions

- [WI-REGISTRY] is the file `.rdd-instance/workdir/work-iteration-registry.json`

- [PROMPT-ID] is the value of the attribute "PROMPT-ID" in the file `.rdd-instance/workdir/work-iteration-registry.json`

- [CONTEXT-ANALYSIS-FILE] is a file, containing the context information needed for proper execution of the current work. The file location is in folder `.rdd-instance/workdir/`. The file name convention is `[PROMPT-ID]-context-analysis.md`, where [PROMPT-ID] should be replaced with the respective [PROMPT-ID] value.

- [PROMPT-TEXT] is the content of the file `.rdd-instance/workdir/work-iteration-prompt.md`


## Execution Step Instructions

- Create [CONTEXT-ANALYSIS-FILE] (if it does not exist, otherwise - reuse the existing file).  

- The `specifications` object in `.rdd-instance\config.json` contains list with the possible specifications. Each specification has attribute "enabled" which could be "true" or "false. Determine those specifications which has "enabled" attribute set to true. For these specifications find their attribute "path" which value defines the file which contains the respective specification. Add (or update) in the [CONTEXT-ANALYSIS-FILE] short summary for each of the enabled specifications of the relevant information for execution of prompt [PROMPT-TEXT]. 

- For each of the files reffered in [PROMPT-TEXT] - read its file and add (or update) in the [CONTEXT-ANALYSIS-FILE] short summary of relevant information for execution of prompt [PROMPT-TEXT]. 

- Readn the files descriptions in `.rdd-instance/specifications/files-and-folders.md` and for each file which description is related to [PROMPT-TEXT] - read its file and add (or update) in the [CONTEXT-ANALYSIS-FILE] short summary of relevant information for execution of prompt [PROMPT-TEXT]. 

- After you finish with generation or update of the content of [CONTEXT-ANALYSIS-FILE]: 
    * set the attribute "context.state" in [WI-REGISTRY] to "done"
    * set in the attribute "context.file" the relative path to [CONTEXT-ANALYSIS-FILE]
    * set "clarity.state" attribute in [WI-REGISTRY] to "ready-to-start" 

## Execution Step Rules

- Write the summary in consise and clear style without ommition of information  

