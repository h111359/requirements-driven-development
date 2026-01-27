#!/usr/bin/env python3
"""
Read technical design answers.

This script reads and outputs the current technical design answers from
.rdd-instance/specifications/technical-design.json.

Usage:
    python .rdd/src/actions/technical_design_read.py

Output:
    JSON object containing all answered questions, or empty object if none exist.

Exit codes:
    0 - Success
    1 - Error reading file
"""

import json
import os
import sys

def main():
    """Read and output technical design answers."""
    tech_design_path = ".rdd-instance/specifications/technical-design.json"
    
    # Check if file exists
    if not os.path.exists(tech_design_path):
        print(json.dumps({}))
        return 0
    
    try:
        with open(tech_design_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if not content:
                print(json.dumps({}))
                return 0
            
            data = json.loads(content)
            print(json.dumps(data, indent=2))
            return 0
    
    except json.JSONDecodeError as e:
        print(json.dumps({
            "error": "Invalid JSON in technical-design.json",
            "details": str(e),
            "recovery": "Fix JSON syntax or delete the file to start fresh"
        }), file=sys.stderr)
        return 1
    
    except Exception as e:
        print(json.dumps({
            "error": "Failed to read technical design",
            "details": str(e),
            "recovery": "Check file permissions and path"
        }), file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
