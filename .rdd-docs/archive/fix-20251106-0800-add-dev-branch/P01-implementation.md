# P01 Implementation

Date: 2025-11-06

## Context gathered
- Read `.rdd-docs/workspace/.rdd.copilot-prompts.md` and located P01.
- Read `.github/prompts/rdd.01-initiate.prompt.md`.
- Read `.rdd/scripts/rdd.py`.
- Consulted RDD requirements in `.rdd-docs/requirements.md` to keep script param-compatibility.

## Changes made
- Updated `.github/prompts/rdd.01-initiate.prompt.md` to stop asking for change type and delegate selection to the script via an interactive menu. Now it runs:
  - `python .rdd/scripts/rdd.py change create`
- Enhanced `.rdd/scripts/rdd.py`:
  - Added an interactive selection menu for change type (arrow keys + enter/space). Implemented with curses and a numeric-input fallback.
  - By default, the menu shows only "Fix" as required. The "Enhancement" option remains implemented but hidden.
  - Hidden reveal toggles:
    - Env var `RDD_REVEAL_ENH=1`
    - CLI flag `--reveal-enh`
  - Preserved parameter support to meet FR-15: `python .rdd/scripts/rdd.py change create enh|fix` still works and bypasses the menu.

## How it works
- If you run without a type: `python .rdd/scripts/rdd.py change create`:
  - You get an interactive menu to choose the type.
  - Only "Fix" is visible by default. Enhancement remains available via the hidden toggles above.
- If you run with a type: `python .rdd/scripts/rdd.py change create fix` or `enh`:
  - The script respects your explicit parameter and skips the menu.

## Verification steps
- Ran `python .rdd/scripts/rdd.py --version` to confirm no syntax/runtime errors.
- Manual review of selection flow in `route_change('create')` confirms menu path is invoked when no type is passed, and parameters still work.

## Notes
- The change avoids exposing the enhancement option in the visible menu, as requested, while keeping it technically present for later enablement.
- The help text remains valid; parameter-based execution is still supported.
