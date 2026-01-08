# Questionnaire - Remove git_commit.py

**ℹ️ Context**

The script `.rdd/src/actions/git_commit.py` was originally created to handle git commits for active prompts. Subsequently, its functionality was integrated directly into `.rdd/src/actions/prompt_complete.py` (during P-010) to avoid state management issues.

**Current Situation:**
- `prompt_complete.py` now contains inline git commit logic that duplicates the functionality of `git_commit.py`
- `git_commit.py` still exists as a standalone script
- The CLI routing system (`rdd.py`) includes a git domain with a `git commit` action that maps to `git_commit.py`
- Requirements document [TR-20251229-1842] and related requirements reference `git_commit.py`

---

## Questions

**Q1: Should the standalone git_commit.py script be removed completely?**

Please choose one:
- [x] **A)** Yes - Remove it completely since prompt_complete.py now handles git commits inline
  - **Pros:** Eliminates code duplication, single source of truth for git operations
  - **Cons:** Removes the ability to manually trigger git commits independent of prompt completion
  
- [ ] **B)** No - Keep it as a standalone utility for manual git commits
  - **Pros:** Provides flexibility for manual git commits outside of prompt completion workflow
  - **Cons:** Maintains code duplication, two places to maintain git commit logic
  
- [ ] **C)** Refactor - Extract common git commit logic into a shared utility function used by both scripts
  - **Pros:** Eliminates duplication while keeping both entry points
  - **Cons:** More complex refactoring, may be over-engineering for current needs
  
- [ ] **D)** Other (please specify): 

---

**Q2: What should happen to the CLI git domain if git_commit.py is removed?**

Please choose one:
- [x] **A)** Remove the entire git domain from CLI (git commit command will no longer be available via CLI)
  - **Pros:** Simplifies CLI, aligns with prompt-centric workflow
  - **Cons:** Users lose the ability to manually trigger commits via CLI
  
- [ ] **B)** Keep the git domain but have it call prompt_complete.py with appropriate parameters
  - **Pros:** Maintains CLI compatibility, leverages existing implementation
  - **Cons:** Indirect routing, may be confusing
  
- [ ] **C)** Rename/redirect git commit to prompt complete in the CLI menu
  - **Pros:** Clear mapping of functionality, straightforward for users
  - **Cons:** Changes user-facing CLI structure
  
- [ ] **D)** Other (please specify): 

---

**Q3: How should requirements [TR-20251229-1841, TR-20251229-1842, TR-20251229-1843, TR-20251229-1844] be handled?**

Please choose one:
- [x] **A)** Mark them as [DELETED] since the functionality is now part of prompt_complete.py
  - **Pros:** Clean removal of obsolete requirements
  - **Cons:** Loses traceability of the feature's evolution
  
- [ ] **B)** Update them to reflect the new implementation in prompt_complete.py
  - **Pros:** Maintains accurate documentation of current state
  - **Cons:** Requires rewriting multiple requirements
  
- [ ] **C)** Keep them as-is but add a note that functionality was moved to prompt_complete.py
  - **Pros:** Preserves history while documenting current state
  - **Cons:** Requirements no longer reflect actual implementation
  
- [ ] **D)** Other (please specify): 

---

**Q4: Should the web UI Git section continue to work with git commits?**

**ℹ️ Note:** The current web UI has a Git section that displays active prompt info and commit messages.

Please choose one:
- [ ] **A)** Keep it as-is - it likely uses actions that will remain (prompt_complete.py or equivalent)
  - **Pros:** No changes needed to web UI
  - **Cons:** None identified
  
- [ ] **B)** Verify and update if it references git_commit.py directly
  - **Pros:** Ensures web UI uses correct implementation
  - **Cons:** Requires investigation and potential updates
  
- [x] **C)** Remove Git section from web UI entirely
  - **Pros:** Simplifies web UI if git commits are always part of prompt completion
  - **Cons:** Reduces functionality available in web interface
  
- [ ] **D)** Other (please specify): 
