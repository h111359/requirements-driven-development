# P09 Implementation: Revise rdd.analyse-and-plan.prompt.md

## Original Prompt Text

[P09] Revise the `.github/prompts/rdd.analyse-and-plan.prompt.md` prompt. This prompt could be executed multiple times but will have different effect based on the state of the file `.rdd-docs/user-story.md`. Change it so it is appropriate for any state in which `.rdd-docs/user-story.md` could be. The states are defined in the current partially fulfilled user story `.rdd-docs/user-story.md`. Use the story `.rdd-docs/user-story.md` as example for the needed format. Change the `.rdd/templates/user-story.md` template to reflect this new format. The prompt `.github/prompts/rdd.analyse-and-plan.prompt.md`  should:
1. Detect in which state the user story is and if the state correctly reflects the reality (and change it if not)
2. Should generate a "Requirements Questionnaire" including all the questions, that need to be answered. For the purpose should follow the instructions in `.rdd/templates/requirements-format.md` how to generate the questions. Also should use `.rdd/templates/clarity-checklist.md` to find if those checks are covered. It is not necessary the `.rdd/user-story.md` itself to cover all the checks - some of the answers could be written already in `.rdd-docs/requirements.md` or in `.rdd-docs/tech-spec.md` - verify agains those files as well, without changing them. And if still the information is not found - generate a question.
3. When all the questions are generated and answered, the prompt should check if there is need of more questions. If yes - adds the question, if no - proceed with generation of the plan.
4. If the state is '"Execution Plan" is considered not detailed enough and revision is needed' - the prompt should take care either to generate more questions (and to reflect the status to some appropriate earlier state) or directly to generate more detailed plan
The generted plan should follown the structure of `.rdd/templates/work-iteration-prompts.md` and should start with the lowest P id accordingly `.rdd-docs/work-iteration-prompts.md`.
The current state in `.rdd-docs/user-story.md` is only an example - do not execute it and do not change it.

## Context Files Analysis

### Current User Story States (from `.rdd-docs/user-story.md`)

The user story file defines **9 states**:
- **State 1**: Not fulfilled "What is needed?"
- **State 2**: "What is needed?" fulfilled, "Why is it needed and for whom?" not fulfilled
- **State 3**: "Why" fulfilled, "What are the acceptance criteria?" not fulfilled
- **State 4**: Main questions answered, "What other considerations?" not fulfilled
- **State 5**: All main questions answered, "Requirements Questionnaire" not generated
- **State 6**: "Requirements Questionnaire" generated, not all questions answered
- **State 7**: All questions answered, not confirmed that no more questions needed (CURRENT STATE)
- **State 8**: No more questions needed, "Execution Plan" generated, not confirmed detailed enough
- **State 9**: "Execution Plan" considered not detailed enough, revision needed

### Current User Story Template (`.rdd/templates/user-story.md`)

The template is **too simple** - only contains the 4 main sections without states or questionnaire/plan sections. It needs to be expanded to match the format shown in the example.

### Current Analyse Prompt (`.github/prompts/rdd.analyse-and-plan.prompt.md`)

The current prompt is **outdated** - it assumes a linear workflow starting from scratch. It doesn't:
- Detect which state the user story is in
- Handle re-execution scenarios
- Check against existing requirements.md/tech-spec.md
- Follow the state-based progression
- Use the clarity checklist properly
- Generate plans in the work-iteration-prompts.md format

### Relevant Files Summary

**`.rdd/templates/requirements-format.md`**: Provides guidelines for writing requirements and generating clarification questions. Key points:
- Use "Shall" language
- Be specific and measurable
- One requirement per line
- Avoid implementation details in FR/NFR

**`.rdd/templates/clarity-checklist.md`**: Contains 50+ checklist items covering:
- Problem statement, business value, acceptance criteria
- Stakeholders, assumptions, constraints, dependencies
- Non-functional requirements (performance, security, etc.)
- Data sources, user interactions, edge cases
- Operational considerations, metrics, risks

**`.rdd/templates/work-iteration-prompts.md`**: Shows structure for execution plan:
- Format: `- [ ] [P01] <PROMPT-TEXT>`
- Checkbox-based tracking
- Sequential P IDs (P01, P02, P03, etc.)

## Implementation Plan

### Phase 1: Update User Story Template
1. Expand `.rdd/templates/user-story.md` to include:
   - State tracking section with all 9 states
   - Requirements Questionnaire section
   - Execution Plan section
   - Instructions for state progression

### Phase 2: Revise Analyse-and-Plan Prompt
2. Rewrite `.github/prompts/rdd.analyse-and-plan.prompt.md` to:
   - **Step 1**: Read and analyze user-story.md, requirements.md, tech-spec.md
   - **Step 2**: Detect current state and validate it matches reality
   - **Step 3**: Based on state, perform appropriate action:
     - States 1-4: Ask main questions one by one
     - State 5: Generate Requirements Questionnaire using clarity checklist
     - State 6: Wait for answers to be filled in by user
     - State 7: Review answers and decide if more questions needed
     - State 8: Generate detailed Execution Plan
     - State 9: Refine plan or generate more questions
   - **Step 4**: Update state in user-story.md after each action
   - **Step 5**: Save all work back to user-story.md

### Phase 3: Test and Validate
3. Ensure the prompt can:
   - Be executed multiple times without losing data
   - Correctly detect and handle each state
   - Generate questions following the formatting guidelines
   - Check clarity-checklist comprehensively
   - Verify answers against requirements.md and tech-spec.md
   - Generate plans with proper P ID sequencing

## Implementation Details

### Phase 1: Update User Story Template - COMPLETED

**File**: `.rdd/templates/user-story.md`

**Changes Made**:
1. Added "## State" section with all 9 states defined
2. Added instructions to mark only ONE state with [x]
3. Added "## Requirements Questionnaire" section with placeholder
4. Added "## Execution Plan" section with P01-P05 placeholders
5. Updated instructions to reference state progression and prompt usage

**Key Features**:
- State tracking mechanism for workflow progression
- Clear separation between main questions, questionnaire, and execution plan
- Instructions guide users through the workflow
- Template follows the format shown in the user-story.md example

### Phase 2: Revise Analyse-and-Plan Prompt - COMPLETED

**File**: `.github/prompts/rdd.analyse-and-plan.prompt.md`

**Complete Rewrite** - Changed from linear to state-based approach:

**Structure**:
- **Role**: Expert Business Analyst and Requirements Engineer
- **Context**: Explains 9-state workflow and supporting files
- **Instructions**: 5 main steps with state-specific actions

**Step 1 - Read and Analyze Context**:
- Read user-story.md, requirements.md, tech-spec.md
- Read clarity-checklist.md, work-iteration-prompts.md
- Important rule: DO NOT modify requirements.md or tech-spec.md

**Step 2 - Detect and Validate Current State**:
- Check which state is marked with [x]
- Verify state matches actual content
- Correct state if misaligned
- Announce state to user

**Step 3 - Execute State-Appropriate Action**:

*State 1*: Ask "What is needed?" → Fill section → Move to State 2
*State 2*: Ask "Why is it needed and for whom?" → Fill section → Move to State 3
*State 3*: Ask "What are the acceptance criteria?" → Fill section → Move to State 4
*State 4*: Ask "What other considerations?" → Fill section → Move to State 5

*State 5*: Generate Requirements Questionnaire:
- Analyze all 4 main sections
- Check clarity checklist for missing/unclear items
- Cross-reference with requirements.md and tech-spec.md
- Generate questions ONLY for items not already documented
- Follow questions-formatting.md guidelines
- Add multiple choice options (a, b, c, z)
- Add to user-story.md → Move to State 6

*State 6*: Wait for user to answer questions:
- Count answered vs total questions
- If all answered → Move to State 7
- If unanswered remain → List them, stay in State 6

*State 7*: Confirm no more questions needed:
- Review all answers for completeness
- Identify contradictions or gaps
- Ask user: Need more questions? (A=No, B=Yes)
- If No → Move to State 8, generate plan
- If Yes → Add questions, move to State 6

*State 8*: Generate and confirm Execution Plan:
- Read work-iteration-prompts.md for next P ID
- Break down story into actionable prompts
- Format: `- [ ] [Pnn] <DETAILED-PROMPT-TEXT>`
- Include file paths, commands, outcomes
- Ask user: Is plan detailed enough? (A=Yes, B=More detail, C=More questions)
- If Yes → Done, user copies to work-iteration-prompts.md
- If More detail → Move to State 9
- If More questions → Move to State 6

*State 9*: Revise plan:
- Ask: What revision needed? (A=Break down, B=More questions, C=Combine, D=Other)
- Revise accordingly
- Return to appropriate state

**Step 4 - Save All Changes**:
- Save modifications to user-story.md
- Ensure only ONE state marked with [x]
- Preserve all existing content

**Step 5 - Provide Clear Next Steps**:
- Inform current state
- Explain action taken
- Tell user what to do next

**Important Rules** (11 rules):
1. Never modify requirements.md or tech-spec.md
2. Only ONE state marked at a time
3. Follow question formatting guidelines
4. Use clarity checklist comprehensively
5. Check existing docs before generating questions
6. Be specific in execution plans
7. Sequence P IDs correctly
8. Preserve data, never delete
9. Ask main questions one at a time
10. Generate all questionnaire questions at once
11. Don't execute the example user story

**Version**: 2.0, Last Updated: 2025-11-15

### Phase 3: Verification - COMPLETED

**Files Updated**:
- `.rdd/templates/user-story.md` - Expanded with states, questionnaire, plan sections
- `.github/prompts/rdd.analyse-and-plan.prompt.md` - Complete rewrite with state-based logic

**Verification Points**:
✅ Prompt supports multiple executions
✅ State detection and validation included
✅ All 9 states have specific handling
✅ Questions follow formatting guidelines (from questions-formatting.md)
✅ Clarity checklist integration (comprehensive checking)
✅ Cross-reference with requirements.md and tech-spec.md
✅ Execution plan generation with P ID sequencing
✅ Data preservation (never delete user's work)
✅ Clear next steps provided after each action
✅ Template matches example format
✅ Rule: Current user story is only example, not to be executed

### Phase 4: Update Requirements and Tech Spec - COMPLETED

**Requirements.md Updates**:
Added 15 new functional requirements (FR-107 through FR-121):
- FR-107: User Story State Tracking
- FR-108: State-Based Prompt Behavior
- FR-109: State Validation
- FR-110: Single State Enforcement
- FR-111: Main Questions Collection (States 1-4)
- FR-112: Questionnaire Generation (State 5)
- FR-113: Questionnaire Answer Tracking (State 6)
- FR-114: Completeness Confirmation (State 7)
- FR-115: Execution Plan Generation (State 8)
- FR-116: Plan Detail Confirmation
- FR-117: Plan Revision Support (State 9)
- FR-118: Cross-Reference Existing Documentation
- FR-119: Question Format Compliance
- FR-120: Data Preservation During Re-execution
- FR-121: Clear Next Steps Guidance

**Tech-Spec.md Updates**:
Added new section: "### User Story State-Based Workflow"
- Documented user story template structure with 9 states
- Described Requirements Questionnaire section
- Described Execution Plan section
- Documented analyse-and-plan prompt behavior (v2.0)
- Detailed state-specific actions for all 9 states
- Listed 11 important rules
- Explained integration with framework

**Files Analysis**:
Created `.rdd-docs/workspace/files-analysis.md` documenting:
- Changed files (2): user-story.md template, analyse-and-plan prompt
- Created files (2): P09-implementation.md, old prompt backup
- Referenced files (9): read but not modified

## Summary

P09 has been successfully completed. The revisions include:

**Template Changes**:
- `.rdd/templates/user-story.md` expanded with State section, Requirements Questionnaire section, and Execution Plan section

**Prompt Rewrite**:
- `.github/prompts/rdd.analyse-and-plan.prompt.md` completely rewritten as v2.0 with state-based logic

**Documentation Updates**:
- `.rdd-docs/requirements.md` updated with 15 new functional requirements (FR-107 to FR-121)
- `.rdd-docs/tech-spec.md` updated with new "User Story State-Based Workflow" section

**Key Features**:
- 9-state workflow for systematic requirement clarification
- State detection and automatic validation
- Cross-referencing with existing requirements and tech specs
- Questionnaire generation based on clarity checklist
- Execution plan generation with proper P ID sequencing
- Multiple execution support with data preservation
- Clear guidance at each step

The prompt can now be executed multiple times, adapting to the current state of the user story, generating appropriate questions only for missing information, and producing detailed execution plans when ready.
