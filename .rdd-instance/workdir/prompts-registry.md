%%PROMPT P-001 "Files view activated from icons"
On "Active Prompt" page, The user could press the execution-mode buttons by mistake while they intend to see the respective file. Instead of having tabs for showing the different files on one place and execution-mode buttons on another, they need to be united in same place on the page. I want the buttons ("Clarity", "Analyze", "Plan", "Implement", "Modifications") under the status icons to be used to show the respective file. Same placeholder where the prompt.md is shown should be reused for the other files (be sure it is the same placeholder as now in some situations several files appear one after another). 

This means the current "No Action" button to be titled "Prompt" and when clicked to show the prompt.md. The "Clarify" button to be titled "Questionnaire" and to show questionnaire.md file of the active prompt. Respectively Analyze -> Analysys to show analysis.md, Plan -> Plan to show plan.md, Implement -> Implementation to show implementation.md. Modification should show a Modifications list as in the modal. 

The current functionality of these buttons - to set execution-mode - should be realized with a new radio button group with labels equal to the current buttons - "Clarify", "Analyze", "Plan", "Implement". The status icon, the file button and the radio for execution-mode setting should be visually grouped together in areas. The "No action" should be in the "Prompt" area. The buttons should be disabled when the statuses are not true (this will mean the respective file is not ready).


### Modification 001

Move the new areas in the same place where the buttons were before - between "Create Modification" button and "Copy Execute Cmd) as a centered sub-area
%%ENDPROMPT

%%PROMPT P-002 "UX changes"
[[[ROLE_SOFTWARE_DEVELOPER]]]

Place the Config tab between Requirements and Help
%%ENDPROMPT

%%PROMPT P-003 "Workdir metadata"
Move the area from Workdir tab with Iteration Metadata (the ID, Name) to the title area of the Active Prompt page.
Do not show Total Prompts, Next ID, Git
%%ENDPROMPT
