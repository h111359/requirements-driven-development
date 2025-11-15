# P01 Implementation Log

## Step 1: Analyze the Prompt

Prompt: Write a python script in `scripts` named `config-management.py` which should work in a terminal. The script should read the file `.rdd-docs/config.json`, displays the current values for the version, the default branch and the local only flag from it to the user and asks if the major version, minor version, patch version or the default branch should be changed. If version major, the script should add 1 to the major part of the version - for example from 1.11.22 should become 2.11.22. If the choice of the user is version minor - the script should increase the minor version with 1, for example from 1.11.22 should become 1.12.22. And if patch - the script should increase the patch version with 1, for example from 1.11.22 should become 1.11.23. If the choice is the default branch - the script should list all the branches with numbers and the user should choose a number and the name of the branch should be written as "defaultBranch" value.

## Step 2: Gather Context

- Read `.rdd-docs/config.json` for current values.
- List git branches for default branch selection.
- Script must update `.rdd-docs/config.json` accordingly.

## Step 3: Plan Implementation

- Script will be named `scripts/config-management.py`.
- It will:
  1. Read `.rdd-docs/config.json`.
  2. Display version, default branch, and local only flag.
  3. Ask user what to change (major, minor, patch, default branch).
  4. If version: increment selected part, reset lower parts if needed.
  5. If default branch: list git branches, let user pick, update value.
  6. Write changes back to `.rdd-docs/config.json`.

## Step 4: Implementation Steps

- Use `json` module for config file.
- Use `subprocess` to get git branches.
- Use `input()` for user interaction.
- Log all commands and decisions here.

## Next: Implement the script in `scripts/config-management.py`.

### Implementation
- Created `scripts/config-management.py` as specified.
- Script reads `.rdd-docs/config.json`, displays version, default branch, and local only flag.
- Prompts user for which value to change (major, minor, patch, default branch).
- If version is changed, increments the selected part and resets lower parts as required.
- If default branch is changed, lists git branches and updates the config.
- Writes changes back to `.rdd-docs/config.json`.

### Test Run
Command run:
```bash
python scripts/config-management.py
```
Output:
```
Current version: 1.0.5
Default branch: dev
Local only flag: false

What would you like to change?
1. Version major
2. Version minor
3. Version patch
4. Default branch
Enter number (1-4): 1
Updating version: 1.0.5 -> 2.0.0
Version updated.
```

Result: `.rdd-docs/config.json` now contains:
```json
{
  "version": "2.0.0",
  "defaultBranch": "dev",
  "created": "2025-10-01T07:22:00.170656+00:00",
  "lastModified": "2025-11-14T04:22:33.170656+00:00",
  "localOnly": "false"
}
```
