# Work Iteration Registry Convention

This document defines the required structure and content conventions for the file:

- `.rdd-instance/workdir/work-iteration-registry.json`

The work-iteration-registry is the single source of truth for the current work-iteration’s progress and prompts queue. Every prompt id in work registry exists in prompts registry. In case of inconsistency between this file and `.rdd-instance/workdir/prompts-registry.md`, the execution should stop and the user should be informed to fix the errors.

## Prompt registration (normative)

Tools that create prompts (scripts / Web UI) MUST treat `.rdd-instance/workdir/work-iteration-registry.json` as the source of truth for prompt metadata.

When a new prompt is created:

1. The tool MUST allocate a new prompt ID using `prompt-id-sequence-next-value` unless the tool is explicitly instructed to use a specific ID.
2. If the tool allocates an ID using `prompt-id-sequence-next-value`, it MUST increment the value by 1 and persist it.
3. The tool MUST append a new `prompt-metadata` object to the `prompts` array.
4. The tool MUST also ensure a matching prompt text record exists in `.rdd-instance/workdir/prompts-registry.md` (see `.rdd/conventions/prompts-registry.convention.md`).
5. Prompt IDs MUST remain unique across both registries.

Validation rules during prompt creation:

- If creating a prompt with state `active`, the tool MUST validate that no other prompt currently has state `active`.

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
  * map prompt IDs to prompt text in the '.rdd-instance/workdir/prompts-registry.md` file
  * associate questionnaire references (without embedding questionnaire content)
  * define capabilities/default execution semantics per prompt
* **Type:** array of `prompt-metadata` objects
* **Uniqueness constraint:** each `id` MUST be unique within the array


### `prompt-metadata` (object)

#### Required keys

* `prompt-id` (string)
  * Format: `P-` followed by digits (regex: `^P-[0-9]{3,}$`) - at least 3 digits, left-pad to 3 for <1000.
  * Example: `"P-003"`

* `prompt-title` (string)
  * Free text up to 128 chars
  * In case of difference of titles of same prompt id in comparison with `.rdd-instance/workdir/prompts-registry.md`, the title in `.rdd-instance/workdir/work-iteration-registry.json` shall be treated as the source of truth

* `state` (string)
  * **Meaning** - Defines if the prompt is currently active or completed. Only one prompt can be in `active` state at a given time, and this is the prompt which `execute command` (as defined in `.rdd-instance/specifications/requirements.md`) will run.
  * Possible values: ["active" | "completed"]

* `questionnaire-generated` (boolean)
  * **Required:** yes
  * **Default value:** false
  * **Meaning:** Indicates whether a questionnaire.md file has been generated for this prompt.

* `questionnaire-answered` (boolean)
  * **Required:** yes
  * **Default value:** false
  * **Meaning:** Indicates whether the questionnaire has been completely answered.

* `plan-generated` (boolean)
  * **Required:** yes
  * **Default value:** false
  * **Meaning:** Indicates whether a plan.md file has been generated for this prompt.

* `implementation-completed` (boolean)
  * **Required:** yes
  * **Default value:** false (true for completed prompts)
  * **Meaning:** Indicates whether the implementation has been completed.

* `execution-mode` (string)
  * **Required:** yes
  * **Default value:** "no-action"
  * **Meaning:** Defines what action the execute command will perform for this prompt.
  * **Allowed values:** "no-action" | "analyze" | "plan" | "implement"
  * **Validation rules:**
    * Can be set to any value for prompts with state `active`
    * Should typically be "no-action" for prompts with state `completed`

* `executed` (boolean)
  * **Required:** no
  * **Default value:** false
  * **Meaning:** Legacy field indicating whether the prompt has been executed at least once. Maintained for backward compatibility.


## Canonical example

The following is the canonical baseline structure (values may be empty during initialization):

```json
{
  "iteration-id": "ITR-20251220-224900",
  "iteration-name": "Prompt prompts-registry + state wiring",
  "prompt-id-sequence-next-value": 5,
  "prompts": [
    {
      "prompt-id": "P-001",
      "prompt-title": "Baseline problem statement",
      "state": "completed",
      "questionnaire-generated": true,
      "questionnaire-answered": true,
      "plan-generated": true,
      "implementation-completed": true,
      "execution-mode": "no-action",
      "executed": true
    },
    {
      "prompt-id": "P-002",
      "prompt-title": "Add architectural constraints",
      "state": "completed",
      "questionnaire-generated": false,
      "questionnaire-answered": false,
      "plan-generated": true,
      "implementation-completed": true,
      "execution-mode": "no-action",
      "executed": true
    },
    {
      "prompt-id": "P-003",
      "prompt-title": "Decision-oriented output",
      "state": "active",
      "questionnaire-generated": true,
      "questionnaire-answered": true,
      "plan-generated": true,
      "implementation-completed": false,
      "execution-mode": "implement",
      "executed": false
    },
    {
      "prompt-id": "P-004",
      "prompt-title": "Add logging",
      "state": "completed",
      "questionnaire-generated": false,
      "questionnaire-answered": false,
      "plan-generated": false,
      "implementation-completed": true,
      "execution-mode": "no-action",
      "executed": true
    }    
  ]
}
```
