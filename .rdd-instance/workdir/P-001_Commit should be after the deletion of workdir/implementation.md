# Implementation for P-001: Commit should be after the deletion of workdir

## Context

The prompt requests changing the git commit timing during the archiving workflow. Currently, the commit happens after creating the zip archive but before deleting the workdir contents. The prompt states the commit should be after both zip creation and workdir deletion.

## Relevant Specifications

### Technical Design
The technical-design.json file is empty, so no specific technical constraints apply.

### Requirements
From requirements.md, the following requirements are relevant:
- **UR-0009**: The framework shall archive working directory content at the end of the current iteration for historical reference. The system shall create a dedicated archive directory during the work iteration archiving. Archives preserve the complete workdir folder state exactly as it existed before archiving.
- **UR-0011**: The system shall clear the workdir folder after archiving by removing all files and subdirectories inside working directory.

### Files and Folders
The archiving functionality is implemented in `.rdd/src/actions/workdir_archive.py`.

### Questionnaire Decisions
Based on the answered questionnaire:
- **Q1 (Commit Timing)**: Selected option D - "After final verification that the new workdir is empty"
  - This ensures the commit happens after the complete cleanup workflow succeeds, including creation and verification of the fresh empty workdir
  - Provides the most confidence in the final state with validation that cleanup succeeded
- **Q2 (Error Handling)**: Selected option C - "Keep the current behavior: fail the entire operation if git-enabled is true and commit fails"
  - Maintains consistency with existing behavior
  - Enforces git-enabled contract

## Implementation Steps

### Step 1: Analyze Current Implementation
Read the current workdir_archive.py to understand the exact workflow and identify where to move the git commit.

Current workflow in workdir_archive.py:
1. Phase 1: Archive to directory and verify
2. Phase 2: Create zip archive and verify integrity
3. Phase 3: Delete directory-based archive
4. **Phase 3.5: Git Commit (CURRENT POSITION)** - lines 422-426
5. Phase 4: Two-phase commit cleanup of workdir
   - Rename workdir to workdir.deleting
   - Delete the renamed folder
   - Create fresh empty workdir
   - Final verification that new workdir is empty

### Step 2: Move Git Commit
The git commit needs to be moved from Phase 3.5 (line 422-426) to after the final verification in Phase 4 (after line 463).

This change aligns with questionnaire answer Q1 option D: "After final verification that the new workdir is empty"
- The commit will happen after all cleanup operations succeed
- The commit will include the fresh empty workdir
- If commit fails, the system is still in a valid state with an empty workdir ready for new work

Error handling remains unchanged per questionnaire answer Q2 option C - the `_git_commit` function already raises an exception on failure, which will fail the entire operation when git-enabled is true.

### Step 3: Execute the Change

Moved the git commit block from Phase 3.5 (after zip creation) to Phase 5 (after final verification that new workdir is empty).

Changes made to `.rdd/src/actions/workdir_archive.py`:
1. Removed Phase 3.5 git commit block (was at lines 422-426)
2. Added Phase 5 git commit block after final verification (after line 463)
3. Updated the docstring to reflect the new workflow order

The new workflow order:
1. Phase 1: Archive to directory and verify completeness
2. Phase 2: Create zip file and verify integrity
3. Phase 3: Delete directory-based archive
4. Phase 4: Rename workdir to workdir.deleting, delete it, create fresh empty workdir
5. **Phase 5: Git commit (NEW POSITION)** - after verifying the new workdir is empty
   - Only executes if git-enabled is true
   - Commit message: "Archive iteration: <iteration-id> - <iteration-name>"
   - Fails the entire operation if commit fails (preserves existing behavior)

### Step 4: Verify the Implementation

The implementation now matches the questionnaire decisions:
- ✅ Q1 Option D: Commit happens "After final verification that the new workdir is empty"
- ✅ Q2 Option C: Error handling unchanged - commit failures still fail the entire operation when git-enabled is true

The commit now represents the complete final state:
- Archive created and verified
- Old workdir completely deleted
- Fresh empty workdir created and verified
- All cleanup operations succeeded

If the commit fails, the system remains in a valid state with an empty workdir ready for new work, but the operation is reported as failed (maintaining the existing contract).

## Requirements Impact

No changes to requirements are needed. The existing requirements already cover this behavior:
- **UR-0009**: Archiving functionality - satisfied by creating and verifying the archive
- **UR-0011**: Clear workdir after archiving - satisfied by the cleanup workflow

The change improves the implementation's alignment with the intent of these requirements by ensuring the git commit captures the complete final state after all archiving and cleanup operations are verified.

## Testing Recommendation

To verify this change works correctly, test the following scenarios:
1. Archive with git-enabled=true and verify commit happens after workdir is empty
2. Archive with git-enabled=false and verify no commit is attempted
3. Simulate git commit failure and verify the operation fails but leaves workdir in a valid empty state
4. Verify the commit includes the empty workdir folder in the repository state
