# Stand-Alone Prompt for Cross-Platform Migration

Copy the text below and paste it into `.rdd-docs/workspace/.rdd.copilot-prompts.md` as a new prompt:

---

## Prompt Text (Copy from here)

```markdown
- [ ] [PXX] Implement cross-platform Python command migration: Replace all `python3` commands with `python` in prompt files. Update the following files: `.github/prompts/rdd.01-initiate.prompt.md`, `.github/prompts/rdd.06-execute.prompt.md`, `.github/prompts/rdd.08-wrap-up.prompt.md`, `.github/prompts/rdd.09-clean-up.prompt.md`, `.github/prompts/rdd.G4-update-from-main.prompt.md`. Change every occurrence of `python3 .rdd/scripts/rdd.py` to `python .rdd/scripts/rdd.py`. Then update `README.md` to add a requirements section stating: "Python 3.7 or higher required. The `python` command must point to Python 3.x. On older Linux systems, you may need to create an alias or symlink if `python` points to Python 2.x." Finally, verify the shebang in `.rdd/scripts/rdd.py` is `#!/usr/bin/env python3`. Test the changes on your current system by running `python .rdd/scripts/rdd.py --version` to ensure it works. Document all changes made.
```

---

## Notes

- Replace `PXX` with the next available prompt ID in your file
- This prompt implements the recommended **Variant 1** from the analysis
- The prompt is designed to be executed as a single, complete task
- After execution, it should be marked as completed using the standard RDD workflow

