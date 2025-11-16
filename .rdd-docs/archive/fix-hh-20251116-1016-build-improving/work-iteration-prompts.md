# Work Iteration Prompts

## Prompt Definitions

 - [x] [P01] The release of the RDD framework should be taken from `.rdd/about.json` file instead of `.rdd-docs/config.json`. The key "version" should be removed. The scripts in `.rdd/scripts` should be changed so to use the value of the key "version" from `.rdd/about.json`. The files in the following locations should be checked and this change should be reflected whenever needed to:
    - `build/create-release.prompt.md`
    - `templates/config.json`
    - `templates/install.bat`
    - `templates/install.sh`
    - `templates/README.md`
    - `templates/requirements.md`
    - `templates/user-guide.md`
    - `scripts`
    - `tests`
    - `rdd.sh`
    - `.rdd-docs/requirements.md`
    - `.rdd-docs/tech-spec.md`
  After the change the tests should be executed and should run without errors
  
 - [ ] [P02] <PROMPT-PLACEHOLDER>

 - [ ] [P03] <PROMPT-PLACEHOLDER>
 
 - [ ] [P04] <PROMPT-PLACEHOLDER>

 - [ ] [P05] <PROMPT-PLACEHOLDER>
