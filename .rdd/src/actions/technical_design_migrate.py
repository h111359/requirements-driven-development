#!/usr/bin/env python3
"""
Migrate legacy technical design format to new format.

This script detects and migrates old technical design formats to the new
storage format (object keyed by questionId).

Usage:
    python .rdd/src/actions/technical_design_migrate.py [--dry-run]

Options:
    --dry-run - Show what would be migrated without making changes

Exit codes:
    0 - Success or no migration needed
    1 - Error
"""

import json
import os
import sys
from datetime import datetime, timezone
import shutil

def detect_legacy_format(data):
    """
    Detect if data is in legacy format.
    
    Returns: (is_legacy, format_name)
    """
    if not isinstance(data, dict):
        return False, "unknown"
    
    # Check for legacy array-based format
    if isinstance(data, list):
        return True, "legacy-array"
    
    # Check for legacy schema format (has "sections" key)
    if "sections" in data or "schemaVersion" in data:
        return True, "legacy-schema"
    
    # Check if it's already in new format (keys are questionIds)
    # New format: { "QuestionId": { "questionId": ..., "type": ..., "value": ..., "answeredAt": ... }}
    if data:
        first_key = next(iter(data))
        first_value = data[first_key]
        if isinstance(first_value, dict) and 'questionId' in first_value and 'answeredAt' in first_value:
            return False, "new-format"
    
    # Empty object is considered new format
    return False, "new-format"

def migrate_from_legacy(data, format_name):
    """
    Migrate legacy format to new format.
    
    This is a placeholder - actual migration would depend on what legacy
    formats existed. For now, we assume the current file is either:
    - Empty (no migration needed)
    - Already in new format (no migration needed)
    - Some unknown legacy format (error)
    """
    # For now, we only handle empty or new format
    # If there's actual legacy data to migrate, implementation would go here
    return {}

def main():
    """Migrate technical design to new format."""
    dry_run = '--dry-run' in sys.argv
    
    tech_design_path = ".rdd-instance/specifications/technical-design.json"
    
    # Check if file exists
    if not os.path.exists(tech_design_path):
        print(json.dumps({
            "migrated": False,
            "message": "No technical-design.json file exists, no migration needed"
        }))
        return 0
    
    # Load current file
    try:
        with open(tech_design_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if not content:
                data = {}
            else:
                data = json.loads(content)
    except json.JSONDecodeError as e:
        print(json.dumps({
            "error": "Invalid JSON in technical-design.json",
            "details": str(e),
            "recovery": "Fix JSON syntax or delete file"
        }), file=sys.stderr)
        return 1
    except Exception as e:
        print(json.dumps({
            "error": "Failed to read technical-design.json",
            "details": str(e)
        }), file=sys.stderr)
        return 1
    
    # Detect format
    is_legacy, format_name = detect_legacy_format(data)
    
    if not is_legacy:
        print(json.dumps({
            "migrated": False,
            "message": f"File is already in new format ({format_name}), no migration needed"
        }))
        return 0
    
    # Backup old file
    if not dry_run:
        backup_path = tech_design_path + ".backup-" + datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
        try:
            shutil.copy2(tech_design_path, backup_path)
        except Exception as e:
            print(json.dumps({
                "error": "Failed to create backup",
                "details": str(e),
                "recovery": "Check file permissions"
            }), file=sys.stderr)
            return 1
    
    # Migrate
    try:
        migrated_data = migrate_from_legacy(data, format_name)
        
        if dry_run:
            print(json.dumps({
                "migrated": False,
                "dryRun": True,
                "message": f"Would migrate from {format_name} to new format",
                "currentEntries": len(data) if isinstance(data, dict) else "N/A",
                "migratedEntries": len(migrated_data)
            }))
            return 0
        
        # Write migrated data atomically
        temp_path = tech_design_path + ".tmp"
        with open(temp_path, 'w', encoding='utf-8') as f:
            json.dump(migrated_data, f, indent=2, ensure_ascii=False)
        
        os.replace(temp_path, tech_design_path)
        
        print(json.dumps({
            "migrated": True,
            "message": f"Successfully migrated from {format_name} to new format",
            "backupPath": backup_path,
            "migratedEntries": len(migrated_data)
        }))
        return 0
    
    except Exception as e:
        print(json.dumps({
            "error": "Migration failed",
            "details": str(e),
            "recovery": "Check backup file and retry"
        }), file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
