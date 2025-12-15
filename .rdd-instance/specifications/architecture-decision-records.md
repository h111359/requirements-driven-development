# Architecture Decision Records

[ADR-001] An empty workdir folder `.rdd-instance/workdir` should exist at the start of each new work iteration

[ADR-002] During active work, files are freely added or modified within the workdir folder.

[ADR-003] At completion, the entire workdir folder is archived as a full snapshot of its final state.

[ADR-004] After archiving, the workdir folder is fully cleaned by removing all files and folders in it.

[ADR-005] Archives preserve the complete workdir folder state exactly as it existed before archiving.

[ADR-007] The system is implemented entirely in Python for cross-platform compatibility.

[ADR-008] The primary script for all operations is `rdd.py`, with helper utilities in `rdd_utils.py`.

[ADR-009] Prompt templates provided by the framework and user are stored in `.rdd/prompts/`.

[ADR-010] GitHub-specific Copilot prompt integrations reside in `.github/prompts/`.

[ADR-011] The work-iteration registry `.rdd-instance/workdir/work-iteration-registry.json` may define multiple User Stories, and each User Story has its own active prompt file (`prompt-file`). The registry selects what to execute via `mode` (`userStory` or `task`) and `active` pointers.

[ADR-012] RDD framework web interface is initiated through the command: `python .rdd/scripts/rdd.py`.

[ADR-013] The command uses `python` rather than `python3` for portability across systems.

[ADR-014] The configuration file for the framework is stored at `.rdd-instance/config.json`.

[ADR-015] A template configuration file is provided at `templates/config.json`.

[ADR-016] Releases are built using the script `build/build.py`.

[ADR-017] Build artifacts are generated in the `build/` directory.

[ADR-018] Releases are distributed as a single cross-platform archive named `rdd-v{version}.zip`. The release zip file includes framework code, installation scripts, templates, and documentation.

[ADR-019] No database is used; all data is stored in Markdown, JSON, or JSONL files.

[ADR-020] Archived workdirs are stored in `.rdd-instance/archive/`.

[ADR-021] GitHub Copilot is optionally supported for prompt execution workflows.

[ADR-022] Python 3.8+ is required as the runtime environment for all scripts.
