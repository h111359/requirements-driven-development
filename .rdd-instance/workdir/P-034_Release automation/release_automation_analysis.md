# Release Automation Analysis

## Executive Summary

This document analyzes options for automating the RDD Framework release process when a PR is merged to the `main` branch. The analysis covers:

1. Current manual release process
2. Automation strategy and options
3. Version management from manifest.json
4. Git tagging strategy
5. Release notes generation best practices
6. GitHub Actions workflow design
7. Implementation recommendations

---

## 1. Current Manual Release Process

### Current State

The RDD Framework currently uses a **manual release process** centered around the `build/build.py` script:

**Process Steps:**
1. Developer manually decides to create a release
2. Run `python build/build.py` locally
3. Script reads version from `.rdd/config/manifest.json`
4. Interactive prompts for version selection and conflict resolution
5. Creates build artifacts:
   - `build/rdd-v{version}.zip` - Archive containing `.rdd/` folder and `README.md`
   - `build/rdd-v{version}.zip.sha256` - Checksum file for integrity verification
6. Developer manually creates GitHub release
7. Developer manually attaches zip and sha256 files
8. Developer manually creates/copies release notes

**Version Source:**
- `.rdd/config/manifest.json` → `framework.version` field (currently "2.1.0")

**Artifacts Location:**
- Build artifacts stored in `build/` folder
- Release notes stored as `build/release-notes-v{version}.md`

**Existing Infrastructure:**
- GitHub Actions workflows exist: `tests.yml`, `main-pr-restriction.yml`
- Git tags follow semantic versioning: `v{major}.{minor}.{patch}` (e.g., v2.0.1)
- Branching strategy: feature branches → `dev` → `main`
- Restriction enforced: only `dev` can merge to `main`

---

## 2. Automation Strategy and Options

### Recommended Approach: **Trigger on PR Merge to Main**

**Rationale:**
- Aligns with existing branching strategy (only `dev` merges to `main`)
- Main branch serves as production/release branch
- Every merge to main represents a releasable state
- Simpler than managing separate release branches

### Trigger Options Analysis

| Option | Description | Pros | Cons | Recommendation |
|--------|-------------|------|------|----------------|
| **1. PR Merge to Main** | Automatically create release when PR merges to main | • Automatic<br>• Aligns with workflow<br>• No manual intervention | • Every merge creates release<br>• Need version bump discipline | ✅ **RECOMMENDED** |
| **2. Manual Workflow Dispatch** | Developer triggers release via GitHub Actions UI | • Full control<br>• Can batch changes | • Manual step required<br>• Can forget to release | ❌ Not recommended |
| **3. Git Tag Push** | Create release when version tag pushed | • Explicit version control<br>• Flexible timing | • Extra manual step<br>• Tag conflicts | ❌ Not recommended |
| **4. Release Branch** | Dedicated release branch triggers automation | • Clear separation<br>• Can stage releases | • Extra branch complexity<br>• Conflicts with current flow | ❌ Not recommended |

### Version Increment Strategy

**Recommended: Automated Patch Increment with Manual Override**

```yaml
Strategy:
1. Default: Auto-increment patch version on each main merge
   - Before merge: 2.1.0
   - After merge: 2.1.1
   
2. Manual override via commit message keywords:
   - "[minor]" → increment minor (2.1.0 → 2.2.0)
   - "[major]" → increment major (2.1.0 → 3.0.0)
   - "[version:X.Y.Z]" → set specific version
   
3. Update manifest.json automatically in the release workflow
```

**Alternative Approaches:**

| Approach | Description | Pros | Cons |
|----------|-------------|------|------|
| **Pre-merge Version Bump** | Version updated in PR before merge | • Explicit<br>• Version in commit | • Manual step<br>• Can forget |
| **Semantic Commit Analysis** | Parse commit messages (feat/fix/BREAKING) | • Fully automatic<br>• Conventional commits | • Requires discipline<br>• Complex parsing |
| **Manual Workflow Input** | Specify version when triggering | • Full control | • Manual process |

---

## 3. Version Management from manifest.json

### Current Structure

File: `.rdd/config/manifest.json`
```json
{
  "framework": {
    "name": "RDD Framework",
    "version": "2.1.0",
    "description": "Requirements-Driven Development framework..."
  }
}
```

### Automation Considerations

**Reading Version:**
```python
import json

def get_current_version():
    with open('.rdd/config/manifest.json', 'r') as f:
        manifest = json.load(f)
    return manifest['framework']['version']
```

**Updating Version:**
```python
def update_version(new_version):
    with open('.rdd/config/manifest.json', 'r') as f:
        manifest = json.load(f)
    
    manifest['framework']['version'] = new_version
    
    with open('.rdd/config/manifest.json', 'w') as f:
        json.dump(manifest, f, indent=2)
```

**Version Increment Logic:**
```python
def increment_version(version, increment_type='patch'):
    major, minor, patch = map(int, version.split('.'))
    
    if increment_type == 'major':
        return f"{major + 1}.0.0"
    elif increment_type == 'minor':
        return f"{major}.{minor + 1}.0"
    else:  # patch
        return f"{major}.{minor}.{patch + 1}"
```

### Integration with GitHub Actions

**Approach 1: Version Bump Committed to Main**
```yaml
- Check out main branch
- Read current version from manifest.json
- Increment version
- Update manifest.json
- Commit and push to main
- Create release with new version
```

**Pros:** Version history in git
**Cons:** Creates extra commit on main after merge

**Approach 2: Version Bump in Tag/Release Only**
```yaml
- Read current version from manifest.json
- Increment version
- Create release and tag with new version
- Build uses version from manifest (unchanged)
- Next PR must update manifest version
```

**Pros:** No extra commits
**Cons:** Manifest and release version can diverge

**Recommendation:** Use **Approach 1** with automatic commit to keep manifest.json synchronized.

---

## 4. Git Tagging Strategy

### Current Tag Format

Existing tags follow semantic versioning:
```
v0.1.0
v1.0.0
v1.0.1
v1.0.2
...
v2.0.0
v2.0.1
v2.1.0 (next expected)
```

Format: `v{major}.{minor}.{patch}`

### Automation Implementation

**Tag Creation in GitHub Actions:**
```yaml
- name: Create and push tag
  run: |
    git config user.name "github-actions[bot]"
    git config user.email "github-actions[bot]@users.noreply.github.com"
    git tag -a "v${{ env.VERSION }}" -m "Release v${{ env.VERSION }}"
    git push origin "v${{ env.VERSION }}"
```

**Tag Validation:**
```bash
# Check if tag already exists
if git rev-parse "v${VERSION}" >/dev/null 2>&1; then
  echo "Tag v${VERSION} already exists"
  exit 1
fi
```

**Best Practices:**
1. **Annotated tags** (not lightweight) - Include release metadata
2. **Consistent format** - Always `v{major}.{minor}.{patch}`
3. **Atomic creation** - Tag creation fails if already exists
4. **Protected tags** - Configure GitHub to protect release tags from deletion

---

## 5. Release Notes Generation Best Practices

### Current State

Release notes are manually created in `build/release-notes-v{version}.md` with structure:
```markdown
# Release Notes v{version}

## Branch Included
- `branch-name`

## Key Changes, Enhancements, and Fixes
- Feature descriptions
- Bug fixes
- Improvements
```

### Automation Options

#### Option 1: Git Commit History Analysis ✅ RECOMMENDED

**Implementation:**
```bash
# Get commits since last tag
git log v2.0.1..HEAD --oneline --no-merges

# Get merged branches
git log v2.0.1..HEAD --merges --pretty=format:"%s"

# Get PR information (if available)
git log v2.0.1..HEAD --merges --pretty=format:"%b" | grep "Merge pull request"
```

**Advantages:**
- Fully automated
- Based on actual changes
- No manual intervention

**Implementation Details:**
```python
import subprocess
import re

def get_commits_since_tag(last_tag):
    cmd = f"git log {last_tag}..HEAD --oneline --no-merges"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip().split('\n')

def get_merged_prs(last_tag):
    cmd = f"git log {last_tag}..HEAD --merges --pretty=format:'%s'"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    prs = []
    for line in result.stdout.strip().split('\n'):
        match = re.search(r'Merge pull request #(\d+)', line)
        if match:
            prs.append(match.group(1))
    return prs
```

#### Option 2: Conventional Commits Parsing

**Format:**
```
feat: Add new feature
fix: Fix bug
docs: Update documentation
chore: Update dependencies
```

**Parser:**
```python
def parse_conventional_commits(commits):
    categories = {
        'Features': [],
        'Bug Fixes': [],
        'Documentation': [],
        'Other': []
    }
    
    for commit in commits:
        if commit.startswith('feat'):
            categories['Features'].append(commit)
        elif commit.startswith('fix'):
            categories['Bug Fixes'].append(commit)
        elif commit.startswith('docs'):
            categories['Documentation'].append(commit)
        else:
            categories['Other'].append(commit)
    
    return categories
```

#### Option 3: RDD Framework Workdir Analysis ⭐ OPTIMAL FOR RDD

**Unique Advantage:** RDD maintains detailed work iteration documentation

**Source Locations:**
```
.rdd-instance/workdir/
├── P-XXX_prompt-title/
│   ├── prompt.md                 # Original prompt
│   ├── implementation.md         # Implementation details
│   ├── questionnaire.json        # Decisions made
│   └── modifications-log.json    # Modification history
└── prompts-registry.md           # All prompts overview
```

**Implementation:**
```python
import json
import os

def extract_release_notes_from_workdir(since_commit):
    """Extract release notes from RDD workdir based on commits"""
    
    # Get list of changed prompts since last release
    cmd = f"git diff --name-only {since_commit}..HEAD .rdd-instance/workdir/"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    changed_prompts = set()
    for line in result.stdout.strip().split('\n'):
        match = re.search(r'P-(\d+)_(.+?)/', line)
        if match:
            changed_prompts.add((match.group(1), match.group(2)))
    
    # Read implementation details for each prompt
    features = []
    for prompt_id, prompt_title in changed_prompts:
        impl_path = f".rdd-instance/workdir/P-{prompt_id}_{prompt_title}/implementation.md"
        if os.path.exists(impl_path):
            with open(impl_path, 'r') as f:
                content = f.read()
                # Extract key changes from implementation
                features.append({
                    'prompt_id': prompt_id,
                    'title': prompt_title,
                    'details': content
                })
    
    return features
```

**Advantages:**
- Leverages RDD's rich metadata
- Detailed implementation context
- Prompt titles are meaningful feature names
- Implementation files contain detailed rationale

### Recommended Hybrid Approach

**Combine:**
1. **Git commit history** - For commit messages and PR numbers
2. **RDD workdir analysis** - For detailed feature descriptions
3. **Prompt registry** - For prompt titles and metadata

**Generated Release Notes Structure:**
```markdown
# Release Notes v{version}

## Summary
{Auto-generated summary of changes}

## Features and Enhancements
{List from completed prompts in this release}

## Bug Fixes
{List from fix-type commits}

## Prompts Completed
{List of RDD prompts from workdir}

## Commits
{Detailed commit list}

## Technical Changes
{From implementation.md files}
```

### Storage and Persistence

**Option 1: File in Repository** ✅ RECOMMENDED
- Store as `build/release-notes-v{version}.md`
- Commit to repository
- Include in release assets

**Option 2: GitHub Release Notes Only**
- Only in GitHub release description
- Not in repository
- Harder to track historically

**Option 3: Dual Storage** ⭐ OPTIMAL
- Store in repository (`build/release-notes-v{version}.md`)
- Also populate GitHub release description
- Best of both worlds

---

## 6. GitHub Actions Workflow Design

### Recommended Workflow Structure

**File:** `.github/workflows/release.yml`

```yaml
name: Create Release

on:
  pull_request:
    types: [closed]
    branches: [main]

jobs:
  create-release:
    # Only run if PR was merged (not closed without merge)
    if: github.event.pull_request.merged == true
    runs-on: ubuntu-latest
    
    permissions:
      contents: write  # Required for creating releases and tags
      
    steps:
      # 1. Checkout code
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Full history for git operations
      
      # 2. Set up Python
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.9'
      
      # 3. Get current version and determine increment type
      - name: Determine version increment
        id: version
        run: |
          # Read current version from manifest
          CURRENT_VERSION=$(python -c "import json; print(json.load(open('.rdd/config/manifest.json'))['framework']['version'])")
          echo "current=$CURRENT_VERSION" >> $GITHUB_OUTPUT
          
          # Check PR title/body for version increment hints
          PR_BODY="${{ github.event.pull_request.body }}"
          if [[ "$PR_BODY" == *"[major]"* ]]; then
            INCREMENT="major"
          elif [[ "$PR_BODY" == *"[minor]"* ]]; then
            INCREMENT="minor"
          else
            INCREMENT="patch"
          fi
          echo "increment=$INCREMENT" >> $GITHUB_OUTPUT
          
          # Calculate new version
          IFS='.' read -r -a VERSION_PARTS <<< "$CURRENT_VERSION"
          MAJOR="${VERSION_PARTS[0]}"
          MINOR="${VERSION_PARTS[1]}"
          PATCH="${VERSION_PARTS[2]}"
          
          if [ "$INCREMENT" == "major" ]; then
            NEW_VERSION="$((MAJOR + 1)).0.0"
          elif [ "$INCREMENT" == "minor" ]; then
            NEW_VERSION="$MAJOR.$((MINOR + 1)).0"
          else
            NEW_VERSION="$MAJOR.$MINOR.$((PATCH + 1))"
          fi
          
          echo "new=$NEW_VERSION" >> $GITHUB_OUTPUT
          echo "New version will be: $NEW_VERSION"
      
      # 4. Update manifest.json with new version
      - name: Update manifest version
        run: |
          python -c "
          import json
          with open('.rdd/config/manifest.json', 'r') as f:
              manifest = json.load(f)
          manifest['framework']['version'] = '${{ steps.version.outputs.new }}'
          with open('.rdd/config/manifest.json', 'w') as f:
              json.dump(manifest, f, indent=2)
          "
      
      # 5. Generate release notes
      - name: Generate release notes
        id: release_notes
        run: |
          # Find last tag
          LAST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "")
          
          if [ -z "$LAST_TAG" ]; then
            echo "No previous tag found, using all commits"
            COMMIT_RANGE="HEAD"
          else
            COMMIT_RANGE="$LAST_TAG..HEAD"
          fi
          
          # Create release notes file
          cat > "build/release-notes-v${{ steps.version.outputs.new }}.md" << 'EOF'
          # Release Notes v${{ steps.version.outputs.new }}
          
          ## Changes Since $LAST_TAG
          
          ### Commits
          EOF
          
          # Add commits
          git log $COMMIT_RANGE --oneline --no-merges >> "build/release-notes-v${{ steps.version.outputs.new }}.md"
          
          # Set output for GitHub release body
          RELEASE_BODY=$(cat "build/release-notes-v${{ steps.version.outputs.new }}.md")
          echo "body<<EOF" >> $GITHUB_OUTPUT
          echo "$RELEASE_BODY" >> $GITHUB_OUTPUT
          echo "EOF" >> $GITHUB_OUTPUT
      
      # 6. Run build script
      - name: Build release artifacts
        run: |
          # The build.py script needs to be non-interactive for CI
          # This may require modifications to build.py or a separate CI mode
          python build/build.py --version ${{ steps.version.outputs.new }} --non-interactive
      
      # 7. Commit version bump and release notes
      - name: Commit version changes
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add .rdd/config/manifest.json
          git add "build/release-notes-v${{ steps.version.outputs.new }}.md"
          git commit -m "chore: Bump version to ${{ steps.version.outputs.new }}"
          git push
      
      # 8. Create and push tag
      - name: Create tag
        run: |
          git tag -a "v${{ steps.version.outputs.new }}" -m "Release v${{ steps.version.outputs.new }}"
          git push origin "v${{ steps.version.outputs.new }}"
      
      # 9. Create GitHub release
      - name: Create GitHub Release
        uses: softprops/action-gh-release@v1
        with:
          tag_name: v${{ steps.version.outputs.new }}
          name: Release v${{ steps.version.outputs.new }}
          body: ${{ steps.release_notes.outputs.body }}
          files: |
            build/rdd-v${{ steps.version.outputs.new }}.zip
            build/rdd-v${{ steps.version.outputs.new }}.zip.sha256
            build/release-notes-v${{ steps.version.outputs.new }}.md
          draft: false
          prerelease: false
```

### Required Modifications to build.py

**Current Issue:** `build.py` is interactive (prompts for version selection)

**Required Changes:**
```python
def main():
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', help='Version to build')
    parser.add_argument('--non-interactive', action='store_true', 
                       help='Run in non-interactive mode for CI')
    args = parser.parse_args()
    
    if args.non_interactive and not args.version:
        print_error("--version required in non-interactive mode")
        sys.exit(1)
    
    if args.non_interactive:
        version = args.version
        # Skip all prompts
    else:
        # Existing interactive logic
        ...
```

### Workflow Triggers and Conditions

**Current Implementation:**
```yaml
on:
  pull_request:
    types: [closed]
    branches: [main]

jobs:
  create-release:
    if: github.event.pull_request.merged == true
```

**Why This Works:**
- Triggers when PR to main is closed
- Only runs if PR was merged (not just closed)
- Aligns with existing restriction: only `dev` can merge to main

**Alternative Triggers:**

| Trigger | When | Pros | Cons |
|---------|------|------|------|
| `push` to main | On every push to main | Simple | Runs on direct pushes |
| `pull_request.closed` + merged check | PR merged | Precise | More complex condition |
| `workflow_dispatch` | Manual trigger | Full control | Manual process |
| `release.published` | After release created | Post-release tasks | Not for creation |

---

## 7. Implementation Recommendations

### Phased Rollout Approach

#### Phase 1: Basic Automation ✅ Start Here
**Goal:** Automate basic release creation

**Tasks:**
1. Create `.github/workflows/release.yml`
2. Implement automatic version increment (patch only)
3. Run existing `build.py` in non-interactive mode
4. Create GitHub release with artifacts
5. Auto-generate basic release notes from commits

**Deliverables:**
- Working GitHub Actions workflow
- Automatic releases on main merge
- Build artifacts attached to releases

**Effort:** 1-2 days

#### Phase 2: Enhanced Release Notes ⭐
**Goal:** Leverage RDD workdir for rich release notes

**Tasks:**
1. Create Python script to analyze workdir changes
2. Extract prompt titles and implementation details
3. Categorize changes by prompt type
4. Generate structured release notes

**Deliverables:**
- Detailed release notes with RDD context
- Prompt-based change categorization
- Implementation summaries

**Effort:** 2-3 days

#### Phase 3: Advanced Features
**Goal:** Full-featured release automation

**Tasks:**
1. Implement major/minor version increment via PR labels/keywords
2. Add release preview comment on PR
3. Automatic changelog generation
4. Validation checks before release
5. Rollback capabilities

**Deliverables:**
- Flexible versioning options
- Pre-release validation
- Enhanced documentation

**Effort:** 3-5 days

### Recommended Immediate Actions

**Priority 1: Prepare build.py for CI**
```python
# Add to build.py
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', help='Specific version to build')
    parser.add_argument('--non-interactive', action='store_true')
    args = parser.parse_args()
    
    if args.non_interactive:
        # Skip all prompts, use provided version
        if not args.version:
            exit_with_error("--version required in non-interactive mode")
        version = args.version
    else:
        # Existing interactive flow
        ...
```

**Priority 2: Create GitHub Actions Workflow**
- Start with basic version (Phase 1)
- Test with non-production branch first
- Validate artifact creation

**Priority 3: Document Process**
- Update README with automated release process
- Document version increment keywords
- Add troubleshooting guide

### Validation and Testing Strategy

**Before Production:**
1. **Test workflow on feature branch**
   ```yaml
   # Test version - triggers on dev instead of main
   on:
     pull_request:
       types: [closed]
       branches: [dev]
   ```

2. **Dry-run mode**
   - Create artifacts without publishing
   - Validate version increment logic
   - Check release notes generation

3. **Manual verification checklist**
   - [ ] Version incremented correctly
   - [ ] Manifest.json updated
   - [ ] Build artifacts created
   - [ ] SHA256 checksum valid
   - [ ] Git tag created
   - [ ] Release published
   - [ ] Release notes accurate

### Rollback Strategy

**If Automated Release Fails:**

1. **Delete the release** (if partially created)
   ```bash
   gh release delete v2.1.1
   ```

2. **Delete the tag**
   ```bash
   git push --delete origin v2.1.1
   ```

3. **Revert manifest.json commit**
   ```bash
   git revert <commit-hash>
   git push
   ```

4. **Fix issues and retry**

**Prevention:**
- Use draft releases initially
- Add validation steps before publishing
- Monitor workflow execution

---

## 8. Best Practices Summary

### Version Management
✅ **DO:**
- Use semantic versioning (major.minor.patch)
- Auto-increment patch by default
- Allow manual override via PR keywords
- Keep manifest.json synchronized

❌ **DON'T:**
- Mix manual and automatic version updates
- Skip version validation
- Allow version conflicts

### Git Tagging
✅ **DO:**
- Use annotated tags (git tag -a)
- Follow consistent format (v{version})
- Protect release tags from deletion
- Tag after successful artifact creation

❌ **DON'T:**
- Use lightweight tags
- Modify or delete release tags
- Tag failed releases

### Release Notes
✅ **DO:**
- Generate automatically from commits
- Leverage RDD workdir metadata
- Store in repository and GitHub release
- Include implementation details
- Categorize changes logically

❌ **DON'T:**
- Rely solely on manual notes
- Omit technical details
- Lose historical release information

### GitHub Actions
✅ **DO:**
- Use workflow permissions explicitly
- Validate before releasing
- Provide rollback mechanisms
- Log all steps clearly
- Test on non-production branches first

❌ **DON'T:**
- Skip validation checks
- Ignore workflow failures
- Commit untested workflows to main

---

## 9. Example Workflow Files

### Complete Release Workflow

See appendix in implementation artifacts for:
- `.github/workflows/release.yml` (full implementation)
- `scripts/generate_release_notes.py` (RDD-aware release notes generator)
- Modified `build/build.py` with CI support

---

## 10. Success Metrics

**How to Measure Success:**

1. **Automation Rate:** % of releases created automatically (target: 100%)
2. **Time to Release:** Minutes from merge to published release (target: <10 min)
3. **Manual Intervention:** Number of manual steps required (target: 0)
4. **Accuracy:** % of releases with correct version and artifacts (target: 100%)
5. **Release Notes Quality:** Completeness and usefulness (target: all prompts documented)

---

## 11. Conclusion

**Recommended Implementation:**

1. **Start with Phase 1** - Basic automation using existing build.py
2. **Enhance in Phase 2** - Add RDD-aware release notes generation
3. **Optimize in Phase 3** - Add advanced features and validation

**Key Benefits:**
- Zero-touch releases on main merges
- Consistent version management
- Rich release notes from RDD metadata
- Reduced manual effort and errors
- Full audit trail in git and GitHub

**Next Steps:**
1. Review and approve this analysis
2. Modify `build/build.py` for CI support
3. Implement Phase 1 workflow
4. Test on development branch
5. Deploy to production (main branch)

---

**Document Version:** 1.0  
**Created:** 2026-01-25  
**RDD Prompt:** P-034 Release automation  
**Author:** GitHub Copilot (Claude Sonnet 4.5)
