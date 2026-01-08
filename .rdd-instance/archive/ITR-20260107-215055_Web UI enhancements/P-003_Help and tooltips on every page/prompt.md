**Background:**
The RDD Web UI currently lacks in-app guidance, which may cause confusion for new users learning the framework's workflow model (clarify → analyze → plan → implement → modification). User feedback indicates confusion around:
- When to use each execution mode
- What the workflow status flags mean
- How to navigate between prompt lifecycle stages

**Objective:**
Implement a tiered contextual help system that provides guidance at critical decision points without cluttering the interface.

**Scope - Tier 1 (This Prompt):**

1. **Execution Mode Guidance:**
   - Add tooltips to each execution mode button (Clarify, Analyze, Plan, Implement, Modify) on the Active Prompt page
   - Tooltip content: One-sentence description of when to use the mode and what it produces
   - Example: "Clarify: Generate questions to resolve ambiguities in the prompt (produces questionnaire.json)"

2. **Page-Level Help:**
   - Add help icon (ℹ️) in the navbar next to page title for: Active Prompt, Prompts History, Technical Design, Requirements
   - Clicking icon opens modal with:
     - Page purpose (1-2 sentences)
     - Key workflows (2-3 bullet points)
     - Link to full user guide
   
3. **Status Flag Tooltips:**
   - Add tooltips to all workflow status flag icons on Active Prompt page
   - Explain what each flag means and what action sets it

4. **Destructive Action Warnings:**
   - Ensure all delete buttons for files (questionnaire, analysis, plan) have confirm dialogs
   - Dialog text should explain what will be reset when file is deleted

**Out of Scope (Future Enhancements):**
- First-time user tour
- Separate help center page
- Video demonstrations
- Field-level help in Technical Design form
- User preference to disable tooltips

**Success Criteria:**
- All execution mode buttons have working tooltips
- All 4 main pages have help icons with modal content
- No visual clutter added to existing layouts
- Help content loads within 200ms
- All help features are keyboard accessible

**Implementation Constraints:**
- Use Bootstrap 5 native tooltip/popover components (already included)
- Store help content in JavaScript constants in app.js (no new files for Tier 1)
- Maintain vanilla JS approach (no new dependencies)
- Ensure mobile responsiveness (tooltips must work on touch devices)

**Technical Notes:**
- Bootstrap tooltips require initialization: `new bootstrap.Tooltip(element)`
- For touch devices, tooltips should trigger on tap, not hover
- Modal content should use existing modal template pattern from app.js
- Follow existing color scheme (use .text-muted for help text)

**Acceptance Criteria:**
1. User can understand what each execution mode does without external documentation
2. User can access page-level help from all main navigation pages
3. All help features pass WCAG 2.1 Level A accessibility audit
4. Help tooltips render correctly on desktop (Chrome, Firefox) and mobile (Safari, Chrome)
5. No performance degradation in page load time (< 50ms added)