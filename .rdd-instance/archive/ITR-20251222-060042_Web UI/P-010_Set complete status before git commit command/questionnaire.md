# Questionnaire for P-010: Set complete status before git commit command

## Context

The current implementation in `prompt_complete.py` executes operations in this order:
1. Execute git commit (if git-enabled)
2. Set prompt state to "completed" in registry
3. Write registry to disk

This creates uncommitted changes after the git commit because the registry state change happens after the commit.

The requirement is to reverse the order: first set status to completed, then commit, so no uncommitted changes exist after the commit.

---

## Questions

**Q1: Should the git commit message reflect that the prompt is being set to completed state?**

Please choose one:
- [ ] **A)** Yes - The commit message should explicitly mention "Setting prompt [ID] to completed state"
  - **Pros:** Clear audit trail, commit message accurately reflects what the commit contains
  - **Cons:** More verbose commit message
  
- [x] **B)** No - Keep the current generic commit message format from git_commit.py
  - **Pros:** Consistent with existing behavior, simpler implementation
  - **Cons:** Less clear what the commit represents
  
- [ ] **C)** Other (please specify): 

**Recommendation:** Option A for better traceability

---

**Q2: What should happen if setting the prompt state to "completed" fails after it has been changed but before git commit?**

Please choose one:
- [x] **A)** Rollback the state change and report error (do not commit)
  - **Pros:** Maintains consistency, no partial state
  - **Cons:** More complex error handling, might leave inconsistent state if rollback fails
  
- [ ] **B)** Keep the state change and skip git commit, report warning
  - **Pros:** Simpler, state is updated even if commit fails
  - **Cons:** Git history won't reflect the state change
  
- [ ] **C)** Keep the state change and attempt git commit anyway, log errors
  - **Pros:** Best effort to complete both operations
  - **Cons:** Unclear behavior on partial failures
  
- [ ] **D)** Other (please specify): 

**Recommendation:** Option A for data consistency

---

**Q3: Should the script verify that the state change was successfully written to disk before attempting git commit?**

Please choose one:
- [ ] **A)** Yes - Read back the registry file to verify the state change is persisted
  - **Pros:** Extra safety, ensures commit includes the actual change
  - **Cons:** Additional I/O overhead, slower execution
  
- [x] **B)** No - Trust that the write operation succeeded
  - **Pros:** Simpler, faster
  - **Cons:** Potential race conditions or file system issues might not be caught
  
- [ ] **C)** Other (please specify): 

**Recommendation:** Option B for simplicity, as Python's file operations will raise exceptions on failure

---

**Q4: When git-enabled is false, should the script still write the registry change to disk?**

Please choose one:
- [x] **A)** Yes - Always persist the state change regardless of git-enabled setting
  - **Pros:** Consistent behavior, state is always updated
  - **Cons:** None
  
- [ ] **B)** No - Only update state if git commit will happen
  - **Pros:** All-or-nothing approach
  - **Cons:** State management becomes dependent on git settings, unusual behavior
  
- [ ] **C)** Other (please specify): 

**Recommendation:** Option A - git-enabled should only control git operations, not state management

---

**Q5: Should there be a way to set a prompt to completed without triggering a git commit, even when git-enabled is true?**

Please choose one:
- [ ] **A)** Yes - Add an optional parameter `skip-git=true` to bypass git commit
  - **Pros:** More flexible, useful for testing or manual operations
  - **Cons:** Added complexity, potential for misuse
  
- [x] **B)** No - Always follow the git-enabled flag setting
  - **Pros:** Simpler, consistent behavior
  - **Cons:** Less flexible
  
- [x] **C)** Other (please specify): If git-enabled is false, no commit should be attempted, but status should be changed to completed.

**Recommendation:** Option B for simplicity and consistency
