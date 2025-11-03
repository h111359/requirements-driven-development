# RDD: Initiate New Change

## Purpose
Start a new enhancement or fix in the RDD framework.

## Instructions

**S01: Determine Change Type**

Ask the user:
> "What type of change would you like to create?
> - **enhancement** - New functionality or enhancement
> - **fix** - Bug fix or correction
> 
> Please respond with either 'enhancement' or 'fix'."

**S02: Execute Command**

Based on the user's response, execute the appropriate command:

- If user chose **enhancement**:
  ```bash
  ./.rdd/scripts/rdd.ps1 change create enh
  ```

- If user chose **fix**:
  ```bash
  ./.rdd/scripts/rdd.ps1 change create fix
  ```


