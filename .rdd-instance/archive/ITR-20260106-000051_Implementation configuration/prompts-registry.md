%%PROMPT P-001 "Files and folders update"
[[[FOLDER_STRUCTURE_UPDATE]]]
%%ENDPROMPT

%%PROMPT P-002 "Instance configuration"
Create new default folder in .rdd-instance named `.rdd-instance/config` 
In it create a file instance-config.json with content

```json
{
  "git-enabled": false
}
```

the key "git-enabled" in `.rdd-instance/config/instance-config.json` should replace the same named key in `.rdd-instance/workdir/work-iteration-registry.json`. The change should be reflected in:

- Workdir page in Web UI should depend on the new key
- The `.rdd/config/manifest.json` should include the file and the folder as mandatory
- `.rdd/src/actions/rdd-instance_seed.py` should be changed so to create the folder and the file
- `.rdd/src/actions/prompt_complete.py` should depend on the new file and its key so to determine should it perform commit
%%ENDPROMPT
