# Archived Prompts

This directory contains deprecated prompts that have been superseded by the simplified RDD workflow.

## Contents

### rdd.01-create-change.prompt.md
**Status:** ⛔ Deprecated (Replaced by `rdd.01-initiate.prompt.md`)

**Why Archived:**
- Contained 8-step manual workflow now fully automated by `.rdd/scripts/rdd.sh`
- Required manual git commands, directory creation, and file manipulation
- File was corrupted with formatting issues

**Replacement:**
Use `.github/prompts/rdd.01-initiate.prompt.md` - a minimal 3-step prompt:
1. Ask user: feature or fix?
2. Execute: `rdd.sh change create feat` or `rdd.sh change create fix`
3. Script handles everything automatically

### rdd.X1-create.prompt.md
**Status:** ⛔ Deprecated (Replaced by `rdd.01-initiate.prompt.md`)

**Why Archived:**
- Documented old script interface: `rdd.sh change init` and `rdd.sh fix init <name>`
- Used deprecated manual prompting workflow
- Superseded by unified `rdd.sh change create [feat|fix]` command

**Replacement:**
Use `.github/prompts/rdd.01-initiate.prompt.md` with new unified command interface.

---

## Migration Notes

**Old Workflow (Deprecated):**
```bash
# Manual steps, multiple prompts
rdd.sh change init
# or
rdd.sh fix init <name>
```

**New Workflow (Current):**
```bash
# Single unified command, interactive
rdd.sh change create feat
# or
rdd.sh change create fix
```

See `.rdd-docs/workspace/scripts-migration-guide.md` for complete migration details.

---

**Archived:** 2025-01-12 (P21 Implementation)  
**Rationale:** Simplification per implementation-plan-P20.md user choices
