The analyze modification of the execute command should depend on an attribute in `.rdd-instance/workdir/work-iteration-registry.json`, not to be expected to be written in the chat.
The convention `.rdd/conventions/work-iteration-registry.convention.md` should be changed so every prompt to have a boolean key if the analyze modification should be turned on.
The prompt snippet `.rdd/prompt-snippets/execution.md` should read the modifier from `.rdd-instance/workdir/work-iteration-registry.json`.
The requirements should be revised so to reflect this change.
There should be created a script - prompt_analyze_on.py which expects a prompt-id and turns on the option in `.rdd-instance/workdir/work-iteration-registry.json`
There should be created a script - prompt_analyze_off.py which expects a prompt-id and turns off the option in `.rdd-instance/workdir/work-iteration-registry.json`
The Web UI should provide a switcher to turn on and off analyze for the active prompt (should not be provided for completed promtpst)
When the analyze execution is completed, the copilot should turn off the analyze option via the prompt_analyze_off.py script.