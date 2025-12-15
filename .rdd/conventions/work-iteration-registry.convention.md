# Work Iteration Registry Convention

This document defines the required structure and content conventions for the file:

- `.rdd-instance/workdir/work-iteration-registry.json`

The registry is the single source of truth for the current work-iteration’s progress and task queue.

## File format

- **Format:** JSON object (UTF-8)
- **Top-level type:** object
- **Key style:**
  - Top-level metadata uses **UPPER-KEBAB-CASE** for prompt identifiers (`PROMPT-ID`, `PROMPT-NAME`).
  - Workflow stage keys use **lowercase** (`context`, `clarity`, `plan`, `implementation`, `tasks`).
  - Task-list item fields use **lower-kebab-case** (`task-id`, `implementation-file`).

## Top-level schema

The JSON file MUST be an object with the following keys:

### `mode` (string)

- **Required:** yes
- **Allowed values:**
  - `userStory`, `task`
- **Meaning:** Declares the operating mode for the iteration.
  - `userStory`: execute a selected user story (with its own prompt and stage tracking).
  - `task`: execute a selected task from the independent `tasks` queue.

### `userStories` (array)

- **Required:** yes
- **Type:** array of **User Story** objects
- **Meaning:** Ordered list of user stories for the iteration. Each user story has its own prompt and its own stage-tracking fields.

#### User Story object schema

Each user story entry MUST be an object with these keys:

- `user-story-id` (string)
  - **Required:** yes
  - **Convention:** `US###` format (e.g., `US001`).
- `name` (string)
  - **Required:** yes
  - **Meaning:** Human-friendly name/title.
- `prompt-file` (string)
  - **Required:** yes
  - **Meaning:** Path to the prompt file for this user story (typically under `.rdd-instance/workdir/`).
  - **Convention:** Empty string means “not set yet”.
- Stage sections: `context`, `clarity`, `plan`, `implementation`
  - **Required:** yes
  - **Meaning:** Per-user-story execution progress and artifact pointers.

##### Stage section schema (per user story)

Each stage section MUST be an object describing completion state and associated artifact(s).

Shared fields:

- `state` (string)
  - **Required:** yes
  - **Allowed values:**
    - `not-started`
    - (Other values may be introduced by the RDD workflow; keep backward compatibility.)
  - **Meaning:** Current state of that stage.

- `file` (string)
  - **Required:** yes
  - **Meaning:** Path to the stage’s primary artifact file (relative or absolute, as used by the tooling).
  - **Convention:** Empty string means “no artifact file yet”.

`implementation` extra fields:

- `approved` (boolean)
  - **Required:** yes (for `implementation`)
  - **Meaning:** Whether the implementation output has been explicitly approved.
  - **Convention:** Defaults to `false`.

### `active` (object)

- **Required:** yes
- **Meaning:** Pointers for what should be executed next.

Fields:

- `active-user-story-id` (string)
  - **Required:** yes
  - **Meaning:** Selected user story for execution when `mode` is `userStory`.
  - **Convention:** Empty string means “not selected”.
- `active-task-id` (string)
  - **Required:** yes
  - **Meaning:** Selected task for execution when `mode` is `task`.
  - **Convention:** Empty string means “not selected”.

### `tasks` (object)

The `tasks` object MUST exist and MUST contain the task queue and ID counters.

Tasks are **independent** from `userStories`:

- Tasks DO NOT belong to a specific user story by default.
- A task may optionally reference a user story (e.g., via a `related-user-story-id` field), but this is not required.
- Tasks MUST be executable without executing any user story.

#### `Next-Task-For-Execution` (string)

- **Required:** yes
- **Meaning:** The next task ID to execute.
- **Convention:** Uses the `T###` format (e.g., `T001`).

#### `Next-Unused-Task-ID` (string)

- **Required:** yes
- **Meaning:** The next unused task ID to allocate when creating a new task.
- **Convention:** Uses the `T###` format and MUST be greater than any existing task ID in `Tasks-List`.

#### `Tasks-List` (array)

- **Required:** yes
- **Type:** array of task objects
- **Meaning:** Ordered list of tasks for the iteration.

##### Task object schema

Each task entry MUST be an object with these keys:

- `task-id` (string)
  - **Required:** yes
  - **Convention:** `T###` format (e.g., `T001`).
- `description` (string)
  - **Required:** yes
  - **Meaning:** Human-readable task description.
- `status` (string)
  - **Required:** yes
  - **Allowed values:**
    - `not-started`
    - (Other values may be introduced by the RDD workflow.)
- `implementation-file` (string)
  - **Required:** yes
  - **Meaning:** File where the task’s implementation lives (if any).
  - **Convention:** Empty string means “not implemented / no file yet”.

## Invariants and consistency rules

Tooling that writes this file SHOULD maintain the following invariants:

1. **Task ID uniqueness**: every `task-id` in `Tasks-List` is unique.
2. **Counters are consistent**:
   - `Next-Unused-Task-ID` MUST NOT collide with any existing `task-id`.
   - `Next-Task-For-Execution` SHOULD refer to an existing task in `Tasks-List` (unless the workflow supports “no next task” semantics).
3. **Stage artifact pointers**:
   - When a stage `state` is not `not-started`, the stage `file` SHOULD typically be set to a non-empty value.

## Canonical example

The following is the canonical baseline structure (values may be empty during initialization):

```json
{
  "mode": "userStory",
  "active": {
    "active-user-story-id": "US001",
    "active-task-id": ""
  },
  "userStories": [
    {
      "user-story-id": "US001",
      "name": "Example user story",
      "prompt-file": ".rdd-instance/workdir/user-story-US001.prompt.md",
      "context": { "state": "not-started", "file": "" },
      "clarity": { "state": "not-started", "file": "" },
      "plan": { "state": "not-started", "file": "" },
      "implementation": { "state": "not-started", "approved": false, "file": "" }
    }
  ],
  "tasks": {
    "Next-Task-For-Execution": "T001",
    "Next-Unused-Task-ID": "T002",
    "Tasks-List": [
      {
        "task-id": "T001",
        "description": "",
        "status": "not-started",
        "implementation-file": ""
      }
    ]
  }
}
```
