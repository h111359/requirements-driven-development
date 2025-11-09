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

RDD requires that your project is already a Git repository. If not, initialize Git first:
```bash
git init
```

### Quick Start Installation (Recommended)

Extract the archive and run the installer launcher:

**Windows:**
1. Extract to a temporary location (e.g., `Downloads\rdd-v{{VERSION}}`)
2. Double-click `install.bat` **OR** run in PowerShell:
   ```powershell
   cd path\to\extracted\rdd-v{{VERSION}}
   .\install.bat
   ```
3. Choose GUI folder browser or enter path manually
4. Confirm installation

**Linux/macOS:**
1. Extract to a temporary location (e.g., `/tmp/rdd-v{{VERSION}}`)
2. Open terminal and run:
   ```bash
   cd /tmp/rdd-v{{VERSION}}
   chmod +x install.sh
   ./install.sh
   ```
3. Choose GUI folder browser or enter path manually
4. Confirm installation

The installer automatically:
- Verifies Python 3.7+ and Git are installed
- Checks the target is a Git repository
- Detects and warns about existing RDD installations
- Copies framework files (.rdd/, .github/prompts/, .rdd-docs/ templates)
- Merges VS Code settings intelligently
- Updates .gitignore
- Verifies successful installation

### Direct Python Installation

If you prefer direct control, navigate to your project directory and run install.py:

**Windows:**
```powershell
cd C:\path\to\your\project
python C:\path\to\extracted\rdd-v{{VERSION}}\install.py
```

**Linux/macOS:**
```bash
cd /path/to/your/project
python /path/to/extracted/rdd-v{{VERSION}}/install.py
```

## Getting Started

After successful installation:

1. **Verify installation:**
   ```bash
   python .rdd/scripts/rdd.py --version
   ```
   Should display: `RDD Framework v{{VERSION}}`

2. **Start interactive menu:**
   ```bash
   python .rdd/scripts/rdd.py
   ```
   Choose "Create new iteration" to begin your first feature or fix.

3. **Open VS Code** and use GitHub Copilot with RDD prompts to guide your development.

## Troubleshooting

**"python: command not found" (Linux)**
```bash
sudo apt-get install python-is-python3
```

**"Not a git repository"**
```bash
cd /path/to/your/project
git init
```

**"Permission denied" (Linux/macOS)**
```bash
chmod +x .rdd/scripts/rdd.py
chmod +x install.sh
```

**VS Code settings not applied**
- Restart VS Code
- Verify `.vscode/settings.json` exists
- Install GitHub Copilot extension if not already installed

## Documentation

For more information, visit: https://github.com/h111359/requirements-driven-development

## License

See LICENSE file for details.
