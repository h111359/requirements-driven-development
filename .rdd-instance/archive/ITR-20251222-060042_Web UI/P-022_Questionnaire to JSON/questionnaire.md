# Questionnaire for P-022: Questionnaire to JSON

## Context

The current questionnaire system uses markdown files for storing questions, options, and user answers. This creates challenges for programmatic parsing and interactive UI implementation. The user wants to convert the questionnaire format to JSON to enable better structure, easier parsing, and form-based UI interaction where users can select answers directly in the Web UI with immediate persistence to the JSON file.

---

**Q1: What should be the JSON structure for storing questionnaire data?**

Please choose one:
- [ ] **A)** Flat array of question objects, where each question contains: `id`, `question`, `options` (array of {id, label, pros, cons}), `recommended-answer`, `rationale`, and `user-answer`.
  - **Pros:** Simple structure, easy to iterate, all data at one level
  - **Cons:** No context metadata, no versioning support
  
- [x] **B)** Nested structure with metadata and questions array: `{ "context": "...", "questions": [{question-object}] }` where each question object includes: `id`, `question-text`, `options`, `recommended-option`, `recommendation-rationale`, `user-selection`, and optional `custom-answer`.
  - **Pros:** Separates context from questions, supports metadata, extensible, matches current markdown format
  - **Cons:** Slightly more complex structure
  
- [ ] **C)** Question-centric structure with separate answer tracking: `{ "questions": {...}, "answers": {...} }` where questions and answers are stored in separate objects keyed by question ID.
  - **Pros:** Clean separation of template from responses, easier to reset answers
  - **Cons:** More complex to manage consistency between questions and answers
  
- [ ] **D)** Other (please specify): _________________

---

**Q2: How should individual question options be structured in the JSON?**

Please choose one:
- [ ] **A)** Simple array of strings: `"options": ["Option A", "Option B", ...]` with a separate field for pros/cons as a dictionary keyed by option index.
  - **Pros:** Minimal structure, easy to read
  - **Cons:** Difficult to associate pros/cons with specific options, no option IDs
  
- [x] **B)** Array of option objects: `"options": [{"id": "A", "label": "...", "pros": "...", "cons": "..."}, ...]` with each option having explicit fields.
  - **Pros:** Clear structure, easy to parse, self-documenting, supports rich metadata
  - **Cons:** More verbose JSON
  
- [ ] **C)** Dictionary keyed by option ID: `"options": {"A": {"label": "...", "pros": "...", "cons": "..."}, "B": {...}}`.
  - **Pros:** Direct access by ID, clean lookup
  - **Cons:** No guaranteed ordering, harder to iterate in display order
  
- [ ] **D)** Other (please specify): _________________

---

**Q3: How should user answers be stored and validated in the JSON?**

Please choose one:
- [ ] **A)** Single `user-answer` field containing the selected option ID (e.g., "A", "B") with a separate `custom-text` field for free-text answers.
  - **Pros:** Simple structure, clear separation between predefined and custom answers
  - **Cons:** Need to check two fields to determine user's full answer
  
- [x] **B)** Object-based answer: `"user-selection": {"type": "predefined|custom", "value": "A|custom-text"}` clearly indicating the answer type.
  - **Pros:** Single source of truth, explicit type indication, easy to validate
  - **Cons:** Slightly more complex to parse
  
- [ ] **C)** Array-based to support multi-select in the future: `"user-answers": ["A", "B"]` with custom text as a special ID like "CUSTOM:<text>".
  - **Pros:** Future-proof for multi-select scenarios, flexible
  - **Cons:** Overengineered for current single-select use case
  
- [ ] **D)** Other (please specify): _________________

---

**Q4: Should the JSON schema include the recommendation and rationale for each question?**

Please choose one:
- [x] **A)** Yes, include `recommended-option` (the option ID) and `recommendation-rationale` (explanation text) as fields in each question object.
  - **Pros:** Preserves current functionality, helps users make informed decisions, visible in UI
  - **Cons:** Adds more data to each question
  
- [ ] **B)** No, remove recommendations to keep the JSON minimal and let users decide independently without bias.
  - **Pros:** Simpler JSON, no potential bias toward copilot's recommendation
  - **Cons:** Loses helpful guidance that speeds up decision-making
  
- [ ] **C)** Make it optional with a flag: `"has-recommendation": true/false` and only include recommendation fields when true.
  - **Pros:** Flexible, can skip recommendations when not needed
  - **Cons:** Adds conditional logic to parsing and rendering
  
- [ ] **D)** Other (please specify): _________________

---

**Q5: How should the Web UI present the questionnaire form to users?**

Please choose one:
- [ ] **A)** Single-page form showing all questions at once with radio buttons for options and a submit button at the bottom to save all answers.
  - **Pros:** See all questions at once, faster for small questionnaires
  - **Cons:** Overwhelming for many questions, no incremental saving
  
- [x] **B)** Accordion-style or tabbed interface where each question is a separate section, with individual save buttons per question for immediate persistence.
  - **Pros:** Focused interaction, incremental saves (matches requirement for immediate reflection), scalable to many questions
  - **Cons:** Slightly more UI complexity, multiple save operations
  
- [ ] **C)** Wizard-style step-by-step flow with Next/Previous buttons and auto-save on each step.
  - **Pros:** Guided experience, auto-save ensures no data loss
  - **Cons:** More navigation clicks, can't see multiple questions simultaneously
  
- [ ] **D)** Collapsible cards for each question with inline editing and auto-save on selection change (no explicit save button).
  - **Pros:** Minimal UI friction, instant persistence, clean layout
  - **Cons:** No explicit confirmation, potential for accidental changes
  
- [ ] **E)** Other (please specify): _________________

---

**Q6: What should happen to existing markdown questionnaire files from previous prompts?**

Please choose one:
- [ ] **A)** Automatically convert all existing questionnaire.md files to questionnaire.json using a migration script that parses markdown and generates JSON.
  - **Pros:** Full backward compatibility, all historical data in new format
  - **Cons:** Complex migration logic, risk of parsing errors, time-consuming
  
- [x] **B)** No conversion - leave existing questionnaire.md files as-is and only generate JSON for new prompts going forward (as specified in the prompt: "Do not change the questionnaires back in time - no need of back compatibility").
  - **Pros:** No migration risk, simpler implementation, respects user's explicit instruction
  - **Cons:** Mixed formats in the system (acceptable per user requirement)
  
- [ ] **C)** Hybrid approach: display old markdown files as read-only text in the UI, but new questionnaires use JSON with interactive forms.
  - **Pros:** Graceful degradation, old data still accessible
  - **Cons:** Two rendering paths in UI code
  
- [ ] **D)** Other (please specify): _________________

---

**Q7: How should the questionnaire JSON file be updated when the user selects an answer in the Web UI?**

Please choose one:
- [x] **A)** Immediate API call on each option selection that updates the JSON file directly without requiring a save button.
  - **Pros:** True real-time persistence (matches requirement), no save button needed, impossible to forget to save
  - **Cons:** Many file writes for rapid changes, potential partial state if connection fails
  
- [ ] **B)** API call triggered by a "Save Answer" button per question that updates only that specific question's user-selection in the JSON.
  - **Pros:** Explicit save action, users confirm choices, batches rapid changes, clearer error handling
  - **Cons:** Requires user to click save, possible to forget
  
- [x] **C)** Debounced auto-save (e.g., 2 seconds after last change) that updates the JSON file automatically after user stops interacting.
  - **Pros:** Balance between auto-save and reducing file writes
  - **Cons:** Delayed persistence, confusing UX (unclear when data is saved)
  
- [x] **D)** Save all answers button at the questionnaire level that updates the entire JSON file with all user selections at once.
  - **Pros:** Single transaction, atomic update
  - **Cons:** Loses answers if user navigates away without saving all
  
- [ ] **E)** Other (please specify): _________________

---

**Q8: Should the system validate that all required questions are answered?**

Please choose one:
- [ ] **A)** Yes, implement validation that prevents moving forward (e.g., setting questionnaire-answered flag) until all questions have either a selected option or custom text.
  - **Pros:** Ensures completeness, prevents skipped questions
  - **Cons:** Rigid, might force answers when user is unsure
  
- [x] **B)** Partial validation: warn users about unanswered questions but allow proceeding anyway with a confirmation dialog.
  - **Pros:** Flexible, guides without blocking
  - **Cons:** Users might ignore warnings
  
- [x] **C)** No validation - allow unanswered questions and let users answer at their own pace, marking questionnaire-answered manually when ready.
  - **Pros:** Maximum flexibility, non-blocking workflow
  - **Cons:** Possible to forget questions, less structured process
  
- [ ] **D)** Other (please specify): _________________

---

**Q9: How should the "custom answer" option be presented in the UI form?**

Please choose one:
- [ ] **A)** Add a radio button for "Other (please specify)" with a disabled text input that enables when the "Other" option is selected.
  - **Pros:** Clear two-step interaction, text input appears only when needed
  - **Cons:** Two clicks required to enter custom text
  
- [x] **B)** Always show a text input field labeled "Custom answer (if none of the above fit)" below the radio options, which becomes active when any text is entered.
  - **Pros:** Visible and accessible at all times, one-step interaction
  - **Cons:** Takes up space even when not used
  
- [ ] **C)** Provide a separate "Add Custom Answer" button that, when clicked, shows a modal dialog for entering custom text.
  - **Pros:** Clean UI when not used, modal provides focus
  - **Cons:** Extra click, breaks inline flow
  
- [ ] **D)** Other (please specify): _________________

---

**Q10: What API endpoint should be used for updating user answers in the questionnaire JSON?**

Please choose one:
- [ ] **A)** Create a new dedicated endpoint POST `/api/questionnaire/update` that accepts `prompt-id`, `question-id`, and `answer` parameters.
  - **Pros:** Specialized endpoint, clear intent, can add questionnaire-specific logic
  - **Cons:** Another endpoint to maintain
  
- [x] **B)** Reuse the existing POST `/api/file/save` endpoint by reading the entire JSON, updating the specific question's user-selection, and writing back the entire file.
  - **Pros:** Reuses existing infrastructure, no new endpoints
  - **Cons:** Reads and writes entire file for small changes, potential race conditions
  
- [ ] **C)** Create a specialized endpoint POST `/api/questionnaire/answer` that uses JSON Patch or similar to update only the specific field.
  - **Pros:** Efficient updates, atomic operations, no full file read/write
  - **Cons:** More complex implementation, requires JSON Patch library
  
- [ ] **D)** Other (please specify): _________________

---

**Recommendation:** 
- **Q1:** Option B - Provides clean structure with context separation
- **Q2:** Option B - Self-documenting option objects
- **Q3:** Option B - Explicit type indication for validation
- **Q4:** Option A - Preserve helpful recommendations
- **Q5:** Option B - Accordion style matches incremental save requirement
- **Q6:** Option B - Follows user's explicit "no back compatibility" instruction
- **Q7:** Option B - Explicit save balances UX and reliability
- **Q8:** Option C - Maximum flexibility for user workflow
- **Q9:** Option B - Always visible for accessibility
- **Q10:** Option B - Leverage existing infrastructure for faster implementation
