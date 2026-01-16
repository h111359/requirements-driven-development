%%PROMPT P-001 "Commit should be after the deletion of workdir"
Commit happens before deletion of workdir content durin archiving which causes additional uncommitted changes to appeare
Commit should be after workdir content deletion and after zip creation of the archive folder
%%ENDPROMPT
