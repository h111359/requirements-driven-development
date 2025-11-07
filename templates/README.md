# RDD Framework v{{VERSION}}

Requirements-Driven Development (RDD) is a structured workflow automation framework that guides developers through requirement clarification, implementation, and documentation processes.

## System Requirements

- **Python 3.7+** 
  - Windows & macOS: Available by default with modern Python installations
  - Linux: Install `python-is-python3` package or create alias if `python` command is not available
- **Git 2.23+**
- **VS Code** (recommended)
- **GitHub Copilot** (optional but recommended)

### Python Command Setup

The RDD framework uses the `python` command (not `python3`) for cross-platform compatibility.

**Linux users**: If the `python` command is not available on your system, install it with:
```bash
sudo apt-get install python-is-python3  # Ubuntu/Debian
```
Or create an alias:
```bash
echo "alias python=python3" >> ~/.bashrc
source ~/.bashrc
```

## Installation

### Option 1: Interactive Installation (Recommended)

The interactive installer provides a visual menu to navigate and select your project directory.

#### Windows

1. **Extract this archive** to a temporary location (e.g., `C:\Users\YourName\Downloads\rdd-v{{VERSION}}`)
2. **Open PowerShell** (right-click Start menu → Windows PowerShell)
3. **Navigate to extracted folder**:
   ```powershell
   cd C:\Users\YourName\Downloads\rdd-v{{VERSION}}
   ```
4. **Run the interactive installer**:
   ```powershell
   .\install.ps1
   ```
5. **Navigate with arrow keys** (↑/↓) to browse folders
6. **Press Enter** on a folder to enter it, or select `[SELECT THIS DIRECTORY]` to install here
7. **Confirm installation** when prompted

#### Linux/macOS

1. **Extract this archive** to a temporary location (e.g., `/tmp/rdd-v{{VERSION}}`)
2. **Open terminal**
3. **Navigate to extracted folder**:
   ```bash
   cd /tmp/rdd-v{{VERSION}}
   ```
4. **Make the installer executable**:
   ```bash
   chmod +x install.sh
   ```
5. **Run the interactive installer**:
   ```bash
   ./install.sh
   ```
6. **Navigate with arrow keys** (↑/↓) to browse folders
7. **Press Enter** on a folder to enter it, or select `[SELECT THIS DIRECTORY]` to install here
8. **Confirm installation** when prompted

### Option 2: Direct Python Installation

If you prefer to specify the path directly or the interactive installer doesn't work:

#### Windows
```powershell
cd C:\path\to\your\project
python C:\Users\YourName\Downloads\rdd-v{{VERSION}}\install.py
```

#### Linux/macOS
```bash
cd /path/to/your/project
python /tmp/rdd-v{{VERSION}}/install.py
```

The installer will:
- Verify prerequisites
- Copy RDD framework files to your project
- Merge VS Code settings
- Update .gitignore

### Option 3: Manual Installation

If you prefer manual installation or the installers don't work:

#### Windows (PowerShell)
```powershell
# Copy prompts
Copy-Item -Recurse .github\prompts C:\path\to\your\project\.github\

# Copy RDD framework
Copy-Item -Recurse .rdd C:\path\to\your\project\

# Update .gitignore
Add-Content C:\path\to\your\project\.gitignore ".rdd-docs/workspace/"
```

#### Linux/macOS (Bash)
```bash
# Copy prompts
cp -r .github/prompts /path/to/your/project/.github/

# Copy RDD framework
cp -r .rdd /path/to/your/project/

# Set executable permissions
chmod +x /path/to/your/project/.rdd/scripts/rdd.py

# Update .gitignore
echo ".rdd-docs/workspace/" >> /path/to/your/project/.gitignore
```

**Then manually merge VS Code settings**:
- Copy settings from `.vscode/settings.json` to your project's `.vscode/settings.json`
- Merge the arrays (don't replace existing settings)

## Verification

After installation, verify RDD is working:

#### Windows
```powershell
cd C:\path\to\your\project
python .rdd\scripts\rdd.py --version
```

#### Linux/macOS
```bash
cd /path/to/your/project
python .rdd/scripts/rdd.py --version
```

You should see: `RDD Framework v{{VERSION}}`

## Getting Started

Initialize your first enhancement or fix:

#### Windows
```powershell
python .rdd\scripts\rdd.py change create enh my-first-feature
```

#### Linux/macOS
```bash
python .rdd/scripts/rdd.py change create enh my-first-feature
```

Then follow the RDD workflow prompts in VS Code with GitHub Copilot.

## Troubleshooting

### "python: command not found" (Linux)
Install the python-is-python3 package or create an alias (see System Requirements above).

### "Not a git repository"
RDD requires your project to be a Git repository. Initialize one with:
```bash
git init
```

### "Permission denied" (Linux/macOS)
Make the script executable:
```bash
chmod +x .rdd/scripts/rdd.py
```

### VS Code settings not taking effect
1. Restart VS Code
2. Check `.vscode/settings.json` was created/updated
3. Verify GitHub Copilot extension is installed

## Documentation

For more information, visit: https://github.com/h111359/requirements-driven-development

## License

See LICENSE file for details.
