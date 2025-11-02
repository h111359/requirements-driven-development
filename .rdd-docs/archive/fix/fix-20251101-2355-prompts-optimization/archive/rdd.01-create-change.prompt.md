````prompt````prompt# Role:

# Role:

# Role:

You are here to create a new Change using the RDD framework.

You are here to create a new Change using the RDD framework.

# Context:

You are here to create a new Change using the RDD framework.

C01: This prompt leverages GitHub Copilot to create a new Change folder from template, capturing the essence of what needs to be done.

# Context:

C02: The change creation uses the unified RDD wrapper script `.rdd/scripts/rdd.sh` which automates folder creation, branch creation, file setup, and user input collection.

# Context:

C03: A "kebab-case" name is a lowercase string where words are separated by hyphens (e.g., `add-user-authentication`, `fix-login-bug`). The script automatically normalizes user input to this format.

C01: This prompt leverages GitHub Copilot to create a new Change folder from template, capturing the essence of what needs to be done.

# Rules:

C01: This prompt leverages GitHub Copilot to create a new Change folder from template, capturing the essence of what needs to be done.

R01: Never make technological or implementation decisions in this stage.

C02: The change creation uses the unified RDD wrapper script `.rdd/scripts/rdd.sh` which automates folder creation, branch creation, and file setup.

R02: DO NOT include any implementation or technical details during change creation.

C02: The change creation uses the unified RDD wrapper script `.rdd/scripts/rdd.sh` which automates folder creation, branch creation, file setup, and user input collection.

R03: The script will create a git branch with format `feat/<timestamp>-<change-name>` or `fix/<timestamp>-<change-name>`.

C03: A "kebab-case" name is a lowercase string where words are separated by hyphens (e.g., `add-user-authentication`, `fix-login-bug`).

R04: Follow the Steps section sequentially without skipping any part.

C03: A "kebab-case" name is a lowercase string where words are separated by hyphens (e.g., `add-user-authentication`, `fix-login-bug`). The script automatically normalizes user input to this format.

R05: The script handles all user input, name normalization, and validation automatically.

# Rules:

# Steps:

# Rules:

S01: The banner is automatically displayed by the rdd.sh script when executed. You do not need to display it in chat.

R01: Never make technological or implementation decisions in this stage.

S02: The git repository check is automatically performed by the rdd.sh wrapper. If not in a git repository, the command will fail with an error message.

R01: Never make technological or implementation decisions in this stage.

S03: The user description and name are automatically collected by rdd.sh when executed. The script will:

  1. Display a prompt: "Please provide a short description..."R02: Do NOT include any implementation or technical details during change creation.

  2. Wait for user input (description)

  3. Display a prompt: "Please provide a name for the change..."R02: DO NOT include any implementation or technical details during change creation.

  4. Wait for user input (name in any format)

  5. Automatically normalize the name to kebab-caseR03: The script will create a git branch with format `cng/<change-name>`.

  6. Validate the normalized name (kebab-case, max 5 words)

  7. If invalid: Show error and loop back to step 4R03: The script will create a git branch with format `feat/<timestamp>-<change-name>` or `fix/<timestamp>-<change-name>`.

  8. If valid: Display normalized name and ask for confirmation

  9. If confirmed: Proceed with change creationR04: Follow the Steps section sequentially without skipping any part.

  

  You do NOT need to ask for description or name in chat. The rdd.sh script handles all user input and validation automatically.R04: Follow the Steps section sequentially without skipping any part.



S04: Execute the unified RDD wrapper script to trigger the interactive workflow:R05: The change name must be in kebab-case format, maximum 5 words, lowercase, hyphen-separated.

  ```bash

  ./.rdd/scripts/rdd.sh change createR05: The script handles all user input, name normalization, and validation automatically.

  ```

  R06: Always propose 3 variations of the change name for user selection.

  Optional: Specify change type (defaults to 'feat'):

  ```bash# Steps:

  ./.rdd/scripts/rdd.sh change create feat    # For features (default)

  ./.rdd/scripts/rdd.sh change create fix     # For bug fixes# Steps:

  ```

  S01: The banner is automatically displayed by the rdd.sh script when executed. You do not need to display it in chat.

  The script will handle all interaction with the user automatically:

  - Display bannerS01: Display the following banner to the user:

  - Check git repository

  - Collect description from userS02: The git repository check is automatically performed by the rdd.sh wrapper. If not in a git repository, the command will fail with an error message.

  - Collect and normalize name from user

  - Create branch with format: feat/YYYYMMDD-HHmm-<normalized-name>```

  - Initialize workspace

  - Display resultsS03: The user description and name are automatically collected by rdd.sh when executed. The script will:─── RDD-COPILOT ───



S05: The results are automatically displayed by rdd.sh, including:  1. Display a prompt: "Please provide a short description..." Prompt: Create Change  

  - ✓ Change created with timestamp ID

  - 📍 Branch name (feat/YYYYMMDD-HHmm-name or fix/YYYYMMDD-HHmm-name)  2. Wait for user input (description) Description: 

  - 📁 Workspace path (.rdd-docs/workspace/)

  - 📋 Next steps:  3. Display a prompt: "Please provide a name for the change..." > Create a new Change folder with timestamped naming,

    1. Edit requirements-changes.md

    2. Use open-questions.md for clarifications  4. Wait for user input (name in any format) > branch setup, and template initialization.

    3. Run: rdd.sh change wrap-up when complete

    5. Automatically normalize the name to kebab-case

  Simply display this output to the user. The workflow is now complete, and the user can begin working on their change.

  6. Validate the normalized name (kebab-case, max 5 words) User Action: 

````

  7. If invalid: Show error and loop back to step 4 > Provide a short description of the change needed.

  8. If valid: Display normalized name and ask for confirmation───────────────

  9. If confirmed: Proceed with change creation```

  

  You do NOT need to ask for description or name in chat. The rdd.sh script handles all user input and validation automatically.S02: Check if the current folder is a git repository. If not, inform the user that this must be run from a git repository and abort.



S04: Execute the unified RDD wrapper script to trigger the interactive workflow:S03: Ask the user to provide a short description of the change. Example:

  ```bash  - Q: "Please provide a short description of the change you want to create (e.g., 'Add user authentication feature', 'Fix login page bug'):"

  ./.rdd/scripts/rdd.sh change create  - A: "I need to add a feature for users to authenticate using email and password"

  ```

  S04: Based on the user's description, generate 3 kebab-case name variations (maximum 5 words each, lowercase, hyphen-separated). Present them to the user for selection. Example:

  Optional: Specify change type (defaults to 'feat'):  ```

  ```bash  Based on your description, here are 3 suggested change names:

  ./.rdd/scripts/rdd.sh change create feat    # For features (default)  

  ./.rdd/scripts/rdd.sh change create fix     # For bug fixes  1. add-user-authentication

  ```  2. implement-email-login

    3. add-email-password-auth

  The script will handle all interaction with the user automatically:  

  - Display banner  Which option do you prefer? (enter 1, 2, 3, or provide your own kebab-case name)

  - Check git repository  ```

  - Collect description from user

  - Collect and normalize name from userS07: When user answers with the selected option, execute the unified RDD wrapper script with the change domain:

  - Create branch with format: feat/YYYYMMDD-HHmm-<normalized-name>  ```

  - Initialize workspace  ./.rdd/scripts/rdd.sh change create <selected-name> feat

  - Display results  ```

  Note: The 'feat' parameter indicates this is a feature change (use 'fix' for bug fixes).

S05: The results are automatically displayed by rdd.sh, including:

  - ✓ Change created with timestamp IDS08: Display the result to the user, including:

  - 📍 Branch name (feat/YYYYMMDD-HHmm-name or fix/YYYYMMDD-HHmm-name)  - Created folder path

  - 📁 Workspace path (.rdd-docs/workspace/)  - Created branch name

  - 📋 Next steps:  - Next steps (edit the change.md file with details)

    1. Edit requirements-changes.md
    2. Use open-questions.md for clarifications
    3. Run: rdd.sh change wrap-up when complete
  
  Simply display this output to the user. The workflow is now complete, and the user can begin working on their change.

````
