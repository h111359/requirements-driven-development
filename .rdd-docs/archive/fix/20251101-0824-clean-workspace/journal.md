## Stand Alone Prompts

Prompts that the agent execute - follow the instructions which promts to be executed. If nothing provided - execute only one prompt - the first not executed and stop. When a given prompt is executed, the checkbox infront of it should be marked. Changing the checkbox to `- [x]` is **the only change you are allowed to do**. Never change anything else than marking a checkbox! 

 - [x] [P001] Create a new file.github/prompts/rdd.F3-execute-sa-prompt.prompt.md. This should be a github prompt that instructs the agent to execute the instructions in a promts from "## Stand Alone Prompts" section in the file `.rdd-docs/workspace/fix-journal.md`. If nothing provided as prompt ID - list to the user the prompts in `.rdd-docs/workspace/fix-journal.md` file, section "## Stand Alone Prompts" which are not marked and ask the user to choose which prompt to be executed. When the ID of the prompt is clear - take the text from the prompt and execute it in the same way as if the user had entered it in the chat. After a given prompt is executed, the checkbox infront of it should be marked. Changing the checkbox to `- [x]` is **the only change you are allowed to do**. Never change anything else than marking a checkbox! In case of unclarity or in cases there are multiple choices how to achieve the prompt - ask the user for their preferences - **never anticipate you know the preference**

- [x] [P002] Modify the script `.rdd/scripts/fix-management.sh` - add functionality (invent the parameters needed) so a prompt, written in `.rdd-docs/workspace/fix-journal.md` in section "## Stand Alone Prompts" to be marked as completed (to be changed the preffix from `- [ ]` to `- [x]`). The script should receive the ID of the prompt as parameter. The format of the prompt could be seen in the current file `.rdd/scripts/fix-management.sh`
  
- [x] [P003] Modify `.github/prompts/rdd.F3-execute-sa-prompt.prompt.md` so to use the script `.rdd/scripts/fix-management.sh` to modify thg checkbox of a promt instead of doing it itself.

- [x] [P004] Add instruction in `.github/prompts/rdd.F3-execute-sa-prompt.prompt.md` after each prompt execution to make a log entry in a file `.rdd-docs/workspace/log.jsonl`. For the purpose change accordingly and use the script `.rdd/scripts/fix-management.sh`. The script should check if the file `.rdd-docs/workspace/log.jsonl` exists and if not - to create it. After that to enter a new log entry accordingly the received arguments content. The log entry should contain the full answer and communication from the agent while execution of a prompt from `.rdd-docs/workspace/fix-journal.md`. See how similar logging is realized in `.rdd/scripts/clarify-changes.sh`. Add detail comments in the script describing the added functionality.

- [x] [P005] In the current branch I have made some cleanup and have commited changes which are not related to the branch itself. Still I want these fixes to be merged in main (for which I have to do a pull request). Propose me how to achieve that. Create a script in the workspace folder that will do the work.

- [x] [P005-01] Check `.rdd-docs/workspace/merge-fixes-to-main.sh`. Have in mind that I have also not commited changes left in the current branch. Also I don't want to enter SHA hashes. If you need a name for a temporary branch - follow the specification in `.rdd/templates/version-control.md` and use the name "cleaning-workspace". This is one time script - I don't want to provide paramenters to it. Find out what the current state is and act accordingly.

- [x] [P006] Create .gitignore file in the root folder. 
  
- [x] [P007] Rename `.rdd-docs/workspace/fix-journal.md` to `.rdd-docs/workspace/journal.md` and update `.rdd/scripts/fix-management.sh` and `.github/prompts/rdd.F3-execute-sa-prompt.prompt.md` respectively.

- [x] [P008] create a script build.sh in the folder scripts/, which is doing the following steps exactly in the order they are listed here:
    - creates or if exists - removes all the content of a folder build/ in the root folder
    - creates folder `build/.rdd/`
    - creates folder `build/.github/`
    - copy the folder `.github/prompts/` in `build/.github/`
    - copy the file `.github/copilot-instructions.md` in folder `build/.github/templates`    -  
    - copy of `.rdd/templates/` folder in `build/.rdd/` 
    - copy of `.rdd/scripts/` folder in `build/.rdd/` 


