# Questionnaire for P-004: Add prompt completion with commit command

## Context

The active prompt requests a new action for making a git commit with changes during the current prompt. The commit message should follow a specific format: `iteration-id_prompt-id_prompt-title`. The action will be executed manually by the user, independently from other actions.

This questionnaire aims to clarify implementation details that have multiple reasonable interpretations.

---

## Questions

**Q1: What should be the domain assignment for the new commit command in the CLI?**

ℹ️ **Context:** The RDD CLI uses a domain-based routing architecture. Currently, there are two domains: `prompt` and `workdir`. The commit action could logically belong to either the `prompt` domain (as it commits work for the current prompt) or could be added to a new domain like `git` or `vcs`.

Please choose one:
- [ ] **A)** Add to existing `prompt` domain as `python rdd.py prompt commit`
  - **Pros:** Semantically fits with prompt-related operations; simple integration
  - **Cons:** Mixes version control with prompt management concerns
  
- [ ] **B)** Add to existing `workdir` domain as `python rdd.py workdir commit`
  - **Pros:** Workdir domain already handles iteration-level operations
  - **Cons:** Less intuitive discoverability; workdir is more about setup/archive operations
  
- [x] **C)** Create a new `git` domain as `python rdd.py git commit` 
  - **Pros:** Clean separation of concerns; extensible for future git operations
  - **Cons:** Adds complexity; only one command in the domain initially
  
- [ ] **D)** Other (please specify): _______________

---

**Q2: Should the commit action automatically stage all changes, or require pre-staging?**

ℹ️ **Context:** When the user executes the commit command, the script needs to determine what files to commit.

Please choose one:
- [x] **A)** Auto-stage all changes (equivalent to `git commit -a`)
  - **Pros:** Simpler user workflow; one command does everything
  - **Cons:** User might accidentally commit unwanted changes
  
- [ ] **B)** Only commit already-staged changes (equivalent to `git commit`)
  - **Pros:** User has explicit control; follows standard git workflow
  - **Cons:** Requires user to manually stage changes first
  
- [ ] **C)** Auto-stage only files in `.rdd-instance/` and repository root files
  - **Pros:** Focused scope; reduces accidental commits of unrelated work
  - **Cons:** More complex logic; might miss legitimate changes
  
- [ ] **D)** Other (please specify): _______________

---

**Q3: How should the commit message be formatted when the prompt title contains spaces or special characters?**

ℹ️ **Context:** The requirement states the format should be `iteration-id_prompt-id_prompt-title`. For example, the current prompt "Add prompt completion with commit command" contains spaces.

**Current active prompt example:**
- iteration-id: `ITR-20251222-060042`
- prompt-id: `P-004`
- prompt-title: `Add prompt completion with commit command`

Please choose one:
- [ ] **A)** Replace spaces with underscores: `ITR-20251222-060042_P-004_Add_prompt_completion_with_commit_command`
  - **Pros:** Clean filename-safe format; maintains readability
  - **Cons:** Less natural to read; underscores everywhere
  
- [ ] **B)** Replace spaces with hyphens: `ITR-20251222-060042_P-004_Add-prompt-completion-with-commit-command`
  - **Pros:** More readable; common convention in URLs/slugs
  - **Cons:** Inconsistent delimiter usage (underscores between components, hyphens within)
  
- [ ] **C)** Remove spaces entirely: `ITR-20251222-060042_P-004_Addpromptcompletionwithcommitcommand`
  - **Pros:** Most compact
  - **Cons:** Hard to read; loses word boundaries
  
- [x] **D)** Keep spaces as-is (quote the message): `ITR-20251222-060042_P-004_Add prompt completion with commit command`
  - **Pros:** Most readable; preserves original title
  - **Cons:** Requires proper shell quoting; might cause issues in some tools
  
- [ ] **E)** Other (please specify): _______________

---

**Q4: Should the script validate that there are changes to commit before attempting the commit?**

ℹ️ **Context:** Users might run the commit command when there are no staged/unstaged changes.

Please choose one:
- [x] **A)** Yes, check for changes first and exit gracefully with a message if none exist
  - **Pros:** Better user experience; prevents empty commits; clear feedback
  - **Cons:** Slight additional complexity
  
- [ ] **B)** No, let git handle it (git will reject empty commits by default)
  - **Pros:** Simpler implementation; delegates to git's built-in behavior
  - **Cons:** Error message might be less user-friendly
  
- [ ] **C)** Yes, but allow forcing empty commits with a flag (e.g., `allow-empty=true`)
  - **Pros:** Flexibility for special cases; maintains validation
  - **Cons:** Most complex; edge case might not be needed
  
- [ ] **D)** Other (please specify): _______________

---

**Q5: What should happen if the repository is not in a clean state (e.g., in the middle of a merge, rebase, or has unresolved conflicts)?**

ℹ️ **Context:** Git operations can fail or behave unexpectedly when the repository is in certain states.

Please choose one:
- [x] **A)** Check repository state and refuse to commit with a clear error message
  - **Pros:** Safest approach; prevents potentially problematic commits
  - **Cons:** Users might need to resolve issues manually before committing
  
- [ ] **B)** Proceed anyway and let git handle any errors
  - **Pros:** Simplest implementation; might work in some edge cases
  - **Cons:** Could lead to confusing error messages or unexpected states
  
- [ ] **C)** Detect specific states (merge/rebase) and provide tailored guidance
  - **Pros:** Most helpful user experience; educational feedback
  - **Cons:** More complex implementation; needs to handle multiple scenarios
  
- [ ] **D)** Other (please specify): _______________

---

**Q6: Should the commit command support additional git commit options (e.g., --amend, --no-verify)?**

ℹ️ **Context:** Users might want to amend the last commit, skip pre-commit hooks, or use other git commit flags.

Please choose one:
- [x] **A)** No, keep it simple with just the basic commit functionality
  - **Pros:** Easier to implement and maintain; clear single-purpose command
  - **Cons:** Less flexible; users need to use git directly for advanced options
  
- [ ] **B)** Yes, support common flags like `--amend` and `--no-verify` through parameters
  - **Pros:** More powerful; reduces need to use git directly
  - **Cons:** More complex; needs parameter parsing and validation
  
- [ ] **C)** Yes, allow passing arbitrary git flags through a parameter like `git-flags="--amend --no-verify"`
  - **Pros:** Maximum flexibility; future-proof
  - **Cons:** Less validation; users could pass dangerous flags
  
- [ ] **D)** Other (please specify): _______________

---

## Instructions for Completing This Questionnaire

1. Select your preferred option for each question by marking the checkbox with an `x`: `[x]`
2. If you select "Other", please provide detailed specifications in the blank space
3. Save this file after making your selections
4. The implementation will proceed based on your chosen answers
