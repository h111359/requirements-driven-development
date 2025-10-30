# Role:

You are here to create a new Change Request (CR).

# Context:

C01: This prompt should leverage GitHub Copilot to create a new Change Request file from template, capturing only business / functional requirements, and initializing a draft branch & file using timestamped naming.

# Rules:


R01: Never make technological or implementation decisions in this stage.

R02: Do NOT include any implementation or technical details in the CR creation stage.

R03: Always work on a separate git branch. The expected branch name is `cr/<cr-id>-<cr-name>`, where `<cr-id>` and `<cr-name>` are derived from the CR file name (it is explained how to get them in Steps).

R04: The initial CR state must be `draft`.

R05: Requirements must be expressed from the requestor perspective (problem, motivation, business value, constraints) before clarification loop begins.

R06: Follow the Instructions section step-by-step without skipping any part.

R07; Section 7 and 8 of the CR template must be left without change for now.

# Steps:

S01: Display the following banner to the user:

```
─── RDD-COPILOT ───
 Prompt: CR Create  
 Description: 
 > Create a new Change Request capturing only 
 > business / functional requirements (problem, value,
 > constraints, acceptance criteria) and initialize draft
 > branch & file using timestamped naming.

 User Action: 
 > Provide short CR name & initial requirement details;
 > confirm sanitized filename components.
───────────────
```

S02: Check if the current folder is a git repository. If not, initialize a git repository and set the default branch to `main`.

S03: Before creating the change request file, retrieve and display the current date and time in the format `YYYYMMDD-HHmm`. Remember this timestamp for use in the CR filename as `<cr-id>`.

S04: Ask the user to provide a short name of the change request. Sanitize the name to create a concise, hyphen-separated summary (lowercase, remove unsupported characters, collapse spaces to single hyphen). Ensure the name is no longer than 30 characters after sanitization; if too long, request a shorter phrase.Remember this name for use in the CR filename as `<cr-name>`. The example of Question and answer is:
  - Q: "What should be the short name of the change request?"
  - A: "Add user authentication"
  - Q: Confirm the name "add-user-authentication"
  - A: "Confirmed"

S05: Create and switch to a new branch for the CR using the format: `cr/<cr-id>-<cr-name>` 

S06: Ask the user to answer on the question "Who is the requester?". Follow the example of Question and answer:
  - Q: "Who is the requester? Please provide name, role, and contact details."
  - A: "Jane Doe, Product Manager, jane.doe@example.com"
Take the answer and remember it to <who-is-the-requester> variable.

S07: Ask the user to answer on the question "What is needed?". Follow the example of Question and answer:
  - Q: "What is needed?"
  - A: "User authentication feature"
Take the answer and remember it to <what-is-needed> variable.

S08: Ask the user to answer on the question "Why is this change needed?". Follow the example of Question and answer:
  - Q: "Why is this change needed?"
  - A: "To enhance security and protect user data"
Take the answer and remember it to <why-is-this-change-needed> variable.

S09: Ask the user to provide Acceptance Criteria for the change request. Follow the example of Question and answer:
  - Q: "Please list the Acceptance Criteria for this change request."
  - A: "1. Users can register with email and password. 2. Users can log in and log out securely. 3. Passwords are stored encrypted."
Take the answer and remember it to <acceptance-criteria> variable.

S10. Check if file `.rdd-docs/change-requests/cr-<cr-id>-<cr-name>-[draft|clarified|designed|completed].cr.md` exists where [draft|clarified|designed|completed] means one of the states draft, clarified, designed, or completed is on this place. If not, create it from `.rdd-docs/templates/cr.md` (preserve template structure exactly) and assign the collected variables to the corresponding placeholders in the template:
   - `<cr-id>` -> timestamp from S03
   - `<cr-name>` -> sanitized name from S04
   - `<who-is-the-requester>` -> answer from S06
   - `<what-is-needed>` -> answer from S07
   - `<why-is-this-change-needed>` -> answer from S08
   - `<acceptance-criteria>` -> answer from S09

S11: If the file already exists, notify the user and abort the process to avoid overwriting existing CRs.

S12: Ask the user if they want to stage the new CR file, commit it with message `chore(cr): create draft change request cr-<cr-id>-<cr-name>`, and push the branch to the remote repository.