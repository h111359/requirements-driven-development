# Release Automation Prompts

This document contains a sequential series of prompts for implementing the complete RDD Framework release automation system. These prompts should be executed in order by GitHub Copilot agent.

The implementation follows these key decisions (from questionnaire):
- **Scope**: Complete end-to-end implementation of all three phases
- **Build script**: Modify build.py to add --version and --non-interactive flags
- **Version strategy**: Manual manifest version - user updates manifest.json before merge
- **Release notes**: Manual release notes - user creates release-notes-v{version}.md file before merge
- **Testing**: Include testing strategy with dev branch validation
- **Format**: Sequential numbered prompts with clear objectives

---

## Prompt 1: Modify build.py for CI/CD Support

**Objective**: Add command-line arguments to build.py to support non-interactive execution in GitHub Actions workflows.

**Context**: The current build.py script is interactive, prompting users for version selection and conflict resolution. For CI/CD automation, we need a non-interactive mode that accepts version as a command-line argument.

**Requirements**:
1. Add argparse support to build.py
2. Add `--version` argument to specify the version to build
3. Add `--non-interactive` flag to skip all user prompts
4. When `--non-interactive` is used without `--version`, exit with clear error message
5. Preserve existing interactive functionality when arguments are not provided
6. Ensure version validation still occurs in non-interactive mode

**Implementation Details**:
- Import argparse at the beginning of the script
- Create argument parser with two arguments:
  - `--version`: String argument for specifying version (e.g., "2.1.0")
  - `--non-interactive`: Boolean flag (action='store_true')
- Modify main() function to check for non-interactive mode
- In non-interactive mode:
  - Skip all interactive prompts
  - Use provided version directly
  - Exit with error code 1 if version is invalid or missing
- Maintain backward compatibility - script works as before when no arguments provided

**Validation**:
- Test interactive mode still works: `python build/build.py`
- Test non-interactive mode: `python build/build.py --version 2.1.1 --non-interactive`
- Test error handling: `python build/build.py --non-interactive` (should fail with error)
- Verify artifacts are created correctly in both modes

**Expected Output**:
- Modified build/build.py with argparse support
- Script works in both interactive and non-interactive modes
- Clear error messages for invalid usage

---

## Prompt 2: Create GitHub Actions Release Workflow - Basic Structure

**Objective**: Create the foundation of the GitHub Actions workflow for automated releases when PRs merge to main.

**Context**: We need a GitHub Actions workflow that triggers when a PR is merged to the main branch. This workflow will orchestrate the entire release process. This is Phase 1: Basic Automation.

**Requirements**:
1. Create `.github/workflows/release.yml`
2. Configure workflow to trigger on PR merge to main branch only
3. Set up job with required permissions for creating releases and tags
4. Add steps for:
   - Checking out repository with full git history
   - Setting up Python 3.9+
   - Installing any required dependencies

**Implementation Details**:
- Create `.github/workflows/` directory if it doesn't exist
- Workflow trigger configuration:
  ```yaml
  on:
    pull_request:
      types: [closed]
      branches: [main]
  ```
- Job condition to only run on merged PRs (not just closed):
  ```yaml
  if: github.event.pull_request.merged == true
  ```
- Required permissions:
  ```yaml
  permissions:
    contents: write  # For creating releases, tags, and pushing commits
  ```
- Use `fetch-depth: 0` in checkout to get full git history for release notes
- Set up Python using actions/setup-python@v5

**Validation**:
- Workflow file has valid YAML syntax
- Workflow appears in GitHub Actions tab (after push)
- Conditional logic ensures it only runs on merged PRs

**Expected Output**:
- `.github/workflows/release.yml` file created
- Basic workflow structure in place
- Ready for adding release automation steps

---

## Prompt 3: Add Version Reading Step to Workflow

**Objective**: Add workflow steps to read the current version from manifest.json and validate it.

**Context**: The release workflow needs to read the version that the user has manually set in `.rdd/config/manifest.json`. This version will be used for creating the release tag and artifacts.

**Requirements**:
1. Add a workflow step that reads version from manifest.json
2. Store the version in a workflow output variable for use in subsequent steps
3. Add validation to ensure version format is valid (semantic versioning: X.Y.Z)
4. Add validation to ensure the version doesn't already have a git tag
5. Fail the workflow with a clear error if version is invalid or tag already exists

**Implementation Details**:
- Create a workflow step "Read and validate version"
- Use Python inline script to read manifest.json:
  ```python
  import json
  with open('.rdd/config/manifest.json', 'r') as f:
      manifest = json.load(f)
  version = manifest['framework']['version']
  ```
- Validate version format using regex: `^\d+\.\d+\.\d+$`
- Check if tag `v{version}` already exists:
  ```bash
  if git rev-parse "v${VERSION}" >/dev/null 2>&1; then
    echo "Error: Tag v${VERSION} already exists"
    exit 1
  fi
  ```
- Set output variable: `echo "version=$VERSION" >> $GITHUB_OUTPUT`
- Use step id to reference output: `id: read_version`

**Validation**:
- Version is correctly read from manifest.json
- Invalid version formats are rejected
- Duplicate tags are detected and cause workflow to fail
- Version is available to subsequent steps via `steps.read_version.outputs.version`

**Expected Output**:
- Workflow step that reads and validates version
- Version available as output variable
- Clear error messages for invalid versions or duplicate tags

---

## Prompt 4: Add Release Notes Validation Step

**Objective**: Add workflow step to validate that the required release notes file exists before proceeding with the release.

**Context**: Based on the manual release notes strategy (Q4 answer D), users must create a release notes file `build/release-notes-v{version}.md` before merging their PR. The workflow needs to validate this file exists.

**Requirements**:
1. Add a workflow step that checks for the existence of `build/release-notes-v{version}.md`
2. Read the release notes file content
3. Store the content in a workflow output variable for use in GitHub release
4. Fail the workflow with a clear error message if the file doesn't exist or is empty

**Implementation Details**:
- Create a workflow step "Validate release notes"
- Check file existence:
  ```bash
  RELEASE_NOTES_FILE="build/release-notes-v${{ steps.read_version.outputs.version }}.md"
  if [ ! -f "$RELEASE_NOTES_FILE" ]; then
    echo "Error: Release notes file not found: $RELEASE_NOTES_FILE"
    echo "Please create the release notes file before merging to main"
    exit 1
  fi
  ```
- Check file is not empty:
  ```bash
  if [ ! -s "$RELEASE_NOTES_FILE" ]; then
    echo "Error: Release notes file is empty: $RELEASE_NOTES_FILE"
    exit 1
  fi
  ```
- Read file content and store in output:
  ```bash
  RELEASE_NOTES=$(cat "$RELEASE_NOTES_FILE")
  echo "notes<<EOF" >> $GITHUB_OUTPUT
  echo "$RELEASE_NOTES" >> $GITHUB_OUTPUT
  echo "EOF" >> $GITHUB_OUTPUT
  ```
- Use step id: `id: validate_release_notes`

**Validation**:
- Workflow fails if release notes file is missing
- Workflow fails if release notes file is empty
- Release notes content is correctly stored in output variable
- Error messages clearly guide users on how to fix the issue

**Expected Output**:
- Workflow step that validates release notes file
- Release notes content available as output variable
- Clear error messages for missing or empty release notes

---

## Prompt 5: Add Build Artifacts Generation Step

**Objective**: Add workflow step to run the modified build.py script in non-interactive mode to generate release artifacts.

**Context**: The build.py script (modified in Prompt 1) needs to be executed to create the release zip file and SHA256 checksum. This must run in non-interactive mode using the version from manifest.json.

**Requirements**:
1. Add a workflow step that runs build.py in non-interactive mode
2. Pass the version from manifest.json to the build script
3. Verify that the expected artifacts are created:
   - `build/rdd-v{version}.zip`
   - `build/rdd-v{version}.zip.sha256`
4. Fail the workflow if artifacts are not created successfully

**Implementation Details**:
- Create a workflow step "Build release artifacts"
- Run build.py with non-interactive flag:
  ```bash
  python build/build.py --version ${{ steps.read_version.outputs.version }} --non-interactive
  ```
- Verify artifacts exist after build:
  ```bash
  VERSION=${{ steps.read_version.outputs.version }}
  if [ ! -f "build/rdd-v${VERSION}.zip" ]; then
    echo "Error: Build artifact not created: build/rdd-v${VERSION}.zip"
    exit 1
  fi
  if [ ! -f "build/rdd-v${VERSION}.zip.sha256" ]; then
    echo "Error: Checksum file not created: build/rdd-v${VERSION}.zip.sha256"
    exit 1
  fi
  ```
- Log artifact sizes and checksums for verification:
  ```bash
  ls -lh build/rdd-v${VERSION}.*
  cat build/rdd-v${VERSION}.zip.sha256
  ```

**Validation**:
- Build script runs successfully in CI environment
- Both artifacts (zip and sha256) are created
- Artifacts have expected content and valid checksums
- Workflow logs show artifact details

**Expected Output**:
- Workflow step that builds release artifacts
- Artifacts created in build/ directory
- Verification that artifacts are valid

---

## Prompt 6: Add Git Tag Creation Step

**Objective**: Add workflow step to create and push an annotated git tag for the release.

**Context**: After successfully building artifacts, we need to create a git tag following the format `v{version}` (e.g., v2.1.0). This tag will be used for the GitHub release.

**Requirements**:
1. Configure git user for the workflow
2. Create an annotated git tag with the release version
3. Push the tag to the repository
4. Include the release version in the tag message

**Implementation Details**:
- Create a workflow step "Create and push git tag"
- Configure git user (required for tag creation):
  ```bash
  git config user.name "github-actions[bot]"
  git config user.email "github-actions[bot]@users.noreply.github.com"
  ```
- Create annotated tag:
  ```bash
  VERSION=${{ steps.read_version.outputs.version }}
  git tag -a "v${VERSION}" -m "Release v${VERSION}"
  ```
- Push tag to remote:
  ```bash
  git push origin "v${VERSION}"
  ```
- Add error handling:
  ```bash
  if [ $? -ne 0 ]; then
    echo "Error: Failed to push tag v${VERSION}"
    exit 1
  fi
  ```

**Validation**:
- Annotated tag is created (not lightweight tag)
- Tag is pushed to the repository
- Tag message includes release version
- Tag is visible in GitHub tags UI

**Expected Output**:
- Git tag created and pushed to repository
- Tag follows naming convention v{version}
- Tag is annotated with release message

---

## Prompt 7: Add GitHub Release Creation Step

**Objective**: Add workflow step to create a GitHub release with the generated artifacts and release notes.

**Context**: After creating the git tag and building artifacts, we need to create a GitHub release that includes the zip file, checksum file, release notes file, and release notes as the description.

**Requirements**:
1. Use GitHub's official release action (softprops/action-gh-release)
2. Attach all three files to the release:
   - `build/rdd-v{version}.zip`
   - `build/rdd-v{version}.zip.sha256`
   - `build/release-notes-v{version}.md`
3. Use the release notes content as the release description
4. Mark the release as published (not draft)
5. Mark the release as a production release (not prerelease)

**Implementation Details**:
- Create a workflow step "Create GitHub Release"
- Use the softprops/action-gh-release@v1 action
- Configure the action:
  ```yaml
  - name: Create GitHub Release
    uses: softprops/action-gh-release@v1
    with:
      tag_name: v${{ steps.read_version.outputs.version }}
      name: Release v${{ steps.read_version.outputs.version }}
      body: ${{ steps.validate_release_notes.outputs.notes }}
      files: |
        build/rdd-v${{ steps.read_version.outputs.version }}.zip
        build/rdd-v${{ steps.read_version.outputs.version }}.zip.sha256
        build/release-notes-v${{ steps.read_version.outputs.version }}.md
      draft: false
      prerelease: false
  ```
- Ensure GITHUB_TOKEN is available (automatic in GitHub Actions)

**Validation**:
- GitHub release is created and visible in Releases page
- All three files are attached to the release
- Release notes appear in the description
- Release is marked as "Latest" (not draft or prerelease)
- Release has the correct tag association

**Expected Output**:
- Published GitHub release
- Release includes all artifacts
- Release notes are displayed in description
- Release is accessible via GitHub UI and API

---

## Prompt 8: Add Workflow Summary and Notification

**Objective**: Add a final workflow step that provides a summary of the release and optionally posts a comment on the PR.

**Context**: After successfully creating the release, it's helpful to provide a summary in the workflow output and optionally comment on the merged PR with release details.

**Requirements**:
1. Create a workflow step that generates a summary of the release
2. Output the summary to the GitHub Actions workflow summary
3. Optionally (if desired) post a comment on the PR with release details
4. Include in the summary:
   - Version released
   - Git tag created
   - Artifacts generated
   - Release URL

**Implementation Details**:
- Create a workflow step "Generate release summary"
- Generate summary:
  ```bash
  VERSION=${{ steps.read_version.outputs.version }}
  echo "## Release Summary" >> $GITHUB_STEP_SUMMARY
  echo "" >> $GITHUB_STEP_SUMMARY
  echo "✅ Successfully created release v${VERSION}" >> $GITHUB_STEP_SUMMARY
  echo "" >> $GITHUB_STEP_SUMMARY
  echo "### Details" >> $GITHUB_STEP_SUMMARY
  echo "- **Version**: v${VERSION}" >> $GITHUB_STEP_SUMMARY
  echo "- **Tag**: v${VERSION}" >> $GITHUB_STEP_SUMMARY
  echo "- **Artifacts**:" >> $GITHUB_STEP_SUMMARY
  echo "  - rdd-v${VERSION}.zip" >> $GITHUB_STEP_SUMMARY
  echo "  - rdd-v${VERSION}.zip.sha256" >> $GITHUB_STEP_SUMMARY
  echo "  - release-notes-v${VERSION}.md" >> $GITHUB_STEP_SUMMARY
  echo "- **Release URL**: https://github.com/${{ github.repository }}/releases/tag/v${VERSION}" >> $GITHUB_STEP_SUMMARY
  ```
- Optional: Add a step to comment on the PR using github-script action:
  ```yaml
  - name: Comment on PR
    uses: actions/github-script@v7
    with:
      script: |
        github.rest.issues.createComment({
          issue_number: context.payload.pull_request.number,
          owner: context.repo.owner,
          repo: context.repo.repo,
          body: '✅ Release v${{ steps.read_version.outputs.version }} created successfully!\n\n' +
                'View the release: https://github.com/${{ github.repository }}/releases/tag/v${{ steps.read_version.outputs.version }}'
        })
  ```

**Validation**:
- Workflow summary appears in Actions UI
- Summary includes all expected details
- PR comment appears if enabled
- Links in summary are clickable and valid

**Expected Output**:
- Clear workflow summary with release details
- Optional PR comment confirming release
- Easy access to release URL

---

## Prompt 9: Create Testing Workflow for Dev Branch

**Objective**: Create a separate testing workflow that runs on the dev branch to validate the release automation without creating actual releases.

**Context**: Before using the release workflow on the main branch, we need to test it safely. This testing workflow will run on dev branch merges and simulate the release process without creating actual releases or tags.

**Requirements**:
1. Create `.github/workflows/test-release.yml`
2. Configure to trigger on PR merges to dev branch
3. Run all the same steps as the release workflow
4. Do NOT create actual git tags or GitHub releases
5. Generate a summary showing what would have been released
6. Use the same validation checks to catch issues early

**Implementation Details**:
- Copy the structure from release.yml
- Change trigger to dev branch:
  ```yaml
  on:
    pull_request:
      types: [closed]
      branches: [dev]
  ```
- Keep all validation steps:
  - Read and validate version
  - Validate release notes exist
  - Build artifacts
- Replace tag/release creation with simulation:
  ```bash
  echo "TEST MODE: Would create tag v${VERSION}"
  echo "TEST MODE: Would create GitHub release"
  echo "TEST MODE: Would attach artifacts:"
  ls -lh build/rdd-v${VERSION}.*
  ```
- Generate test summary:
  ```bash
  echo "## Test Release Summary (DRY RUN)" >> $GITHUB_STEP_SUMMARY
  echo "" >> $GITHUB_STEP_SUMMARY
  echo "✅ Release automation test passed" >> $GITHUB_STEP_SUMMARY
  echo "" >> $GITHUB_STEP_SUMMARY
  echo "### What would be released:" >> $GITHUB_STEP_SUMMARY
  echo "- Version: v${VERSION}" >> $GITHUB_STEP_SUMMARY
  echo "- Tag: v${VERSION} (not created in test)" >> $GITHUB_STEP_SUMMARY
  echo "- Artifacts validated: ✓" >> $GITHUB_STEP_SUMMARY
  echo "- Release notes validated: ✓" >> $GITHUB_STEP_SUMMARY
  ```
- Add cleanup step to remove test artifacts if desired

**Validation**:
- Test workflow runs on dev branch merges
- All validation checks execute correctly
- No actual tags or releases are created
- Summary clearly indicates this is a test run
- Can validate workflow changes safely

**Expected Output**:
- `.github/workflows/test-release.yml` file
- Safe testing environment for workflow changes
- Clear indication of test vs production runs

---

## Prompt 10: Create Release Process Documentation

**Objective**: Create comprehensive documentation for the automated release process to guide developers on how to create releases.

**Context**: Developers need clear instructions on how to prepare for and trigger automated releases, what prerequisites are required, and how to troubleshoot issues.

**Requirements**:
1. Create or update documentation explaining the release process
2. Include prerequisites for creating a release
3. Explain the workflow steps
4. Provide troubleshooting guidance
5. Include examples of release notes format
6. Document how to test changes safely using the dev branch workflow

**Implementation Details**:
- Create `docs/RELEASE_PROCESS.md` or add section to existing README.md
- Document structure:
  
  **Prerequisites**:
  - Manual version update in `.rdd/config/manifest.json`
  - Creation of `build/release-notes-v{version}.md`
  - PR merged from dev to main (enforced by branch protection)
  
  **Release Workflow Steps**:
  1. Update version in manifest.json
  2. Create release notes file
  3. Test on dev branch (optional but recommended)
  4. Create PR from dev to main
  5. Merge PR - release is automatic
  6. Verify release created successfully
  
  **Release Notes Template**:
  ```markdown
  # Release Notes v{version}
  
  ## Summary
  Brief description of this release
  
  ## Key Changes
  - Feature 1
  - Feature 2
  - Bug fix 1
  
  ## Breaking Changes
  (if any)
  
  ## Migration Guide
  (if needed)
  ```
  
  **Testing on Dev Branch**:
  - Explain that merging to dev runs test-release.yml
  - Shows what would be released without creating actual release
  - Validates manifest version and release notes
  
  **Troubleshooting**:
  - Missing release notes file
  - Duplicate version/tag
  - Build failures
  - Permission issues
  - How to rollback failed release
  
  **Rollback Procedure**:
  ```bash
  # Delete release (if created)
  gh release delete v{version}
  
  # Delete tag
  git push --delete origin v{version}
  
  # Fix issues and retry
  ```

**Validation**:
- Documentation is clear and complete
- Examples are accurate and helpful
- Troubleshooting covers common issues
- Process is easy for developers to follow

**Expected Output**:
- Complete release process documentation
- Clear instructions for developers
- Troubleshooting guide
- Examples and templates

---

## Prompt 11: Create Release Validation Checklist

**Objective**: Create a checklist document that can be used to manually verify releases are working correctly.

**Context**: When first deploying the release automation, and periodically thereafter, it's important to validate that releases are created correctly and all components work as expected.

**Requirements**:
1. Create a validation checklist document
2. Include checks for all aspects of the release
3. Provide both automated and manual validation steps
4. Include verification commands where applicable

**Implementation Details**:
- Create `docs/RELEASE_VALIDATION.md`
- Structure the checklist:

  **Pre-Release Validation** (before merging to main):
  - [ ] Version number updated in `.rdd/config/manifest.json`
  - [ ] Version follows semantic versioning (X.Y.Z format)
  - [ ] Version doesn't conflict with existing tag
  - [ ] Release notes file created: `build/release-notes-v{version}.md`
  - [ ] Release notes are complete and accurate
  - [ ] All tests pass
  - [ ] Dev branch test workflow passed (if tested)
  
  **Post-Release Validation** (after workflow completes):
  - [ ] Git tag created: Verify with `git tag | grep v{version}`
  - [ ] GitHub release published: Check https://github.com/{org}/{repo}/releases
  - [ ] Release has correct version number
  - [ ] Release notes appear in description
  - [ ] All artifacts attached to release:
    - [ ] rdd-v{version}.zip
    - [ ] rdd-v{version}.zip.sha256
    - [ ] release-notes-v{version}.md
  - [ ] ZIP file is downloadable and extractable
  - [ ] SHA256 checksum is valid: `sha256sum -c rdd-v{version}.zip.sha256`
  - [ ] ZIP contains expected files (`.rdd/` folder and README.md)
  - [ ] Release is marked as "Latest"
  - [ ] Release is not marked as draft or prerelease
  
  **Artifact Integrity Checks**:
  ```bash
  # Download and verify release
  wget https://github.com/{org}/{repo}/releases/download/v{version}/rdd-v{version}.zip
  wget https://github.com/{org}/{repo}/releases/download/v{version}/rdd-v{version}.zip.sha256
  
  # Verify checksum
  sha256sum -c rdd-v{version}.zip.sha256
  
  # Extract and inspect
  unzip rdd-v{version}.zip -d test-extract/
  ls -la test-extract/
  ```
  
  **Workflow Validation**:
  - [ ] Workflow completed successfully
  - [ ] All workflow steps passed
  - [ ] No error messages in logs
  - [ ] Workflow summary generated
  - [ ] Execution time reasonable (< 10 minutes)

**Validation**:
- Checklist is comprehensive
- Commands are correct and helpful
- Can be used by any team member
- Covers both happy path and error scenarios

**Expected Output**:
- Complete validation checklist document
- Verification commands included
- Easy to follow step-by-step process

---

## Prompt 12: Add Error Handling and Retry Logic

**Objective**: Enhance the release workflow with robust error handling, clear error messages, and guidance for common failure scenarios.

**Context**: The release workflow can fail for various reasons (network issues, permission problems, etc.). We need to ensure failures are clear and provide actionable guidance for resolution.

**Requirements**:
1. Add error handling to each critical workflow step
2. Provide clear, actionable error messages
3. Add validation gates before destructive operations (tag creation, release publishing)
4. Include rollback instructions in failure scenarios
5. Consider adding retry logic for transient failures

**Implementation Details**:

- Enhance version validation with detailed error messages:
  ```bash
  if ! [[ "$VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "❌ ERROR: Invalid version format in manifest.json: $VERSION"
    echo "Expected format: X.Y.Z (e.g., 2.1.0)"
    echo "Please update .rdd/config/manifest.json with a valid semantic version"
    exit 1
  fi
  ```

- Add artifact validation with helpful errors:
  ```bash
  if [ ! -f "build/rdd-v${VERSION}.zip" ]; then
    echo "❌ ERROR: Build failed - artifact not created"
    echo "Expected: build/rdd-v${VERSION}.zip"
    echo "Check build.py output above for errors"
    echo ""
    echo "Common causes:"
    echo "- Python dependencies missing"
    echo "- File permissions issue"
    echo "- Insufficient disk space"
    exit 1
  fi
  ```

- Add tag conflict detection with rollback guidance:
  ```bash
  if git rev-parse "v${VERSION}" >/dev/null 2>&1; then
    echo "❌ ERROR: Tag v${VERSION} already exists"
    echo ""
    echo "This means a release for v${VERSION} already exists."
    echo ""
    echo "To fix:"
    echo "1. If this is a duplicate, increment version in manifest.json"
    echo "2. If previous release was bad and needs replacement:"
    echo "   - Delete the release: gh release delete v${VERSION}"
    echo "   - Delete the tag: git push --delete origin v${VERSION}"
    echo "   - Re-run this workflow"
    exit 1
  fi
  ```

- Add release notes validation with helpful guidance:
  ```bash
  NOTES_FILE="build/release-notes-v${VERSION}.md"
  if [ ! -f "$NOTES_FILE" ]; then
    echo "❌ ERROR: Release notes file not found"
    echo "Expected file: $NOTES_FILE"
    echo ""
    echo "To fix:"
    echo "1. Create $NOTES_FILE with your release notes"
    echo "2. Commit and push the file"
    echo "3. Re-merge the PR to main"
    exit 1
  fi
  ```

- Add GitHub release creation error handling:
  ```yaml
  - name: Create GitHub Release
    id: create_release
    uses: softprops/action-gh-release@v1
    continue-on-error: true
    with:
      # ... existing configuration ...
  
  - name: Check release creation
    if: steps.create_release.outcome == 'failure'
    run: |
      echo "❌ ERROR: Failed to create GitHub release"
      echo ""
      echo "Possible causes:"
      echo "- Network connectivity issue"
      echo "- Insufficient permissions"
      echo "- Release with this tag already exists"
      echo ""
      echo "The git tag v${VERSION} was created."
      echo "To retry: Delete the tag and re-run"
      echo "  git push --delete origin v${VERSION}"
      exit 1
  ```

- Add a final validation step:
  ```bash
  # Verify release was created
  if ! gh release view "v${VERSION}" >/dev/null 2>&1; then
    echo "❌ ERROR: Release verification failed"
    echo "Tag was created but release is not visible"
    echo "This may resolve in a few moments (GitHub propagation)"
    echo "If persists, check GitHub UI manually"
    exit 1
  fi
  ```

**Validation**:
- Each failure scenario has clear error message
- Error messages include actionable steps to fix
- Workflow fails fast on critical errors
- Rollback instructions are provided where applicable

**Expected Output**:
- Enhanced workflow with robust error handling
- Clear, helpful error messages
- Guidance for resolution of common issues

---

## Prompt 13: Update .gitignore for Build Artifacts

**Objective**: Ensure the .gitignore file is properly configured to handle the build artifacts and test files created during the release process.

**Context**: The release workflow creates build artifacts that should be tracked in git (release notes) and some that might be temporary (test extractions). We need to ensure .gitignore is configured appropriately.

**Requirements**:
1. Review current .gitignore file
2. Ensure release notes files are NOT ignored (they should be committed)
3. Ensure temporary test artifacts are ignored
4. Keep the release package files (.zip and .sha256) tracked in git (they're intentionally committed)
5. Add any new temporary files created by the workflows

**Implementation Details**:

- Check if .gitignore exists in the root directory
- Review current ignore patterns
- Verify that `build/release-notes-*.md` files are NOT ignored
- Verify that `build/rdd-v*.zip` and `build/rdd-v*.zip.sha256` are NOT ignored (if they are meant to be committed)
- Add ignore patterns for any test artifacts:
  ```
  # Release testing artifacts
  test-extract/
  *.download
  ```
- Add ignore patterns for Python cache if not already present:
  ```
  __pycache__/
  *.pyc
  *.pyo
  ```
- Ensure .github/workflows/ is NOT ignored (workflows must be committed)

**Note**: Based on the existing files-and-folders.md, it appears that release packages are stored in the build/ directory and should be committed to git. Verify this is the intended behavior.

**Validation**:
- .gitignore doesn't block required files
- Temporary files are properly ignored
- Workflow files are not ignored
- Release artifacts follow intended policy

**Expected Output**:
- Updated .gitignore file (if changes needed)
- Documentation of what is/isn't ignored and why

---

## Prompt 14: Create GitHub Branch Protection Rules Documentation

**Objective**: Document the recommended GitHub branch protection rules for the main and dev branches to ensure the release workflow works correctly and safely.

**Context**: The release automation assumes certain branch protection rules are in place (e.g., only dev can merge to main). These rules should be documented so teams can configure their repositories correctly.

**Requirements**:
1. Create documentation for required branch protection settings
2. Include settings for both main and dev branches
3. Explain why each setting is important
4. Provide instructions for configuring via GitHub UI
5. Include API/terraform examples for automated setup

**Implementation Details**:

- Create `docs/BRANCH_PROTECTION.md` or add section to main documentation
- Document required settings:

  **Main Branch Protection** (critical for release automation):
  - **Require pull request before merging**: ✅ Enabled
    - Reason: Triggers the release workflow
  - **Require approvals**: Recommended (1 or more)
  - **Dismiss stale reviews**: Recommended
  - **Require review from code owners**: Optional
  - **Require status checks to pass**: ✅ Enabled
    - Required checks: Any test workflows, build validation
  - **Require branches to be up to date**: ✅ Enabled
  - **Require conversation resolution**: Recommended
  - **Require linear history**: Optional
  - **Include administrators**: Recommended
  - **Restrict who can push**: ✅ Critical
    - Only allow: dev branch (enforces dev → main flow)
    - Block direct pushes
  - **Allow force pushes**: ❌ Disabled
  - **Allow deletions**: ❌ Disabled
  
  **Dev Branch Protection** (recommended):
  - **Require pull request before merging**: ✅ Enabled
  - **Require status checks to pass**: ✅ Enabled
  - **Allow force pushes**: ❌ Disabled (recommended)

- Provide GitHub UI configuration steps:
  ```
  1. Go to repository Settings
  2. Click "Branches" in left sidebar
  3. Click "Add branch protection rule"
  4. Enter "main" as branch name pattern
  5. Configure settings as documented above
  6. Click "Create" or "Save changes"
  7. Repeat for "dev" branch
  ```

- Provide API example for automation:
  ```bash
  # Using GitHub CLI
  gh api repos/{owner}/{repo}/branches/main/protection \
    --method PUT \
    --field required_pull_request_reviews[required_approving_review_count]=1 \
    --field enforce_admins=true \
    --field restrictions[users][]=dev
  ```

- Include tag protection settings:
  ```
  Tag Protection Rules:
  - Pattern: v*
  - Prevent tag deletion: ✅
  - Prevent tag updates: ✅
  ```

**Validation**:
- Documentation is clear and complete
- Settings align with workflow requirements
- Configuration steps are accurate
- API examples work correctly

**Expected Output**:
- Complete branch protection documentation
- Configuration instructions for GitHub UI
- API/automation examples
- Tag protection guidance

---

## Prompt 15: Create Release Workflow Testing Guide

**Objective**: Create a comprehensive guide for testing the release workflow end-to-end before using it in production.

**Context**: Before trusting the release automation on the main branch, teams should test it thoroughly on the dev branch. This guide provides a step-by-step testing procedure.

**Requirements**:
1. Create a testing guide for the release workflow
2. Include setup instructions
3. Provide step-by-step test scenarios
4. Include both success and failure scenarios
5. Document expected outcomes for each test

**Implementation Details**:

- Create `docs/RELEASE_WORKFLOW_TESTING.md`
- Structure the guide:

  **Setup for Testing**:
  1. Ensure test-release.yml workflow is deployed to dev branch
  2. Create a test feature branch from dev
  3. Prepare test version and release notes
  
  **Test Scenario 1: Successful Release (Happy Path)**:
  ```
  Step 1: Update version
  - Edit .rdd/config/manifest.json
  - Change version to a test version (e.g., "2.1.99-test1")
  
  Step 2: Create release notes
  - Create build/release-notes-v2.1.99-test1.md
  - Add sample content
  
  Step 3: Commit and push
  - git add .rdd/config/manifest.json build/release-notes-v2.1.99-test1.md
  - git commit -m "test: Prepare test release 2.1.99-test1"
  - git push
  
  Step 4: Create PR to dev
  - Create PR from feature branch to dev
  - Merge the PR
  
  Step 5: Verify workflow
  - Check GitHub Actions tab
  - Verify test-release.yml runs
  - Check workflow summary
  - Verify artifacts are built
  - Confirm NO tag or release is created
  
  Expected Outcome:
  ✅ Workflow completes successfully
  ✅ Artifacts are validated
  ✅ No actual release created
  ✅ Summary shows "would create release"
  ```
  
  **Test Scenario 2: Missing Release Notes**:
  ```
  Step 1: Update version only
  - Edit manifest.json with new version
  - Do NOT create release notes file
  
  Step 2: Create PR and merge
  
  Expected Outcome:
  ❌ Workflow fails at "Validate release notes" step
  ❌ Clear error message about missing file
  ✅ No artifacts created
  ```
  
  **Test Scenario 3: Invalid Version Format**:
  ```
  Step 1: Set invalid version
  - Edit manifest.json
  - Set version to "2.1" (missing patch)
  
  Step 2: Create release notes and merge
  
  Expected Outcome:
  ❌ Workflow fails at version validation
  ❌ Error message explains valid format
  ✅ No artifacts created
  ```
  
  **Test Scenario 4: Build Failure**:
  ```
  Step 1: Temporarily break build.py
  - Add syntax error or import error
  
  Step 2: Prepare valid version and notes
  
  Step 3: Merge PR
  
  Expected Outcome:
  ❌ Workflow fails at build step
  ❌ Build error shown in logs
  ✅ No tag created
  ```
  
  **Test Scenario 5: Production Test (Final Validation)**:
  ```
  Only after all dev tests pass!
  
  Step 1: Prepare real release
  - Update to real version number
  - Create proper release notes
  
  Step 2: Create PR from dev to main
  
  Step 3: Merge PR to main
  
  Step 4: Monitor release.yml workflow
  
  Expected Outcome:
  ✅ Workflow completes successfully
  ✅ Git tag created
  ✅ GitHub release published
  ✅ All artifacts attached
  ✅ Release notes appear correctly
  ```
  
  **Cleanup After Testing**:
  ```bash
  # Remove test artifacts
  rm build/rdd-v2.1.99-test*.zip
  rm build/rdd-v2.1.99-test*.zip.sha256
  rm build/release-notes-v2.1.99-test*.md
  
  # Restore manifest version
  # Edit .rdd/config/manifest.json back to production version
  ```

**Validation**:
- Test guide is clear and detailed
- All scenarios are realistic
- Expected outcomes are documented
- Can be followed by any team member

**Expected Output**:
- Comprehensive testing guide
- Multiple test scenarios
- Clear expected outcomes
- Cleanup instructions

---

## Prompt 16: Final Integration and Documentation Review

**Objective**: Review all components of the release automation system, ensure they work together correctly, and finalize all documentation.

**Context**: All individual pieces have been created. This final step ensures everything is integrated correctly, documentation is complete, and the system is ready for production use.

**Requirements**:
1. Review all created files and workflows
2. Verify integration between components
3. Check for consistency across documentation
4. Create a final README or update existing README with release automation section
5. Verify all documentation is linked correctly
6. Create a quick reference guide

**Implementation Details**:

**Files Review Checklist**:
- [ ] build/build.py - Modified with --version and --non-interactive flags
- [ ] .github/workflows/release.yml - Production release workflow
- [ ] .github/workflows/test-release.yml - Testing workflow for dev branch
- [ ] docs/RELEASE_PROCESS.md - Developer guide for creating releases
- [ ] docs/RELEASE_VALIDATION.md - Validation checklist
- [ ] docs/BRANCH_PROTECTION.md - Branch protection configuration
- [ ] docs/RELEASE_WORKFLOW_TESTING.md - Testing guide
- [ ] .gitignore - Properly configured
- [ ] README.md - Updated with release automation section

**Integration Verification**:
1. Verify workflow files reference correct script paths
2. Check version references are consistent
3. Ensure documentation cross-references are correct
4. Verify file paths in examples match actual structure
5. Check that all shell commands in docs are correct

**Documentation Structure**:
```
README.md (add section)
├── Release Automation
    ├── Overview
    ├── Quick Start
    └── Links to detailed docs

docs/
├── RELEASE_PROCESS.md - How to create releases
├── RELEASE_VALIDATION.md - How to validate releases
├── BRANCH_PROTECTION.md - Required GitHub settings
└── RELEASE_WORKFLOW_TESTING.md - How to test the automation
```

**Quick Reference Guide** (add to README.md):
```markdown
## Release Automation Quick Reference

### Creating a Release

1. **Update Version**: Edit `.rdd/config/manifest.json`
   ```json
   "version": "2.2.0"
   ```

2. **Create Release Notes**: Create `build/release-notes-v2.2.0.md`

3. **Test (Optional)**: Merge to dev first to run test workflow

4. **Release**: Create PR from dev to main and merge

5. **Verify**: Check GitHub Releases page

### Troubleshooting

- **Workflow failed**: Check GitHub Actions logs
- **Version conflict**: Ensure version doesn't exist as a tag
- **Missing release notes**: Create the file and re-merge

For details, see:
- [Release Process](docs/RELEASE_PROCESS.md)
- [Validation Checklist](docs/RELEASE_VALIDATION.md)
- [Testing Guide](docs/RELEASE_WORKFLOW_TESTING.md)
```

**Final Checks**:
- All documentation uses consistent terminology
- All file paths are correct
- All code examples are tested and working
- All links are valid
- Documentation is clear for new team members
- No TODO or placeholder text remains

**Create Summary Document**:
- Create `docs/RELEASE_AUTOMATION_SUMMARY.md` that provides:
  - Overview of the entire system
  - Architecture diagram (text-based)
  - Component list with descriptions
  - Links to all documentation
  - Maintenance notes
  - Future enhancement ideas

**Validation**:
- All documentation is complete
- Integration between components works
- Documentation is clear and helpful
- System is ready for production use

**Expected Output**:
- Complete, integrated release automation system
- Comprehensive documentation
- Quick reference guide
- System ready for production deployment

---

## Summary

This release automation implementation includes:

**Core Components**:
1. Modified build.py with CI/CD support (Prompt 1)
2. GitHub Actions release workflow (Prompts 2-7)
3. Workflow notifications and summaries (Prompt 8)
4. Testing workflow for safe validation (Prompt 9)
5. Error handling and rollback guidance (Prompt 12)

**Documentation**:
6. Release process guide (Prompt 10)
7. Validation checklist (Prompt 11)
8. Branch protection configuration (Prompt 14)
9. Testing guide (Prompt 15)
10. Final integration review (Prompt 16)

**Infrastructure**:
11. .gitignore configuration (Prompt 13)

**Execution Strategy**:
- Execute prompts sequentially in order
- Test each component before proceeding to next
- Use dev branch for safe testing (Prompt 9)
- Validate with test scenarios (Prompt 15)
- Final production test on main branch (Prompt 16)

**Key Design Decisions** (from questionnaire):
- Complete end-to-end implementation (all phases)
- Modify existing build.py (not creating new script)
- Manual version management (user updates manifest.json)
- Manual release notes (user creates file before merge)
- Include testing strategy with dev branch
- Sequential numbered prompt format

**Total Effort Estimate**: 3-5 days for complete implementation

This prompt sequence provides a complete, production-ready release automation system for the RDD Framework.
