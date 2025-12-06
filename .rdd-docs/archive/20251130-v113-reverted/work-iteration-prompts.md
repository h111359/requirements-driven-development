# Work Iteration Prompts

## Prompt Definitions

 - [x] [P01] Add to `.rdd/scripts/rdd.py` and `.rdd/scripts/rdd_utils.py` functionality which lists all the files, folders and recursively do the same for their subfolders and stores the result in `.rdd-docs/workspace/files-list.json`. If this file exists - recreate it. For each file write its name, relative path and the time of last change. Exclude folders and subfolders which start with "." or folders like "venv". 
  
 - [x] [P02] Web UI

### What is needed:

What is the possibility to be created a web interface over `.rdd/scripts/rdd.py`. It should be running both under windows and linux and if possible - not to use additional libraries and not be dependent on additional installations. I don't want additional scripts to be created. Everything should be integrated in rdd.py and when rdd.py is started - to open the UI in browser. Use as style the styles in the file `.rdd-docs/workspace/system-questionnaire.html`

### Why it is needed:

More convenience in RDD processing and more ability for additional help and explanations of the options to the user

### Additional Considerations

Plan: Embed Web UI in `.rdd/scripts/rdd.py`
TL;DR: Add a small HTTP server and minimal SPA directly inside rdd.py (no extra files) using only Python stdlib (http.server, threading, webbrowser, subprocess, json). The server binds to loopback, opens the browser, exposes JSON/SSE endpoints and invokes existing RDD functions in-process (with a subprocess fallback). Minimal safe changes to rdd.py are required so import/use is non-destructive.

Goal: Add an embedded web UI inside .rdd/scripts/rdd.py only (no extra files, no new deps beyond Python stdlib). Running python .rdd/scripts/rdd.py on Windows and Linux should start a localhost HTTP server, open the browser to the UI, and expose endpoints to run RDD actions.

Server: use ThreadingHTTPServer (or similar) bound to 127.0.0.1, port=0 for auto-pick. Generate a random token; require it via header or ?token=. HTTP only on loopback.

Start a loopback-only server with defaults host=127.0.0.1 and port=0 (OS picks a free port). If binding fails, retry on a new ephemeral port; if the IPv4 loopback isn’t available, switch to the IPv6 loopback address 0:0:0:0:0:0 (line 0, column 1). Also honor optional env/flags (RDD_HOST, RDD_PORT, --host, --port) when set.

UI assets: inline HTML/JS/CSS strings served by the handler (no external files). If SSE is supported via stdlib, serve logs as text/event-stream; otherwise allow long-polling fallback—pick one and implement it fully.

Actions: support all actions in rdd.py available. Provide a start_rdd_task(action, options, log_cb) running in background threads in-process; if in-process fails, fallback to a subprocess using sys.executable rdd.py <domain> <action>. No interactive prompts; if required input is missing, return structured errors.

Cancellation: implement cancel_rdd_task(run_id); on Unix use process groups and os.killpg; on Windows use CREATE_NEW_PROCESS_GROUP and TerminateProcess/CTRL_BREAK as appropriate.
Main entry: default to web UI when no args; provide --cli or RDD_NO_WEB_UI=1 to force the old CLI menu.

Behavior guarantees: no top-level side effects on import; avoid sys.exit inside internal call paths; return structured JSON responses {run_id, state, error?}.
Concurrency/state: in-memory run registry; reasonable cap on concurrent tasks (e.g., 2-4) is fine; no persistence needed.

Validation: describe a quick manual check (run script, see URL printed, browser opens, start action, see live logs, cancel works).


 - [ ] [P03] <PROMPT-PLACEHOLDER>
 
 - [ ] [P04] <PROMPT-PLACEHOLDER>

 - [ ] [P05] <PROMPT-PLACEHOLDER>
