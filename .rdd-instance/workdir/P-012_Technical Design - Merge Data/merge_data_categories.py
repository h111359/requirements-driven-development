#!/usr/bin/env python3
"""
Merge Data-related categories into Data & Analytics category.

This script merges:
- Expanded Data
- Data Visualization  
- Data Lifecycle & Retention

Into:
- Data & Analytics

Following questionnaire decisions:
- Q1: Append in order (Expanded Data, Data Visualization, Data Lifecycle & Retention)
- Q2: Update all question IDs to DA_ prefix
- Q3: Merge ALL questions
- Q4: Remove source categories completely
"""

import json
import sys
from pathlib import Path

def create_id_mapping(questions, prefix, start_num):
    """Create mapping from old IDs to new DA_ prefixed IDs."""
    mapping = {}
    counter = start_num
    
    for q in questions:
        old_id = q['id']
        # Extract the suffix part after the underscore
        suffix = old_id.split('_', 1)[1] if '_' in old_id else old_id
        new_id = f"{prefix}_{suffix}"
        
        # Ensure uniqueness by adding counter if needed
        base_new_id = new_id
        check_num = 1
        while new_id in mapping.values():
            new_id = f"{base_new_id}{check_num}"
            check_num += 1
            
        mapping[old_id] = new_id
        q['id'] = new_id
        counter += 1
    
    return mapping

def merge_categories(schema_path, output_path):
    """Perform the category merge operation."""
    
    # Load schema
    with open(schema_path, 'r', encoding='utf-8') as f:
        schema = json.load(f)
    
    # Find the categories
    data_analytics = None
    expanded_data = None
    data_viz = None
    data_lifecycle = None
    
    categories_to_remove = []
    
    for idx, cat in enumerate(schema['categories']):
        if cat['id'] == 'DataAnalytics':
            data_analytics = cat
            data_analytics_idx = idx
        elif cat['id'] == 'ExpandedData':
            expanded_data = cat
            categories_to_remove.append(idx)
        elif cat['id'] == 'DataVisualization':
            data_viz = cat
            categories_to_remove.append(idx)
        elif cat['id'] == 'DataLifecycleRetention':
            data_lifecycle = cat
            categories_to_remove.append(idx)
    
    if not data_analytics:
        print("ERROR: DataAnalytics category not found!")
        return False
    
    if not all([expanded_data, data_viz, data_lifecycle]):
        print("ERROR: One or more source categories not found!")
        return False
    
    # Track ID mappings for migration
    id_mappings = {}
    
    # Get the starting number for new questions
    current_da_count = len(data_analytics.get('questions', []))
    
    # Process each source category in order
    print(f"Merging categories into Data & Analytics (currently {current_da_count} questions)...")
    
    # 1. Expanded Data
    print(f"  - Adding {len(expanded_data['questions'])} questions from Expanded Data")
    expanded_mapping = create_id_mapping(expanded_data['questions'], 'DA', current_da_count + 1)
    id_mappings.update(expanded_mapping)
    data_analytics['questions'].extend(expanded_data['questions'])
    
    # 2. Data Visualization
    print(f"  - Adding {len(data_viz['questions'])} questions from Data Visualization")
    viz_mapping = create_id_mapping(data_viz['questions'], 'DA', 
                                     current_da_count + len(expanded_data['questions']) + 1)
    id_mappings.update(viz_mapping)
    data_analytics['questions'].extend(data_viz['questions'])
    
    # 3. Data Lifecycle & Retention
    print(f"  - Adding {len(data_lifecycle['questions'])} questions from Data Lifecycle & Retention")
    lifecycle_mapping = create_id_mapping(data_lifecycle['questions'], 'DA',
                                          current_da_count + len(expanded_data['questions']) + 
                                          len(data_viz['questions']) + 1)
    id_mappings.update(lifecycle_mapping)
    data_analytics['questions'].extend(data_lifecycle['questions'])
    
    final_count = len(data_analytics['questions'])
    print(f"  - Final Data & Analytics: {final_count} questions")
    
    # Remove the source categories (in reverse order to maintain indices)
    for idx in sorted(categories_to_remove, reverse=True):
        removed = schema['categories'].pop(idx)
        print(f"  - Removed category: {removed['id']} ({removed['label']})")
    
    # Save the updated schema
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(schema, f, indent=2, ensure_ascii=False)
    
    print(f"\nSchema updated successfully!")
    print(f"Saved to: {output_path}")
    
    # Save ID mappings for migration reference
    mapping_file = output_path.parent / 'id_mappings.json'
    with open(mapping_file, 'w', encoding='utf-8') as f:
        json.dump(id_mappings, f, indent=2)
    print(f"ID mappings saved to: {mapping_file}")
    
    return True

if __name__ == '__main__':
    repo_root = Path(__file__).parent.parent.parent.parent
    schema_path = repo_root / '.rdd/config/technical-design-schema.json'
    
    # Create backup
    backup_path = schema_path.with_suffix('.json.backup')
    import shutil
    shutil.copy2(schema_path, backup_path)
    print(f"Backup created: {backup_path}")
    
    # Perform merge
    if merge_categories(schema_path, schema_path):
        print("\n✓ Merge completed successfully")
        sys.exit(0)
    else:
        print("\n✗ Merge failed")
        sys.exit(1)
