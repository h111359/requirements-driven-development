Implementation details for prompt P-056: Active Page refreshes

Summary
-------
Implemented client-side background refresh for the Active Prompt page that updates status indicators (workflow flags) and execution-mode buttons every 2 seconds, using lightweight polling. The refresh is partially suppressed while the user is interacting with the Active Prompt UI (focused elements inside the active prompt or an open modal) to avoid interrupting user activities.

Files changed
-------------
- Modified: .rdd/src/web/static/app.js
  - Added: `startActivePromptRefresh()` to schedule targeted updates every 2000 ms
  - Added: `refreshActivePromptStatuses()` which fetches `/api/registry` and updates only:
    - workflow flags via `updateWorkflowFlags(activePrompt)`
    - execution-mode radio/button state (tries `mode-<mode>` id, falls back to inputs named `execution-mode`)
    - complete button enabled/disabled state (silently)
  - Added: `isUserInteractingWithActivePrompt()` to implement partial suppression when:
    - any Bootstrap modal is open (element `.modal.show` present), or
    - any element inside `#active-prompt-content` has focus (e.g., typing in prompt.md textarea)
  - Hooked `startActivePromptRefresh()` into `initializeApp()` so the refresh starts after initial load.

Rationale and decisions (based on questionnaire answers)
--------------------------------------------------------
- Q1 (which elements): user selected option B — "All status indicators and mode buttons across the Active Prompt page". Implementation updates workflow flags and execution-mode controls as targeted DOM updates rather than reloading the entire page.
- Q2 (interval): user selected fixed 2 seconds. The refresh interval is fixed at 2000 ms.
- Q3 (approach): user selected client-side polling. Implementation uses periodic `fetch('/api/registry')` polling to retrieve the latest prompt state and update only the needed DOM elements.
- Q4 (suppression): user selected partial suppression. Refresh is skipped while user interaction is detected (focus inside the active prompt or an open modal).

Why targeted updates
--------------------
Performing small, targeted DOM updates (flags and mode inputs) minimizes risk of interfering with the user's current actions, reduces flicker, and is easier to implement and test than a full page refresh or replacing large parts of the DOM. This approach follows the "minimal scope, low risk" principle while honoring the user's choice to update all visible status indicators and mode controls.

Requirements and spec traceability
----------------------------------
Changes relate to the following requirements and technical constraints (observed in `.rdd-instance/specifications/requirements.md`):

- UR-0017: Web UI Prompt Management / Active Prompt page — this change is an enhancement to the Active Prompt page behavior.
- UR-0074: Enhanced visibility for form controls — we update mode controls programmatically and keep interactions accessible.
- UR-0075 / TR-0063 / TR-0062: Active Prompt page tabbed editor and API endpoints — the implementation relies on the existing `/api/registry` endpoint (TR-0062) to read prompt flags, which is consistent with the current web API design.
- TR-0001 / TR-0016: Implementation is client-side JavaScript and uses existing REST-like endpoints; no server changes were made.

Technical design
----------------
- `.rdd-instance/specifications/technical-design.json` is empty; no constraints were found there specifically affecting this change.
- Files and folders used: `.rdd/src/web/static/app.js` per files-and-folders guidance (Web UI static assets).

Commands executed
-----------------
No terminal scripts were required by the change itself (pure frontend JS modification). To verify manually, the following steps are recommended:

1. Start the web server (if not running):

```bash
python .rdd/src/web/start_web.py
```

2. Open the Web UI in the browser (the server usually opens the default browser automatically). Navigate to the Active Prompt page.

3. Observe the status flags and mode buttons for the active prompt — they should update approximately every 2 seconds.

4. While editing `prompt.md` (typing in the prompt editor) or when a modal is open, the background refresh should pause to avoid interfering with typing or modal interactions.

5. To simulate registry updates, modify `work-iteration-registry.json` (or trigger actions via the provided API) and observe the flags updating in the UI.

Notes on safety and rollback
---------------------------
- The change is limited to client-side behavior and is non-destructive.
- Rollback: revert `.rdd/src/web/static/app.js` to the previous revision (git checkout or restore from backup) if needed.

Next steps and suggestions
--------------------------
- Consider exposing the refresh interval in UI settings (questionnaire recommended option B for configurability); current implementation uses a fixed 2s interval as selected by the user.
- Optionally, implement a WebSocket/SSE server push solution if polling becomes a performance concern (questionnaire option C was considered, but user chose polling).
- Add unit/integration tests for the web UI (end-to-end test harness) to validate suppression behavior during user interactions.

Implementation log
------------------
- Modified `.rdd/src/web/static/app.js` in-place.
- No requirement scripts were run since no `requirements.md` changes were necessary.

If you want, I can now run the web server locally and validate the behavior interactively, or commit these changes for you.
