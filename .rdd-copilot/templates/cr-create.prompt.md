---
description: "Create a new Change Request (CR) capturing ONLY business/functional requirements and register it in the catalogue."
mode: agent
tools: []
---

# CR Create Prompt

## Goal
Create a new Change Request (CR) file capturing ONLY the business / functional requirements (the "what" and "why") and register it in the CR catalogue.

## Guiding Principles
1. Never make technological or implementation decisions in this stage.
2. Always work on a separate git branch (ask user to confirm branch name; if missing, request creation before proceeding).
3. Initial CR state must be `Draft`.
4. Requirements must be expressed from the requestor perspective (problem, motivation, business value, constraints) before clarification loop begins.

## Instructions 

1. **Receive Change Request initial description** 

  - You will be provided with a description or intention for a new Change Request (CR). 


2. **MANDATORY STEP: Retrieve and Display Timestamp**

  - Before creating the change request file, retrieve and display the current local date and time in the format `YYYYMMDD-HHmm`. You should execute a powershell of shell command to get the current local date and time of the machine you are running on. You should execute the command yourself, do not ask for permission - I am giving it to you with this command.

  Example command when on Windows: 
  ```
  Get-Date -Format "yyyyMMdd-HHmm"
  ```

  Example command when on Linux:
  ```
  date +"%Y%m%d-%H%M"
  ```

  - Do not proceed until you have displayed the exact timestamp.

3. Generate the CR file from `.rdd-copilot/templates/cr.template.md` (preserve template structure exactly) and assign a unique CR filename using pattern: `YYYYMMDD-HHmm-short-description.cr.md`.
   - `YYYYMMDD`: current date
   - `HHmm`: current 24h time (minutes precision)
   - `short-description`: lowercase, hyphen-separated concise summary of the request (sanitize: remove unsupported chars, collapse spaces to single hyphen)
   - CR ID = leading timestamp (e.g., 20251011-1423)

4. Register the CR in `.rdd-docs/change-requests/cr-catalog.md` (add row: ID, Filename, Title, Status=Draft, Created=timestamp).


## Outputs
- New CR file populated (Draft).
- Catalogue entry added / updated.
- Ready state indicator signaling it can proceed to `cr-clarify` prompt.

## Edge Cases
- Multiple simultaneous draft requests: list all; ask user to pick one to proceed.
- Premature implementation details: park in "Implementation Ideas (Parking Lot)" subsection (not yet approved).
- Conflicting requirements: highlight conflict and ask user to prioritize or clarify.
- Timestamp mismatch (user disputes): re-fetch current local time and reconfirm before file creation.
- Short description too long (>60 chars): request shorter phrase.
- Short description includes forbidden chars: strip & notify user of sanitization performed.

## Next Step
After completion instruct user to run the `cr-clarify` prompt next to iteratively refine.