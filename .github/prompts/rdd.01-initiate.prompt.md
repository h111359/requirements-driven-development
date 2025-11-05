# RDD: Initiate New Change

## Purpose
Start a new enhancement or fix in the RDD framework.

## Instructions

**S01: Determine Change Type**

Ask the user:
> "What type of change would you like to create?
> - E:) **enhancement** - New functionality or enhancement
> - F:) **fix** - Bug fix or correction
>
> Please respond with either 'e' or 'f'

**S02: Execute Command**

Based on the user's response, execute the appropriate command:

- If user chose **enhancement**:
  ```python
  python .rdd/scripts/rdd.py change create enh
  ```

- If user chose **fix**:
  ```python
  python .rdd/scripts/rdd.py change create fix
  ```


  