# Implementation Plan for P16
# Analysis of rdd.01-create-change.prompt.md Automation Opportunities

**Date:** November 2, 2025  
**Prompt ID:** P16  
**Objective:** Analyze GitHub prompt `.github/prompts/rdd.01-create-change.prompt.md` and identify which instructions can be automated via `.rdd/scripts/rdd.sh` and utility scripts.

---

## Executive Summary

The prompt file `rdd.01-create-change.prompt.md` contains 8 steps (S01-S08) for creating a new RDD change. After analysis, **all required steps** can be fully automated using existing and new utility scripts *(updated from 3→4 in P16.1, 4→5 in P16.2, then complete automation in P16.3 by eliminating S04)*. With P16.3, the workflow requires no AI assistance, making it suitable for both Copilot-assisted and pure CLI usage.

### Automation Status

| Step | Description | Can Be Automated? | Implementation Path |
|------|-------------|-------------------|---------------------|
| S01 | Display banner | ✅ **Yes** *(Updated in P16.1)* | Add to `rdd.sh::route_change()` |
| S02 | Check git repository | ✅ **Yes** | `git-utils.sh::check_git_repo()` |
| S03 | Ask user for description and name | ✅ **Yes** *(Enhanced in P16.3)* | Use bash `read` + `normalize_to_kebab_case()` |
| S04 | Generate 3 name variations | ❌ **ELIMINATED** *(P16.3)* | No longer needed - user provides name directly |
| S07 | Execute rdd.sh command | ✅ **Already automated** | Calls existing `change-utils.sh` |
| S08 | Display results | ⚠️ Partial | Output from `change-utils.sh` |

**Note:** Steps S05 and S06 were never part of the original prompt. After eliminating S04, the remaining steps (S07, S08) should be renumbered to S04, S05 respectively.

---

## Detailed Step-by-Step Analysis

### S01: Display Banner

```
─── RDD-COPILOT ───
 Prompt: Create Change  
 Description: 
 > Create a new Change folder with timestamped naming,
 > branch setup, and template initialization.

 User Action: 
 > Provide a short description of the change needed.
───────────────
```

**Analysis:**
- **Current State:** Hardcoded in prompt, rendered by Copilot
- **Automation Potential:** **UPDATED** - High - can be displayed by rdd.sh wrapper
- **Recommendation:** **CHANGED** - Move banner display to `rdd.sh` in the `route_change()` function when action is "create"
- **Utility Script Capability:** `core-utils.sh::print_banner()` exists for section headers; can use plain echo statements for this specific banner

**Decision:** ✅ **SHOULD BE AUTOMATED** - Banner should be displayed by rdd.sh, not in chat

**Implementation Plan:**

Add banner display to `.rdd/scripts/rdd.sh` in the `route_change()` function:

```bash
route_change() {
    local action="$1"
    shift
    
    case "$action" in
        create)
            # Display banner for change creation
            echo ""
            echo "─── RDD-COPILOT ───"
            echo " Prompt: Create Change"
            echo " Description:"
            echo " > Create a new Change folder with timestamped naming,"
            echo " > branch setup, and template initialization."
            echo ""
            echo " User Action:"
            echo " > Provide a short description of the change needed."
            echo "───────────────"
            echo ""
            
            if [ $# -lt 2 ]; then
                print_error "Change name and type required"
                echo "Usage: rdd.sh change create <name> <type>"
                return 1
            fi
            create_change "$1" "$2"
            ;;
        # ... rest of function
    esac
}
```

**Prompt File Update:**

Update `.github/prompts/rdd.01-create-change.prompt.md` S01:

```markdown
S01: The banner will be automatically displayed by rdd.sh when the command 
     is executed in S07. You do not need to display it in chat.
```

**Benefits:**
1. Consistent presentation - always shows before change creation
2. Reduces Copilot prompt complexity - one less step to remember
3. Works even if user runs rdd.sh directly (without Copilot)
4. Better separation of concerns - UI/presentation in script, logic in Copilot

---

### S02: Check if Git Repository

**Prompt Requirement:**
> Check if the current folder is a git repository. If not, inform the user that this must be run from a git repository and abort.

**Analysis:**
- **Current State:** Manual check required by Copilot
- **Available Function:** `git-utils.sh::check_git_repo()`
- **Function Signature:**
  ```bash
  check_git_repo()
  # Returns: 0 if in git repo, 1 if not
  # Output: Error message if not in git repo
  ```

**Implementation:**

```bash
# In git-utils.sh (already exists)
check_git_repo() {
    if ! git rev-parse --git-dir >/dev/null 2>&1; then
        print_error "Not a git repository"
        echo "This command must be run from within a git repository."
        return 1
    fi
    return 0
}
```

**Integration into Prompt:**

The prompt should instruct Copilot to:
1. Before any other action, run: `source .rdd/scripts/git-utils.sh && check_git_repo || exit 1`
2. Or rely on `rdd.sh change create` which already includes this check

**Decision:** ✅ **Fully automated** - Already available in `git-utils.sh`

**Recommendation:** Update prompt S02 to reference the utility function:
```markdown
S02: The git repository check is automatically performed by the rdd.sh wrapper. 
     If not in a git repository, the command will fail with an error message.
```

---

### S03: Ask User for Description (and Name)

**Prompt Requirement:**
> Ask the user to provide a short description of the change.

**Analysis:**
- **Current State:** Interactive dialog with user via Copilot chat
- **Automation Potential:** **UPDATED in P16.2** - High - can be handled by rdd.sh with interactive prompt
- **Automation Potential (P16.3):** **ENHANCED** - Can ask for both description AND name, normalizing input automatically
- **Recommendation:** **CHANGED in P16.3** - Collect both description and name, eliminate need for AI-generated suggestions
- **Utility Script Capability:** Bash built-in `read` command + text normalization functions

**Decision:** ✅ **SHOULD BE FULLY AUTOMATED** - Both description and normalized name collected by rdd.sh

**Implementation Plan (P16.3 - Enhanced with Name Normalization):**

Modify `.rdd/scripts/rdd.sh` in the `route_change()` function to collect both description and name with automatic normalization:

```bash
route_change() {
    local action="$1"
    shift
    
    case "$action" in
        create)
            # Display banner
            echo ""
            echo "─── RDD-COPILOT ───"
            echo " Prompt: Create Change"
            echo " Description:"
            echo " > Create a new Change folder with timestamped naming,"
            echo " > branch setup, and template initialization."
            echo ""
            echo " User Action:"
            echo " > Provide a short description and name for the change."
            echo "───────────────"
            echo ""
            
            # 1. Prompt for description
            echo "Please provide a short description of the change:"
            echo "(e.g., 'Add user authentication feature', 'Fix login page bug')"
            read -p "> " change_description
            
            # Validate description was provided
            if [ -z "$change_description" ]; then
                print_error "Change description cannot be empty"
                return 1
            fi
            
            print_info "Description: $change_description"
            echo ""
            
            # 2. Prompt for name with normalization loop
            local change_name=""
            local normalized_name=""
            
            while true; do
                echo "Please provide a name for the change (will be normalized to kebab-case):"
                echo "(e.g., 'add user auth', 'Fix Login Bug', 'update-readme')"
                read -p "> " change_name
                
                # Check if name was provided
                if [ -z "$change_name" ]; then
                    print_error "Change name cannot be empty"
                    continue
                fi
                
                # Normalize the name to kebab-case
                normalized_name=$(normalize_to_kebab_case "$change_name")
                
                # Check if normalization was successful
                if [ $? -ne 0 ]; then
                    print_error "Unable to normalize name: $change_name"
                    echo "Please try a different name (use only letters, numbers, spaces, hyphens)"
                    continue
                fi
                
                # Validate normalized name
                if ! validate_name "$normalized_name"; then
                    print_warning "Normalized name '$normalized_name' doesn't meet requirements"
                    echo "Requirements: kebab-case, max 5 words, lowercase, hyphens only"
                    echo ""
                    continue
                fi
                
                # Show normalized name and confirm
                print_success "Normalized name: $normalized_name"
                read -p "Use this name? (y/n): " confirm
                
                if [[ "$confirm" =~ ^[Yy] ]]; then
                    break
                fi
                
                echo "Let's try again..."
                echo ""
            done
            
            # Store description in temp file (for reference/logging)
            local desc_file="/tmp/rdd-change-description-$$.txt"
            echo "$change_description" > "$desc_file"
            
            print_info "Description saved to: $desc_file"
            echo ""
            
            # Get change type or use default
            local change_type="${1:-feat}"
            
            # Create the change with normalized name
            create_change "$normalized_name" "$change_type"
            ;;
        # ... rest of function
    esac
}
```

**New Utility Function (add to `core-utils.sh`):**

```bash
# Normalize text to kebab-case format
# Handles various inputs: "Add User Auth", "fix_login_bug", "update-README"
# Returns: kebab-case string or exits with error code 1
normalize_to_kebab_case() {
    local input="$1"
    
    # Check if input is empty
    if [ -z "$input" ]; then
        return 1
    fi
    
    # Normalization steps:
    # 1. Convert to lowercase
    # 2. Replace underscores and spaces with hyphens
    # 3. Remove any characters that aren't lowercase letters, numbers, or hyphens
    # 4. Replace multiple consecutive hyphens with single hyphen
    # 5. Remove leading and trailing hyphens
    
    local normalized
    normalized=$(echo "$input" | \
        tr '[:upper:]' '[:lower:]' | \
        tr '_' '-' | \
        tr ' ' '-' | \
        sed 's/[^a-z0-9-]//g' | \
        sed 's/-\+/-/g' | \
        sed 's/^-//; s/-$//')
    
    # Check if result is empty (all characters were invalid)
    if [ -z "$normalized" ]; then
        return 1
    fi
    
    echo "$normalized"
    return 0
}

# Export the function
export -f normalize_to_kebab_case
```

**Normalization Examples:**

| User Input | Normalized Output | Valid? |
|------------|-------------------|--------|
| `Add User Auth` | `add-user-auth` | ✅ Yes |
| `Fix_Login_Bug` | `fix-login-bug` | ✅ Yes |
| `update-README` | `update-readme` | ✅ Yes |
| `Create  New    Feature` | `create-new-feature` | ✅ Yes |
| `add-user-authentication-system` | `add-user-authentication-system` | ❌ No (6 words) |
| `123-test` | `123-test` | ✅ Yes |
| `test@#$%feature` | `testfeature` | ✅ Yes |
| `!!!` | `` (empty) | ❌ No (no valid chars) |

**Validation After Normalization:**

After normalization, the result is passed to `validate_name()` which checks:
1. Not empty
2. Kebab-case format (lowercase, hyphens only)
3. Maximum 5 words (4 hyphens)

If validation fails, the user is prompted to try again.

**Copilot Integration Strategy (OBSOLETE with P16.3):**

~~After `rdd.sh change create` prompts for description, Copilot needs to access it for S04 (name generation). Three approaches:~~

**P16.3 Update:** This integration is no longer needed. With automatic name normalization in S03, there is no S04 step requiring Copilot to read the description. The workflow is now fully self-contained in the terminal.

<details>
<summary>Click to expand original P16.2 Copilot integration approaches (for reference)</summary>

**Approach 1: Read from Temp File (Recommended)**
```markdown
S04: Read the user's description from the temp file displayed in the output:
     ```bash
     desc_file=$(grep "Description file:" <previous output> | awk '{print $3}')
     description=$(cat "$desc_file")
     ```
     Then generate 3 kebab-case name variations based on: "$description"
```

**Approach 2: Parse Terminal Output**
```markdown
S04: The description was displayed in the output as "Description saved: <text>".
     Extract this text and generate 3 kebab-case name variations based on it.
```

**Approach 3: Ask User to Re-enter (Fallback)**
```markdown
S04: If unable to parse the description from terminal output, ask the user:
     "What description did you provide to rdd.sh?" and generate names based on that.
```

**Recommended Approach:** **Approach 1** - Most reliable

</details>

**Benefits:**
1. Complete automation of user input collection
2. Consistent UX - all interaction in terminal, not split between chat and terminal
3. Works for both Copilot and direct rdd.sh usage
4. Description is validated and stored for reference

**Challenges:**
1. Copilot needs to parse terminal output or read temp file
2. Requires update to prompt workflow instructions
3. Temp file cleanup needed (can be done at end of create_change)

**Prompt File Update (P16.3 - Updated):**

Update `.github/prompts/rdd.01-create-change.prompt.md`:

**Remove S04 entirely** - Name generation step is no longer needed

**Update S03:**
```markdown
S03: The user description and name are automatically collected by rdd.sh when executed.
     The script will:
     1. Display a prompt: "Please provide a short description..."
     2. Wait for user input (description)
     3. Display a prompt: "Please provide a name for the change..."
     4. Wait for user input (name in any format)
     5. Automatically normalize the name to kebab-case
     6. Validate the normalized name (kebab-case, max 5 words)
     7. If invalid: Show error and loop back to step 4
     8. If valid: Display normalized name and ask for confirmation
     9. If confirmed: Proceed with change creation
     
     You do NOT need to ask for description or generate name suggestions in chat.
     
     The rdd.sh script handles all user input and validation automatically.
```

**Renumber remaining steps:**
- Old S07 → **New S04**: Execute `./.rdd/scripts/rdd.sh change create`
  - Note: No arguments needed - script collects all input interactively
- Old S08 → **New S05**: Display results

**Update new S04 (was S07):**
```markdown
S04: The change creation is triggered automatically by running:
     ```bash
     ./.rdd/scripts/rdd.sh change create
     ```
     
     No arguments needed - the script will:
     - Display banner
     - Check git repository
     - Collect description from user
     - Collect and normalize name from user
     - Create branch with format: feat/YYYYMMDD-HHmm-<normalized-name>
     - Initialize workspace
     - Display results
```

**Update new S05 (was S08):**
```markdown
S05: The results are automatically displayed by rdd.sh, including:
     - ✓ Change created with timestamp ID
     - 📍 Branch name (feat/YYYYMMDD-HHmm-name)
     - 📁 Workspace path (.rdd-docs/workspace/)
     - 📋 Next steps
     
     The workflow is now complete. The user can begin working on their change.
```

**Alternative: Interactive Mode Flag**

Add `--interactive` flag to rdd.sh:

```bash
rdd.sh change create --interactive
# Prompts for all inputs: description, then shows name suggestions,
# then asks user to select one, then creates the change
```

This would make the entire flow non-interactive with Copilot, but less flexible.

**Decision:** Implement basic version with description prompt, keep name generation in Copilot for AI quality

---

### S04: Generate 3 Kebab-Case Name Variations (ELIMINATED IN P16.3)

**Prompt Requirement:**
> Based on the user's description, generate 3 kebab-case name variations (maximum 5 words each, lowercase, hyphen-separated).

**Analysis:**
- **Current State:** Copilot AI generates names based on description
- **Available Functions:**
  - `core-utils.sh::validate_name()` - validates kebab-case format
  - No generation function exists
- **Automation Potential:** Medium - could create utility function, but AI is better suited

**P16.3 Decision:** ❌ **STEP ELIMINATED** - No longer needed

**Rationale:**
With the implementation of automatic name normalization in S03 (P16.3):
1. User provides their own name directly (no AI generation needed)
2. Script automatically normalizes input to kebab-case format
3. Validation happens immediately with feedback loop
4. User confirms normalized name before proceeding

**Impact:**
- **Reduces workflow complexity** - One less step in the prompt
- **Eliminates AI dependency** - No need for Copilot to generate creative names
- **Faster execution** - Direct user input → normalized → validated → create
- **More user control** - User chooses their preferred name directly

**Trade-offs:**
- ❌ **Loss:** AI-generated creative name suggestions
- ✅ **Gain:** Faster workflow, no AI token usage for names
- ✅ **Gain:** User has full control over naming
- ✅ **Gain:** Works without Copilot (pure CLI usage)

**Migration Note:**
This step should be **removed** from `.github/prompts/rdd.01-create-change.prompt.md` and subsequent steps renumbered (S07→S04, S08→S05).

---

**Original Analysis (for reference):**

<details>
<summary>Click to expand original S04 analysis from P16</summary>

**Existing Validation Function:**

```bash
# In core-utils.sh (already exists)
validate_name() {
    local name="$1"
    
    # Check if name is empty
    if [ -z "$name" ]; then
        print_error "Name cannot be empty"
        return 1
    fi
    
    # Check kebab-case format
    if ! [[ "$name" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
        print_error "Name must be in kebab-case format (lowercase, hyphens only)"
        echo "Example: add-user-authentication"
        return 1
    fi
    
    # Check max 5 words
    local word_count=$(echo "$name" | tr '-' '\n' | wc -l)
    if [ "$word_count" -gt 5 ]; then
        print_error "Name must be maximum 5 words (found: $word_count)"
        return 1
    fi
    
    return 0
}
```

**Potential Enhancement:**

Could add to `core-utils.sh`:

```bash
# New function (PROPOSAL)
suggest_kebab_names() {
    local description="$1"
    # Basic suggestion algorithm (would need AI for quality)
    # Extract key words, convert to kebab-case, generate variations
    # This is better left to AI like Copilot
}
```

**Decision:** ⚠️ **Partial automation possible, but not recommended**

**Reasoning:**
1. Name generation requires semantic understanding - AI excels here
2. Creating a basic algorithm would produce lower-quality names
3. Validation function already exists for checking the result
4. The prompt's current approach (AI generates, utility validates) is optimal

**Recommendation:** 
- Keep name generation in Copilot prompt (AI-driven)
- Use `validate_name()` to validate user's final selection
- Add validation step to prompt after S04

**Updated Prompt Section:**

```markdown
S04: Based on the user's description, generate 3 kebab-case name variations...

S05: [NEW] Validate the selected name using core-utils.sh::validate_name()
     This ensures kebab-case format and max 5 words before proceeding.
```

</details>

---

### S07: Execute rdd.sh Command

**Prompt Requirement:**
> Execute the unified RDD wrapper script with the change domain:
> `./.rdd/scripts/rdd.sh change create <selected-name> feat`

**Analysis:**
- **Current State:** Already calls the unified wrapper
- **Automation Status:** ✅ **Fully automated**
- **Call Chain:**
  1. `rdd.sh change create <name> feat`
  2. Routes to `change-utils.sh::create_change()`
  3. Which orchestrates:
     - `core-utils.sh::validate_name()`
     - `git-utils.sh::check_git_repo()`
     - `branch-utils.sh::create_branch()`
     - `workspace-utils.sh::init_workspace()`
     - `clarify-utils.sh::init_clarification()`

**Functions Called (from change-utils.sh):**

```bash
create_change() {
    local change_name="$1"
    local change_type="${2:-feat}"
    
    # 1. Validate parameters
    validate_name "$change_name" || return 1
    
    # 2. Validate change type
    [[ "$change_type" == "feat" || "$change_type" == "fix" ]] || return 1
    
    # 3. Generate change ID (YYYYMMDD-HHmm format)
    local date_time=$(date +"%Y%m%d-%H%M")
    local change_id="${date_time}-${change_name}"
    local branch_name="${change_type}/${change_id}"
    
    # 4. Create branch
    create_branch "$branch_name" || return 1
    
    # 5. Initialize workspace
    init_workspace "$change_type" || return 1
    
    # 6. Initialize tracking
    init_change_tracking "$change_id" "$branch_name" "$change_type" || return 1
    
    # 7. Create config
    create_change_config "{...}" || return 1
    
    # Output results
    print_success "Change created: $change_id"
    print_info "Branch: $branch_name"
    print_info "Workspace initialized at: .rdd-docs/workspace/"
    # ... more output
}
```

**Decision:** ✅ **Already fully automated** - This step is complete

---

### S08: Display Results

**Prompt Requirement:**
> Display the result to the user, including:
> - Created folder path
> - Created branch name
> - Next steps (edit the change.md file with details)

**Analysis:**
- **Current State:** `create_change()` already outputs detailed results
- **Automation Status:** ⚠️ **Partially automated**
- **What's Automated:**
  - Success/error messages (via `core-utils.sh::print_*()`)
  - Branch name display
  - Workspace path display
- **What's Not Automated:**
  - "Next steps" guidance (could be enhanced)

**Current Output from create_change():**

```bash
# Success case:
print_success "Change created: $change_id"
print_info "Branch: $branch_name"
print_info "Workspace initialized at: .rdd-docs/workspace/"
print_step "Next steps:"
echo "  1. Review and edit .rdd-docs/workspace/requirements-changes.md"
echo "  2. Add clarifications to .rdd-docs/workspace/open-questions.md"
echo "  3. When ready, run: rdd.sh change wrap-up"
```

**Enhancement Opportunity:**

Could add to `change-utils.sh`:

```bash
display_change_next_steps() {
    local change_id="$1"
    local branch_name="$2"
    
    print_step "📋 Next Steps:"
    echo ""
    echo "  ${BOLD}1. Document Requirements${NC}"
    echo "     Edit: .rdd-docs/workspace/requirements-changes.md"
    echo "     Add any [ADDED], [MODIFIED], or [DELETED] requirements"
    echo ""
    echo "  ${BOLD}2. Clarify Unknowns${NC}"
    echo "     Edit: .rdd-docs/workspace/open-questions.md"
    echo "     Document questions and answers during development"
    echo ""
    echo "  ${BOLD}3. Complete the Change${NC}"
    echo "     Run: ./.rdd/scripts/rdd.sh change wrap-up"
    echo "     This will archive, commit, push, and create PR"
    echo ""
    print_info "Current branch: $branch_name"
    print_info "Change ID: $change_id"
}
```

**Decision:** ⚠️ **Partially automated, enhancement recommended**

**Recommendation:**
1. Keep existing output from `create_change()`
2. Enhance with more detailed "Next Steps" section
3. Update prompt S08 to reference the enhanced output

---

## Automation Coverage Matrix

### Functions Already Used by rdd.sh change create

| Utility Script | Function | Purpose | Called By |
|----------------|----------|---------|-----------|
| `core-utils.sh` | `validate_name()` | Validate kebab-case format | `create_change()` |
| `core-utils.sh` | `print_success()` | Success messages | `create_change()` |
| `core-utils.sh` | `print_error()` | Error messages | `create_change()` |
| `core-utils.sh` | `print_info()` | Information output | `create_change()` |
| `core-utils.sh` | `print_step()` | Step indicators | `create_change()` |
| `git-utils.sh` | `check_git_repo()` | Verify git repository | `create_change()` |
| `git-utils.sh` | `get_default_branch()` | Get main/master | `create_change()` |
| `git-utils.sh` | `get_current_branch()` | Get current branch | `create_change()` |
| `git-utils.sh` | `get_git_user()` | Get git user info | `create_change()` |
| `branch-utils.sh` | `create_branch()` | Create git branch | `create_change()` |
| `branch-utils.sh` | `branch_exists()` | Check branch existence | `create_change()` |
| `workspace-utils.sh` | `init_workspace()` | Initialize workspace | `create_change()` |
| `workspace-utils.sh` | `copy_template()` | Copy template files | `init_workspace()` |
| `clarify-utils.sh` | `init_clarification()` | Setup clarification | `create_change()` |
| `clarify-utils.sh` | `create_open_questions_template()` | Create questions file | `init_clarification()` |

**Total: 15 functions** from 4 utility scripts are already integrated into the workflow.

---

## Recommendations

### 1. Prompt File Updates (Immediate)

**Update `.github/prompts/rdd.01-create-change.prompt.md`:**

```markdown
# BEFORE S07, ADD:

S05: [OPTIONAL] Validate the user's selected name against RDD naming rules.
     The rdd.sh script will perform validation automatically, but you can
     provide immediate feedback by checking:
     - Lowercase letters and hyphens only
     - Maximum 5 words (4 hyphens)
     - No leading/trailing hyphens
     - Example valid names: add-user-auth, fix-login-bug, update-readme

S06: [OPTIONAL] Confirm the change type with the user:
     - 'feat' for new features (default)
     - 'fix' for bug fixes
     This determines the branch prefix (feat/ or fix/)
```

**Update S02:**

```markdown
S02: Check if the current folder is a git repository. 
     Note: The rdd.sh command automatically performs this check using
     git-utils.sh::check_git_repo(). If not in a git repo, the command
     will fail with a clear error message.
```

**Update S08:**

```markdown
S08: The rdd.sh command will automatically display:
     - ✓ Change created with timestamp ID
     - 📍 Branch name (feat/YYYYMMDD-HHmm-name or fix/YYYYMMDD-HHmm-name)
     - 📁 Workspace path (.rdd-docs/workspace/)
     - 📋 Next steps:
       1. Edit requirements-changes.md
       2. Use open-questions.md for clarifications
       3. Run: rdd.sh change wrap-up when complete
     
     Simply display this output to the user.
```

### 2. Utility Script Enhancements (Optional)

**Enhancement 1: Add to `change-utils.sh`**

Add a dedicated function for displaying next steps:

```bash
# At end of change-utils.sh

display_change_next_steps() {
    local change_id="$1"
    local branch_name="$2"
    
    echo ""
    print_banner "Next Steps"
    echo ""
    echo "  ${BOLD}📝 Step 1: Document Requirements${NC}"
    echo "     File: .rdd-docs/workspace/requirements-changes.md"
    echo "     - Add [ADDED] for new requirements"
    echo "     - Add [MODIFIED] for changed requirements"
    echo "     - Add [DELETED] for removed requirements"
    echo ""
    echo "  ${BOLD}❓ Step 2: Track Clarifications${NC}"
    echo "     File: .rdd-docs/workspace/open-questions.md"
    echo "     - Document questions as they arise"
    echo "     - Log answers using: rdd.sh clarify log \"Q\" \"A\""
    echo ""
    echo "  ${BOLD}✅ Step 3: Complete Change${NC}"
    echo "     Command: ./.rdd/scripts/rdd.sh change wrap-up"
    echo "     - Archives workspace"
    echo "     - Commits changes"
    echo "     - Pushes to remote"
    echo "     - Creates pull request"
    echo ""
    print_info "Branch: $branch_name"
    print_info "Change ID: $change_id"
    echo ""
}
```

Then call from `create_change()` at the end:

```bash
# In create_change(), replace final output with:
display_change_next_steps "$change_id" "$branch_name"
```

**Enhancement 2: Add to `core-utils.sh`**

Add basic name suggestion (optional, low priority):

```bash
suggest_kebab_alternatives() {
    local base_name="$1"
    # Simple word substitution suggestions
    # Not as sophisticated as AI, but provides basic options
    echo "Suggestions based on '$base_name':"
    echo "  1. $base_name"
    echo "  2. implement-$base_name"
    echo "  3. add-$base_name"
}
```

**Priority:** Low - AI (Copilot) is better suited for creative name generation

### 3. Documentation Updates (Recommended)

**Update `.rdd-docs/workspace/scripts-migration-guide.md`:**

Add section explaining prompt automation:

```markdown
### Prompt Integration with Utility Scripts

GitHub prompts (`.github/prompts/*.prompt.md`) leverage the utility scripts
automatically through the rdd.sh wrapper. When using prompts:

1. **Validation happens automatically** - No need to manually check formats
2. **Git operations are handled** - Repository checks, branch creation, etc.
3. **Output is standardized** - Consistent success/error messages
4. **Workflow is orchestrated** - Multiple utility functions work together

Example: `rdd.01-create-change.prompt.md`
- Uses: core-utils.sh, git-utils.sh, branch-utils.sh, workspace-utils.sh, clarify-utils.sh
- Total: 15 utility functions called automatically
- Manual steps: Only user input and name generation (by design)
```

---

## Implementation Tasks

### Phase 1: Core Utility Enhancement (HIGH PRIORITY - P16.3)

- [ ] **Task 1.1:** Add `normalize_to_kebab_case()` to `core-utils.sh`
  - Implement normalization logic (lowercase, replace spaces/underscores, remove invalid chars)
  - Handle edge cases (empty input, all invalid chars, multiple hyphens)
  - Add function export
  - **Estimated Time:** 30 minutes
  - **Files Changed:** 1
  - **Lines Added:** ~30
  - **Priority:** CRITICAL (required for P16.3)

- [ ] **Task 1.2:** Test `normalize_to_kebab_case()` function
  - Test valid inputs: "Add User Auth", "fix_login_bug", "update-README"
  - Test edge cases: empty string, special characters, multiple spaces
  - Verify output matches expected kebab-case format
  - **Estimated Time:** 15 minutes
  - **Priority:** HIGH

### Phase 2: rdd.sh Enhancement (HIGH PRIORITY - P16.3)

- [ ] **Task 2.1:** Update `rdd.sh::route_change()` create action
  - Add banner display (P16.1)
  - Add description prompt with bash read
  - Add name prompt loop with normalization and validation
  - Add confirmation step before creation
  - Remove command-line argument parsing (name from user input, not args)
  - **Estimated Time:** 45 minutes
  - **Files Changed:** 1
  - **Lines Added:** ~80
  - **Priority:** CRITICAL (required for P16.3)

- [ ] **Task 2.2:** Test enhanced `route_change()` function
  - Test description collection
  - Test name normalization with various inputs
  - Test validation loop (invalid → valid flow)
  - Test confirmation and creation
  - **Estimated Time:** 20 minutes
  - **Priority:** HIGH

### Phase 3: Prompt File Update (HIGH PRIORITY - P16.3)

- [ ] **Task 3.1:** Update `.github/prompts/rdd.01-create-change.prompt.md`
  - Update S01 to note automatic banner display
  - Update S02 to reference automatic git check
  - Update S03 to describe automatic description + name collection with normalization
  - **Remove S04 entirely** (name generation step eliminated)
  - Renumber S07 → S04 (Execute command)
  - Renumber S08 → S05 (Display results)
  - Update command in new S04 to: `./.rdd/scripts/rdd.sh change create`
    (no arguments - all input collected interactively)
  - **Estimated Time:** 25 minutes
  - **Files Changed:** 1
  - **Priority:** CRITICAL (required for P16.3)

### Phase 4: Documentation Updates (MEDIUM PRIORITY)

- [ ] **Task 4.1:** Update `.rdd-docs/workspace/scripts-migration-guide.md`
  - Document new interactive workflow
  - Explain name normalization feature
  - Update command examples
  - **Estimated Time:** 20 minutes
  - **Files Changed:** 1
  - **Priority:** MEDIUM

- [ ] **Task 4.2:** Update README.md (if needed)
  - Mention automatic name normalization
  - Update usage examples
  - **Estimated Time:** 10 minutes
  - **Files Changed:** 1
  - **Priority:** LOW

### Phase 5: Testing (HIGH PRIORITY)

- [ ] **Task 5.1:** End-to-end workflow test
  - Run complete change creation from start to finish
  - Test with various name formats
  - Test validation loop with invalid names
  - Verify branch creation and workspace initialization
  - **Estimated Time:** 25 minutes
  - **Priority:** HIGH

- [ ] **Task 5.2:** CLI-only usage test
  - Run workflow without Copilot
  - Verify all prompts display correctly
  - Verify normalization and validation work
  - **Estimated Time:** 15 minutes
  - **Priority:** HIGH

- [ ] **Task 5.3:** Copilot-assisted workflow test
  - Ensure prompt file works with new changes
  - Verify Copilot can guide user through process
  - Test that no manual intervention needed
  - **Estimated Time:** 15 minutes
  - **Priority:** MEDIUM

### Phase 6: Optional Enhancements (LOW PRIORITY)

- [ ] **Task 6.1:** Add `display_change_next_steps()` to `change-utils.sh`
  - Create function with enhanced formatting
  - Update `create_change()` to call it
  - Test output formatting
  - **Estimated Time:** 30 minutes
  - **Files Changed:** 1
  - **Lines Added:** ~40
  - **Priority:** LOW

- [ ] **Task 6.2:** Add `--non-interactive` flag
  - Allow users to provide all inputs as command args
  - Useful for scripting/automation
  - Fallback to interactive if args missing
  - **Estimated Time:** 1 hour
  - **Priority:** LOW (deferred)

---

## Cost-Benefit Analysis

### Benefits of Current Automation Level

| Benefit | Impact | Evidence |
|---------|--------|----------|
| **Consistency** | High | All changes use same format, validation |
| **Error Reduction** | High | Automatic validation catches issues early |
| **User Experience** | High | Clear colored output, helpful messages |
| **Maintainability** | High | Logic centralized in utility scripts |
| **Documentation** | Medium | Output serves as inline documentation |

### Costs of Over-Automation

| Risk | Impact | Mitigation |
|------|--------|-----------|
| **Less Flexibility** | Low | Prompts can still customize behavior |
| **Harder Debugging** | Low | Functions are well-documented |
| **Learning Curve** | Medium | Good docs reduce this |

### Optimal Automation Level

**Current State: 95% automated** *(Updated from 85% → 90% in P16.1 → 95% in P16.2)*

**Evolution:**
- **P16 (Original):** 85% - S02, S07, S08 automated
- **P16.1:** 90% - Added S01 (banner display)
- **P16.2:** 95% - Added S03 (description collection)

**Recommendation:** The remaining 5% (name generation in S04) requires AI creativity and semantic understanding, which is best handled by Copilot. This is the optimal balance for an AI-assisted workflow.

---

## Alternative Approaches Considered

### Alternative 1: Fully Automated Change Creation

**Approach:** Add CLI flags to skip all prompts
```bash
rdd.sh change create <name> feat --description "Add user auth" --auto-approve
```

**Pros:**
- Useful for CI/CD automation
- Faster for power users

**Cons:**
- Reduces thoughtfulness (RDD is about deliberate planning)
- Skips important validation steps
- Not aligned with RDD philosophy

**Decision:** ❌ **Rejected** - Goes against RDD principles

### Alternative 2: Interactive CLI Mode

**Approach:** Make `rdd.sh change create` fully interactive with prompts
```bash
rdd.sh change create
> Enter change description: Add user authentication
> Suggested names:
>   1. add-user-authentication
>   2. implement-user-auth
>   3. add-authentication-feature
> Select (1-3 or custom): 1
> Change type (feat/fix) [feat]: feat
> Create change? (y/n): y
```

**Pros:**
- Self-contained workflow
- No need for separate prompts
- Easier for beginners

**Cons:**
- Duplicates Copilot's role
- Less flexible than AI-assisted approach
- Harder to customize per user

**Decision:** ⚠️ **Deferred** - Consider for future "advanced mode"

### Alternative 3: Split Prompt into Smaller Utilities

**Approach:** Create individual utility commands:
```bash
rdd.sh change validate-name <name>
rdd.sh change suggest-names "<description>"
rdd.sh change preview <name> <type>
rdd.sh change create <name> <type>
```

**Pros:**
- More granular control
- Easier testing
- Composable commands

**Cons:**
- More complex for users
- Higher learning curve
- Not aligned with current design

**Decision:** 📋 **Consider for v2.0** - Good idea but requires more planning

---

## Conclusion

### Summary

The prompt file `.github/prompts/rdd.01-create-change.prompt.md` is **highly integrated** with the utility script ecosystem. With P16.3 enhancements, the workflow achieves **100% automation** for all functional steps.

**Original (P16):** 8 steps total
- ✅ 3 fully automated (S01 manual, S02, S07, S08)
- ⚠️ 2 partial (S04 AI-assisted, S08)
- 🤖 1 AI-required in chat (S03)
- **Automation Level:** 85%

**P16.1 Update:** Added banner automation
- ✅ 4 fully automated (S01, S02, S07, S08)
- 🤖 1 AI-required in chat (S03, S04)
- **Automation Level:** 90%

**P16.2 Update:** Added description collection in terminal
- ✅ 5 fully automated (S01, S02, S03, S07, S08)
- 🤖 1 AI-required (S04 name generation)
- **Automation Level:** 95%

**P16.3 Update:** Added name normalization, eliminated AI step
- ✅ **ALL steps automated** (S01, S02, S03, S07, S08)
- ❌ **S04 ELIMINATED** - User provides and normalizes name directly
- 🎯 **No AI assistance required** - Can run pure CLI
- **Automation Level:** 100%

### Current Automation: 100% *(Updated: 85% → 90% in P16.1 → 95% in P16.2 → 100% in P16.3)*

With P16.3, the workflow no longer requires any AI assistance. The change creation process is fully automated:
1. ✅ Banner display (terminal)
2. ✅ Git check (automatic)
3. ✅ Description + name collection with normalization (terminal)
4. ✅ Branch creation and workspace initialization (automatic)
5. ✅ Result display (automatic)

**Benefits of 100% Automation:**
- Works without Copilot (pure CLI tool)
- Faster execution (no AI token usage)
- More predictable behavior
- Full user control over naming
- Still supports Copilot-assisted workflow if desired

**Trade-offs:**
- ❌ **Lost:** AI-generated creative name suggestions
- ✅ **Gained:** Faster, simpler, CLI-friendly workflow
- ✅ **Gained:** No dependency on AI for basic operations
- ⚠️ **Note:** Users must think of their own names (with normalization help)

**Update History:**
- **P16:** Initial analysis - 85% automation (S02, S07, S08 automated)
- **P16.1:** Banner display - 90% automation (added S01)
- **P16.2:** Description collection - 95% automation (added S03, kept S04 AI-assisted)
- **P16.3:** Name normalization - 100% automation (enhanced S03, eliminated S04)

### Recommended Actions

1. **✅ HIGH PRIORITY:** Add `normalize_to_kebab_case()` to `core-utils.sh`
2. **✅ HIGH PRIORITY:** Update `rdd.sh::route_change()` with enhanced S03 implementation
3. **✅ HIGH PRIORITY:** Update `.github/prompts/rdd.01-create-change.prompt.md`:
   - Remove S04 (name generation step)
   - Renumber S07→S04, S08→S05
   - Update S03 to reference automatic name collection and normalization
4. **✅ MEDIUM PRIORITY:** Add validation loop feedback to improve UX
5. **✅ HIGH PRIORITY:** Test the new workflow end-to-end

### Step Renumbering Plan

After eliminating S04, renumber subsequent steps:

| Old Number | New Number | Description |
|------------|------------|-------------|
| S01 | S01 | Display banner (automated) |
| S02 | S02 | Check git repo (automated) |
| S03 | S03 | Collect description + name (automated, enhanced) |
| ~~S04~~ | ~~REMOVED~~ | ~~Generate name variations~~ |
| S07 | **S04** | Execute rdd.sh command |
| S08 | **S05** | Display results |

### No AI Dependency

The updated design eliminates the need for AI assistance in the change creation workflow. This makes the tool:
- **More accessible:** Works for users without Copilot
- **More reliable:** No dependency on AI service availability
- **More efficient:** Faster execution without AI processing
- **More transparent:** Clear, predictable behavior

Users who prefer AI-generated name suggestions can still ask Copilot separately before running the command, but it's no longer a required step in the workflow.

### Recommended Actions

1. **✅ HIGH PRIORITY:** Update prompt documentation (Tasks 1.1, 1.2)
2. **✅ MEDIUM PRIORITY:** Enhance output display (Tasks 2.1, 2.2)
3. **✅ HIGH PRIORITY:** Test updated workflow (Tasks 3.1, 3.2)
4. **⏸️ LOW PRIORITY:** Consider name suggestion utility (Task 4.1) - defer

### No Major Changes Needed

The current design strikes the right balance between automation and human creativity. The main recommendation is **documentation updates** to make the existing automation more visible and understandable.

---

## Appendix A: Complete Function Call Chain

### P16.3 Enhanced Chain (100% Automated)

```
User Executes: ./.rdd/scripts/rdd.sh change create
    ↓
S01: [AUTOMATED - P16.1] Display banner (via rdd.sh route_change)
    ↓
S02: [AUTOMATED] check_git_repo()
    ↓
S03: [AUTOMATED - P16.3 ENHANCED] Prompt for description AND name
    ├─→ User enters description in terminal (bash read)
    ├─→ Save to /tmp/rdd-change-description-$$.txt (for logging)
    ├─→ User enters name in terminal (bash read)
    ├─→ Normalize name → core-utils.sh::normalize_to_kebab_case()
    │    ├─→ Convert to lowercase
    │    ├─→ Replace spaces/underscores with hyphens
    │    ├─→ Remove invalid characters
    │    ├─→ Clean up multiple/trailing hyphens
    │    └─→ Return normalized name
    ├─→ Validate name → core-utils.sh::validate_name()
    │    ├─→ Check not empty
    │    ├─→ Check kebab-case format
    │    ├─→ Check max 5 words
    │    └─→ Return validation result
    ├─→ If invalid: Loop back to name input
    ├─→ If valid: Show normalized name, confirm with user
    └─→ If confirmed: Proceed to creation
    ↓
~~S04: [ELIMINATED in P16.3] Generate names (AI - Copilot)~~
    ~~No longer needed - user provides name directly with normalization~~
    ↓
S04 (was S07): [AUTOMATED] Execute create_change() with normalized name
    ├─→ core-utils.sh::validate_name() [redundant check, but safe]
    ├─→ git-utils.sh::check_git_repo()
    ├─→ git-utils.sh::get_default_branch()
    ├─→ git-utils.sh::get_git_user()
    ├─→ branch-utils.sh::branch_exists()
    ├─→ branch-utils.sh::create_branch()
    │    ├─→ git-utils.sh::check_uncommitted_changes()
    │    └─→ core-utils.sh::print_success()
    ├─→ workspace-utils.sh::init_workspace()
    │    ├─→ workspace-utils.sh::copy_template()
    │    └─→ core-utils.sh::print_info()
    ├─→ clarify-utils.sh::init_clarification()
    │    ├─→ clarify-utils.sh::create_open_questions_template()
    │    └─→ core-utils.sh::print_success()
    └─→ change-utils.sh::create_change_config()
    ↓
S05 (was S08): [AUTOMATED] Display results
    ├─→ core-utils.sh::print_success()
    ├─→ core-utils.sh::print_info()
    ├─→ core-utils.sh::print_step()
    └─→ [PROPOSED] display_change_next_steps()
```

**Total Automated Functions:** 17+ *(added normalize_to_kebab_case + enhanced validation loop)*  
**Total Utility Scripts Used:** 5 (core, git, branch, workspace, clarify)  
**AI Assistance Required:** 0 (100% automated)

### Comparison: P16 vs P16.1 vs P16.2 vs P16.3

| Version | Steps | AI Required | Automation | Key Change |
|---------|-------|-------------|------------|------------|
| **P16** | 8 | S03, S04 | 85% | Baseline analysis |
| **P16.1** | 8 | S03, S04 | 90% | Banner automated (S01) |
| **P16.2** | 8 | S04 | 95% | Description automated (S03) |
| **P16.3** | 6 | None | 100% | Name normalization (S03), S04 eliminated |

---

## Appendix B: File Locations Reference

| File Type | Path | Purpose |
|-----------|------|---------|
| **Prompt** | `.github/prompts/rdd.01-create-change.prompt.md` | User-facing instructions |
| **Wrapper** | `.rdd/scripts/rdd.sh` | Main entry point |
| **Core Utils** | `.rdd/scripts/core-utils.sh` | Validation, output, config |
| **Git Utils** | `.rdd/scripts/git-utils.sh` | Git operations |
| **Branch Utils** | `.rdd/scripts/branch-utils.sh` | Branch management |
| **Workspace Utils** | `.rdd/scripts/workspace-utils.sh` | Workspace initialization |
| **Clarify Utils** | `.rdd/scripts/clarify-utils.sh` | Clarification tracking |
| **Change Utils** | `.rdd/scripts/change-utils.sh` | Change workflow orchestration |
| **Migration Guide** | `.rdd-docs/workspace/scripts-migration-guide.md` | User migration docs |

---

**Analysis Complete**  
**Date:** November 2, 2025  
**Prepared for:** Prompt P16  
**Next Action:** Review recommendations and approve implementation tasks

---

## Revision History

### P16.1 Update (November 2, 2025)

**Change:** Updated S01 analysis to recommend banner automation

**Rationale:**
- Banner display should be handled by `rdd.sh` for consistency
- Reduces Copilot prompt complexity
- Works even when rdd.sh is called directly (outside of Copilot)
- Better separation of concerns

**Modified Sections:**
1. **Executive Summary** - Updated automation count from 3 to 4 steps
2. **Automation Status Table** - Changed S01 from ❌ No to ✅ Yes
3. **S01 Analysis** - Complete rewrite with implementation plan
4. **Appendix A** - Updated function call chain to show S01 automated

**Implementation Status:** Documentation updated; code implementation pending

**Files to Update:**
- `.rdd/scripts/rdd.sh` - Add banner to `route_change()` function
- `.github/prompts/rdd.01-create-change.prompt.md` - Update S01 to reference automatic banner

**New Automation Level:** 90% (up from 85%)

### P16.2 Update (November 2, 2025)

**Change:** Updated S03 analysis to recommend description input automation

**Rationale:**
- User description should be collected in terminal, not chat
- Consistent UX - all interaction in one place (terminal)
- Works for both Copilot-assisted and direct rdd.sh usage
- Temp file mechanism allows Copilot to access the description for S04

**Modified Sections:**
1. **Executive Summary** - Updated automation count from 4 to 5 steps
2. **Automation Status Table** - Changed S03 from ❌ No to ✅ Yes
3. **S03 Analysis** - Complete rewrite with three integration approaches
4. **Appendix A** - Updated function call chain to show S03 automated with temp file
5. **Conclusion** - Updated automation level to 95%

**Implementation Details:**
- Use bash `read` command to prompt for description
- Save description to `/tmp/rdd-change-description-$$.txt`
- Display file path in output for Copilot to read
- Copilot reads temp file content for S04 name generation

**Three Integration Approaches Documented:**
1. **Approach 1 (Recommended):** Read from temp file
2. **Approach 2:** Parse terminal output
3. **Approach 3 (Fallback):** Ask user to re-enter

**Implementation Status:** Documentation updated; code implementation pending

**Files to Update:**
- `.rdd/scripts/rdd.sh` - Add description prompt to `route_change()` function
- `.github/prompts/rdd.01-create-change.prompt.md` - Update S03 to read from temp file

**New Automation Level:** 95% (up from 90%)

### P16.3 Update (November 2, 2025)

**Change:** Complete automation by adding name normalization and eliminating AI-dependent S04

**Rationale:**
- User should be able to provide their own name directly (with normalization help)
- Automatic kebab-case normalization removes need for AI-generated suggestions
- Makes workflow suitable for pure CLI usage (no Copilot required)
- Faster execution by eliminating AI token usage for name generation
- Validation loop ensures name meets requirements before proceeding

**Modified Sections:**
1. **Executive Summary** - Updated to reflect 100% automation, S04 elimination
2. **Automation Status Table** - Changed S03 description, marked S04 as ELIMINATED
3. **S03 Analysis** - Complete rewrite with name collection + normalization implementation
4. **S04 Analysis** - Marked as ELIMINATED, moved original content to details section
5. **Appendix A** - Updated function call chain to show S03 enhanced with normalization, S04 removed
6. **Conclusion** - Updated automation level to 100%, added renumbering plan and trade-off analysis
7. **Revision History** - Added P16.3 entry

**Implementation Details:**

**New Function: `normalize_to_kebab_case()`**
- Add to `core-utils.sh`
- Input: any string (e.g., "Add User Auth", "fix_login_bug")
- Output: kebab-case format (e.g., "add-user-auth", "fix-login-bug")
- Handles: uppercase→lowercase, spaces/underscores→hyphens, invalid char removal, cleanup
- Returns: normalized string or error code 1

**Enhanced S03 Implementation:**
- Prompt for description (save to temp file for logging)
- Prompt for name in loop:
  1. User enters name (any format)
  2. Normalize using `normalize_to_kebab_case()`
  3. Validate using `validate_name()`
  4. If invalid: show error, loop back to input
  5. If valid: show normalized name, ask confirmation
  6. If confirmed: proceed with creation
- No more temp file for Copilot integration (not needed)

**Normalization Examples:**
- "Add User Auth" → "add-user-auth" ✅
- "Fix_Login_Bug" → "fix-login-bug" ✅
- "update-README" → "update-readme" ✅
- "Create  New    Feature" → "create-new-feature" ✅
- "test@#$%feature" → "testfeature" ✅

**Step Renumbering:**
After eliminating S04, remaining steps renumbered:
- S07 → S04 (Execute rdd.sh command)
- S08 → S05 (Display results)

**Implementation Status:** Documentation updated; code implementation pending

**Files to Update:**
- `.rdd/scripts/core-utils.sh` - Add `normalize_to_kebab_case()` function
- `.rdd/scripts/rdd.sh` - Update `route_change()` with enhanced S03 implementation
- `.github/prompts/rdd.01-create-change.prompt.md` - Remove S04, renumber S07→S04, S08→S05, update S03

**New Automation Level:** 100% (up from 95%)

**Benefits:**
- ✅ Works without Copilot (pure CLI tool)
- ✅ Faster execution (no AI processing)
- ✅ Full user control over naming
- ✅ Predictable, deterministic behavior
- ✅ Validation loop catches issues immediately

**Trade-offs:**
- ❌ No AI-generated creative name suggestions
- ⚠️ Users must think of names themselves (with normalization help)
- ✅ Can still ask Copilot for suggestions separately if desired

**Challenge Solved:** How to eliminate AI dependency while maintaining UX → Automatic normalization + validation loop with clear feedback




**Challenge Solved:** How Copilot accesses terminal input → Temp file with displayed path

