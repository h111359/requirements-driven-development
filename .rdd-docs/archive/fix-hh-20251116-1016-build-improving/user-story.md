# User Story

## State

<!-- Mark the current state with [x]. Only ONE state should be marked at a time. -->

 - [ ] State 1: Not fulfilled "What is needed?"
 - [ ] State 2: "What is needed?" is fulfilled and not fulfilled "Why is it needed and by whom??"
 - [ ] State 3: "Why is it needed and by whom??" is fulfilled and not fulfilled "What are the acceptance criteria?"
 - [ ] State 4: All the main questions are answered - "What is needed?", "Why is it needed and by whom??", "What are the acceptance criteria?" and "What other considerations should be taken into account?" is not fulfilled
 - [ ] State 5: All the main questions are answered - "What is needed?", "Why is it needed and by whom??", "What are the acceptance criteria?", "What other considerations should be taken into account?" are fulfilled. "Requirements Questionnaire" is not generated
 - [ ] State 6: "Requirements Questionnaire" is generated, but not all questions are answered
 - [ ] State 7: "Requirements Questionnaire" is generated, all questions are answered, still not confirmed that no more questions are needed
 - [ ] State 8: No more questions are needed so the "Execution Plan" is generated, but not confirmed that it is detailed enough
 - [ ] State 9: "Execution Plan" is considered not detailed enough and revision is needed

## What is needed?

<!-- Describe the feature, functionality, or change that needs to be implemented -->


## Why is it needed and by whom??

<!-- Explain the problem being solved, the value delivered, and who will benefit from this change -->


## What are the acceptance criteria?

<!-- List specific, measurable criteria that must be met for this user story to be considered complete -->

- [ ] 
- [ ] 
- [ ] 


## What other considerations should be taken into account?

<!-- Note any technical constraints, dependencies, risks, or other factors that should be considered during implementation -->


## Requirements Questionnaire

<!-- This section will be populated by the analyse-and-plan prompt based on the clarity checklist -->
<!-- Questions should follow the format from .rdd/templates/questions-formatting.md -->
<!-- Each question should have multiple choice options (a, b, c, z for "Other") -->
<!-- Mark answered questions with [x] -->


## Execution Plan

<!-- This section will be populated when all requirements questions are answered and confirmed complete -->
<!-- Follow the structure from .rdd/templates/work-iteration-prompts.md -->
<!-- Format: - [ ] [Pnn] <PROMPT-TEXT> -->
<!-- P IDs should start from the lowest unchecked ID in .rdd-docs/work-iteration-prompts.md -->

 - [ ] [P01] <PROMPT-PLACEHOLDER>
  
 - [ ] [P02] <PROMPT-PLACEHOLDER>

 - [ ] [P03] <PROMPT-PLACEHOLDER>
 
 - [ ] [P04] <PROMPT-PLACEHOLDER>

 - [ ] [P05] <PROMPT-PLACEHOLDER>


---

**Instructions:**
1. Fill out each main section (What, Why, Acceptance Criteria, Considerations) before moving to questionnaire
2. The state marker will be updated by the analyse-and-plan prompt
3. Requirements Questionnaire will be generated based on clarity checks
4. Execution Plan will be generated after all questions are answered and confirmed
5. This file will be backed up to workspace and reset to template during iteration completion
