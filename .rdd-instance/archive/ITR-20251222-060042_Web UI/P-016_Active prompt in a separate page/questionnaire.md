# Questionnaire for Active Prompt in a Separate Page

**ℹ️ Context**
We're redesigning the Web UI to have a separate "Active Prompt" page and rename the current "Prompts" tab to "Prompts History". The Active Prompt page will have mode selection (no-action, analyze, plan, implement) and status indicators for questionnaire, plan, and implementation states.

---

## Question 1: Navigation Structure

**Q: How should the navigation between "Prompts History" and "Active Prompt" pages be structured?**

Please choose one:
- [x] **A)** Two separate tabs in the main navigation bar (side by side)
  - **Pros:** Clear separation, easy switching, both visible at all times
  - **Cons:** Takes up more navigation space
  
- [ ] **B)** "Active Prompt" as a prominent card/button on the "Prompts History" page, clicking it navigates to a dedicated page
  - **Pros:** Single entry point, clear workflow from history to active
  - **Cons:** Requires more clicks to switch between views
  
- [ ] **C)** Split screen view with "Prompts History" list on left and "Active Prompt" details on right
  - **Pros:** Everything visible at once, no navigation needed
  - **Cons:** Less space for each section, may be cluttered on smaller screens
  
- [ ] **D)** Other (please specify): 

**Recommendation:** Option A for clear separation and easy access to both views

---

## Question 2: Mode Selection UI Component

**Q: Which UI component should be used for the mode selection (no-action|analyze|plan|implement)?**

Please choose one:
- [ ] **A)** Radio buttons in a vertical list with clear labels and descriptions
  - **Pros:** Clear mutual exclusivity, accessible, traditional
  - **Cons:** Takes up vertical space
  
- [x] **B)** Button group (like Bootstrap's btn-group) with active state highlighting
  - **Pros:** Compact, modern look, clear visual state
  - **Cons:** May be less obvious they're mutually exclusive
  
- [ ] **C)** Dropdown/select menu
  - **Pros:** Very compact, saves space
  - **Cons:** Requires click to see options, less discoverable
  
- [ ] **D)** Segmented control (iOS-style toggle between options)
  - **Pros:** Modern, space-efficient, clear mutual exclusivity
  - **Cons:** May require custom CSS implementation
  
- [ ] **E)** Other (please specify): 

**Recommendation:** Option B for modern UI and clear visual feedback

---

## Question 3: Status Indicator Colors for Not Generated State

**Q: What color should be used for status indicators when questionnaire/plan/implementation is NOT generated?**

Please choose one:
- [x] **A)** Light gray (#CCCCCC or Bootstrap's text-muted)
  - **Pros:** Neutral, clearly indicates "not started", standard convention
  - **Cons:** May blend too much with background
  
- [ ] **B)** White with gray border
  - **Pros:** Clean, distinguishable from other states
  - **Cons:** May look incomplete or unpolished
  
- [ ] **C)** Light blue (info color)
  - **Pros:** More noticeable than gray, indicates "available action"
  - **Cons:** May confuse with other semantic colors
  
- [ ] **D)** Transparent/no indicator
  - **Pros:** Minimalist, doesn't clutter UI
  - **Cons:** Less clear what's missing
  
- [ ] **E)** Other (please specify): 

**Recommendation:** Option A for standard convention and clarity

---

## Question 4: Status Indicator Visual Style

**Q: How should the status indicators for questionnaire, plan, and implementation be displayed?**

Please choose one:
- [ ] **A)** Badge/pill style (like Bootstrap badges) next to labels
  - **Pros:** Compact, standard UI pattern, clear color coding
  - **Cons:** May be too small for detailed status
  
- [x] **B)** Larger cards/panels for each mode with icon, status color, and description
  - **Pros:** Very clear, room for additional info and actions
  - **Cons:** Takes up more screen space
  
- [ ] **C)** Progress bar style with color segments
  - **Pros:** Shows overall progress, visual progression
  - **Cons:** May not clearly show individual state details
  
- [ ] **D)** Icon-based indicators (checkmark, warning, clock icons) with color coding
  - **Pros:** Visual and intuitive, language-independent
  - **Cons:** Requires learning icon meanings
  
- [ ] **E)** Other (please specify): 

**Recommendation:** Option D for clear visual communication with minimal space

---

## Question 5: Questionnaire Status Detail Level

**Q: For the questionnaire status indicator (yellow=generated but not answered, green=answered), should we show additional details?**

Please choose one:
- [ ] **A)** Just the color indicator (yellow or green)
  - **Pros:** Simple, clean UI
  - **Cons:** User may not know how many questions remain
  
- [x] **B)** Color indicator plus count (e.g., "5/10 questions answered")
  - **Pros:** Shows progress, helps user plan time
  - **Cons:** Requires tracking individual question states
  
- [ ] **C)** Color indicator plus percentage (e.g., "50% complete")
  - **Pros:** Shows progress clearly, simple metric
  - **Cons:** Requires tracking individual question states
  
- [ ] **D)** Color indicator plus simple text label (e.g., "In Progress" or "Complete")
  - **Pros:** Clear status without complexity, easy to implement
  - **Cons:** Less specific about progress
  
- [ ] **E)** Other (please specify): 

**Recommendation:** Option D for simplicity in initial implementation, can be enhanced later

---

## Question 6: Unused Attributes Handling

**Q: The prompt mentions removing unused attributes from work-iteration-registry.json. Which attributes specifically should be removed?**

**ℹ️ Context:** Current prompt entries have nested objects for "analysis", "questionnaire", and "plan" with "approval" and "state" sub-attributes. These may be replaced by simpler boolean attributes.

Please choose one:
- [x] **A)** Remove all nested objects ("analysis", "questionnaire", "plan") and replace with flat boolean attributes:
  - `questionnaire-generated`, `questionnaire-answered`, `plan-generated`, `implementation-completed`
  - **Pros:** Simpler structure, easier to work with, clearer naming
  - **Cons:** Requires migration of existing data
  
- [ ] **B)** Keep nested structure but simplify to only needed attributes
  - **Pros:** Less breaking change, maintains some organization
  - **Cons:** Still more complex than needed
  
- [ ] **C)** Remove only the "approval" sub-attribute from nested objects, keep "state"
  - **Pros:** Minimal change, removes clearly unused attribute
  - **Cons:** Doesn't fully simplify structure
  
- [ ] **D)** Conduct full analysis first to identify all unused attributes before removal
  - **Pros:** Ensures nothing important is lost
  - **Cons:** Takes more time
  
- [ ] **E)** Other (please specify): 

**Recommendation:** Option A for cleaner, more maintainable structure

---

## Question 7: Python Script Naming Convention

**Q: What naming pattern should the new Python scripts follow for setting the new boolean attributes?**

**ℹ️ Context:** Need scripts to set/unset: questionnaire-generated, questionnaire-answered, plan-generated, implementation-completed

Please choose one:
- [x] **A)** `prompt_<attribute>_on.py` / `prompt_<attribute>_off.py`
  - Example: `prompt_questionnaire_generated_on.py`, `prompt_questionnaire_generated_off.py`
  - **Pros:** Follows existing pattern (prompt_analyze_on/off), clear verb (on/off)
  - **Cons:** Long file names
  
- [ ] **B)** `prompt_set_<attribute>.py` / `prompt_unset_<attribute>.py`
  - Example: `prompt_set_questionnaire_generated.py`, `prompt_unset_questionnaire_generated.py`
  - **Pros:** More descriptive verbs, clear action
  - **Cons:** Different from existing pattern
  
- [ ] **C)** `prompt_<attribute>_true.py` / `prompt_<attribute>_false.py`
  - Example: `prompt_questionnaire_generated_true.py`, `prompt_questionnaire_generated_false.py`
  - **Pros:** Explicit about boolean nature
  - **Cons:** Slightly verbose
  
- [ ] **D)** Single script with parameter: `prompt_set_attribute.py --name questionnaire-generated --value true`
  - **Pros:** Single script handles all attributes, most flexible
  - **Cons:** Different pattern from existing scripts
  
- [ ] **E)** Other (please specify): 

**Recommendation:** Option A for consistency with existing pattern

---

## Question 8: Default Mode Selection

**Q: When the Active Prompt page loads, which mode should be selected by default if none is currently active?**

Please choose one:
- [x] **A)** "no-action" - requires explicit user selection
  - **Pros:** Safe default, prevents accidental execution
  - **Cons:** Adds extra step for user
  
- [ ] **B)** Smart default based on current state:
  - If questionnaire not generated → "analyze"
  - Else if plan not generated → "plan"
  - Else if implementation not completed → "implement"
  - Else → "no-action"
  - **Pros:** Guides user through workflow, intelligent
  - **Cons:** More complex logic, user may want different order
  
- [ ] **C)** Last used mode (stored in registry or browser)
  - **Pros:** Convenient for repeated tasks
  - **Cons:** May be confusing if context changed
  
- [ ] **D)** Always default to "analyze" as first step
  - **Pros:** Encourages thorough analysis first
  - **Cons:** May not fit all workflows
  
- [ ] **E)** Other (please specify): 

**Recommendation:** Option B for guided workflow

---

## Question 9: Mode Execution Button Behavior

**Q: How should the "Execute" button behavior change based on selected mode?**

Please choose one:
- [ ] **A)** Different button label for each mode:
  - "Analyze" button when analyze mode selected
  - "Plan" button when plan mode selected
  - "Implement" button when implement mode selected
  - Button disabled/hidden when no-action selected
  - **Pros:** Very clear what will happen, self-documenting
  - **Cons:** UI changes based on selection
  
- [ ] **B)** Always show "Execute" button, with description text showing what will execute
  - **Pros:** Consistent UI, predictable button location
  - **Cons:** Less obvious at a glance
  
- [ ] **C)** Separate buttons for each mode (Analyze, Plan, Implement) with the selected one highlighted
  - **Pros:** All options visible, can see what's available
  - **Cons:** More buttons, may clutter UI
  
- [ ] **D)** Single "Execute" button that opens confirmation dialog showing selected mode
  - **Pros:** Safe with confirmation, prevents accidental execution
  - **Cons:** Extra click required
  
- [x] **E)** Other (please specify): There should be no execute button. Selecting the mode should be immediately reflected in `.rdd-instance/workdir/work-iteration-registry.json`. Execution is triggered manually by the user in Visual Studio Code GitHub Copilot chat.

**Recommendation:** Option A for clearest user experience

---

## Question 10: Prompts History View Content

**Q: What information should be shown for each completed prompt in the "Prompts History" view?**

Please choose one:
- [ ] **A)** Minimal: Prompt ID, Title, View button
  - **Pros:** Clean, simple, fast to scan
  - **Cons:** Limited information at a glance
  
- [ ] **B)** Basic: Prompt ID, Title, Completed date, View button
  - **Pros:** Useful chronological context
  - **Cons:** Requires storing completion timestamp
  
- [x] **C)** Detailed: Prompt ID, Title, Questionnaire/Plan/Implementation indicators (badges), View button
  - **Pros:** See what was generated for each prompt
  - **Cons:** More visual clutter
  
- [ ] **D)** Full: All above plus excerpt/preview of prompt text
  - **Pros:** Maximum context without clicking
  - **Cons:** Takes much more space, may slow down with many prompts
  
- [ ] **E)** Other (please specify): 

**Recommendation:** Option C for useful overview without clutter
