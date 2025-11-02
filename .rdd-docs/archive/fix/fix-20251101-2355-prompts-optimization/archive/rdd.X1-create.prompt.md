# Role:

You are here to create a new Fix branch using the RDD framework for quick fixes and patches.

# Context:

C01: This prompt helps developers create a fix branch from uncommitted work, capturing the essential information about what's being fixed and why.

C02: The fix creation uses the script `.rdd/scripts/fix-management.sh` which automates branch creation, file setup, and workspace preparation.

C03: A "kebab-case" name is a lowercase string where words are separated by hyphens (e.g., `fix-login-button`, `patch-api-timeout`).

C04: Fixes are simpler than Changes - they don't require full clarification and design phases.

# Rules:

R01: Never make technological or implementation decisions in this stage.

R02: Do NOT include any implementation or technical details during fix creation.

R03: The script will create a git branch with format `fix/<fix-name>`.

R04: Follow the Steps section sequentially without skipping any part.

R05: The fix name must be in kebab-case format, maximum 5 words, lowercase, hyphen-separated.

R06: Always propose 3 variations of the fix name for user selection.

R07: Fixes should be focused and narrow in scope - for larger work, use the Change creation prompt instead.

# Steps:

S01: Display the following banner to the user:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   RDD FRAMEWORK - Create Fix Branch
   
   → Preserve uncommitted work in new branch
   → Document the fix clearly
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

S02: Check if the current folder is a git repository. If not, inform the user that this must be run from a git repository and abort.

S03: Check for uncommitted changes using git status. If no uncommitted changes exist, inform the user and ask if they want to proceed anyway.

S04: Ask the user to provide a short description of the fix. Example:
```markdown
**Q: Please provide a short description of what you're fixing:**

Examples:
- "Fix login button not responding on mobile"
- "Patch API timeout issue"
- "Correct typo in user welcome message"

Your description:
```

S05: Based on the user's description, generate 3 kebab-case name variations (maximum 5 words each, lowercase, hyphen-separated). Present them to the user for selection. Example:

```markdown
**📋 Suggested Fix Names:**

Based on your description, here are 3 options:

- **1)** fix-login-button-mobile
- **2)** fix-mobile-login-response
- **3)** patch-login-button-issue

**Q: Which option do you prefer?**

- Enter **1**, **2**, or **3** to select
- Or provide your own kebab-case name

Your choice:
```

S06: When user provides their selection, validate the name:
- Must be kebab-case
- Maximum 5 words
- Lowercase only
- No special characters except hyphens

If invalid, explain the issue and ask again.

S07: Execute the script to initialize the fix branch and workspace:

```bash
./.rdd/scripts/fix-management.sh init <selected-fix-name>
```

This will:
- Create branch `fix/<selected-fix-name>`
- Create `.rdd-docs/workspace/` folder if needed
- Copy `journal.md` template to workspace
- Checkout the new branch

S08: Display confirmation message:

```markdown
**✓ Fix branch created successfully!**

- **Branch:** fix/<fix-name>
- **Workspace:** `.rdd-docs/workspace/`
- **Template:** journal.md copied

**You're ready to start working on the fix!**

---
```

S09: Display completion summary:

S09: Display completion summary:

```markdown
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   ✓ FIX BRANCH READY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 📋 Fix Branch Created

**Branch:** fix/<fix-name>

---

## 📁 Files Created

- `.rdd-docs/workspace/journal.md` - Fix journal for tracking work

---

## 🎯 Next Steps

1. **Document your work** in `.rdd-docs/workspace/journal.md`
2. **Make your changes** to the codebase
3. **Commit** your work with descriptive messages
4. **Push** the branch when ready:
   ```bash
   git push -u origin fix/<fix-name>
   ```

✓ You're on the fix branch and ready to code!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

S10: Offer final options:
```

S10: Offer final options:

```markdown
**Q: What would you like to do next?**

- **A)** Review the journal.md file
- **B)** Start making code changes (exit this prompt)
- **C)** Push branch to remote now

Your choice:
```

Handle based on choice:
- A → Open and display `.rdd-docs/workspace/journal.md`
- B → Exit gracefully with success message
- C → Execute push command and confirm

---

# Script Integration

The prompt uses `.rdd/scripts/fix-management.sh` with these actions:

- `init <fix-name>` - Create branch and initialize workspace
- `push` - Push branch to remote with upstream tracking
- `mark-prompt-completed <id>` - Mark a stand-alone prompt as completed in journal.md
- `log-prompt-execution <id> "<details>" [session-id]` - Log prompt execution details to log.jsonl

---

# Notes

- This prompt is designed for quick, focused fixes
- For larger or more complex changes, use the Change creation prompt instead
- Uncommitted work is preserved through git branching
- The fix branch follows the pattern `fix/<name>` for easy identification
- Documentation is minimal but sufficient for tracking the fix purpose
- The branch can be pushed to remote for collaboration or backup

---

**Version:** 1.0  
**Last Updated:** 2025-10-31  
**Status:** Active
