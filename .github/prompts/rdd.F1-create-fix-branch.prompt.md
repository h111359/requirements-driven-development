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

R08: The file `.rdd-docs/workspace/change.md` will be populated iteratively with user responses.

R09: Acceptance Criteria should be set to "N/A" for fixes.

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
- Copy `change.md` template to workspace
- Checkout the new branch

S08: Display confirmation message:

```markdown
**✓ Fix branch created successfully!**

- **Branch:** fix/<fix-name>
- **Workspace:** `.rdd-docs/workspace/`
- **Template:** change.md copied

**Now let's document the fix details...**

---
```

S09: Ask for the **What** section iteratively:

```markdown
**Q: What needs to be fixed?**

**ℹ️ Be specific about:**
- What is broken or incorrect?
- Where does the issue occur?
- What is the observable symptom?

Your answer:
```

S10: When user provides the **What** answer:
1. Execute the script to update the What section:
   ```bash
   ./.rdd/scripts/fix-management.sh update-what "<user-answer>"
   ```

2. Display confirmation:
   ```markdown
   **✓ Captured:**
   ```
   **What:** [user's answer]
   
   Is this correct? (Yes/No/Refine)
   ```

3. If "No" or "Refine", go back to S09
4. If "Yes", proceed to S11

S11: Ask for the **Why** section iteratively:

```markdown
**Q: Why does this need to be fixed?**

**ℹ️ Consider:**
- What is the impact on users?
- What business problem does this cause?
- Is this blocking any workflows?
- What is the urgency level?

Your answer:
```

S12: When user provides the **Why** answer:
1. Execute the script to update the Why section:
   ```bash
   ./.rdd/scripts/fix-management.sh update-why "<user-answer>"
   ```

2. Display confirmation:
   ```markdown
   **✓ Captured:**
   
   **Why:** [user's answer]
   
   Is this correct? (Yes/No/Refine)
   ```

3. If "No" or "Refine", go back to S11
4. If "Yes", proceed to S13

S13: Set Acceptance Criteria to "N/A":

Execute:
```bash
./.rdd/scripts/fix-management.sh update-acceptance-criteria "N/A"
```

S14: Display completion summary:

```markdown
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   ✓ FIX BRANCH READY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 📋 Fix Documentation

**Branch:** fix/<fix-name>

**What:** [captured what]

**Why:** [captured why]

**Acceptance Criteria:** N/A

---

## 📁 Files Created

- `.rdd-docs/workspace/change.md` - Fix documentation

---

## 🎯 Next Steps

1. **Review** `.rdd-docs/workspace/change.md`
2. **Make your changes** to the codebase
3. **Commit** your work with descriptive messages
4. **Push** the branch when ready:
   ```bash
   git push -u origin fix/<fix-name>
   ```

✓ You're on the fix branch and ready to code!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

S15: Offer final options:

```markdown
**Q: What would you like to do next?**

- **A)** Review the change.md file
- **B)** Start making code changes (exit this prompt)
- **C)** Push branch to remote now
- **D)** Cancel and delete this fix branch

Your choice:
```

Handle based on choice:
- A → Open and display `.rdd-docs/workspace/change.md`
- B → Exit gracefully with success message
- C → Execute push command and confirm
- D → Execute cleanup script and return to previous branch

---

# Script Integration

The prompt uses `.rdd/scripts/fix-management.sh` with these actions:

- `init <fix-name>` - Create branch and initialize workspace
- `update-what "<text>"` - Update What section in change.md
- `update-why "<text>"` - Update Why section in change.md
- `update-acceptance-criteria "<text>"` - Update Acceptance Criteria section
- `validate` - Check if all required sections are filled
- `push` - Push branch to remote with upstream tracking
- `cleanup` - Delete branch and workspace (used for cancellation)

---

# Error Handling

**If script execution fails:**
```markdown
⚠️ Script execution failed: [error message]

**Possible causes:**
- Script not executable (run: `chmod +x .rdd/scripts/fix-management.sh`)
- Git repository issues
- Permission problems

**What to do:**
- Check the error message above
- Verify you're in the repository root
- Ensure git is properly configured
```

**If branch already exists:**
```markdown
⚠️ Branch fix/<fix-name> already exists

**Q: How would you like to proceed?**

- **A)** Switch to existing branch (discard current changes)
- **B)** Choose a different name
- **C)** Delete existing branch and create new one
- **D)** Cancel operation

Your choice:
```

**If no uncommitted changes detected:**
```markdown
ℹ️ No uncommitted changes detected in working directory

**Q: Do you still want to create a fix branch?**

- **A)** Yes, proceed anyway
- **B)** No, cancel operation

Your choice:
```

**If invalid input:**
```markdown
⚠️ Invalid input: "[user input]"

**Please:**
- Choose one of the provided options (A, B, C, D)
- Or enter a number (1, 2, 3)
- Or provide a valid kebab-case name
```

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
