# Modification 006 Implementation Log

## Modification Description
The questionnaire is generated and even answered, but the state in Active Prompt is not reflecting that - stays in the same way as it is not generated at all. Fix that

## Analysis
The issue is that when a questionnaire exists and answers are saved, the web UI never updates the work-iteration-registry.json flags `questionnaire-generated` and `questionnaire-answered`. The updateStatusIndicators() function reads these flags from the prompt metadata, but they are never set to true.

Root cause: The loadQuestionnaire() function successfully loads questionnaire.json but doesn't call the Python scripts to update the registry flags.

## Implementation Steps

### Step 1: Added helper functions to update registry flags
✅ Completed

Added two new functions in `.rdd/src/web/static/app.js`:
- `updateQuestionnaireGeneratedFlag(value)` - calls `/api/action` with `prompt_questionnaire_generated_on` or `_off`
- `updateQuestionnaireAnsweredFlag(value)` - calls `/api/action` with `prompt_questionnaire_answered_on` or `_off`

### Step 2: Update loadQuestionnaire() to set flags when questionnaire exists
✅ Completed

Modified `loadQuestionnaire()` function in `.rdd/src/web/static/app.js`:
- After successfully loading questionnaire.json, call `updateQuestionnaireGeneratedFlag(true)`
- Check if all questions are answered using `data.questions.every(q => q['user-selection'] && q['user-selection'].type)`
- Call `updateQuestionnaireAnsweredFlag(allAnswered)` to set the answered flag appropriately

### Step 3: Update saveQuestionnaireAnswer() to check completion
✅ Completed

Modified `saveQuestionnaireAnswer()` function in `.rdd/src/web/static/app.js`:
- After successfully saving an answer, check if all questions are now answered
- Call `updateQuestionnaireAnsweredFlag(allAnswered)` to update the flag
- Added call to `loadActivePrompt()` to refresh the status badges immediately

## Result
The Active Prompt page now correctly shows:
- Questionnaire badge updates to indicate "Generated" (warning/yellow) or "Answered" (success/green) status
- Status badges refresh automatically when answers are saved
- Registry flags `questionnaire-generated` and `questionnaire-answered` are kept in sync with actual questionnaire state
