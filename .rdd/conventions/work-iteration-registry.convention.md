# Work Iteration Registry Convention

This document defines the required structure and content conventions for the file:

- `.rdd-instance/workdir/work-iteration-registry.json`

The work-iteration-registry is the single source of truth for the current work-iteration’s progress and prompts queue. Every prompt id in work registry exists in prompts registry. In case of inconsistency between this file and `.rdd-instance/workdir/prompts-registry.md`, the execution should stop and the user should be informed to fix the errors.

## File format

- **Format:** JSON object (UTF-8)
- **Top-level type:** object
- **Key style:**
- JSON keys use **lower-kebab-case** (e.g., `iteration-id`, `parent-id`).
- **Prompt IDs:** use `P-###` format (stored in `id` fields, not as keys).

## Top-level schema

The JSON file MUST be an object with the following keys:

### `iteration-id` (string)
- **Required:** yes
- **Allowed values:**
  - Text in format "ITR-YYYYMMDD-HHmiss" where YYYY -> year, MM -> month, DD -> day, HH -> 24 hour formatted hour, mi -> minutes, ss -> seconds)
- **Meaning:** Unique identifier of the iteration based on the time when the iteration was created
- **Example:** "ITR-20251220-224913"

### `iteration-name` (string)
- **Required:** yes
- **Allowed values:**
  - Free text up to 64 symbols
- **Meaning:** Declares the name to be used for reference to the workdir content

### `prompt-id-sequence-next-value` (number)
- **Required:** yes
- **Allowed values:**
  - Integer with minimal value 1 
- **Meaning:** What should be the id of the next created prompt. New prompt IDs MUST be allocated using prompt-id-sequence-next-value. Increment with 1 when a prompt with the current value is created

### `prompts` (array)

* **Required:** yes
* **Meaning:** Registry-owned **prompt definitions** for the current iteration, used by tooling (JS app, scripts, Copilot) to:

  * list of `prompt-metadata` objects
  * resolve parent chains
  * map prompt IDs to prompt text in the '.rdd-instance/workdir/prompts-registry.md` file
  * associate questionnaire references (without embedding questionnaire content)
  * define capabilities/default execution semantics per prompt
* **Type:** array of `prompt-metadata` objects
* **Uniqueness constraint:** each `id` MUST be unique within the array
* **Ordering:** recommended topological (roots first), but not required if `parent-id` is resolvable


### `prompt-metadata` (object)

#### Required keys

* `id` (string)
  * Format: `P-` followed by digits (regex: `^P-[0-9]{3,}$`) - at least 3 digits, left-pad to 3 for <1000.
  * Example: `"P-003"`

* `title` (string)
  * Free text up to 128 chars
  * In case of difference of titles of same prompt id in comparison with `.rdd-instance/workdir/prompts-registry.md`, the title in `.rdd-instance/workdir/work-iteration-registry.json` shall be treated as the source of truth

* `type` (string)
  * **Meaning** - Defines if the prompt is from type `main` or `modification`
  * Possible values: ["main" | "modification"]

* `state` (string)
  * **Meaning** - Defines if the prompt is still a draft, if it is planned for execution, in progress or completed. Only one prompt could be in a state "planned" or "in-progress" at a given time and this it the prompt which `execute command` (as defined in `.rdd-instance/specifications/requirements.md`) will run.
  * Possible values: ["draft" | "planned" | "in-progress" | "completed"]  

* `parent-id` (string | null)
  * **Meaning** - The prompts could be type `main` or type `modification`. When the type is `main`, it does not rely on other prompts for its definition. The definition of the `modification` prompts is always a union of `main` prompt + previously executed `modification` prompts referred tp the same `main` prompt and the current modification own definition.
  * `null` for `main` prompts (not dependent)
  * Otherwise must reference a `main` prompt `id` in the same `prompts` array

* `analysis` (object)
  * **Meaning:**: Each prompt will generate a file `analysis.md` where will be stored the results of analysis of the prompt, the related requirements, found additional information, etc. Two keys manage the behavior of the execution - will the user be waited to approve the analysis or to proceed automatically.
  * Keys: 
    * `approval` (boolean) - false mean no approval is needed, the framework will create the file and will use it. true means the framework will create the file and will wait for approval from the user to continue based on its content.
    * `state` (strings) - the state in which the generation of the file is. Possible values are `not-started` -> `waiting-approval` -> `approved` -> `completed` (or in case `approval` is false: `not-started` -> `completed`)

* `questionnaire` (object)
  * **Meaning:**: Each prompt will generate a file `questionnaire.md` where will be stored the questions for additional clarifications. Two keys manage the behavior of the execution - will the user be waited to approve the questionnaire answers or to proceed automatically.
  * Keys: 
    * `approval` (boolean) - false mean no approval is needed, the framework will create the file and will use it. true means the framework will create the file and will wait for approval from the user to continue based on its content.
    * `state` (strings) - the state in which the generation of the file is. Possible values are `not-started` -> `waiting-approval` -> `approved` -> `completed` (or in case `approval` is false: `not-started` -> `completed`)

* `plan` (object)
  * **Meaning:**: Each prompt will generate a file `plan.md` where will be stored the plan for implementation of the prompt, the steps that will be executed, files to be changed, etc. Two keys manage the behavior of the execution - will the user be waited to approve the plan before implementation or to proceed automatically.
  * Keys: 
    * `approval` (boolean) - false mean no approval is needed, the framework will create the file and will use it. true means the framework will create the file and will wait for approval from the user to continue based on its content.
    * `state` (strings) - the state in which the generation of the file is. Possible values are `not-started` -> `waiting-approval` -> `approved` -> `completed` (or in case `approval` is false: `not-started` -> `completed`)


## Canonical example

The following is the canonical baseline structure (values may be empty during initialization):

```json
{
  "iteration-id": "ITR-20251220-224900",
  "iteration-name": "Prompt prompts-registry + state wiring",
  "prompt-id-sequence-next-value": 5,
  "prompts": [
    {
      "id": "P-001",
      "title": "Baseline problem statement",
      "type": "main",
      "state": "completed",      
      "parent-id": null,
      "analysis": {"approval": true, "state": "completed"},
      "questionnaire": {"approval": true, "state": "completed"},
      "plan": {"approval": true, "state": "completed"}
    },
    {
      "id": "P-002",
      "title": "Add architectural constraints",
      "type": "modification",      
      "state": "completed",         
      "parent-id": "P-001",
      "analysis": {"approval": false, "state": "completed"},
      "questionnaire": {"approval": false, "state": "completed"},
      "plan": {"approval": true, "state": "approved"}
    },
    {
      "id": "P-003",
      "title": "Decision-oriented output",
      "type": "modification",        
      "state": "in-progress",             
      "parent-id": "P-001",
      "analysis": {"approval": false, "state": "completed"},
      "questionnaire": {"approval": true, "state": "approved"},
      "plan": {"approval": true, "state": "waiting-approval"}
    },
    {
      "id": "P-004",
      "title": "Add logging",
      "type": "main",     
      "state": "draft",               
      "parent-id": null,
      "analysis": {"approval": false, "state": "not-started"},
      "questionnaire": {"approval": true, "state": "not-started"},
      "plan": {"approval": false, "state": "not-started"}
    }    
  ]
}
```
