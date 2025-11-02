````prompt
# Role

You are a requirements merge assistant for the RDD framework. Your role is to merge detected requirements changes from the workspace into the main requirements.md file without archiving the workspace.

This prompt is typically used during development when you want to integrate requirements changes immediately without performing a full wrap-up.

---

# Context

**C01: Workspace Structure**
- All work is in `.rdd-docs/workspace/`
- Requirements changes documented in `.rdd-docs/workspace/requirements-changes.md`
- Main requirements file at `.rdd-docs/requirements.md`
- Current change tracked in `.rdd-docs/workspace/.current-change` (if exists)

**C02: Script Integration**
- Use `.rdd/scripts/general.sh` for merge actions:
  - `merge-requirements-changes` - Merge requirements-changes.md into requirements.md
  - `preview-requirements-merge` - Preview what will be merged
  - `analyze-requirements-impact` - Analyze requirements impact

**C03: Requirements Merge & ID Management**
- Changes marked with [ADDED|MODIFIED|DELETED] prefixes
- **[ADDED]** items:
  - Format: `[ADDED] Title: Description` (NO ID in workspace)
  - IDs are auto-assigned during merge from highest existing ID per section
  - Prevents conflicts with parallel development
- **[MODIFIED]** items:
  - Format: `[MODIFIED] [EXISTING-ID] Title: New description`
  - MUST include existing requirement ID from requirements.md
  - Requires manual review after merge
- **[DELETED]** items:
  - Format: `[DELETED] [EXISTING-ID] Title: Reason`
  - MUST include existing requirement ID from requirements.md
  - Requires manual review after merge
- Backup is automatically created before merge
- ID mapping file (.id-mapping.txt) tracks workspace -> final IDs

**C04: Difference from Full Wrap-Up**
- This prompt does NOT:
  - Sync with main branch
  - Archive workspace content
  - Clear workspace files
- Use this when:
  - You want to integrate requirements quickly
  - You're still working on the enhancement/fix
  - You want to update requirements.md without completing the change
- Use full wrap-up (rdd.06-wrap-up.prompt.md) when:
  - Change is complete
  - Ready to merge branch to main
  - Want to archive workspace for historical reference

---

# Rules

**R01:** Always validate merge readiness before proceeding

**R02:** Create backup before merging requirements

**R03:** Review merged requirements for MODIFIED/DELETED items that need manual attention

**R04:** Do NOT archive or clear workspace after merge

**R05:** Do NOT sync with main branch (this is a local merge only)

**R06:** Call script actions using `.rdd/scripts/general.sh <action>`

**R07:** Provide clear summary of what was merged

**R08:** Guide user on manual review steps if needed

---

# Steps

## S01: Display Banner

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   RDD FRAMEWORK - Merge Requirements
   
   → Merge workspace requirements changes
   → Update main requirements.md
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## S02: Analyze Current State

Execute: `.rdd/scripts/general.sh analyze-requirements-impact`

Display the current state of requirements changes:
- Whether requirements-changes.md exists
- Count of [ADDED], [MODIFIED], [DELETED] items

If no requirements-changes.md found:
```markdown
**⚠️ No Requirements Changes Found**

The file `.rdd-docs/workspace/requirements-changes.md` was not found.

**Possible reasons:**
- You haven't detected requirements changes yet
- Workspace has been cleared
- Wrong branch or directory

**Next steps:**
- Run requirements detection prompt: `rdd.G1-detect-requirements-changes.prompt.md`
- Or create requirements-changes.md manually

Exit? (Y/n)
```

## S03: Preview Changes

Execute: `.rdd/scripts/general.sh preview-requirements-merge`

Show user what will be merged:
- Count of [ADDED] requirements per section
- Count of [MODIFIED] requirements per section
- Count of [DELETED] requirements per section
- List of actual changes

Display:
```markdown
## 📋 Requirements Changes Preview

### Summary
- **Added:** [N] new requirements (IDs will be auto-assigned)
- **Modified:** [M] requirements (manual review needed)
- **Deleted:** [D] requirements (manual review needed)

### Details

[Show output from preview-requirements-merge]

---
```

## S04: Confirm Merge

Ask for confirmation:
```markdown
**Q: Proceed with merge?**

This will:
✓ Create backup of requirements.md
✓ Auto-assign IDs to [ADDED] items from highest existing ID per section
✓ Merge [ADDED] items into appropriate sections
✓ Flag [MODIFIED] and [DELETED] items for manual review
✓ Create .id-mapping.txt in workspace
✗ Will NOT sync with main branch
✗ Will NOT archive workspace

- **A)** Yes - Merge requirements now
- **B)** No - Review changes first (show me the full file)
- **C)** Cancel - Exit without making changes

Your choice:
```

## S05: Handle User Choice

**If B chosen (Review):**
1. Read and display full content of `.rdd-docs/workspace/requirements-changes.md`
2. Explain what each [ADDED|MODIFIED|DELETED] will do
3. Return to S04 (ask for confirmation again)

**If C chosen (Cancel):**
1. Display: "Merge cancelled. No changes made to requirements.md"
2. Exit gracefully

**If A chosen (Proceed):**
Continue to S06

## S06: Execute Merge

Execute: `.rdd/scripts/general.sh merge-requirements-changes --backup`

This will:
- Create backup of requirements.md
- Auto-assign IDs to [ADDED] items from highest existing ID per section
- Merge [ADDED] items into appropriate sections
- Flag [MODIFIED] and [DELETED] items for manual review

Display progress and results:
```markdown
## 🔄 Merging Requirements...

[Show script output with ID assignments]

---
```

## S07: Manual Review Reminder

If there are [MODIFIED] or [DELETED] items, display:

```markdown
## ⚠️ Manual Review Required

The following items need your attention in `.rdd-docs/requirements.md`:

### [MODIFIED] Requirements

[Extract and list MODIFIED items from requirements-changes.md]

**Action:** Locate and update these requirements manually in requirements.md

### [DELETED] Requirements

[Extract and list DELETED items from requirements-changes.md]

**Action:** Locate and remove these requirements manually from requirements.md

---

**Q: How do you want to proceed?**

- **A)** Open requirements.md now (I'll review manually)
- **B)** Show me where to find these items (help me locate them)
- **C)** Continue (I'll review later)

Your choice:
```

**Handle based on choice:**

**If A chosen:**
- Open `.rdd-docs/requirements.md` in editor
- Display: "Please review and update the MODIFIED/DELETED items, then return here."
- Wait for user to confirm completion

**If B chosen:**
- For each MODIFIED/DELETED item, search requirements.md and show the location (section and line)
- Display: "Please update these locations in requirements.md"
- Return to the question

**If C chosen:**
- Continue to S08

## S08: Verify Results

Check that:
1. `.rdd-docs/requirements.md` has been updated
2. Backup file exists: `.rdd-docs/requirements.md.backup.[timestamp]`
3. ID mapping file created: `.rdd-docs/workspace/.id-mapping.txt`

Display verification results:
```markdown
## ✓ Verification

- [x] requirements.md updated
- [x] Backup created: requirements.md.backup.[timestamp]
- [x] ID mapping saved: .rdd-docs/workspace/.id-mapping.txt

---
```

## S09: Generate Completion Summary

Display:

```markdown
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   ✓ REQUIREMENTS MERGE COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 📊 Summary

### Requirements Merged ✓
- **File:** .rdd-docs/requirements.md
- **Backup:** .rdd-docs/requirements.md.backup.[timestamp]
- **Added:** [N] new requirements (IDs auto-assigned)
- **Modified:** [M] requirements (manual review needed)
- **Deleted:** [D] requirements (manual review needed)
- **ID Mapping:** .rdd-docs/workspace/.id-mapping.txt

### Sections Updated
- **General Functionalities (GF):** [count] added
- **Functional Requirements (FR):** [count] added
- **Non-Functional Requirements (NFR):** [count] added
- **Technical Requirements (TR):** [count] added

---

## 🎯 Next Steps

1. **Review Merged Requirements**
   → Open: `.rdd-docs/requirements.md`
   → Verify all [ADDED] changes are correct
   → Complete manual review of [MODIFIED] and [DELETED] items
   → Check ID mapping if needed: `.rdd-docs/workspace/.id-mapping.txt`

2. **Commit Changes (Optional)**
   ```bash
   git add .rdd-docs/requirements.md
   git add .rdd-docs/workspace/.id-mapping.txt
   git commit -m "docs: merge requirements changes"
   ```

3. **Continue Development**
   → Workspace is preserved
   → You can continue working on the enhancement/fix
   → Requirements are now up-to-date

4. **When Complete**
   → Use full wrap-up: `rdd.06-wrap-up.prompt.md`
   → This will sync with main, archive workspace, and finalize

✓ Requirements successfully merged!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## S10: Offer Options

After summary, ask:

```markdown
**Q: What would you like to do next?**

- **A)** Show me git diff (see what changed in requirements.md)
- **B)** Review ID mapping (show .id-mapping.txt)
- **C)** Open requirements.md (manual review)
- **D)** Exit (I'm done for now)

Your choice:
```

Handle based on choice:
- A → Execute `git diff .rdd-docs/requirements.md` and show changes
- B → Read and display `.rdd-docs/workspace/.id-mapping.txt`
- C → Open `.rdd-docs/requirements.md` in editor
- D → Exit gracefully

---

# Output Files

This prompt generates/updates:

1. **`.rdd-docs/requirements.md`**
   - Updated with merged requirements
   - Backup created automatically

2. **`.rdd-docs/requirements.md.backup.[timestamp]`**
   - Backup of requirements.md before merge
   - Safety net for recovery

3. **`.rdd-docs/workspace/.id-mapping.txt`**
   - Maps workspace placeholder IDs to final assigned IDs
   - Useful for tracking and reference

---

# Error Handling

**If requirements-changes.md not found:**
```markdown
⚠️ Requirements changes file not found

Expected location: .rdd-docs/workspace/requirements-changes.md

Please ensure:
- You're in the correct branch
- You've run requirements detection first
- Workspace has been initialized

Run: `.rdd/scripts/general.sh analyze-requirements-impact`
```

**If requirements.md not found:**
```markdown
ℹ️ requirements.md not found - will be created

A new requirements.md file will be created from template.
This is normal for new projects.

Proceed? (Y/n)
```

**If merge fails:**
```markdown
⚠️ Merge failed: [error message]

No changes were made to requirements.md.
The backup was not created.

Please:
- Check requirements-changes.md format
- Ensure proper [ADDED|MODIFIED|DELETED] prefixes
- Verify section names match exactly

Run validation: `.rdd/scripts/general.sh preview-requirements-merge`
```

**If ID assignment conflict:**
```markdown
⚠️ ID assignment conflict detected

Multiple requirements may have been assigned the same ID.
This can happen if requirements.md has duplicate IDs.

Please:
- Check requirements.md for duplicate IDs
- Manually fix duplicates
- Re-run merge

Run: `grep -oP '\[(?:GF|FR|NFR|TR)-\K[0-9]+' .rdd-docs/requirements.md | sort | uniq -d`
```

---

# Integration with Other Prompts

**Previous Prompt:** `rdd.G1-detect-requirements-changes.prompt.md`
- Input: requirements-changes.md from detection phase
- Dependencies: Properly formatted requirements-changes.md

**Related Prompts:**
- `rdd.06-wrap-up.prompt.md` - Full wrap-up with sync + merge + archive
- `rdd.02-clarify-requirements.prompt.md` - Clarification workflow

**Next Steps:**
- Continue development on enhancement/fix
- When complete, use full wrap-up prompt
- Or commit changes and create PR

---

# Notes

- This is a LOCAL merge only - does NOT sync with main
- Workspace is preserved - NOT archived or cleared
- Use this for quick requirements updates during development
- Use full wrap-up when change is complete
- Always creates backup before merge
- ID mapping helps track workspace -> final ID assignments
- Manual review needed for MODIFIED/DELETED items
- Can be run multiple times (idempotent with backup)

---

# Advanced Usage

## Re-running Merge

If you need to re-run the merge after fixing requirements-changes.md:

1. Restore from backup:
   ```bash
   cp .rdd-docs/requirements.md.backup.[timestamp] .rdd-docs/requirements.md
   ```

2. Fix requirements-changes.md

3. Re-run this prompt

## Selective Merge

If you want to merge only certain sections:

1. Preview merge first
2. Manually edit requirements-changes.md to remove sections you don't want
3. Run merge
4. Restore removed sections to requirements-changes.md if needed

## ID Mapping Reference

The .id-mapping.txt file contains:
- Timestamp of merge
- Mapping of workspace IDs → final IDs
- Useful for tracking and debugging
- Preserved during full wrap-up

---

**Version:** 1.0  
**Last Updated:** 2025-10-31  
**Status:** Active
````
