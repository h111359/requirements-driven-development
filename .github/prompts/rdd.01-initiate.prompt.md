# RDD: Initiate New Change

## Purpose
Start a new feature or fix in the RDD framework.

## Instructions

**S01: Determine Change Type**

Ask the user:
> "What type of change would you like to create?
> - **feature** - New functionality or enhancement
> - **fix** - Bug fix or correction
> 
> Please respond with either 'feature' or 'fix'."

**S02: Execute Command**

Based on the user's response, execute the appropriate command:

- If user chose **feature**:
  ```bash
  ./.rdd/scripts/rdd.sh change create feat
  ```

- If user chose **fix**:
  ```bash
  ./.rdd/scripts/rdd.sh change create fix
  ```


