#!/usr/bin/env python3
"""
Technical Design Schema Editor - HTTP Server

Provides REST API endpoints for managing the technical design schema file.
This server is independent of the RDD framework runtime and can run standalone.
"""

import http.server
import socketserver
import json
import os
import sys
import shutil
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse, parse_qs
import webbrowser
import time
import threading

# Configuration
PORT = 8765
SCHEMA_PATH = "../.rdd/config/technical-design-schema.json"
BACKUP_DIR = "./backups"

class SchemaEditorHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP request handler for the schema editor with REST API endpoints"""
    
    def __init__(self, *args, **kwargs):
        # Set the directory to serve static files from
        super().__init__(*args, directory=".", **kwargs)
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/api/schema':
            self.get_schema()
        elif parsed_path.path == '/api/backup/list':
            self.list_backups()
        elif parsed_path.path == '/':
            # Serve index.html
            self.path = '/index.html'
            return super().do_GET()
        else:
            # Serve static files
            return super().do_GET()
    
    def do_POST(self):
        """Handle POST requests"""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/api/schema':
            self.save_schema()
        elif parsed_path.path == '/api/validate':
            self.validate_schema()
        elif parsed_path.path == '/api/backup':
            self.create_backup()
        else:
            self.send_error(404, "Endpoint not found")
    
    def get_schema(self):
        """Load and return the schema file"""
        try:
            schema_file = Path(SCHEMA_PATH)
            if not schema_file.exists():
                self.send_json_response({
                    "error": f"Schema file not found at {SCHEMA_PATH}"
                }, 404)
                return
            
            with open(schema_file, 'r', encoding='utf-8') as f:
                schema = json.load(f)
            
            self.send_json_response({
                "schema": schema,
                "path": str(schema_file.resolve())
            })
        except json.JSONDecodeError as e:
            self.send_json_response({
                "error": f"Invalid JSON in schema file: {str(e)}"
            }, 400)
        except Exception as e:
            self.send_json_response({
                "error": f"Error loading schema: {str(e)}"
            }, 500)
    
    def save_schema(self):
        """Save the schema file with validation"""
        try:
            # Read request body
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            data = json.loads(body)
            
            schema = data.get('schema')
            if not schema:
                self.send_json_response({
                    "error": "No schema data provided"
                }, 400)
                return
            
            # Validate schema
            validation_result = self.validate_schema_data(schema)
            if not validation_result['valid']:
                self.send_json_response({
                    "error": "Schema validation failed",
                    "errors": validation_result['errors']
                }, 400)
                return
            
            # Atomic write: write to temp file, then rename
            schema_file = Path(SCHEMA_PATH)
            temp_file = schema_file.with_suffix('.tmp')
            
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(schema, f, indent=2, ensure_ascii=False)
            
            # Rename temp file to actual file (atomic on POSIX systems)
            temp_file.replace(schema_file)
            
            self.send_json_response({
                "success": True,
                "message": "Schema saved successfully"
            })
        except json.JSONDecodeError as e:
            self.send_json_response({
                "error": f"Invalid JSON data: {str(e)}"
            }, 400)
        except Exception as e:
            self.send_json_response({
                "error": f"Error saving schema: {str(e)}"
            }, 500)
    
    def validate_schema(self):
        """Validate schema without saving"""
        try:
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            data = json.loads(body)
            
            schema = data.get('schema')
            if not schema:
                self.send_json_response({
                    "error": "No schema data provided"
                }, 400)
                return
            
            validation_result = self.validate_schema_data(schema)
            self.send_json_response(validation_result)
        except json.JSONDecodeError as e:
            self.send_json_response({
                "error": f"Invalid JSON data: {str(e)}"
            }, 400)
        except Exception as e:
            self.send_json_response({
                "error": f"Error validating schema: {str(e)}"
            }, 500)
    
    def validate_schema_data(self, schema):
        """
        Validate schema structure and content.
        Returns dict with 'valid' boolean and 'errors' list.
        """
        errors = []
        
        # Check required top-level fields
        if not isinstance(schema, dict):
            errors.append("Schema must be a JSON object")
            return {"valid": False, "errors": errors}
        
        if 'categories' not in schema:
            errors.append("Schema must have 'categories' field")
        
        if not isinstance(schema.get('categories'), list):
            errors.append("'categories' must be an array")
            return {"valid": False, "errors": errors}
        
        # Track question IDs for uniqueness check
        question_ids = set()
        category_ids = set()
        
        # Validate categories
        for cat_idx, category in enumerate(schema['categories']):
            # Use category label if available, otherwise use index
            cat_label = category.get('label', f'index {cat_idx}') if isinstance(category, dict) else f'index {cat_idx}'
            cat_path = f'categories["{cat_label}"]'
            
            if not isinstance(category, dict):
                errors.append(f"{cat_path}: must be an object")
                continue
            
            # Check required category fields
            if 'id' not in category:
                errors.append(f"{cat_path}: missing 'id' field")
            elif category['id'] in category_ids:
                errors.append(f"{cat_path}: duplicate category ID '{category['id']}'")
            else:
                category_ids.add(category['id'])
            
            if 'label' not in category:
                errors.append(f"{cat_path}: missing 'label' field")
            
            # Validate questions in category
            questions = category.get('questions', [])
            if not isinstance(questions, list):
                errors.append(f"{cat_path}.questions: must be an array")
                continue
            
            for q_idx, question in enumerate(questions):
                # Use question label or id if available, otherwise use index
                q_label = None
                if isinstance(question, dict):
                    q_label = question.get('label', question.get('id', f'index {q_idx}'))
                else:
                    q_label = f'index {q_idx}'
                q_path = f'{cat_path}.questions["{q_label}"]'
                self.validate_question(question, q_path, question_ids, errors)
        
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }
    
    def validate_question(self, question, path, question_ids, errors):
        """Validate a single question"""
        if not isinstance(question, dict):
            errors.append(f"{path}: must be an object")
            return
        
        # Check required fields
        if 'id' not in question:
            errors.append(f"{path}: missing 'id' field")
        elif question['id'] in question_ids:
            errors.append(f"{path}: duplicate question ID '{question['id']}'")
        else:
            question_ids.add(question['id'])
        
        if 'label' not in question:
            errors.append(f"{path}: missing 'label' field")
        
        if 'type' not in question:
            errors.append(f"{path}: missing 'type' field")
        else:
            # Validate question type
            valid_types = ['radio', 'multiselect', 'dropdown', 'text', 'textarea', 'number', 'checkbox']
            if question['type'] not in valid_types:
                errors.append(f"{path}: invalid question type '{question['type']}'. Valid types: {', '.join(valid_types)}")
            
            # Validate options for choice-based questions
            if question['type'] in ['radio', 'multiselect', 'dropdown']:
                if 'options' not in question:
                    errors.append(f"{path}: '{question['type']}' questions must have 'options' field")
                elif not isinstance(question.get('options'), list):
                    errors.append(f"{path}.options: must be an array")
                elif len(question.get('options', [])) == 0:
                    errors.append(f"{path}.options: must have at least one option")
                else:
                    # Validate each option
                    option_ids = set()
                    for opt_idx, option in enumerate(question['options']):
                        opt_path = f"{path}.options[{opt_idx}]"
                        if not isinstance(option, dict):
                            errors.append(f"{opt_path}: must be an object")
                            continue
                        
                        if 'id' not in option and 'label' not in option:
                            errors.append(f"{opt_path}: must have 'id' or 'label' field")
                        
                        opt_id = option.get('id', option.get('label'))
                        if opt_id in option_ids:
                            errors.append(f"{opt_path}: duplicate option ID '{opt_id}'")
                        else:
                            option_ids.add(opt_id)
        
        # Validate visibleWhen if present
        if 'visibleWhen' in question:
            if not isinstance(question['visibleWhen'], list):
                errors.append(f"{path}.visibleWhen: must be an array")
            else:
                # Validate each condition in the array
                for cond_idx, condition in enumerate(question['visibleWhen']):
                    cond_path = f"{path}.visibleWhen[{cond_idx}]"
                    if not isinstance(condition, dict):
                        errors.append(f"{cond_path}: must be an object")
                        continue
                    
                    if 'questionId' not in condition:
                        errors.append(f"{cond_path}: missing 'questionId' field")
                    elif not isinstance(condition['questionId'], str):
                        errors.append(f"{cond_path}.questionId: must be a string")
                    
                    # Support both old format (equals) and new format (operator + value)
                    has_old_format = 'equals' in condition
                    has_new_format = 'operator' in condition and 'value' in condition
                    
                    if not has_old_format and not has_new_format:
                        errors.append(f"{cond_path}: must have either 'equals' field (old format) or both 'operator' and 'value' fields (new format)")
                    
                    # Validate old format (equals field)
                    if has_old_format:
                        if not isinstance(condition['equals'], (list, str)):
                            errors.append(f"{cond_path}.equals: must be an array or string")
                        elif isinstance(condition['equals'], list) and len(condition['equals']) == 0:
                            errors.append(f"{cond_path}.equals: array must have at least one value")
                        elif isinstance(condition['equals'], str) and len(condition['equals']) == 0:
                            errors.append(f"{cond_path}.equals: string must not be empty")
                    
                    # Validate new format (operator + value fields)
                    if has_new_format:
                        valid_operators = ['equals', 'notEquals', 'contains', 'notContains', 'startsWith', 'greaterThan', 'lessThan']
                        if condition['operator'] not in valid_operators:
                            errors.append(f"{cond_path}.operator: must be one of {', '.join(valid_operators)}")
                        
                        # Value can be string, array, or number depending on operator
                        if not isinstance(condition['value'], (str, list, int, float)):
                            errors.append(f"{cond_path}.value: must be a string, number, or array")
                        elif isinstance(condition['value'], list) and len(condition['value']) == 0:
                            errors.append(f"{cond_path}.value: array must have at least one value")
                        elif isinstance(condition['value'], str) and len(condition['value']) == 0:
                            errors.append(f"{cond_path}.value: string must not be empty")
    
    def create_backup(self):
        """Create a backup of the current schema with validation warnings"""
        try:
            # Load and validate schema before backing up
            schema_file = Path(SCHEMA_PATH)
            if not schema_file.exists():
                self.send_json_response({
                    "error": "Schema file not found"
                }, 404)
                return
            
            # Load schema for validation
            with open(schema_file, 'r', encoding='utf-8') as f:
                schema = json.load(f)
            
            # Validate schema
            validation_result = self.validate_schema_data(schema)
            
            # Create backup regardless of validation status
            backup_path = self.create_backup_file()
            
            # Extract just the filename from the path
            backup_filename = Path(backup_path).name if backup_path else None
            
            # Return response with validation warnings if present
            response = {
                "success": True,
                "filename": backup_filename
            }
            
            if validation_result['valid']:
                response["message"] = f"Backup created: {backup_filename}"
            else:
                response["message"] = f"Backup created: {backup_filename} (with validation warnings)"
                response["warnings"] = validation_result['errors']
            
            self.send_json_response(response)
            
        except json.JSONDecodeError as e:
            self.send_json_response({
                "error": f"Invalid JSON in schema file: {str(e)}"
            }, 400)
        except Exception as e:
            self.send_json_response({
                "error": f"Error creating backup: {str(e)}"
            }, 500)
    
    def create_backup_file(self):
        """Create a timestamped backup of the schema file"""
        schema_file = Path(SCHEMA_PATH)
        if not schema_file.exists():
            return None
        
        # Create backups directory if it doesn't exist
        backup_dir = Path(BACKUP_DIR)
        backup_dir.mkdir(exist_ok=True)
        
        # Create timestamped backup filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"technical-design-schema_{timestamp}.json"
        backup_path = backup_dir / backup_filename
        
        # Copy the file
        shutil.copy2(schema_file, backup_path)
        
        return str(backup_path)
    
    def list_backups(self):
        """List all backup files"""
        try:
            backup_dir = Path(BACKUP_DIR)
            if not backup_dir.exists():
                self.send_json_response({"backups": []})
                return
            
            backups = []
            for backup_file in sorted(backup_dir.glob("*.json"), reverse=True):
                stat = backup_file.stat()
                backups.append({
                    "filename": backup_file.name,
                    "path": str(backup_file),
                    "size": stat.st_size,
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
                })
            
            self.send_json_response({"backups": backups})
        except Exception as e:
            self.send_json_response({
                "error": f"Error listing backups: {str(e)}"
            }, 500)
    
    def send_json_response(self, data, status=200):
        """Send a JSON response"""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode('utf-8'))
    
    def log_message(self, format, *args):
        """Override to customize log messages"""
        # Only log errors, not every request
        if args[1] != '200':
            super().log_message(format, *args)


def open_browser():
    """Open the default browser after a short delay"""
    time.sleep(1)
    webbrowser.open(f'http://localhost:{PORT}')


def main():
    """Start the HTTP server"""
    # Resolve schema path
    schema_path = Path(SCHEMA_PATH)
    if not schema_path.exists():
        print(f"WARNING: Schema file not found at {schema_path.resolve()}")
        print("The editor will still start, but you won't be able to load the schema.")
        print()
    
    # Start the server
    with socketserver.TCPServer(("", PORT), SchemaEditorHandler) as httpd:
        print("=" * 70)
        print("Technical Design Schema Editor")
        print("=" * 70)
        print(f"Server running on http://localhost:{PORT}")
        print(f"Schema file: {schema_path.resolve()}")
        print(f"Backups directory: {Path(BACKUP_DIR).resolve()}")
        print()
        print("Press Ctrl+C to stop the server")
        print("=" * 70)
        print()
        
        # Open browser in a separate thread
        browser_thread = threading.Thread(target=open_browser, daemon=True)
        browser_thread.start()
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\nShutting down server...")
            sys.exit(0)


if __name__ == "__main__":
    main()
