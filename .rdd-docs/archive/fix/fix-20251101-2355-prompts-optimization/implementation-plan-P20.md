# Implementation Plan for P20
# Analysis: Create Simple Initiate Prompt

**Date:** November 2, 2025  
**Prompt ID:** P20  
**Objective:** Create a concise prompt `rdd.01-initiate.prompt.md` that asks user for feature/fix and runs the appropriate `rdd.sh` command, potentially replacing existing prompts.

---

## Current State Analysis

### Existing Prompts

**1. `.github/prompts/rdd.01-create-change.prompt.md`**
- **Status:** CORRUPTED with duplicated content (similar to P16.5 issue)
- **Purpose:** Create a new Change using RDD framework
- **Current Approach:** References `rdd.sh change create` command
- **Complexity:** ~70 lines (when cleaned), describes automated workflow
- **Key Features:**
  - Explains what `rdd.sh` does automatically (banner, git check, description/name collection)
  - Documents the interactive workflow
  - Shows command: `./.rdd/scripts/rdd.sh change create`
  - Notes that script handles all user input

**2. `.github/prompts/rdd.X1-create.prompt.md`**
- **Status:** Uses deprecated script
- **Purpose:** Create a Fix branch
- **Current Approach:** Uses old `.rdd/scripts/fix-management.sh init <name>`
- **Complexity:** ~170 lines with detailed steps
- **Key Features:**
  - Manual steps: banner display, git check, uncommitted changes check
  - Asks for description in chat
  - AI generates 3 name variations
  - Validates name format
  - Executes deprecated script
  - Extensive completion summary

### Current rdd.sh Implementation

After P17-P19 enhancements:

```bash
# Interactive change creation (asks for type)
./.rdd/scripts/rdd.sh change create          # Defaults to 'feat'
./.rdd/scripts/rdd.sh change create feat     # Explicit feature
./.rdd/scripts/rdd.sh change create fix      # Explicit fix
```

**Workflow:**
1. Safety checks (P17): Must be on main branch, workspace must be empty
2. Display banner
3. Prompt for description (interactive)
4. Prompt for name (interactive with normalization loop)
5. Create branch: `feat/YYYYMMDD-HHmm-<name>` or `fix/YYYYMMDD-HHmm-<name>`
6. Initialize workspace
7. Display results

---

## Critical Questions for User

### Question 1: Purpose and Scope

**Q1.1:** What is the intended purpose of the new `rdd.01-initiate.prompt.md`?

**Option A:** A **minimal wrapper** that only asks "feature or fix?" and then runs the command  
- Prompt would be ~15-20 lines
- No AI interaction needed (script handles everything)
- Just documentation of what will happen

**Option B:** A **replacement** with similar functionality but simplified  
- Keep some guidance/context
- Still let script do the work
- ~30-40 lines

**User Decision Needed:** Which approach do you prefer?
**User Answer:** A
---

### Question 2: Fix vs Change Terminology

**Q2.1:** The current `rdd.sh` uses:
```bash
rdd.sh change create       # Can create both feat and fix
rdd.sh change create fix   # Specifically creates fix
```

But we also have:
```bash
rdd.sh fix init <name>     # Old approach, still exists
```

**Concern:** The naming is confusing:
- "change" domain can create both features AND fixes
- "fix" domain also exists separately

**Questions:**
1. Should the new prompt use `rdd.sh change create [feat|fix]`?
2. Or should it use `rdd.sh fix init` for fixes?
3. Should we standardize on one approach and deprecate the other?

**User Decision Needed:** Which command pattern should the prompt use?
**User Answer:** 
./.rdd/scripts/rdd.sh change create feat   # For features
./.rdd/scripts/rdd.sh change create fix    # For fixes

---

### Question 3: Replacement Strategy

**Q3.1:** Regarding `rdd.01-create-change.prompt.md`:
- This file is currently **corrupted** (needs fixing like P16.5)
- It already references the new `rdd.sh change create` command
- It's reasonably concise (~70 lines when clean)

**Options:**
- **A)** Fix the corruption, keep it as-is (it's already updated)
- **B)** Replace it with new simpler `rdd.01-initiate.prompt.md`
- **C)** Keep both: one for detailed docs, one for quick start

**Q3.2:** Regarding `rdd.X1-create.prompt.md`:
- Uses deprecated `.rdd/scripts/fix-management.sh` 
- Much more complex (~170 lines)
- Has many manual steps that are now automated

**Options:**
- **A)** Delete it entirely (workflow is now in `rdd.sh`)
- **B)** Update it to use `rdd.sh change create fix`
- **C)** Replace with new `rdd.01-initiate.prompt.md`

**User Decision Needed:** What's the replacement/deprecation strategy?
**User Answer:**  Q3.1: B; Q3.2: A
---

### Question 4: Prompt Location

**Q4.1:** The prompt requests location `.rdd/scripts/rdd.01-initiate.prompt.md`

**Concern:** This is unusual because:
- `.rdd/scripts/` contains executable bash scripts
- Prompts are typically in `.github/prompts/`
- Example: existing prompts are in `.github/prompts/`

**Was this intentional or a typo?**

**Options:**
- **A)** `.github/prompts/rdd.01-initiate.prompt.md` (standard location)
- **B)** `.rdd/scripts/rdd.01-initiate.prompt.md` (as requested)

**User Decision Needed:** Confirm the correct location.
**User Answer:**  A
---

### Question 5: Workflow Differences

**Q5.1:** The old `rdd.X1-create.prompt.md` has steps that are NOT in the new workflow:

**Old workflow included:**
- Check for uncommitted changes
- AI generates 3 name variations
- User selects from options
- Extensive guidance and prompts

**New workflow (`rdd.sh`):**
- User types their own name
- Script normalizes it automatically
- No AI involvement in naming

**Question:** Do you want the new prompt to:
- **A)** Match the new simplified workflow (no AI naming)
- **B)** Add back AI name generation as optional guidance
- **C)** Provide both approaches

**User Decision Needed:** Should AI assist with naming suggestions?
**User Answer:**  A
---



