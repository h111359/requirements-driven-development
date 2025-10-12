# Task Executor Prompt

## Purpose
Automate the process of checking for new tasks in `.rdd-docs/tasks`, updating `.rdd-docs/tasks-catalog.md`, and executing not-started tasks in chronological order.

## Instructions
  - Read the `.rdd-docs/tasks-catalog.md` file to identify existing tasks and their statuses.
   - Ensure the table with the tasks is sorted by date and time from the filename.
   - Find the first by time task with status `not-started` and follow the next instructions for it.
  - Change its status to `in-progress` in `.rdd-docs/tasks-catalog.md`.
  - Open the corresponding task file in `.rdd-docs/tasks/`.
   - Read the task definition and follow the instructions to execute the task.
   - If the task description is unclear or lacks necessary details, ask for clarification before proceeding.
   - First create a detailed plan for completing the task and write it down at the end of the task definition file in a new section `## Execution Plan`.
   - Then start executing the task step-by-step, documenting each step in an execution log written in the same task file under new `## Execution Log` section. 
   - In this execution log section, write: 
     - Each step taken, including details, decisions, and references found. 
     - The flow of execution, status of tests, and any encountered issues or resolutions. 
     - Any additional information relevant to the execution. 
   - At the end of the task create tests to verify the task completion and document their results in a new section `## Test Results`. In this section, write: 
     - The tests created to verify the task completion. 
     - The results of each test (pass/fail) and any relevant details. 
   - If the task needs to be executed again, create a new log entry with a new timestamp in the same task file. 
   - Save the execution log in the same task file under the `## Execution Log` section. 
  - After completion, update status to `done` in `.rdd-docs/tasks-catalog.md`.
  - Auto-fill the UTC completion timestamp and add a summary note in the corresponding columns for the completed task row.
  - Make sure that the task row in `.rdd-docs/tasks-catalog.md` is moved in the section of completed tasks, maintaining the chronological order.
   - If in the section with the completed tasks there is at least one real task, remove the example row from that section.
   - If the section with active tasks is empty, add an example row to that section.

   - Proceed to the next not-started task in chronological order. 

## Notes
- Only one task should be `in-progress` at a time.
- All actions must be logged in `tasks-catalog.md`.
- Task execution should follow the instructions in each task file.
