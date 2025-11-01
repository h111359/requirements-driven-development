## Stand Alone Prompts

Prompts that the agent execute - follow the instructions which promts to be executed. If nothing provided - execute only one prompt - the first not executed and stop. When a given prompt is executed, the checkbox infront of it should be marked. Changing the checkbox to `- [x]` is **the only change you are allowed to do**. Never change anything else than marking a checkbox! 

 - [x] [P01] Change `.github/prompts/rdd.F1-create-fix-branch.prompt.md`. Instead of creation of a file `.rdd-docs/workspace/change.md` to create file `.rdd-docs/workspace/journal.md` as copy from `.rdd/templates/journal.md`. You should apply the change in `./.rdd/scripts/fix-management.sh ` as well. 
  
 - [x] [P02] As the change.md is replaced by journal.md in the prompt `.github/prompts/rdd.F1-create-fix-branch.prompt.md`, it is not meaningfull to be executed the steps S09, S10, S11, S12, S13, S15. Respectively revise the "# Script Integration" sections and remove from it the respective entries as well. Remove section "# Error Handling" as well. Also in `.rdd/scripts/fix-management.sh` exists functions for clarification of What, Why, Acceptance Criteria. These are not valid anymore for this script - remove them. Check both`.github/prompts/rdd.F1-create-fix-branch.prompt.md` and `.rdd/scripts/fix-management.sh` for consistency and fix the issues if found.  

 - [x] [P03] I want to rename the prompt `.github/prompts/rdd.F1-create-fix-branch.prompt.md` to `.github/prompts/rdd.X1-create.prompt.md`, the prompt `.github/prompts/rdd.F3-execute-sa-prompt.prompt.md` to `.github/prompts/rdd.X2-execute.prompt.md` and the prompt `.github/prompts/rdd.F6-wrap-up.prompt.md` to `.github/prompts/rdd.X3-complete.prompt.md`
 
 - [x] [P04] Inspect the logic in `.github/prompts/rdd.F6-wrap-up.prompt.md`. Analyse in detail if the same logic can be achieved only with .sh script. Write the analysis and the conclusions, pros and cons, what could and what could not be done from a script (with checkboxes on each) in a file `.rdd-docs/workspace/F6-to-script-analysis.md`

 - [x] [P05] Create a script `.rdd/scripts/complete-branch.sh` which should replace `.github/prompts/rdd.F6-wrap-up.prompt.md`. Read the analysis `.rdd-docs/workspace/F6-to-script-analysis.md`. Skip those parts, which are marked as not possible to be automated - we can live without them. The main goal is the files from the folder `.rdd-docs/workspace/` to be moved in a new folder under `.rdd-docs/archive/` named after the branch name. To be checked if there are uncommited changes and if there are - to be asked the user to commit them first before continuation. Also to be checked if the current branch is merged in main and if it is - to be deleted both locally and remotely.
  
 - [x] [P06] Split the script `.rdd/scripts/complete-branch.sh` on two separate scripts: `.rdd/scripts/archive.sh` which only moves the files in an archive folder and `.rdd/scripts/delete-branch.sh` which checks the branch if it is merged in main and without uncommited changes and deletes locally and remotely. 
  
 - [x] [P07] Add to `.rdd/scripts/archive.sh` functionality in the beginning to check if there are uncommited changes and to inform the user if there are such and to stop. If not - to continue. Also after creation of the archive folder there will appear new uncommited changes - without confirmation from the user do a commit with message "archiving workspace folder for <put-branchname-here>".
 
 - [x] [P08] Check why the script `.rdd/scripts/archive.sh` sais "ℹ Checking for uncommitted changes...
✓ No uncommitted changes found" but actually there are two uncmmited changes