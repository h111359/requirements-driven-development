%%PROMPT P-001 "Windows test failures"
The github execution of windows tests in `.github/workflows/tests.yml` failed with error. 
See the file `.rdd-instance/workdir/P-001_Windows test failures/logs_54574600190/All Tests (Windows)/2_Run actions_checkout@v4.txt` and the whole test log in `.rdd-inld stance/workdir/P-001_Windows test failures/logs_54574600190`
Troubleshoot.
Fix the issue.
The tests should succeed on 100%
Explore the possibility to compress to a zip file the workdir during archive
%%ENDPROMPT

%%PROMPT P-002 "Commit during archive"
When the workdir is archived, changes in the repo are generated and stay uncommitted.
Add to the archive iteration functionality to make git commit (if git option is true) with the name of the itteration


### Modification 001

The git message should include iteration ID as well
%%ENDPROMPT

%%PROMPT P-003 "Archive operation failiure"
During archive appears error: "Failed to archive work iteration: ERROR: Failed to create zip archive at /home/hromar/Desktop/vscode/requirements-driven-development/.rdd-instance/archive/ITR-20260116-153840_Tests failures fixes.zip. Error: ZIP does not support timestamps before 1980"

Find the problem.
Fix the code.
Test yourself (do not corrupt the workdir content)
%%ENDPROMPT
