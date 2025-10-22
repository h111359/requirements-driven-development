import os
import shutil
from pathlib import Path

# Banner
BANNER = '''\n───── RDD-COPILOT ─────\n Prompt: Project Setup                                    \n Description:                                             \n > Recreate full project structure from                   \n > .rdd-copilot assets: restore folders, move templates,  \n > seed documentation, and prepare prompts/instructions.  \n ──────────────────────\n'''

ROOT = Path(__file__).resolve().parent.parent.parent
COPILOT = ROOT / ".rdd-copilot"
PROMPTS = COPILOT / "prompts"
GITHUB = ROOT / ".github"
DOCS = ROOT / ".rdd-docs"
TEMPLATES = COPILOT / "templates"

summary = {}


def ensure_dir(path):
    if not path.exists():
        path.mkdir(parents=True)
        summary[str(path.relative_to(ROOT))] = "created"
    else:
        summary[str(path.relative_to(ROOT))] = "already-present"

def copy_file(src, dst):
    if src.exists():
        if not dst.exists():
            shutil.copy2(str(src), str(dst))
            summary[str(dst.relative_to(ROOT))] = "created"
        else:
            summary[str(dst.relative_to(ROOT))] = "already-present"
    else:
        summary[str(dst.relative_to(ROOT))] = "missing-source"

def move_file(src, dst):
    if src.exists():
        if not dst.exists():
            shutil.copy2(str(src), str(dst))
            summary[str(dst.relative_to(ROOT))] = "created"
        else:
            summary[str(dst.relative_to(ROOT))] = "already-present"
    else:
        summary[str(dst.relative_to(ROOT))] = "missing-source"

def copy_folder(src, dst):
    if src.exists():
        if not dst.exists():
            shutil.copytree(str(src), str(dst))
            summary[str(dst.relative_to(ROOT))] = "created"
        else:
            summary[str(dst.relative_to(ROOT))] = "already-present"
    else:
        summary[str(dst.relative_to(ROOT))] = "missing-source"

def ensure_file(src_path, dst_path):
    if not dst_path.exists():
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        with open(src_path, "r") as src, open(dst_path, "w") as dst:
            dst.write(src.read())
        summary[str(dst_path.relative_to(ROOT))] = "created"
    else:
        summary[str(dst_path.relative_to(ROOT))] = "already-present"

def main():
    print(BANNER)

    # S02: Setup .github
    # Setup prompts and instructions in .github
    ensure_dir(GITHUB)
    ensure_dir(GITHUB / "prompts")
    ensure_dir(GITHUB / "instructions")
    ensure_dir(GITHUB / "chatmodes")
    copy_file(PROMPTS / "rdd-copilot.cr-create.prompt.md", GITHUB / "prompts" / "rdd-copilot.cr-create.prompt.md")
    copy_file(PROMPTS / "rdd-copilot.cr-clarify.prompt.md", GITHUB / "prompts" / "rdd-copilot.cr-clarify.prompt.md")
    copy_file(PROMPTS / "rdd-copilot.cr-design.prompt.md", GITHUB / "prompts" / "rdd-copilot.cr-design.prompt.md")
    copy_file(PROMPTS / "rdd-copilot.cr-implement.prompt.md", GITHUB / "prompts" / "rdd-copilot.cr-implement.prompt.md")
    copy_file(COPILOT / "instructions" / "rdd-copilot.python.instructions.md", GITHUB / "instructions" / "rdd-copilot.python.instructions.md")
    copy_file(COPILOT / "instructions" / "rdd-copilot.devops-core-principles.instructions.md", GITHUB / "instructions" / "rdd-copilot.devops-core-principles.instructions.md")
    copy_file(COPILOT / "instructions" / "rdd-copilot.sql-sp-generation.instructions.md", GITHUB / "instructions" / "rdd-copilot.sql-sp-generation.instructions.md")
    copy_file(COPILOT / "instructions" / "rdd-copilot.technologies.instructions.md", GITHUB / "instructions" / "rdd-copilot.technologies.instructions.md")
    copy_file(COPILOT / "chatmodes" / "rdd-copilot.Agent.chatmode.md", GITHUB / "chatmodes" / "rdd-copilot.Agent.chatmode.md")
    copy_file(COPILOT / "copilot-instructions.md", GITHUB / "copilot-instructions.md")

    # S03: Setup .rdd-docs
    # Setup documentation in .rdd-docs
    ensure_dir(DOCS)
    ensure_file(TEMPLATES / "requirements.md", DOCS / "specs" / "requirements.md")
    ensure_file(TEMPLATES / "design.md", DOCS / "specs" / "design.md")
    ensure_file(TEMPLATES / "change.md", DOCS / "templates" / "change.md")
    ensure_dir(DOCS / "templates")
    ensure_dir(DOCS / "changes")
    ensure_dir(DOCS / "specs")

    # S04: Summary
    # Summary
    for k, v in summary.items():
        print(f"{k}: {v}")

if __name__ == "__main__":
    main()



