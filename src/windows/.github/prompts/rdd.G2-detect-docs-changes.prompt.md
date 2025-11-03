S01: Read all the files in `.github/prompts`, all the files in `.rdd/scripts` and all the files in `.rdd/templates` - this will give you understanding for the current state and logic of the project. 

S02: Create copies in `.rdd-docs/workspace` of the files:
- `.rdd-docs/requirements.md`
- `.rdd-docs/tech-spec.md`
- `.rdd-docs/folder-structure.md`
- `.rdd-docs/data-model.md`

S03: Stop and ask the user to keep the changes so to be visible what ammendments will be done later. 

S04: Revise each of the copied files in `.rdd-docs/workspace` row by row and decide if some ammendment should be made so to reflect the reality. You also can choose to add new statements (follow the format of the files and always continue the sequential list numbers, do not put in between). Mark each row which needs modification as in the very beginning of the row make tagging with one of [ADDED], [MODIFIED], [DELETED]. When [ADDED] is used - make sure the new statement has a new unique sequential number. When [MODIFIED] or [DELETED] is used - keep the original numbering. When [DELETED] is used - do not remove the statement, just mark it as deleted.
