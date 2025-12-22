## Execution Step Name

Context Gathering

## Execution Step Definitions

- [WI-REGISTRY] is the file `.rdd-instance/workdir/rdd-prompt-setup.json`

- [USER-STORY-ID] is the value of the attribute "active.active-user-story-id" in the file `.rdd-instance/workdir/rdd-prompt-setup.json`

- [CONTEXT-ANALYSIS-FILE] is a file, containing the context information needed for proper execution of the current work. The file location is in folder `.rdd-instance/workdir/`. The file name convention is `[USER-STORY-ID]-context-analysis.md`, where [USER-STORY-ID] should be replaced with the respective [USER-STORY-ID] value.

- [PROMPT-TEXT] is the content of the file in the attribute prompt-file in the respective object under userStories key with id equal to [USER-STORY-ID] 


## Execution Step Instructions

- Create [CONTEXT-ANALYSIS-FILE] (if it does not exist; otherwise reuse the existing file).

- Add (or update) in the [CONTEXT-ANALYSIS-FILE] a short summary of specifications in `.rdd-instance/specifications` with the relevant information needed to execute the prompt [PROMPT-TEXT].

- For each file referred to in [PROMPT-TEXT], read that file and add (or update) in the [CONTEXT-ANALYSIS-FILE] a short summary of relevant information for executing the prompt [PROMPT-TEXT].

- Read the file descriptions in `.rdd-instance/specifications/files-and-folders.md` and, for each file whose description is related to [PROMPT-TEXT], read that file and add (or update) in the [CONTEXT-ANALYSIS-FILE] a short summary of relevant information for executing the prompt [PROMPT-TEXT].

- After you finish generating or updating the content of [CONTEXT-ANALYSIS-FILE]:
    * set the attribute "context.state" in [WI-REGISTRY] to "done"
    * set the attribute "context.file" to the relative path of [CONTEXT-ANALYSIS-FILE]
    * set the "clarity.state" attribute in [WI-REGISTRY] to "ready-to-start"

## Execution Step Rules

- Write the summary in a concise and clear style without omission of information

