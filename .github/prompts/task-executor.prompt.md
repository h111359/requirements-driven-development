# Task Executor Prompt

## Purpose
Automate the process of checking for new tasks in `/docs/tasks`, updating `tasks-catalog.md`, and executing not-started tasks in chronological order.

## Instructions
1. **Scan `/docs/tasks` folder**
   - List all files matching the format `T-YYYYMMDD-HHmm-name.task.md`.
   - Identify tasks not present in `tasks-catalog.md`.

2. **Update `tasks-catalog.md`**
   - Add new tasks to the catalog table with status `not-started`.
   - Ensure the table is sorted by date and time from the filename.

3. **Execute Tasks**
   - For each task with status `not-started`, execute the task as described in its file.
   - Mark the task as `in-progress` during execution.
   - After completion, update status to `done` in `tasks-catalog.md`.
   - Proceed to the next not-started task in chronological order.

## Example Workflow
- New task file `T-20250929-1635-add-feature.task.md` is added.
- The prompt detects it, adds it to `tasks-catalog.md` as `not-started`.
- Executes the task, marks it as `done` after completion.
- Repeats for all new tasks.

## Notes
- Only one task should be `in-progress` at a time.
- All actions must be logged in `tasks-catalog.md`.
- Task execution should follow the instructions in each task file.
