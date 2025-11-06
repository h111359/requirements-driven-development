# P02 Implementation: Configurable Default Branch

## Prompt
The prompt `.github/prompts/rdd.01-initiate.prompt.md` executes command `python .rdd/scripts/rdd.py change create` which expects to be on the default branch. But currently the default branch functionality searches for exactly main or master. I want now to change the default branch to some other branch in my repo. And I want this to be configurable. Make an analysis for the best practices according to the current situation of the scripts in `.rdd/scripts` and the prompts in `.github/prompts`.

## Context Files Read
- `.rdd-docs/requirements.md`
- `.rdd-docs/tech-spec.md`
- `.rdd-docs/folder-structure.md`
- `.rdd-docs/data-model.md`
- `.github/prompts/rdd.01-initiate.prompt.md`
- `.rdd/scripts/rdd.py`
- `.rdd/scripts/rdd_utils.py`

## Current Implementation Analysis

### 1. Current Default Branch Detection

The function `get_default_branch()` in `.rdd/scripts/rdd_utils.py` (lines 299-324) uses a **hardcoded fallback approach**:

```python
def get_default_branch() -> str:
    """
    Get the default branch name (main or master).
    Returns "main" or "master" depending on what exists.
    """
    # Check if main branch exists
    result = subprocess.run(
        ['git', 'show-ref', '--verify', '--quiet', 'refs/heads/main'],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    
    if result.returncode == 0:
        return "main"
    
    # Check if master branch exists
    result = subprocess.run(
        ['git', 'show-ref', '--verify', '--quiet', 'refs/heads/master'],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    
    if result.returncode == 0:
        return "master"
    
    return "main"  # Default to main
```

**Problems with current implementation:**
- Hardcoded to only check "main" and "master"
- Cannot detect repository's actual default branch if it has a different name
- Falls back to "main" even if it doesn't exist
- No configuration mechanism to override the detection

### 2. Places Where Default Branch is Used

The default branch is used in multiple places:
- `rdd.py`: In `route_change()` (line ~850) - validation before creating changes
- `rdd.py`: In `create_branch()` (line ~350) - switching to default before creating new branch
- `rdd.py`: In `delete_branch()` (line ~410) - switching to default before deleting
- `rdd.py`: In `cleanup_after_merge()` (line ~500) - switching back to default after PR merge
- `rdd_utils.py`: In `pull_main()` (line ~511) - pulling latest changes
- Multiple other git operations

### 3. Existing Configuration System

The RDD framework has a **workspace-specific configuration** system:
- Config files: `.rdd.[fix|enh].[branch-name]` in workspace
- Helper functions: `find_change_config()`, `get_config()`, `set_config()`
- Format: JSON files
- Location: `.rdd-docs/workspace/`
- Purpose: Track current change metadata

**However**, there is **NO global/project-level configuration** system for repository-wide settings like default branch.

## Best Practices Analysis

### Option 1: Query Git's Remote HEAD (Recommended)

**Approach:** Use Git's native capability to detect the default branch from remote.

**Advantages:**
✓ Respects repository's actual default branch setting
✓ Works automatically when default branch changes on remote
✓ No manual configuration needed
✓ Standard Git practice
✓ Handles all branch names (main, master, dev, develop, etc.)
✓ Aligns with GitHub's default branch setting

**Implementation:**
```bash
git remote show origin | grep 'HEAD branch' | awk '{print $NF}'
# or
git symbolic-ref refs/remotes/origin/HEAD | sed 's@^refs/remotes/origin/@@'
```

**Disadvantages:**
- Requires remote connection (can fail offline)
- Needs fallback mechanism for offline work

### Option 2: Local Configuration File (.rddrc or .rdd.config.json)

**Approach:** Create a project-level config file in repository root.

**Advantages:**
✓ Works offline
✓ Explicit and version-controlled
✓ Can store other project settings
✓ Fast lookup
✓ User can override if needed

**Disadvantages:**
- Requires manual setup/initialization
- Needs synchronization with actual Git settings
- Can become stale if default branch changes
- Adds another file to maintain

**Implementation:**
Create `.rdd/config.json`:
```json
{
  "defaultBranch": "dev",
  "version": "1.0.0"
}
```

### Option 3: Hybrid Approach (Best of Both Worlds)

**Approach:** Query Git remote first, fall back to config file, then to main/master detection.

**Advantages:**
✓ Automatic detection when online
✓ Works offline with local config
✓ Handles all edge cases
✓ User can override via config if needed
✓ Most flexible solution

**Implementation Priority:**
1. Check local config file (`.rdd/config.json`) if exists
2. Query Git remote for HEAD branch
3. Fall back to checking "main" then "master" existence
4. Final fallback to "main"

### Option 4: Git Config Storage

**Approach:** Store in Git's config system.

**Advantages:**
✓ Uses Git's native configuration
✓ Per-repository or global settings
✓ Standard location

**Implementation:**
```bash
git config --local rdd.defaultBranch dev
git config --get rdd.defaultBranch
```

**Disadvantages:**
- Less discoverable for users
- Requires understanding Git config
- Not version-controlled (local only)

## Recommended Solution: Hybrid Approach (Option 3)

### Why Hybrid is Best

1. **Respects Git's truth**: Queries remote to get actual default branch
2. **User override capability**: Config file allows manual override when needed
3. **Offline resilience**: Works when remote is unavailable
4. **Zero configuration**: Works out-of-box for standard repos
5. **Future-proof**: Handles any branch name without code changes

### Implementation Strategy

#### 1. Create Global Config System

**File:** `.rdd/config.json` (in repository root)
**Purpose:** Store RDD framework settings
**Structure:**
```json
{
  "defaultBranch": "dev",
  "version": "1.0.0",
  "created": "2024-11-06T10:00:00Z",
  "lastModified": "2024-11-06T10:00:00Z"
}
```

**Location Rationale:**
- `.rdd/` directory already exists for framework files
- Version-controlled with the framework
- Gitignored by default in most setups? **NO** - `.rdd/` is tracked
- **Decision:** Place in `.rdd/config.json` so it's version-controlled and shared across team

#### 2. Update `get_default_branch()` Function

**New implementation logic:**
```python
def get_default_branch() -> str:
    """
    Get the default branch name with intelligent detection.
    Priority:
    1. User config file (.rdd/config.json)
    2. Git remote HEAD (actual repository default)
    3. Local branch detection (main, then master)
    4. Fallback to "main"
    """
    
    # 1. Check config file first (user override)
    config_branch = get_rdd_config("defaultBranch")
    if config_branch:
        # Verify branch actually exists
        result = subprocess.run(
            ['git', 'show-ref', '--verify', '--quiet', f'refs/heads/{config_branch}'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        if result.returncode == 0:
            return config_branch
        else:
            print_warning(f"Configured default branch '{config_branch}' not found, using auto-detection")
    
    # 2. Query Git remote for HEAD branch
    try:
        result = subprocess.run(
            ['git', 'symbolic-ref', 'refs/remotes/origin/HEAD'],
            capture_output=True,
            text=True,
            timeout=2  # Quick timeout for offline scenarios
        )
        if result.returncode == 0:
            # Output format: refs/remotes/origin/main
            branch = result.stdout.strip().replace('refs/remotes/origin/', '')
            if branch:
                debug_print(f"Detected default branch from remote: {branch}")
                return branch
    except (subprocess.TimeoutExpired, Exception):
        debug_print("Could not query remote (offline or slow connection)")
    
    # 3. Check common branch names locally
    for branch_name in ['main', 'master']:
        result = subprocess.run(
            ['git', 'show-ref', '--verify', '--quiet', f'refs/heads/{branch_name}'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        if result.returncode == 0:
            debug_print(f"Found local default branch: {branch_name}")
            return branch_name
    
    # 4. Final fallback
    print_warning("Could not detect default branch, falling back to 'main'")
    return "main"
```

#### 3. Add Config Management Functions

Add to `rdd_utils.py`:

```python
# Global config file path
RDD_CONFIG_FILE = ".rdd/config.json"

def get_rdd_config(key: str, default: Optional[str] = None) -> Optional[str]:
    """
    Get value from global RDD config file.
    Returns value or default if not found.
    """
    config_path = os.path.join(get_repo_root(), RDD_CONFIG_FILE)
    
    if not os.path.isfile(config_path):
        return default
    
    try:
        with open(config_path, 'r') as f:
            data = json.load(f)
            return data.get(key, default)
    except Exception:
        return default


def set_rdd_config(key: str, value: str) -> bool:
    """
    Set value in global RDD config file.
    Creates file if it doesn't exist.
    """
    repo_root = get_repo_root()
    config_path = os.path.join(repo_root, RDD_CONFIG_FILE)
    
    # Create .rdd directory if needed
    rdd_dir = os.path.join(repo_root, ".rdd")
    os.makedirs(rdd_dir, exist_ok=True)
    
    # Load existing config or create new
    if os.path.isfile(config_path):
        with open(config_path, 'r') as f:
            data = json.load(f)
    else:
        data = {
            "version": "1.0.0",
            "created": datetime.utcnow().isoformat() + "Z"
        }
    
    # Update value and timestamp
    data[key] = value
    data["lastModified"] = datetime.utcnow().isoformat() + "Z"
    
    # Write back
    with open(config_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    return True


def init_rdd_config() -> bool:
    """
    Initialize RDD config file with detected default branch.
    Only creates if file doesn't exist.
    """
    repo_root = get_repo_root()
    config_path = os.path.join(repo_root, RDD_CONFIG_FILE)
    
    if os.path.isfile(config_path):
        print_info("RDD config file already exists")
        return True
    
    # Detect current default branch
    detected_branch = get_default_branch()
    
    # Create initial config
    data = {
        "version": "1.0.0",
        "defaultBranch": detected_branch,
        "created": datetime.utcnow().isoformat() + "Z",
        "lastModified": datetime.utcnow().isoformat() + "Z"
    }
    
    # Create .rdd directory if needed
    rdd_dir = os.path.join(repo_root, ".rdd")
    os.makedirs(rdd_dir, exist_ok=True)
    
    # Write config
    with open(config_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    print_success(f"Initialized RDD config with default branch: {detected_branch}")
    return True
```

#### 4. Add CLI Commands for Config Management

Add to `rdd.py`:

```python
def route_config(args: List[str]) -> int:
    """Route config domain commands."""
    if not args or args[0] in ['--help', '-h']:
        show_config_help()
        return 0
    
    action = args[0]
    
    if action == 'init':
        return 0 if init_rdd_config() else 1
    
    elif action == 'get':
        if len(args) < 2:
            print_error("Config key required")
            return 1
        value = get_rdd_config(args[1])
        if value:
            print(f"{args[1]}: {value}")
            return 0
        else:
            print_warning(f"Config key '{args[1]}' not found")
            return 1
    
    elif action == 'set':
        if len(args) < 3:
            print_error("Config key and value required")
            return 1
        return 0 if set_rdd_config(args[1], args[2]) else 1
    
    elif action == 'show':
        config_path = os.path.join(get_repo_root(), RDD_CONFIG_FILE)
        if not os.path.isfile(config_path):
            print_warning("No RDD config file found")
            return 1
        with open(config_path, 'r') as f:
            print(f.read())
        return 0
    
    else:
        print_error(f"Unknown config action: {action}")
        return 1


def show_config_help() -> None:
    """Show config management help."""
    print_banner("Configuration Management")
    print()
    print("Usage: rdd.py config <action> [options]")
    print()
    print("Actions:")
    print("  init                   Initialize config file with detected defaults")
    print("  get <key>              Get config value")
    print("  set <key> <value>      Set config value")
    print("  show                   Show entire config file")
    print()
    print("Examples:")
    print("  rdd.py config init")
    print("  rdd.py config get defaultBranch")
    print("  rdd.py config set defaultBranch dev")
    print("  rdd.py config show")
```

Update main routing:
```python
def main() -> int:
    # ... existing code ...
    
    if domain == 'config':
        return route_config(domain_args)
    # ... rest of domains ...
```

#### 5. Update Documentation

Files to update:
- `.rdd-docs/requirements.md`: Add new functional requirement
- `.rdd-docs/tech-spec.md`: Document config system architecture
- `.rdd-docs/data-model.md`: Add config file schema
- `README.md`: Add config usage examples

### Migration Path

1. **Backward Compatibility**: Old behavior continues to work (main/master detection)
2. **Opt-in Enhancement**: Users can run `rdd.py config init` to create config
3. **No Breaking Changes**: Existing workflows unaffected
4. **Automatic Detection**: Config file created on first `change create` if missing

### User Experience

**First-time user (no config):**
```bash
$ python .rdd/scripts/rdd.py change create
# Works automatically, detects default branch from Git remote
```

**User wants to override:**
```bash
$ python .rdd/scripts/rdd.py config set defaultBranch dev
✓ Configuration updated: defaultBranch = dev

$ python .rdd/scripts/rdd.py config show
{
  "version": "1.0.0",
  "defaultBranch": "dev",
  "created": "2024-11-06T10:00:00Z",
  "lastModified": "2024-11-06T10:15:00Z"
}
```

**User wants to check current setting:**
```bash
$ python .rdd/scripts/rdd.py config get defaultBranch
defaultBranch: dev
```

## Summary

The recommended solution is a **hybrid approach** that:

1. ✅ **Queries Git remote** for automatic detection (respects repository settings)
2. ✅ **Allows user override** via `.rdd/config.json` (configurable)
3. ✅ **Falls back gracefully** to main/master detection (offline resilience)
4. ✅ **Zero configuration needed** for standard repositories
5. ✅ **Fully backward compatible** with existing workflows
6. ✅ **Version-controlled** configuration shared across team
7. ✅ **Extensible** for future RDD settings

### Implementation Checklist

- [ ] Create config management functions in `rdd_utils.py`
- [ ] Update `get_default_branch()` with hybrid logic
- [ ] Add `config` domain commands to `rdd.py`
- [ ] Add help documentation for config commands
- [ ] Update requirements and tech-spec documentation
- [ ] Add config file schema to data-model
- [ ] Test with non-standard default branch names
- [ ] Update README with config examples

## Questions for User

Before proceeding with implementation, I need your input on:

1. **Config file location**: Should I use `.rdd/config.json` (version-controlled, shared) or a different location?
   
2. **Auto-initialization**: Should I automatically create the config file on first `change create`, or require explicit `config init`?

3. **Default branch name in your repo**: What is your desired default branch name? (Currently detected as "main" from remote)

4. **Remote HEAD update**: Should I add a command to update the remote HEAD reference if it's not set? (e.g., `git remote set-head origin dev`)

