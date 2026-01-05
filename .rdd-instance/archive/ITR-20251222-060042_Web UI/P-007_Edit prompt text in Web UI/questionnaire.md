# Questionnaire - Edit prompt text in Web UI

## Scope and Interpretation

**ℹ️ Understanding the Requirement**

**Context:** The title "Edit prompt text in Web UI" is ambiguous. Based on the existing Web UI implementation and requirements, this could mean different things:

- The existing Web UI already has a file browser (Files section) that can load and edit any file including prompt.md files
- There's a need for a dedicated prompt editor integrated into the Prompts section
- The requirement might be about editing prompt properties (title, type, state) vs. the actual prompt text content

**Q1: What specific editing capability should be added to the Web UI?**

Please choose one:
- [x] **A)** Add a dedicated "Edit Prompt" button in the Prompts table that opens the prompt's prompt.md file
  - **Pros:** Direct access from prompt list, user-friendly workflow, contextual
  - **Cons:** Duplicates some file browser functionality, needs additional UI components
  
- [x] **B)** Add a comprehensive "Prompt Editor" modal with tabs for prompt.md, plan.md, questionnaire.md, and implementation.md (view-only)
  - **Pros:** Complete prompt management in one place, aligns with UR-20251224-0917, professional UX
  - **Cons:** More complex UI, larger development scope
  
- [ ] **C)** Enhance the existing Files section with quick-access buttons for common prompt files
  - **Pros:** Reuses existing infrastructure, minimal changes, simple
  - **Cons:** Less intuitive, doesn't provide integrated prompt management experience
  
- [ ] **D)** Add inline editing directly in the Prompts table for prompt metadata (title, type, state) only, not the full text
  - **Pros:** Quick edits without page navigation, minimal UI
  - **Cons:** Doesn't address full prompt text editing, limited functionality
  
- [ ] **E)** Other (please specify):

**Recommendation:** Option B aligns best with UR-20251224-0917 "The Web UI shall provide a Prompt Management page enabling loading, editing, saving, questionnaire interaction, and plan review for the active prompt."

---

## File Access Permissions

**ℹ️ Edit vs. View Permissions**

**Context:** Based on P-006 requirements, different files should have different access levels:
- Prompt text (prompt.md): Editable for active and draft prompts, view-only for completed
- Plan (plan.md): Editable for active and draft prompts, view-only for completed  
- Questionnaire (questionnaire.md): Editable for active and draft prompts, view-only for completed
- Implementation (implementation.md): View-only for active and draft prompts, view-only for completed

**Q2: Should the Web UI enforce these file access restrictions programmatically?**

Please choose one:
- [ ] **A)** Yes - Backend validates prompt state and returns errors for invalid edit attempts
  - **Pros:** Enforces workflow integrity, prevents accidental modifications, clear rules
  - **Cons:** More complex server logic, requires state checking
  
- [x] **B)** Yes - Frontend disables edit UI elements based on prompt state (soft enforcement)
  - **Pros:** User-friendly, prevents mistakes, simpler than backend validation
  - **Cons:** Can be bypassed by API calls, not truly secure
  
- [ ] **C)** Yes - Both frontend UI controls and backend validation (defense in depth)
  - **Pros:** Robust, secure, best practice, prevents both accidental and intentional violations
  - **Cons:** Most development effort, needs coordination between frontend and backend
  
- [ ] **D)** No - Trust user to follow conventions, all files editable at all times
  - **Pros:** Simplest implementation, maximum flexibility for power users
  - **Cons:** Easy to accidentally modify completed prompt files, no workflow protection
  
- [ ] **E)** Other (please specify):

**Recommendation:** Option C for production quality, or Option B for MVP if time is limited.

---

## User Interface Design

**ℹ️ Layout and Navigation**

**Context:** The current Web UI has sections: Prompts, Workdir, Git, Files. A prompt editor could be:
- A new section in the navigation bar
- A modal dialog (like create prompt)
- An overlay/side panel
- A sub-page under the Prompts section

**Q3: Where should the prompt editor interface be located?**

Please choose one:
- [ ] **A)** New navigation section "Edit Prompt" (visible when active prompt exists)
  - **Pros:** Prominent, dedicated space, easy to find
  - **Cons:** Clutters navbar, only useful when editing
  
- [x] **B)** Modal dialog opened from "Edit" button in Prompts table
  - **Pros:** Contextual, familiar pattern (like create prompt), doesn't clutter UI
  - **Cons:** Limited screen space, harder to work with large texts
  
- [ ] **C)** Replace Prompts section content with editor when "Edit" is clicked, with "Back" button
  - **Pros:** Full screen space, clear context, simple navigation
  - **Cons:** Loses prompt list visibility, requires back navigation
  
- [ ] **D)** Side panel that slides in from right when editing
  - **Pros:** Modern UX, keeps prompt list visible, nice animation
  - **Cons:** Split screen may be cramped, more complex CSS
  
- [ ] **E)** Other (please specify):

**Recommendation:** Option C for simplicity and full-screen editing experience.

---

## Multi-File Editing

**ℹ️ Editing Multiple Files Per Prompt**

**Context:** Each prompt has multiple associated files (prompt.md, plan.md, questionnaire.md, implementation.md). The editor interface needs to handle switching between these files.

**Q4: How should the editor handle multiple files per prompt?**

Please choose one:
- [x] **A)** Tabbed interface - Tabs for each file, click to switch
  - **Pros:** Familiar pattern, easy to implement, clear separation
  - **Cons:** Can't see multiple files simultaneously
  
- [ ] **B)** Dropdown selector - Single editor, dropdown to choose which file to load
  - **Pros:** Simple, minimal UI, clear focus
  - **Cons:** Less discoverable, requires extra click to switch
  
- [ ] **C)** Split panes - View/edit multiple files side by side
  - **Pros:** See everything at once, great for cross-referencing
  - **Cons:** Complex UI, limited screen space per file
  
- [ ] **D)** Accordion - Expandable sections for each file
  - **Pros:** See all files in one scroll, expand what you need
  - **Cons:** Can get long, requires scrolling
  
- [ ] **E)** Other (please specify):

**Recommendation:** Option A (tabs) for best balance of usability and screen space.

---

## Save Behavior

**ℹ️ When and How to Save**

**Context:** The file editor needs a save mechanism. Options include auto-save, explicit save button, or save-on-blur.

**Q5: What save behavior should the prompt editor implement?**

Please choose one:
- [x] **A)** Explicit save button - User clicks "Save" to persist changes
  - **Pros:** User control, clear action, prevents accidental saves
  - **Cons:** Easy to forget, can lose work
  
- [ ] **B)** Auto-save on blur - Saves automatically when leaving the textarea
  - **Pros:** Convenient, won't forget, modern UX
  - **Cons:** May save incomplete thoughts, less user control
  
- [ ] **C)** Auto-save with debouncing - Saves automatically after N seconds of no typing
  - **Pros:** Very modern, hands-free, preserves work
  - **Cons:** Can be surprising, may save mid-edit
  
- [ ] **D)** Save button + confirmation on navigate away - Warns if unsaved changes exist
  - **Pros:** Best of both worlds, prevents data loss, user aware
  - **Cons:** More complex implementation, requires change tracking
  
- [ ] **E)** Other (please specify):

**Recommendation:** Option D for best UX and data safety.

---

## Active vs. Draft vs. Completed Prompts

**ℹ️ Which Prompts Should Be Editable**

**Context:** The requirements from P-006 specify that active and draft prompts should be editable, while completed prompts should be view-only. This needs clarification on how to handle different states.

**Q6: How should the UI differentiate between editable and view-only prompt files?**

Please choose one:
- [x] **A)** Show "Edit" button only for active/draft prompts, "View" button for completed
  - **Pros:** Clear distinction, prevents confusion, intuitive
  - **Cons:** Requires checking prompt state for each action
  
- [ ] **B)** Always show "Edit" button, but disable textarea for completed prompts
  - **Pros:** Consistent UI, opens in same interface
  - **Cons:** Potentially confusing (why is there an edit button if I can't edit?)
  
- [ ] **C)** Show "Edit" for active/draft, no button for completed (use Files section to view)
  - **Pros:** Clean separation, forces users to be intentional
  - **Cons:** Inconsistent experience, harder to view completed prompts
  
- [ ] **D)** Show both "Edit" and "View" buttons for all prompts, Edit disabled for completed
  - **Pros:** Explicit choice, clear capabilities, always accessible
  - **Cons:** More buttons, potential UI clutter
  
- [ ] **E)** Other (please specify):

**Recommendation:** Option A for clearest user experience.
