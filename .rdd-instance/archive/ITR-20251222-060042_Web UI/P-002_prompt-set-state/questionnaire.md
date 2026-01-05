**ℹ️ Prompt State Change Script — Clarifications**

**Context**
We’re adding a deterministic script `prompt_set_state.py` that updates a prompt’s `state` in `.rdd-instance/workdir/work-iteration-registry.json`.

**Current Situation**
- `prompt_create.py` already enforces the invariant: only one prompt may be `planned` or `in-progress` at a time.
- This new script needs to enforce the same invariant when *changing* state.

---

**Q: How should `prompt_set_state.py` identify which prompt to update?**

Please choose one:
- [ ] **A)** Require `prompt-id=` parameter (e.g., `prompt-id=P-002`) 
  - **Pros:** Explicit; easy to reason about; deterministic
  - **Cons:** Slightly more typing
- [x] **B)** If `prompt-id=` is omitted, default to the currently active prompt (the one in state `planned` or `in-progress`)
  - **Pros:** Convenient for common workflow
  - **Cons:** Fails when there is no active prompt; can be surprising
- [ ] **C)** Support both `prompt-id=` and `title=` (with `prompt-id=` taking precedence)
  - **Pros:** User-friendly
  - **Cons:** Titles might not be unique; more edge cases
- [ ] **D)** Other (please specify): 

---

**Q: If setting a prompt to `planned` or `in-progress` would violate the “single active prompt” invariant, what should happen?**

Please choose one:
- [x] **A)** Fail with a clear error and make no changes
  - **Pros:** Safest; avoids implicit state changes
  - **Cons:** Requires an extra step to resolve conflicts
- [ ] **B)** Automatically demote the existing active prompt to `draft`, then proceed
  - **Pros:** One-command workflow
  - **Cons:** Implicitly changes a different prompt
- [ ] **C)** Automatically set the existing active prompt to `completed`, then proceed
  - **Pros:** Keeps “forward progress”
  - **Cons:** Risky if the prompt wasn’t actually complete
- [ ] **D)** Other (please specify): 

---

**Q: Should `prompt_set_state.py` enforce allowed state transitions (beyond validating the state value itself)?**

Please choose one:
- [x] **A)** No — allow changing to any valid state (`draft|planned|in-progress|completed`) as long as invariants hold
  - **Pros:** Simple; flexible
  - **Cons:** Easier to accidentally skip workflow steps
- [ ] **B)** Yes — only allow forward transitions (`draft → planned → in-progress → completed`)
  - **Pros:** Prevents accidental regressions/skips
  - **Cons:** Less flexible for corrections
- [ ] **C)** Yes — forward-only by default, but allow backward transitions with an explicit flag (e.g., `allow-backward=true`)
  - **Pros:** Safe by default, flexible when needed
  - **Cons:** Slightly more complexity
- [ ] **D)** Other (please specify): 
