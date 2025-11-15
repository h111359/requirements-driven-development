#!/usr/bin/env python3
import json
import os
import subprocess
from datetime import datetime, timezone

CONFIG_PATH = os.path.join(os.path.dirname(__file__), '..', '.rdd-docs', 'config.json')


def read_config():
    with open(CONFIG_PATH, 'r') as f:
        return json.load(f)


def update_last_modified(config):
    # Format: 2025-11-14T04:22:33.170656+00:00
    now = datetime.now(timezone.utc).astimezone()
    config['lastModified'] = now.isoformat()

def write_config(config):
    update_last_modified(config)
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=2)
        f.write('\n')


def display_config(config):
    version = config.get('version', 'N/A')
    default_branch = config.get('defaultBranch', 'N/A')
    local_only = config.get('localOnly', 'N/A')
    print(f"Current version: {version}")
    print(f"Default branch: {default_branch}")
    print(f"Local only flag: {local_only}")


def get_git_branches():
    try:
        result = subprocess.run(['git', 'branch', '--format=%(refname:short)'],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, text=True)
        branches = [b.strip() for b in result.stdout.splitlines() if b.strip()]
        return branches
    except Exception as e:
        print(f"Error getting git branches: {e}")
        return []


def update_version(version, part):
    parts = version.split('.')
    if len(parts) != 3 or not all(p.isdigit() for p in parts):
        print("Invalid version format. Should be MAJOR.MINOR.PATCH")
        return version
    major, minor, patch = map(int, parts)
    if part == 'major':
        major += 1
    elif part == 'minor':
        minor += 1
    elif part == 'patch':
        patch += 1
    if part == 'major':
        minor = 0
        patch = 0
    elif part == 'minor':
        patch = 0
    return f"{major}.{minor}.{patch}"


def main():
    config = read_config()
    display_config(config)
    print("\nWhat would you like to change?")
    print("1. Version major")
    print("2. Version minor")
    print("3. Version patch")
    print("4. Default branch")
    choice = input("Enter number (1-4): ").strip()
    if choice in {'1', '2', '3'}:
        part = { '1': 'major', '2': 'minor', '3': 'patch' }[choice]
        old_version = config.get('version', '0.0.0')
        new_version = update_version(old_version, part)
        print(f"Updating version: {old_version} -> {new_version}")
        config['version'] = new_version
        write_config(config)
        print("Version updated.")
    elif choice == '4':
        branches = get_git_branches()
        if not branches:
            print("No branches found.")
            return
        print("Available branches:")
        for idx, branch in enumerate(branches, 1):
            print(f"{idx}. {branch}")
        sel = input("Select branch number: ").strip()
        try:
            sel_idx = int(sel) - 1
            if 0 <= sel_idx < len(branches):
                config['defaultBranch'] = branches[sel_idx]
                write_config(config)
                print(f"Default branch updated to: {branches[sel_idx]}")
            else:
                print("Invalid selection.")
        except Exception:
            print("Invalid input.")
    else:
        print("No changes made.")

if __name__ == '__main__':
    main()
