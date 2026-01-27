#!/usr/bin/env python3
"""
Merge Expanded Security category into Security & IAM category.
Rename Security & IAM to Security.
Remove Expanded Security category.
"""

import json
import sys
from pathlib import Path

def merge_security_categories(schema_path):
    """Merge Expanded Security into Security & IAM, rename to Security."""
    
    # Load schema
    with open(schema_path, 'r', encoding='utf-8') as f:
        schema = json.load(f)
    
    # Find the categories
    security_iam_idx = None
    expanded_security_idx = None
    
    for idx, category in enumerate(schema['categories']):
        if category['id'] == 'Security_IAM':
            security_iam_idx = idx
        elif category['id'] == 'ExpandedSecurity':
            expanded_security_idx = idx
    
    if security_iam_idx is None:
        print("ERROR: Security_IAM category not found")
        return False
    
    if expanded_security_idx is None:
        print("ERROR: ExpandedSecurity category not found")
        return False
    
    print(f"Found Security_IAM at index {security_iam_idx}")
    print(f"Found ExpandedSecurity at index {expanded_security_idx}")
    
    # Get references to the categories
    security_iam = schema['categories'][security_iam_idx]
    expanded_security = schema['categories'][expanded_security_idx]
    
    # Rename Security_IAM to Security
    security_iam['id'] = 'Security'
    security_iam['label'] = 'Security'
    security_iam['description'] = 'Identity, authentication, authorization, secrets, encryption, platform security, scanning, compliance, hardening, and SDLC security'
    
    print(f"Renamed Security_IAM to Security")
    
    # Build merged questions list
    merged_questions = list(security_iam['questions'])
    
    # Track which ES questions to add (not overlapping)
    questions_to_add = []
    
    # Merge overlapping questions
    for es_question in expanded_security['questions']:
        es_id = es_question['id']
        
        # Find corresponding SEC question if it exists
        sec_question = None
        for sq in merged_questions:
            if sq['id'] == es_id.replace('ES_', 'SEC_'):
                sec_question = sq
                break
        
        if es_id == 'ES_AuthProviders':
            # Merge with SEC_AuthProviders
            if sec_question:
                # Combine options (they're mostly the same, use SEC version)
                # Add any unique options from ES
                sec_labels = {opt['label'] for opt in sec_question.get('options', [])}
                for es_opt in es_question.get('options', []):
                    if es_opt['label'] not in sec_labels:
                        sec_question['options'].append(es_opt)
                print(f"Merged {es_id} into SEC_AuthProviders")
            
        elif es_id == 'ES_AuthModel':
            # Merge with SEC_AuthorizationModel
            if sec_question:
                # Options are similar, keep SEC version with slight enhancement
                sec_labels = {opt['label'] for opt in sec_question.get('options', [])}
                for es_opt in es_question.get('options', []):
                    if es_opt['label'] not in sec_labels and es_opt['label'] != 'Hybrid authorization model':
                        sec_question['options'].append(es_opt)
                # Add "Hybrid" option if not present
                if 'Hybrid authorization model' not in sec_labels and 'Combination of models' not in sec_labels:
                    sec_question['options'].append({
                        "id": "Hybrid authorization model",
                        "label": "Hybrid authorization model"
                    })
                print(f"Merged {es_id} into SEC_AuthorizationModel")
        
        elif es_id == 'ES_PrivilegedAccess':
            # Merge with SEC_PrivilegedAccess
            if sec_question:
                # Combine options
                sec_labels = {opt['label'] for opt in sec_question.get('options', [])}
                for es_opt in es_question.get('options', []):
                    # Map similar options
                    if es_opt['label'] == 'PIM (Privileged Identity Management)':
                        if 'Privileged identity management' not in sec_labels:
                            sec_question['options'].append({
                                "id": "Privileged identity management",
                                "label": "Privileged identity management"
                            })
                    elif es_opt['label'] == 'Separate admin accounts':
                        if 'Restricted admin accounts' not in sec_labels:
                            sec_question['options'].append({
                                "id": "Restricted admin accounts",
                                "label": "Restricted admin accounts"
                            })
                    elif es_opt['label'] == 'Zero Trust privileged access':
                        if es_opt['label'] not in sec_labels:
                            sec_question['options'].append(es_opt)
                    elif es_opt['label'] not in sec_labels:
                        sec_question['options'].append(es_opt)
                print(f"Merged {es_id} into SEC_PrivilegedAccess")
        
        elif es_id == 'ES_SecretsStorage':
            # Merge with SEC_SecretsStorage
            if sec_question:
                # Combine options
                sec_labels = {opt['label'] for opt in sec_question.get('options', [])}
                for es_opt in es_question.get('options', []):
                    if es_opt['label'] == 'Hardware Security Module (HSM)' and es_opt['label'] not in sec_labels:
                        sec_question['options'].append(es_opt)
                    elif es_opt['label'] == 'No secret storage' and es_opt['label'] not in sec_labels:
                        sec_question['options'].append(es_opt)
                print(f"Merged {es_id} into SEC_SecretsStorage")
        
        elif es_id == 'ES_EncryptionAtRest':
            # Already have SEC_DataEncryptionAtRest, merge options
            for sq in merged_questions:
                if sq['id'] == 'SEC_DataEncryptionAtRest':
                    # Options are identical, keep SEC version
                    print(f"Merged {es_id} into SEC_DataEncryptionAtRest")
                    break
        
        elif es_id == 'ES_EncryptionInTransit':
            # Already have SEC_EncryptionInTransit with identical options
            print(f"Merged {es_id} into SEC_EncryptionInTransit (identical)")
        
        elif es_id == 'ES_VulnDetection':
            # Merge with SEC_VulnerabilityScanning
            for sq in merged_questions:
                if sq['id'] == 'SEC_VulnerabilityScanning':
                    # Combine unique options
                    sec_labels = {opt['label'] for opt in sq.get('options', [])}
                    for es_opt in es_question.get('options', []):
                        # Map similar ones
                        if es_opt['label'] == 'Defender for Cloud' and 'Microsoft Defender for Cloud' not in str(sq.get('options', [])):
                            sq['options'].append({
                                "id": "Defender for Cloud vulnerability scanning",
                                "label": "Defender for Cloud vulnerability scanning"
                            })
                        elif es_opt['label'] not in sec_labels:
                            sq['options'].append(es_opt)
                    print(f"Merged {es_id} into SEC_VulnerabilityScanning")
                    break
        
        else:
            # This is a unique ES question, convert to SEC and add
            new_question = dict(es_question)
            new_question['id'] = es_id.replace('ES_', 'SEC_')
            questions_to_add.append(new_question)
    
    # Add all unique questions
    merged_questions.extend(questions_to_add)
    print(f"Added {len(questions_to_add)} unique questions from Expanded Security")
    
    # Update the Security category with merged questions
    security_iam['questions'] = merged_questions
    
    # Remove ExpandedSecurity category
    del schema['categories'][expanded_security_idx]
    print(f"Removed ExpandedSecurity category")
    
    # Write back to file
    with open(schema_path, 'w', encoding='utf-8') as f:
        json.dump(schema, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully merged categories. Total questions in Security: {len(merged_questions)}")
    return True

if __name__ == '__main__':
    schema_path = Path(__file__).parent.parent.parent.parent / '.rdd' / 'config' / 'technical-design-schema.json'
    
    if not schema_path.exists():
        print(f"ERROR: Schema file not found at {schema_path}")
        sys.exit(1)
    
    # Create backup
    backup_path = schema_path.with_suffix('.json.backup')
    import shutil
    shutil.copy2(schema_path, backup_path)
    print(f"Created backup at {backup_path}")
    
    success = merge_security_categories(schema_path)
    
    if success:
        print("✓ Schema merge completed successfully")
        sys.exit(0)
    else:
        print("✗ Schema merge failed")
        sys.exit(1)
