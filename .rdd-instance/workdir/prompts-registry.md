%%PROMPT P-001 "Analysis of the issue"
According `https://github.com/h111359/requirements-driven-development/issues/84` when user archives the current iteration, the folders without files remain in `.rdd-instance/workdir`
Make in the prompt workdir root cause analysis about this issue in a file - issue_84_analysis.md with exact cause of the issue, the way suggested to be fixed, best practices, etc.

Most probably the issue is in the logic of `.rdd/src/actions/workdir_archive.py`. Make sure the suggested solution is reliable. The prime concern should be not to lose the files and subfolders of the workdir. This is the reason the script first makes a copy and then tries delete. No delete should be made if the copy operation is not successful. Still - you can propose better approach.

Do not try to judge for the error from the current state of the repo. Currently this issue can not be seen as we are in a new iteration and the leftover folders are deleted manually. If you want to test - create in the prompt folder a script which uses similar code as the one in `.rdd/src/actions/workdir_archive.py` and try with mockup folders. **DO NOT EXECUTE** `.rdd/src/actions/workdir_archive.py` as I don't want to ruin the current iteration - work with temporary scripts and mockup folders. 

Improve the existing script with better error handling and verification without changing the overall structure.

**Changes**:
1. Add verification that the archive copy is complete before cleanup
2. Replace "best-effort" cleanup with strict cleanup that fails if any deletion fails
3. Add retry logic for transient failures (e.g., temporary file locks)
4. Provide detailed error messages identifying which folders failed to delete
5. Add a final verification step that confirms workdir is empty (except for registry if needed)

Implement a two-phase commit where cleanup is verified before committing.

**Changes**:
1. After copying, rename workdir to workdir.deleting
2. Verify archive completeness
3. Delete the renamed folder
4. Create fresh empty workdir
%%ENDPROMPT
