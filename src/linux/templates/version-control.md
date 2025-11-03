# Version Control and Branching Strategy
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


