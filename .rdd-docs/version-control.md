# Version Control and Branching Strategy

## Overview

This document defines the Git and GitHub version control strategy for this project, combining best practices from modern workflows including GitHub Flow, Trunk-Based Development, and adaptations for the RDD (Requirements-Driven Development) framework.

## Core Principles

1. **Single Source of Truth**: The `main` branch is always deployable and represents the production-ready state
2. **Short-Lived Branches**: Feature branches should be small, focused, and merged quickly (ideally within 1-2 days)
3. **Continuous Integration**: All changes are validated through automated builds and tests before merging
4. **Code Review**: All changes go through pull request review before merging to main
5. **Clean History**: Maintain a readable and meaningful commit history

## Branch Naming Convention

### Main Branch
- **Name**: `main`
- **Purpose**: Production-ready code, always deployable
- **Protection**: Protected branch with required reviews and status checks

### Enhancement Branches
- **Prefix**: `enh/`
- **Format**: `enh/YYYYMMDD-HHmm-<enhancement-name>`
- **Example**: `enh/20251031-1430-add-user-authentication`
- **Purpose**: Implement new features or enhancements
- **Lifespan**: Short-lived (1-3 days ideally)

### Bug Fix Branches
- **Prefix**: `fix/`
- **Format**: `fix/YYYYMMDD-HHmm-<bug-description>`
- **Example**: `fix/20251031-1430-fix-login-error`
- **Purpose**: Fixes and bugs
- **Lifespan**: Short-lived (1-3 days ideally)

### Release Branches (Optional - for versioned releases)
- **Prefix**: `release/`
- **Format**: `release/v<major>.<minor>.<patch>`
- **Example**: `release/v1.2.0`
- **Purpose**: Prepare and stabilize a release
- **Lifespan**: Short (few days to a week)

## Workflow

### Quick Workflow Overview

The typical development cycle follows these steps:

1. **Start**: Branch from `main` → Create `enh/` or `fix/` branch
2. **Develop**: Make commits → Push regularly
3. **Review**: Open Pull Request → Address feedback
4. **Merge**: Squash and merge to `main` → Delete branch
5. **Deploy**: Changes automatically deploy from `main`

```
main ──┬─→ enh/20251031-1430-add-auth ─→ commits ─→ PR ─→ merge ─→ main
       │                                                              │
       └─→ fix/20251031-1500-login-bug ──→ commits ─→ PR ─→ merge ──┘
```

### Standard Change Workflow (GitHub Flow + RDD)

1. **Create Change**
   ```bash
   # Use RDD script to create change folder and branch
   ./.rdd/scripts/rdd.sh change create [enh|fix]
   ```
   - Creates branch: `enh/YYYYMMDD-HHmm-<change-name>` or `fix/YYYYMMDD-HHmm-<change-name>`
   - Creates change folder: `docs/changes/YYYYMMDD-HHmm-<change-name>/`
   - Branches from: `main`
   - Default type: `enh` (if not specified)

2. **Develop**
   - Make small, focused commits with descriptive messages
   - Commit early and often
   - Push regularly to backup work and enable collaboration
   - Keep branch up-to-date with main (rebase or merge)

3. **Commit Message Format**
    ```
    <type>: <short description>
    ```
    - Types: `enh`, `fix`, `docs`, `refactor`, `test`, `chore`, `style`
    - Keep it concise and under 50 characters
    - Example: `enh: add user authentication module`

4. **Create Pull Request**
   ```bash
   # After pushing your commits, create PR via:
   # 1. GitHub web interface (recommended)
   # 2. GitHub CLI: gh pr create --title "Your title" --body "Description"
   ```
   - Title: Clear description of the change
   - Description: Reference the change.md document
   - Link related issues
   - Request reviewers
   - Ensure CI checks pass

5. **Code Review**
   - Address feedback promptly
   - Push additional commits as needed
   - Maintain conversation in PR
   - Resolve all comments

6. **Merge**
   - Squash and merge for clean history (recommended)
   - Delete branch after merge
   - Ensure main remains deployable

### Hotfix Workflow

1. **Create Hotfix Branch**
   ```bash
   git checkout main
   git pull origin main
   git checkout -b hotfix/YYYYMMDD-HHmm-<description>
   ```

2. **Fix and Test**
   - Make minimal, focused changes
   - Test thoroughly
   - Document the fix

3. **Create Pull Request**
   - Mark as urgent/priority
   - Request immediate review
   - Fast-track through CI

4. **Merge to Main**
   - Merge immediately after approval
   - Tag the release if needed
   - Deploy to production

## Branch Protection Rules

### Main Branch Protection
- ✅ Require pull request reviews (minimum 1 approval)
- ✅ Require status checks to pass
- ✅ Require branches to be up to date before merging
- ✅ Require conversation resolution before merging
- ✅ Include administrators (enforce for everyone)
- ✅ Restrict who can push to matching branches
- ✅ Do not allow force pushes
- ✅ Do not allow deletions

## Best Practices

### Branch Management
- **Keep branches small**: Focus on one change at a time
- **Update frequently**: Sync with main at least daily
- **Delete after merge**: Clean up merged branches immediately
- **Avoid long-lived branches**: Merge within 1-3 days

### Commit Practices
- **Atomic commits**: Each commit should be a complete, logical unit
- **Meaningful messages**: Write clear, descriptive commit messages
- **Test before commit**: Ensure code compiles and tests pass
- **Sign commits**: Use GPG signing for security (optional but recommended)

### Pull Request Practices
- **Small PRs**: Aim for 200-400 lines changed per PR
- **Self-review first**: Review your own changes before requesting review
- **Link documentation**: Reference the change.md document
- **Respond promptly**: Address feedback within 24 hours
- **Update description**: Keep PR description current as changes evolve

### Merge Strategies

#### Recommended: Squash and Merge
- Combines all commits into one
- Keeps main history clean and linear
- Best for feature branches with many small commits

#### Alternative: Merge Commit
- Preserves full commit history
- Creates merge commit
- Use for important branches with meaningful commit history

## Continuous Integration

### Pre-Merge Requirements
- All automated tests pass
- Code coverage meets threshold (if configured)
- Linting and formatting checks pass
- Security scanning passes (if configured)
- Build succeeds on all target platforms

### CI Pipeline Stages
1. **Lint**: Code style and formatting
2. **Build**: Compile and package
3. **Test**: Unit, integration, and E2E tests
4. **Security**: Vulnerability scanning
5. **Deploy**: Deploy to staging (for main branch)

## Release Strategy

### Continuous Deployment (Recommended)
- Deploy from main branch automatically
- Use feature flags for incomplete features
- Roll forward for fixes (no rollbacks)
- Tag releases for reference: `v<major>.<minor>.<patch>`

### Scheduled Releases (Alternative)
- Create release branch from main
- Harden and test on release branch
- Merge to main and tag
- Delete release branch after deployment

## Git Configuration

### Required Configuration
```bash
# Set user identity
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Set default branch name
git config init.defaultBranch main

# Set pull strategy (rebase recommended)
git config pull.rebase true

# Set push behavior
git config push.default simple
```

## Troubleshooting

### Creating a Pull Request

**Method 1: GitHub Web Interface (Recommended)**
```bash
# 1. Push your branch to GitHub
git push origin feat/your-branch-name

# 2. Visit your repository on GitHub
# 3. Click "Compare & pull request" button (appears after push)
# 4. Fill in:
#    - Title: Brief description of changes
#    - Description: Link to change.md, explain what/why
#    - Reviewers: Select team members
#    - Labels: Add appropriate labels
# 5. Click "Create pull request"
```

**Method 2: GitHub CLI**
```bash
# Install GitHub CLI if not already: https://cli.github.com/
gh pr create --title "enh: add user authentication" \
             --body "Implements user auth as per docs/changes/20251031-1430-add-auth/change.md" \
             --reviewer username1,username2 \
             --label enhancement
```

**Method 3: VS Code GitHub Pull Requests Extension**
```bash
# 1. Install "GitHub Pull Requests and Issues" extension
# 2. Push your branch: git push origin enh/your-branch-name
# 3. Click "Create Pull Request" in the GitHub panel
# 4. Fill in details and submit
```

### Sync Branch with Main
```bash
# Update local main
git checkout main
git pull origin main

# Update enhancement branch
git checkout enh/your-branch
# Or for fix branch: git checkout fix/your-branch
git merge main
# Or: git rebase main
```

### Resolve Merge Conflicts
```bash
# During merge/rebase
# 1. Edit conflicted files
# 2. Mark as resolved
git add <file>
# 3. Continue
git merge --continue
# Or: git rebase --continue
```

### Undo Last Commit (Not Pushed)
```bash
# Keep changes staged
git reset --soft HEAD~1

# Keep changes unstaged
git reset HEAD~1

# Discard changes
git reset --hard HEAD~1
```

## References

- [GitHub Flow](https://docs.github.com/en/get-started/using-github/github-flow)
- [Trunk-Based Development](https://trunkbaseddevelopment.com/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Git Best Practices](https://www.atlassian.com/git/tutorials/comparing-workflows)

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-10-31 | Initial version control strategy |
