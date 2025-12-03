# P01 Implementation

- [ ] [P01] Add to `.rdd/scripts/rdd.py` and `.rdd/scripts/rdd_utils.py` functionality which lists all the files, folders and recursively do the same for their subfolders and stores the result in `.rdd-docs/workspace/files-list.json`. If this file exists - recreate it. For each file write its name, relative path and the time of last change. Exclude folders and subfolders which start with "." or folders like "venv". 


## Related files read
- `.rdd-docs/requirements.md` — general requirements and workspace rules (GF/FR) relevant to workspace file handling and workspace location `.rdd-docs/workspace/`.
- `.rdd-docs/tech-spec.md` — describes `rdd.py` and `rdd_utils.py` responsibilities and locations, confirms workspace paths and that scripts live in `.rdd/scripts/`.
- `.rdd-docs/user-story.md` — user-story template (no direct changes required for this prompt).
- `.rdd/scripts/rdd.py` — main entrypoint; will add a `workspace list-files` action that invokes the new utility.
- `.rdd/scripts/rdd_utils.py` — utilities file; will add the recursive directory listing function that writes `.rdd-docs/workspace/files-list.json`.


## Short summaries (what relates / will be affected)
- `requirements.md` and `tech-spec.md` both reference `.rdd-docs/workspace/` as the active workspace location; the JSON output will be stored there.
- `rdd_utils.py` currently provides workspace helpers; adding `create_files_list()` aligns with existing utility placement and coding style (returns True/False, uses `print_*` helpers and `ensure_dir`).
- `rdd.py` already routes `workspace` actions; adding `list-files` as a new action keeps the domain-based pattern.


## Plan
1. Add a new utility function `create_files_list(root_dir='.', output_path='.rdd-docs/workspace/files-list.json', exclude_names=None)` to `.rdd/scripts/rdd_utils.py`.
   - Walk the tree top-down, skip directories that start with `.` or are named `venv` (or in `exclude_names`).
   - Collect entries for directories and files. For each item include: `type` (`file`|`dir`), `name`, `relpath` (relative to repository root), and `mtime` (ISO8601 UTC format).
   - Ensure `.rdd-docs/workspace/` exists and write JSON (recreate if exists).
2. Import `create_files_list` in `.rdd/scripts/rdd.py` and add `workspace list-files` route which calls the utility.
3. Run the new action to generate `.rdd-docs/workspace/files-list.json` and verify it was created.
4. Mark prompt P01 as completed using the required script: `python .rdd/scripts/rdd.py prompt mark-completed P01`.


## Commands to be executed (documented here and executed):
- `python .rdd/scripts/rdd.py workspace list-files`
- `python .rdd/scripts/rdd.py prompt mark-completed P01`


## Notes on ambiguities
- The prompt asks to "list all the files, folders" — implementation records both directories and files with `type` field, and for both stores `mtime`.
- Relative paths will be computed relative to repository root (`git rev-parse --show-toplevel` via existing `get_repo_root()` helper).


## Implementation steps log
- Created this implementation file and will now patch the code files and run the commands.

