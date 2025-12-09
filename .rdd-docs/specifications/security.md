## Security

### Overview

- [Define authentication and authorization requirements]
- [Specify data protection and privacy requirements]
- [List compliance requirements]

### Script Execution Safety
- Scripts use `set -e` (Bash) or `$ErrorActionPreference = 'Stop'` (PowerShell) to fail fast
- No arbitrary code execution from user input
- Git operations use local repository only (no remote credential handling)

### Data Protection
- All data stored in git repository
- No external service dependencies
- Workspace files cleared after archiving (no sensitive data retention)

### Access Control
- Relies on OS-level file permissions
- Git credentials managed by user's git configuration
- No authentication or authorization system within framework