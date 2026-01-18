#!/usr/bin/env python3
"""
Migrate technical-design.json from old question IDs to new unified Product category IDs.

This script:
1. Reads the technical-design.json file
2. For each answered question, maps old IDs to new IDs:
   - ProjectScale_* → Product_*
   - ProductType_* → Product_*
   - Criticality_* → Product_*
3. Updates the questionId field in place
4. Preserves all other data (type, value, answeredAt)
5. Writes the migrated file back

Usage:
    python .rdd/src/actions/technical_design_migrate_product_unification.py
"""

import json
import sys
from pathlib import Path

def main():
    """Migrate technical-design.json to use new Product_ question IDs."""
    
    # Define paths
    repo_root = Path(__file__).parent.parent.parent.parent
    tech_design_path = repo_root / ".rdd-instance" / "specifications" / "technical-design.json"
    
    # Read the technical design file
    try:
        with open(tech_design_path, 'r', encoding='utf-8') as f:
            tech_design = json.load(f)
    except FileNotFoundError:
        print(f"✓ No technical-design.json file found - nothing to migrate")
        sys.exit(0)
    except Exception as e:
        print(f"Error reading technical-design.json: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Check if it's empty or has no answered questions
    if not tech_design:
        print(f"✓ Technical design file is empty - nothing to migrate")
        sys.exit(0)
    
    # Helper function to rename question IDs
    def rename_question_id(old_id):
        """Convert old question ID to new Product_ prefixed ID."""
        if old_id.startswith("ProjectScale_"):
            return old_id.replace("ProjectScale_", "Product_")
        elif old_id.startswith("ProductType_"):
            return old_id.replace("ProductType_", "Product_")
        elif old_id.startswith("Criticality_"):
            return old_id.replace("Criticality_", "Product_")
        return old_id
    
    # Migrate the question IDs
    migrated_design = {}
    migrated_count = 0
    unchanged_count = 0
    
    for question_id, question_data in tech_design.items():
        new_id = rename_question_id(question_id)
        migrated_design[new_id] = question_data
        
        if new_id != question_id:
            migrated_count += 1
        else:
            unchanged_count += 1
    
    # Write the migrated file
    try:
        with open(tech_design_path, 'w', encoding='utf-8') as f:
            json.dump(migrated_design, f, indent=2, ensure_ascii=False)
        print(f"✓ Successfully migrated technical-design.json")
        print(f"  - Migrated question IDs: {migrated_count}")
        print(f"  - Unchanged question IDs: {unchanged_count}")
        print(f"  - Total questions: {len(migrated_design)}")
    except Exception as e:
        print(f"Error writing technical-design.json: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
