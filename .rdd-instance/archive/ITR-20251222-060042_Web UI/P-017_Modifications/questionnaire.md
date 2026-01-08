# Questionnaire for P-017: Modifications

## Context

The user needs to add a "Correction" mode for handling small post-implementation modifications without creating a new prompt. This mode should only be available when `implementation-completed` is true, addressing cases where users spot small corrections needed after implementation.

---

**Q1: What should be the primary mechanism for entering and tracking modifications?**

Please choose one:
- [ ] **A)** Add a `modifications` array field to each prompt in work-iteration-registry.json, where each modification entry contains `modification-id`, `description`, `status` ("pending", "in-progress", "completed"), and `created-timestamp`. This keeps all modification history within the prompt metadata.
  - **Pros:** Centralized tracking, modification history preserved in registry, easy to query status
  - **Cons:** Registry file becomes larger, more complex JSON structure
  
- [ ] **B)** Create a separate file `modifications.json` in each prompt's working folder (e.g., `P-017_Modifications/modifications.json`) to store the modification entries independently from the registry.
  - **Pros:** Keeps registry cleaner, modification details isolated per prompt, scalable for many modifications
  - **Cons:** Scattered data across multiple files, requires additional file I/O operations
  
- [ ] **C)** Use a sequential numbering system in the prompt.md file itself with markers like `## Modification 1`, `## Modification 2`, etc., and track only the count and current status in the registry.
  - **Pros:** Modifications visible directly in prompt.md, simple to edit manually
  - **Cons:** Harder to parse programmatically, less structured data
  
- [x] **D)** Add a single `current-modification` field in the registry pointing to the active modification ID, and store modification text in separate markdown files like `modification-001.md`, `modification-002.md` in the prompt folder.
  - **Pros:** One modification active at a time (simpler state), text in readable markdown files
  - **Cons:** Requires managing multiple files, modification switching needs file operations
  
- [ ] **E)** Other (please specify): 

---

**Q2: How should the execution-mode field interact with modifications?**

Please choose one:
- [x] **A)** Add a new execution-mode value "modification" that replaces "no-action" when a modification is active. The mode switches back to "no-action" after modification completion.
  - **Pros:** Clear mode indication, fits existing execution-mode pattern
  - **Cons:** Adds another mode to manage, complicates mode switching logic
  
- [ ] **B)** Keep execution-mode as "implement" but add a separate boolean field `modification-mode` that is true when working on modifications.
  - **Pros:** Separates concerns, implementation logic reusable
  - **Cons:** Two fields to check for understanding execution context
  
- [ ] **C)** Add a new execution-mode value "correction" (matching user's terminology) that is only selectable when implementation-completed is true.
  - **Pros:** Matches user's terminology, clear semantic meaning, enforces prerequisites
  - **Cons:** Another mode value, need to update all mode-checking logic
  
- [ ] **D)** Use execution-mode "implement" with a registry field `active-modification-id` (null when not in modification mode) to distinguish between initial implementation and modifications.
  - **Pros:** Reuses implement mode logic, modification tracking via separate field
  - **Cons:** Same mode for different purposes, less explicit
  
- [ ] **E)** Other (please specify): _________________

---

**Q3: What should be the naming convention and structure for modification-related files?**

Please choose one:
- [x] **A)** Create `modification-<ID>.md` files in the prompt folder (e.g., `modification-001.md`, `modification-002.md`) and track them in a `modifications-log.md` index file.
  - **Pros:** Each modification has its own file, clear separation, easy to archive
  - **Cons:** Many files for many modifications, need index maintenance
  
- [ ] **B)** Append modifications to `implementation.md` with section headers like `## Modification 1 - [Description]` including timestamp and status markers.
  - **Pros:** All implementation work in one file, chronological record
  - **Cons:** File grows large, harder to isolate modification-specific content
  
- [ ] **C)** Create a single `modifications.md` file in the prompt folder with all modifications listed sequentially with status markers and timestamps.
  - **Pros:** Single file for all modifications, easy to review modification history
  - **Cons:** Could become lengthy, less modular
  
- [ ] **D)** Create a `modifications/` subfolder in each prompt's working folder, with individual markdown files like `001-description.md`, `002-description.md`.
  - **Pros:** Very organized, scalable, clear folder structure
  - **Cons:** Deeper nesting, more complex file navigation
  
- [ ] **E)** Other (please specify): _________________

---

**Q4: Should modifications require their own questionnaire and planning steps, or reuse the existing files?**

Please choose one:
- [ ] **A)** Each modification gets its own `modification-<ID>-questionnaire.md` and `modification-<ID>-plan.md` files for complex modifications that need analysis.
  - **Pros:** Full workflow support for complex modifications, consistent with prompt pattern
  - **Cons:** Heavy process for "small corrections", many files
  
- [x] **B)** Modifications skip questionnaire and planning - they are direct implementations using `modification-<ID>-implementation.md` only.
  - **Pros:** Lightweight for small corrections, faster workflow
  - **Cons:** No structured analysis for modifications that might need it
  
- [ ] **C)** Optional questionnaire/plan: generate `modification-<ID>-questionnaire.md` and `modification-<ID>-plan.md` only if the modification description exceeds a certain length or complexity markers are present.
  - **Pros:** Flexible approach, scales with complexity
  - **Cons:** Requires complexity detection logic, inconsistent workflow
  
- [ ] **D)** Reuse the existing `questionnaire.md` and `plan.md` files by appending modification-specific sections with clear markers.
  - **Pros:** Fewer files, everything in context
  - **Cons:** Files become cluttered, hard to separate initial work from modifications
  
- [ ] **E)** Other (please specify): _________________

---

**Q5: How should the CLI and Web UI expose modification functionality?**

Please choose one:
- [ ] **A)** Add new CLI actions `prompt modification-create`, `prompt modification-list`, `prompt modification-activate` and corresponding Web UI buttons in the prompt editor.
  - **Pros:** Explicit commands, clear intent, follows CLI pattern
  - **Cons:** More commands to maintain
  
- [ ] **B)** Add a "Modifications" tab in the Web UI prompt editor with a form to add/edit modifications, and CLI actions under a new `modification` domain.
  - **Pros:** Dedicated UI space, separate domain in CLI
  - **Cons:** New domain adds complexity, tab might be hidden
  
- [x] **C)** Extend the existing prompt editor with a "+" button for "Add Modification" that appears only when implementation-completed is true, and use `prompt set-execution-mode mode=correction` in CLI.
  - **Pros:** Minimal UI changes, integrated workflow
  - **Cons:** Less discoverable, mode name might confuse with existing modes
  
- [ ] **D)** Add a "Corrections" section to the Web UI prompt list page showing all prompts with active modifications, and add `prompt correction-create`, `prompt correction-complete` CLI actions.
  - **Pros:** Dashboard visibility for corrections, dedicated CLI actions
  - **Cons:** Two places to view prompt status
  
- [ ] **E)** Other (please specify): _________________
