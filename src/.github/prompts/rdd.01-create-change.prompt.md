# Role:

You are here to create a new Change using the RDD framework.

# Context:

C01: This prompt leverages GitHub Copilot to create a new Change folder from template, capturing the essence of what needs to be done.

C02: The change creation uses the script `.rdd/scripts/create-change.sh` which automates folder creation, branch creation, and file setup.

C03: A "kebab-case" name is a lowercase string where words are separated by hyphens (e.g., `add-user-authentication`, `fix-login-bug`).

# Rules:

R01: Never make technological or implementation decisions in this stage.

R02: Do NOT include any implementation or technical details during change creation.

R03: The script will create a git branch with format `cng/<change-name>`.

R04: Follow the Steps section sequentially without skipping any part.

R05: The change name must be in kebab-case format, maximum 5 words, lowercase, hyphen-separated.

R06: Always propose 3 variations of the change name for user selection.

# Steps:

S01: Display the following banner to the user:

```
─── RDD-COPILOT ───
 Prompt: Create Change  
 Description: 
 > Create a new Change folder with timestamped naming,
 > branch setup, and template initialization.

 User Action: 
 > Provide a short description of the change needed.
───────────────
```

S02: Check if the current folder is a git repository. If not, inform the user that this must be run from a git repository and abort.

S03: Ask the user to provide a short description of the change. Example:
  - Q: "Please provide a short description of the change you want to create (e.g., 'Add user authentication feature', 'Fix login page bug'):"
  - A: "I need to add a feature for users to authenticate using email and password"

S04: Based on the user's description, generate 3 kebab-case name variations (maximum 5 words each, lowercase, hyphen-separated). Present them to the user for selection. Example:
  ```
  Based on your description, here are 3 suggested change names:
  
  1. add-user-authentication
  2. implement-email-login
  3. add-email-password-auth
  
  Which option do you prefer? (enter 1, 2, 3, or provide your own kebab-case name)
  ```

S07: When user answers with the selected option, execute the script `.rdd/scripts/create-change.sh` with the selected name as parameter:
  ```
  ./.rdd/scripts/create-change.sh <selected-name>
  ```

S08: Display the result to the user, including:
  - Created folder path
  - Created branch name
  - Next steps (edit the change.md file with details)
