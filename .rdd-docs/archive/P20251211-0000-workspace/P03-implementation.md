# Prompt P03 Implementation

## 1. Prompt Text

 - [ ] [P03]  Analyze and update requirements and tech-spec based on PRS

Context:
- Product Requirements: docs/ProductRequirementsSpecification.md
- Baseline requirements: .rdd-docs/requirements.md
- Baseline technical spec: .rdd-docs/tech-spec.md
- Comparison notes (draft): .rdd-docs/workspace/compare-requirements.md

Task:
1. Re-read docs/ProductRequirementsSpecification.md and .rdd-docs/requirements.md.
2. Treat .rdd-docs/requirements.md as the primary requirements document; PRS overrides only where it introduces new behavior or clearly replaces existing behavior.
3. Using .rdd-docs/workspace/compare-requirements.md as input (not as truth), produce:
  - A list of concrete requirement changes to apply to .rdd-docs/requirements.md:
    - New requirements to add (with proper IDs and sections GF/FR/NFR/TR).
    - Existing requirements to modify (show [OLD] and [NEW] text).
    - Existing requirements to mark as [DELETED] or [DEPRECATED].
  - A list of matching updates needed in .rdd-docs/tech-spec.md (sections, paragraphs, bullets).

4. Output three clearly separated sections in your answer:
  - "Planned changes for .rdd-docs/requirements.md"
  - "Planned changes for .rdd-docs/tech-spec.md"
  - Implementation steps to be executed so to implement the changes

5. Then, at the end of your reply, generate a *single* implementation prompt P04(detailed prompt text) that will:
  - Apply all decided changes to .rdd-docs/requirements.md and .rdd-docs/tech-spec.md.
  - Keep formatting and IDs consistent with .rdd/templates/requirements-format.md.
  - Implement the changes in the code

Constraints:
- Do NOT directly edit any file in this step; only propose exact P04 text in markdown.
- Respect existing numbering and [DELETED]/[DEPRECATED] conventions in .rdd-docs/requirements.md.
- Reference sections in .rdd-docs/tech-spec.md by headings so edits are easy to apply manually.

Deliverables:
- Validated and complete list of requirement and tech-spec updates.
- A ready-to-use P04 implementation prompt text that I can copy into .rdd-docs/work-iteration-prompts.md.

---

## 2. Context Summaries

### 2.1 Related/affected context from core RDD docs

- `.rdd-docs/requirements.md`: Primary, current list of General, Functional, Non-Functional, and Technical requirements. P03 uses this as the authoritative baseline; changes derived from PRS must be expressed as additions, modifications, or deprecations here.
- `.rdd-docs/tech-spec.md`: Consolidated technical documentation (including Data Architecture and Project Folder Structure). P03 will drive updates here to reflect any requirement changes, keeping architecture and implementation notes aligned.
- `.rdd-docs/user-story.md`: Describes the current iteration’s user story, states, and context. It provides narrative framing but P03 treats requirements.md as the primary truth and doesn’t directly modify user-story.md.

### 2.2 Additional useful context files

- `docs/ProductRequirementsSpecification.md`: Product-level requirements (PRS). For P03, PRS serves as source of new or overriding behavior where it clearly extends or replaces baseline requirements.
- `.rdd-docs/workspace/compare-requirements.md`: Draft comparison/notes between PRS and current requirements/tech-spec. Used as input hints only—not authoritative—and may contain outdated or partial conclusions.


---

## 3. Ambiguities, Questions, and Clarifications

Questions posed to user following `.rdd/templates/questions-formatting.md`:

**Q1. Relationship between PRS and current RDD behavior**
- **Answer**: b) PRS is a partial redesign: keep core iteration concepts (workspace, archive, requirements/tech-spec), but prompt execution flow is now centered on `execute` + Web UI. Where old flow conflicts, mark older requirements as `[DEPRECATED]` and introduce new ones aligned with PRS.

**Q2. Web UI scope vs. existing CLI/menu**
- **Answer**: a) Document the full portal as described (all pages), assuming we'll implement them over time; keep existing CLI/menu-based flows but treat Web UI as the preferred interface.

**Q3. Single vs. multiple prompt files**
- **Answer**: b) Move towards a single-active-prompt model (one active prompt file at a time) as the main workflow, and treat the existing multi-prompt checklist as a supporting artifact or legacy option.

**Q4. Execute command integration into requirements**
- **Answer**: a) Add new FR/TR requirements explicitly for `execute` (its steps, inputs/outputs, interaction with requirements/tech-spec, implementation file, questionnaire, etc.) but leave older generic "clarify / execute / wrap-up" requirements in place.

**Q5. Web-UI implementation constraints**
- **Answer**: a) Treat the Web UI as a full functional requirement: specify pages, operations, and data flows in enough detail that follow-up work will be clearly driven to implement them fairly completely.

**Design Decisions Summary**:
- Partial redesign: keep iteration concepts, center prompt execution on `execute` + Web UI
- Document full Web portal (all pages from PRS) with detailed functional requirements
- Adopt single-active-prompt model: `work-iteration-prompt.md` (singular) as canonical, multi-prompt lists as supporting
- Add explicit `execute` command requirements without refactoring older generic prompts
- Treat Web UI as full functional requirement with detailed page/operation specs

---

## 4. Detailed Plan and Execution Log

This section tracks the detailed plan and step-by-step execution, including commands used.

### 4.1 Plan (including mandatory steps from execute-work-iteration prompt)

- Step 1: Read `.rdd-docs/work-iteration-prompts.md` and identify the selected prompt (P03) per rules.
- Step 2: Create `.rdd-docs/workspace/P03-implementation.md` and copy the full P03 prompt text.
- Step 3: Read and summarize:
  - `.rdd-docs/requirements.md`
  - `.rdd-docs/tech-spec.md`
  - `.rdd-docs/user-story.md`
  - All files mentioned in the prompt text itself.
- Step 4: Identify additional potentially relevant files and summarize them.
- Step 5: Check the prompt instructions for ambiguities; if needed, formulate questions following `.rdd/templates/questions-formatting.md` and record them here.
- Step 6: Develop a detailed plan for executing P03 and document it in this file.
- Step 7: Execute the prompt instructions exactly, logging implementation details and every command run.
- Step 8: Update `.rdd-docs/requirements.md` according to the changes made, preserving IDs and structure (use [DELETED] when needed, don’t renumber; ensure sections and sequences remain valid).
- Step 9: Update `.rdd-docs/tech-spec.md` to reflect all technical changes, preserving structure and ID sequences.
- Step 10: Mark P03 as completed by running:
  - `python .rdd/scripts/rdd.py prompt mark-completed P03`
- Step 11: Verify that the checkbox in `.rdd-docs/work-iteration-prompts.md` is updated by the script and that no other manual edits were made there.
- Step 12: Final verification that all mandatory rules from the execute-work-iteration prompt have been followed.

### 4.2 Execution Log

**2025-12-07 - Initial context gathering**:
- Read `.rdd-docs/work-iteration-prompts.md`: identified P03 as lowest unchecked, non-placeholder prompt
- Created `P03-implementation.md` and copied full prompt text
- Read `requirements.md`, `tech-spec.md`, `user-story.md`, `docs/ProductRequirementsSpecification.md`
- Read `.rdd-docs/workspace/compare-requirements.md` (draft comparison notes)

**2025-12-07 - Clarification questionnaire**:
- Detected ambiguities requiring user guidance (5 design questions)
- Posted questionnaire following `.rdd/templates/questions-formatting.md` format
- User provided answers: Q1=b, Q2=a, Q3=b, Q4=a, Q5=a

**2025-12-07 - Analysis phase**:
- Analyzed PRS vs. baseline requirements using compare-requirements.md as input (not truth)
- Applied user's design preferences: partial redesign, full Web portal, single-prompt model, new execute requirements, detailed Web UI specs
- Identified concrete changes needed for requirements.md and tech-spec.md
- Preparing three planned-changes sections and P04 prompt text per P03 deliverables

---

## 5. Analysis / Design / Results

### 5.1 Comparative Analysis Summary

Based on user's design preferences and the PRS/baseline comparison:

**Major Themes**:
1. **Web UI as primary interface**: Add full portal specification (Prompt Management, Technical Spec, File/Folder, Requirements, Version Control, Administration pages)
2. **Execute command formalization**: Add explicit FR/TR for execute command workflow (9-step flow from PRS)
3. **Single-prompt model**: Transition from multi-prompt checklist (`work-iteration-prompts.md`) to single active prompt (`work-iteration-prompt.md`)
4. **Prompt persistence policy**: Formalize requirement that prompts must be authored via Web UI and saved as Markdown (not ad-hoc chat)
5. **Prompt folder clarification**: Resolve `.rdd/prompts/` vs `.github/prompts/` conflict with two-location model and precedence
6. **Git operational modes**: Expand local-only mode to three explicit modes (noGit, localGit, remoteGit)
7. **Deprecate conflicting legacy requirements**: Mark Bash/PowerShell script requirements (TR-24..TR-28) as deprecated in favor of Python-first policy

**Key Design Constraints**:
- Keep existing iteration/workspace/archive concepts intact (not a full rewrite)
- Add new requirements for Web UI and execute command without refactoring existing workflow prompts
- Preserve ID sequences, use [DEPRECATED] marker instead of deletion where appropriate
- Reference tech-spec.md sections by headings for easy manual application

### 5.2 Requirements Coverage

**New Requirements to Add**:
- GF-13: Web-based UI general functionality
- GF-14: Prompt authoring persistence policy
- FR-130: Canonical prompt storage and precedence (two-location model)
- FR-131: Single active work-iteration prompt file
- FR-132: Execute command ordered workflow (9 steps)
- FR-133..FR-140: Web UI page-specific requirements (Prompt Management, Tech Spec, File/Folder, Requirements, Version Control, Administration)
- NFR-21: Web UI user experience requirements
- TR-130: Prompts folder in .rdd for framework prompts
- TR-131: Operational modes explicit enumeration (noGit, localGit, remoteGit)
- TR-132: Web server implementation requirements

**Requirements to Modify**:
- TR-12: Update to document two-location prompt model with precedence
- FR-05: Update to reference `work-iteration-prompt.md` (singular)
- FR-82: Update to reference `work-iteration-prompt.md` and single-prompt model
- FR-100: Update filename reference to singular form

**Requirements to Deprecate**:
- TR-24..TR-28: Mark as [DEPRECATED] - replace with Python-first archival policy

### 5.3 Tech-Spec Coverage

**Sections to Add**:
- Web UI Architecture (new major section under Component Architecture)
  - Web server implementation (Python http.server or similar)
  - Page structure and routing
  - Data persistence and file operations
  - UI technology stack (HTML/CSS/JS inline or templated)
- Execute Command Flow (new subsection under Command Routing Pattern)
  - Detailed 9-step workflow
  - Implementation file format and location
  - Questionnaire generation logic
  - Requirements/tech-spec auto-update mechanism

**Sections to Update**:
- Project Folder Structure: Add `.rdd/prompts/` directory
- Configuration Management: Add `gitMode` field to config.json schema
- Command Routing Pattern: Add `execute` command documentation

**Sections to Deprecate/Archive**:
- Note in "Migration Notes" that TR-24..TR-28 script requirements are deprecated
- Add "Operational Modes" subsection explaining three git modes
