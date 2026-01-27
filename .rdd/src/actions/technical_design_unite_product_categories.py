#!/usr/bin/env python3
"""
Unite ProjectScale, ProductType, and Criticality categories into a single 'Product' category.

This script:
1. Reads the technical-design-schema.json file
2. Merges the three categories into one 'Product' category
3. Renames all question IDs to use 'Product_' prefix
4. Reorders questions: type → scale → criticality
5. Updates visibleWhen references to use new question IDs
6. Writes the updated schema back

Usage:
    python .rdd/src/actions/technical_design_unite_product_categories.py
"""

import json
import sys
from pathlib import Path

def main():
    """Unite Product scale, Product type, and Criticality categories."""
    
    # Define paths
    repo_root = Path(__file__).parent.parent.parent.parent
    schema_path = repo_root / ".rdd" / "config" / "technical-design-schema.json"
    
    # Read the schema
    try:
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema = json.load(f)
    except Exception as e:
        print(f"Error reading schema file: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Find the three categories to merge
    categories = schema.get("categories", [])
    project_scale = None
    product_type = None
    criticality = None
    other_categories = []
    
    for category in categories:
        cat_id = category.get("id", "")
        if cat_id == "ProjectScale":
            project_scale = category
        elif cat_id == "ProductType":
            product_type = category
        elif cat_id == "Criticality":
            criticality = category
        else:
            other_categories.append(category)
    
    if not all([project_scale, product_type, criticality]):
        print("Error: Could not find all three categories to merge", file=sys.stderr)
        sys.exit(1)
    
    # Create the new unified Product category
    product_category = {
        "id": "Product",
        "label": "Product definition",
        "description": "Core product attributes that shape architectural decisions",
        "questions": []
    }
    
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
    
    # Helper function to update visibleWhen references
    def update_visible_when(question):
        """Update visibleWhen questionId references to new IDs."""
        if "visibleWhen" in question:
            for condition in question["visibleWhen"]:
                if "questionId" in condition:
                    condition["questionId"] = rename_question_id(condition["questionId"])
        return question
    
    # Process and add questions in order: ProductType, ProjectScale, Criticality
    for question in product_type.get("questions", []):
        new_question = question.copy()
        new_question["id"] = rename_question_id(new_question["id"])
        new_question = update_visible_when(new_question)
        product_category["questions"].append(new_question)
    
    for question in project_scale.get("questions", []):
        new_question = question.copy()
        new_question["id"] = rename_question_id(new_question["id"])
        new_question = update_visible_when(new_question)
        product_category["questions"].append(new_question)
    
    for question in criticality.get("questions", []):
        new_question = question.copy()
        new_question["id"] = rename_question_id(new_question["id"])
        new_question = update_visible_when(new_question)
        product_category["questions"].append(new_question)
    
    # Build new categories list with Product first
    new_categories = [product_category] + other_categories
    schema["categories"] = new_categories
    
    # Write the updated schema
    try:
        with open(schema_path, 'w', encoding='utf-8') as f:
            json.dump(schema, f, indent=2, ensure_ascii=False)
        print(f"✓ Successfully united categories into 'Product' category")
        print(f"  - Merged 3 categories into 1")
        print(f"  - Updated {len(product_category['questions'])} question IDs")
        print(f"  - New category count: {len(new_categories)}")
    except Exception as e:
        print(f"Error writing schema file: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
