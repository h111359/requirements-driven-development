# Work Iteration Prompts

## Prompt Definitions

 - [x] [P01] During the build, the script `build/build.py` should copy the file `.rdd/about.json` in the `.rdd` of the release. During installation, if in the repo is installed previous version of the RDD framework, the installation script `scripts/install.py` should create a folder `.rdd-docs/archive/installation_<version>` and should move there the obsolete files `.rdd-docs/data-model.md` and `.rdd-docs/folder-structure.md` and should inform the user to merge by themselves if important information is left in these files.  
  
 - [x] [P02] Change `build/build.py` so to check if there are files in `build` folder for the version seen in `.rdd/about.json` file. If there are generated files - suggest for confirmation the user to be increased the patch number from the version or to stop the biuld process. If chosen to be increased the patch number - display the new number and ask for confirmation before proceeding further.

 - [ ] [P03] <PROMPT-PLACEHOLDER>
 
 - [ ] [P04] <PROMPT-PLACEHOLDER>

 - [ ] [P05] <PROMPT-PLACEHOLDER>
