#!/usr/bin/env python3
"""RDD Web Interface Server.

A lightweight HTTP server providing a web-based interface for RDD framework operations.
Uses Python standard library components, binds to localhost, and provides REST-like
JSON endpoints for managing prompts and workdir operations.

Features:
  - Session token authentication for operations
  - RESTful JSON API endpoints
  - Static file serving for HTML/CSS/JS
  - Auto-opens browser on startup
  - Cross-platform (Windows/Linux)

Usage:
  python server.py [--port PORT]
"""

from __future__ import annotations

import http.server
import json
import os
import secrets
import socketserver
import subprocess
import sys
import webbrowser
from pathlib import Path
from typing import Any, Dict, Optional
from urllib.parse import parse_qs, urlparse, unquote


def _repo_root() -> Path:
    """Get the repository root directory.
    
    Returns:
        Path: Absolute path to the repository root.
    """
    # This file lives at: <repo>/.rdd/src/web/server.py
    return Path(__file__).resolve().parents[3]


def _actions_dir() -> Path:
    """Get the actions directory path.
    
    Returns:
        Path: Absolute path to the .rdd/src/actions directory.
    """
    return _repo_root() / ".rdd" / "src" / "actions"


def _markdown_to_html(markdown_text: str) -> str:
    """Convert markdown to HTML using simple pattern matching.
    
    This is a lightweight markdown converter that handles common markdown
    syntax without requiring external dependencies.
    
    Args:
        markdown_text: Markdown formatted text.
        
    Returns:
        HTML formatted text.
    """
    import re
    import html
    
    lines = markdown_text.split('\n')
    html_lines = []
    in_code_block = False
    code_language = ""
    in_list = False
    
    for line in lines:
        # Handle code blocks
        if line.strip().startswith('```'):
            if in_code_block:
                html_lines.append('</code></pre>')
                in_code_block = False
                code_language = ""
            else:
                in_code_block = True
                code_language = line.strip()[3:].strip()
                lang_class = f' class="language-{code_language}"' if code_language else ''
                html_lines.append(f'<pre{lang_class}><code>')
            continue
        
        if in_code_block:
            html_lines.append(html.escape(line))
            continue
        
        # Close list if we're not in a list item anymore
        if in_list and not line.strip().startswith(('- ', '* ', '1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.')):
            html_lines.append('</ul>')
            in_list = False
        
        # Headers
        if line.startswith('# '):
            html_lines.append(f'<h1>{html.escape(line[2:])}</h1>')
        elif line.startswith('## '):
            html_lines.append(f'<h2>{html.escape(line[3:])}</h2>')
        elif line.startswith('### '):
            html_lines.append(f'<h3>{html.escape(line[4:])}</h3>')
        elif line.startswith('#### '):
            html_lines.append(f'<h4>{html.escape(line[5:])}</h4>')
        # Bold and emphasis inline
        elif '**' in line or '_' in line or '`' in line or '[' in line:
            # Check if this is a list item first (must have space after marker)
            is_list_item = line.strip().startswith(('- ', '* '))
            if is_list_item:
                # Extract content after list marker
                content = line.strip()[2:].strip()
            else:
                content = line
            
            # Process markdown patterns and escape content
            # Strategy:
            # 1. Match markdown patterns in original text
            # 2. For each match, create HTML tag with escaped content
            # 3. For non-matched text, escape it
            # This ensures each piece of text is escaped exactly once
            
            def process_markdown(text):
                result = []
                pos = 0
                
                # Find all markdown patterns (bold, italic, code, links)
                # Combine all patterns into one regex
                pattern = r'(\*\*(.+?)\*\*)|(_(.+?)_)|(`(.+?)`)|(\[(.+?)\]\((.+?)\))'
                
                for match in re.finditer(pattern, text):
                    # Add escaped text before this match
                    if pos < match.start():
                        result.append(html.escape(text[pos:match.start()]))
                    
                    # Process the match
                    if match.group(1):  # Bold **text**
                        result.append(f'<strong>{html.escape(match.group(2))}</strong>')
                    elif match.group(3):  # Italic _text_
                        result.append(f'<em>{html.escape(match.group(4))}</em>')
                    elif match.group(5):  # Code `text`
                        result.append(f'<code>{html.escape(match.group(6))}</code>')
                    elif match.group(7):  # Link [text](url)
                        link_text = html.escape(match.group(8))
                        link_url = match.group(9)
                        result.append(f'<a href="{link_url}" target="_blank">{link_text}</a>')
                    
                    pos = match.end()
                
                # Add escaped text after the last match
                if pos < len(text):
                    result.append(html.escape(text[pos:]))
                
                return ''.join(result)
            
            content = process_markdown(content)
            
            if is_list_item:
                if not in_list:
                    html_lines.append('<ul>')
                    in_list = True
                html_lines.append(f'<li>{content}</li>')
            else:
                html_lines.append(f'<p>{content}</p>')
        # List items
        elif line.strip().startswith(('- ', '* ')):
            if not in_list:
                html_lines.append('<ul>')
                in_list = True
            html_lines.append(f'<li>{html.escape(line.strip()[2:])}</li>')
        # Empty line
        elif not line.strip():
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            html_lines.append('<br>')
        # Regular paragraph
        else:
            html_lines.append(f'<p>{html.escape(line)}</p>')
    
    # Close any open lists
    if in_list:
        html_lines.append('</ul>')
    
    return '\n'.join(html_lines)


class RDDWebHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP request handler for RDD web interface.
    
    Handles both API endpoints and static file serving.
    """
    
    # Class-level session token (generated on server startup)
    session_token: str = ""
    # Class-level shutdown flag
    shutdown_requested: bool = False
    
    def __init__(self, *args, **kwargs):
        """Initialize handler with the web directory as base."""
        web_dir = _repo_root() / ".rdd" / "src" / "web"
        super().__init__(*args, directory=str(web_dir), **kwargs)
    
    def log_message(self, format, *args):
        """Override to customize logging format."""
        sys.stderr.write(f"[{self.log_date_time_string()}] {format % args}\n")
    
    def send_json_response(self, data: Dict[str, Any], status: int = 200) -> None:
        """Send a JSON response.
        
        Args:
            data: Dictionary to send as JSON.
            status: HTTP status code.
        """
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode())
    
    def send_error_response(self, message: str, status: int = 400) -> None:
        """Send an error response.
        
        Args:
            message: Error message.
            status: HTTP status code.
        """
        self.send_json_response({"error": message}, status)
    
    def verify_session_token(self, params: Dict[str, Any]) -> bool:
        """Verify the session token from request parameters.
        
        Args:
            params: Request parameters dictionary.
            
        Returns:
            True if token is valid, False otherwise.
        """
        token_value = params.get("token", "")
        token = token_value[0] if isinstance(token_value, list) else token_value
        return token == self.session_token
    
    def execute_action(self, domain: str, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute an RDD action script.
        
        Args:
            domain: Action domain (prompt, workdir).
            action: Action name (create, list, etc.).
            params: Parameters to pass to the action.
            
        Returns:
            Dictionary with execution result.
        """
        script_name = f"{domain}_{action}.py"
        script_path = _actions_dir() / script_name
        
        if not script_path.exists():
            return {"success": False, "error": f"Action script not found: {script_name}"}
        
        # Build command arguments
        cmd = [sys.executable, str(script_path)]
        
        # Add parameters (excluding token)
        for key, value in params.items():
            if key == "token":
                continue
            if isinstance(value, list):
                value = value[0] if value else ""
            cmd.append(f"{key}={value}")
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=_repo_root()
            )
            
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def read_json_file(self, filepath: str) -> Dict[str, Any]:
        """Read a JSON file from .rdd-instance.
        
        Args:
            filepath: Relative path from .rdd-instance.
            
        Returns:
            Dictionary with file content or error.
        """
        try:
            full_path = _repo_root() / ".rdd-instance" / filepath
            if not full_path.exists():
                return {"success": False, "error": f"File not found: {filepath}"}
            
            with open(full_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            return {"success": True, "data": data}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def read_text_file(self, filepath: str) -> Dict[str, Any]:
        """Read a text file from .rdd-instance.
        
        Args:
            filepath: Relative path from .rdd-instance.
            
        Returns:
            Dictionary with file content or error.
        """
        try:
            full_path = _repo_root() / ".rdd-instance" / filepath
            if not full_path.exists():
                return {"success": False, "error": f"File not found: {filepath}"}
            
            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            return {"success": True, "content": content}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def write_text_file(self, filepath: str, content: str) -> Dict[str, Any]:
        """Write a text file to .rdd-instance.
        
        Args:
            filepath: Relative path from .rdd-instance.
            content: Content to write.
            
        Returns:
            Dictionary with result.
        """
        try:
            full_path = _repo_root() / ".rdd-instance" / filepath
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
            
            return {"success": True, "message": "File saved successfully"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def do_GET(self):
        """Handle GET requests."""
        parsed = urlparse(self.path)
        path = parsed.path
        params = parse_qs(parsed.query)
        
        # API endpoints
        if path == "/api/token":
            # Return session token for authentication
            self.send_json_response({"token": self.session_token})
            return
        
        elif path == "/api/registry":
            # Get work iteration registry
            result = self.read_json_file("workdir/work-iteration-registry.json")
            
            # Add git-enabled from instance config
            if result.get("success"):
                config_result = self.read_json_file("config/instance-config.json")
                if config_result.get("success"):
                    # Inject git-enabled into registry data for backward compatibility
                    result["data"]["git-enabled"] = config_result["data"].get("git-enabled", False)
                else:
                    # Config file missing - use default
                    result["data"]["git-enabled"] = False
            
            self.send_json_response(result)
            return
        
        elif path == "/api/snippets":
            # Get prompt snippets from manifest.json
            try:
                manifest_path = _repo_root() / ".rdd" / "config" / "manifest.json"
                if not manifest_path.exists():
                    self.send_error_response("Manifest file not found")
                    return
                
                with open(manifest_path, "r", encoding="utf-8") as f:
                    manifest = json.load(f)
                
                snippets = []
                prompt_snippets = manifest.get("promptSnippets", [])
                
                for snippet_def in prompt_snippets:
                    key = snippet_def.get("prompt-snippet-key", "")
                    path_str = snippet_def.get("prompt-snippet-path", "")
                    
                    if not key or not path_str:
                        continue
                    
                    # Read snippet content
                    snippet_path = _repo_root() / path_str
                    content = ""
                    description = ""
                    
                    if snippet_path.exists():
                        try:
                            with open(snippet_path, "r", encoding="utf-8") as sf:
                                content = sf.read()
                                # Use first line as description (if it's not too long)
                                first_line = content.split('\n')[0].strip()
                                if len(first_line) < 100:
                                    description = first_line
                                else:
                                    description = key.replace("[[[", "").replace("]]]", "")
                        except Exception as e:
                            content = f"Error reading file: {str(e)}"
                    else:
                        content = "File not found"
                    
                    snippets.append({
                        "key": key,
                        "path": path_str,
                        "description": description,
                        "content": content
                    })
                
                self.send_json_response({"success": True, "snippets": snippets})
            except Exception as e:
                self.send_error_response(f"Failed to load snippets: {str(e)}")
            return
        
        elif path == "/api/config":
            # Get instance config
            result = self.read_json_file("config/instance-config.json")
            self.send_json_response(result)
            return
        
        elif path == "/api/help/user-guide":
            # Get user guide as rendered HTML
            try:
                user_guide_path = _repo_root() / ".rdd" / "docs" / "user-guide.md"
                if not user_guide_path.exists():
                    self.send_error_response("User guide file not found")
                    return
                
                with open(user_guide_path, "r", encoding="utf-8") as f:
                    markdown_content = f.read()
                
                html_content = _markdown_to_html(markdown_content)
                self.send_json_response({"success": True, "html": html_content})
            except Exception as e:
                self.send_error_response(f"Failed to load user guide: {str(e)}")
            return
        
        elif path == "/api/technical-design/schema":
            # Get technical design schema
            try:
                schema_path = _repo_root() / ".rdd" / "config" / "technical-design-schema.json"
                if not schema_path.exists():
                    self.send_error_response("Schema file not found")
                    return
                
                with open(schema_path, "r", encoding="utf-8") as f:
                    schema = json.load(f)
                
                self.send_json_response({"success": True, "schema": schema})
            except Exception as e:
                self.send_error_response(f"Failed to load schema: {str(e)}")
            return
        
        elif path == "/api/technical-design/answers":
            # Get technical design answers
            script_path = _actions_dir() / "technical_design_read.py"
            if not script_path.exists():
                self.send_error_response("technical_design_read.py not found")
                return
            
            try:
                result = subprocess.run(
                    [sys.executable, str(script_path)],
                    capture_output=True,
                    text=True,
                    cwd=_repo_root()
                )
                
                if result.returncode == 0:
                    answers = json.loads(result.stdout) if result.stdout.strip() else {}
                    self.send_json_response({"success": True, "answers": answers})
                else:
                    self.send_error_response(f"Failed to read answers: {result.stderr}")
            except Exception as e:
                self.send_error_response(f"Failed to read answers: {str(e)}")
            return
        
        elif path == "/README.md":
            # Serve README.md as HTML for help modals
            try:
                readme_path = _repo_root() / "README.md"
                if not readme_path.exists():
                    self.send_error(404, "README.md not found")
                    return
                
                with open(readme_path, "r", encoding="utf-8") as f:
                    markdown_content = f.read()
                
                html_content = _markdown_to_html(markdown_content)
                
                # Create a simple HTML page with the content
                full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RDD Framework - User Guide</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {{ padding: 20px; max-width: 900px; margin: 0 auto; }}
        pre {{ background-color: #f5f5f5; padding: 15px; border-radius: 5px; overflow-x: auto; }}
        code {{ background-color: #f5f5f5; padding: 2px 6px; border-radius: 3px; }}
        h1, h2, h3, h4 {{ margin-top: 1.5em; margin-bottom: 0.5em; }}
    </style>
</head>
<body>
    <div class="container">
        {html_content}
    </div>
</body>
</html>"""
                
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", len(full_html.encode('utf-8')))
                self.end_headers()
                self.wfile.write(full_html.encode('utf-8'))
            except Exception as e:
                self.send_error(500, f"Failed to load README: {str(e)}")
            return
        
        elif path.startswith("/api/file/"):
            # Read a file
            if not self.verify_session_token(params):
                self.send_error_response("Invalid session token", 403)
                return
            
            filepath = unquote(path[10:])  # Remove "/api/file/" and decode URL encoding
            if filepath.endswith(".json"):
                result = self.read_json_file(filepath)
            else:
                result = self.read_text_file(filepath)
            self.send_json_response(result)
            return
        
        # Serve static files
        elif path == "/":
            # Serve index.html
            self.path = "/templates/index.html"
        
        return super().do_GET()
    
    def do_POST(self):
        """Handle POST requests."""
        parsed = urlparse(self.path)
        path = parsed.path
        
        # Read POST data
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length).decode("utf-8")
        
        try:
            params = json.loads(post_data)
        except json.JSONDecodeError:
            self.send_error_response("Invalid JSON in request body")
            return
        
        # Handle shutdown before token verification to allow graceful shutdown
        if path == "/api/shutdown":
            # Verify session token for shutdown
            if not self.verify_session_token(params):
                self.send_error_response("Invalid session token", 403)
                return
            # Shutdown the server
            print("\nShutdown request received from Web UI")
            RDDWebHandler.shutdown_requested = True
            self.send_json_response({"success": True, "message": "Server shutdown initiated"})
            return
        
        # Verify session token for all other POST requests
        if not self.verify_session_token(params):
            self.send_error_response("Invalid session token", 403)
            return
        
        # API endpoints
        if path == "/api/action":
            # Execute an action
            domain = params.get("domain", "")
            action = params.get("action", "")
            action_params = params.get("params", {})
            
            if not domain or not action:
                self.send_error_response("Missing domain or action")
                return
            
            result = self.execute_action(domain, action, action_params)
            self.send_json_response(result)
            return
        
        elif path == "/api/technical-design/answer/set":
            # Set technical design answer
            question_id = params.get("questionId", "")
            question_type = params.get("type", "")
            value = params.get("value", "")
            rationale = params.get("rationale", "")
            
            if not question_id or not question_type or value == "":
                self.send_error_response("Missing questionId, type, or value")
                return
            
            script_path = _actions_dir() / "technical_design_answer_set.py"
            if not script_path.exists():
                self.send_error_response("technical_design_answer_set.py not found")
                return
            
            # Build command
            cmd = [sys.executable, str(script_path)]
            cmd.append(f"questionId={question_id}")
            cmd.append(f"type={question_type}")
            
            # Handle value based on type
            if question_type == "multiselect" and isinstance(value, list):
                cmd.append(f"value={','.join(value)}")
            else:
                cmd.append(f"value={value}")
            
            if rationale:
                cmd.append(f"rationale={rationale}")
            
            try:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    cwd=_repo_root()
                )
                
                if result.returncode == 0:
                    self.send_json_response(json.loads(result.stdout))
                else:
                    error_data = json.loads(result.stderr) if result.stderr.strip() else {"error": "Unknown error"}
                    self.send_json_response(error_data)
            except Exception as e:
                self.send_error_response(f"Failed to set answer: {str(e)}")
            return
        
        elif path == "/api/technical-design/answer/remove":
            # Remove technical design answer
            question_id = params.get("questionId", "")
            
            if not question_id:
                self.send_error_response("Missing questionId")
                return
            
            script_path = _actions_dir() / "technical_design_answer_remove.py"
            if not script_path.exists():
                self.send_error_response("technical_design_answer_remove.py not found")
                return
            
            try:
                result = subprocess.run(
                    [sys.executable, str(script_path), f"questionId={question_id}"],
                    capture_output=True,
                    text=True,
                    cwd=_repo_root()
                )
                
                if result.returncode == 0:
                    self.send_json_response(json.loads(result.stdout))
                else:
                    error_data = json.loads(result.stderr) if result.stderr.strip() else {"error": "Unknown error"}
                    self.send_json_response(error_data)
            except Exception as e:
                self.send_error_response(f"Failed to remove answer: {str(e)}")
            return
        
        elif path == "/api/technical-design/validate":
            # Validate technical design answers
            script_path = _actions_dir() / "technical_design_validate.py"
            if not script_path.exists():
                self.send_error_response("technical_design_validate.py not found")
                return
            
            try:
                result = subprocess.run(
                    [sys.executable, str(script_path)],
                    capture_output=True,
                    text=True,
                    cwd=_repo_root()
                )
                
                if result.returncode == 0:
                    self.send_json_response(json.loads(result.stdout))
                else:
                    # Validation failed - return validation errors
                    error_data = json.loads(result.stderr) if result.stderr.strip() else {"valid": False, "error": "Unknown error"}
                    self.send_json_response(error_data)
            except Exception as e:
                self.send_error_response(f"Failed to validate: {str(e)}")
            return
        
        elif path == "/api/technical-design/migrate":
            # Migrate technical design format
            script_path = _actions_dir() / "technical_design_migrate.py"
            if not script_path.exists():
                self.send_error_response("technical_design_migrate.py not found")
                return
            
            try:
                result = subprocess.run(
                    [sys.executable, str(script_path)],
                    capture_output=True,
                    text=True,
                    cwd=_repo_root()
                )
                
                if result.returncode == 0:
                    self.send_json_response(json.loads(result.stdout))
                else:
                    error_data = json.loads(result.stderr) if result.stderr.strip() else {"error": "Unknown error"}
                    self.send_json_response(error_data)
            except Exception as e:
                self.send_error_response(f"Failed to migrate: {str(e)}")
            return
        
        elif path == "/api/config/save":
            # Save instance config
            git_enabled = params.get("gitEnabled", False)
            
            try:
                config_path = _repo_root() / ".rdd-instance" / "config" / "instance-config.json"
                config_data = {"git-enabled": git_enabled}
                
                with open(config_path, 'w', encoding='utf-8') as f:
                    json.dump(config_data, f, indent=2)
                
                self.send_json_response({"success": True, "message": "Configuration saved successfully"})
            except Exception as e:
                self.send_error_response(f"Failed to save configuration: {str(e)}")
            return
        
        elif path == "/api/file/save":
            # Save a file
            filepath = params.get("filepath", "")
            content = params.get("content", "")
            
            if not filepath:
                self.send_error_response("Missing filepath")
                return
            
            result = self.write_text_file(filepath, content)
            self.send_json_response(result)
            return
        
        elif path == "/api/modification/create":
            # Create a modification
            description = params.get("description", "")
            
            if not description:
                self.send_error_response("Missing description")
                return
            
            result = self.execute_action("modification", "create", {"description": description})
            self.send_json_response(result)
            return
        
        elif path == "/api/modification/list":
            # List modifications
            result = self.execute_action("modification", "list", {})
            
            # If successful, try to parse and enhance the output
            if result.get("success"):
                try:
                    # Try to read the modifications-log.json file
                    registry_path = _repo_root() / ".rdd-instance" / "workdir" / "work-iteration-registry.json"
                    if registry_path.exists():
                        with open(registry_path, 'r', encoding='utf-8') as f:
                            registry = json.load(f)
                        
                        # Find active prompt
                        active_prompt = None
                        for prompt in registry.get('prompts', []):
                            if prompt.get('state') == 'active':
                                active_prompt = prompt
                                break
                        
                        if active_prompt:
                            prompt_id = active_prompt.get('prompt-id')
                            prompt_title = active_prompt.get('prompt-title', '')
                            
                            # Find prompt folder
                            workdir = _repo_root() / ".rdd-instance" / "workdir"
                            prompt_folder = None
                            for item in workdir.iterdir():
                                if item.is_dir() and item.name.startswith(f"{prompt_id}_"):
                                    prompt_folder = item
                                    break
                            
                            if prompt_folder:
                                modifications_log_file = prompt_folder / "modifications-log.json"
                                if modifications_log_file.exists():
                                    with open(modifications_log_file, 'r', encoding='utf-8') as f:
                                        modifications_log = json.load(f)
                                    
                                    # Read descriptions from modification files
                                    modifications = []
                                    for mod in modifications_log.get('modifications', []):
                                        mod_id = mod.get('modification-id')
                                        mod_file = prompt_folder / f"modification-{mod_id}.md"
                                        description = ""
                                        if mod_file.exists():
                                            with open(mod_file, 'r', encoding='utf-8') as f:
                                                description = f.read().strip()
                                        
                                        modifications.append({
                                            'modification-id': mod_id,
                                            'created': mod.get('created'),
                                            'status': mod.get('status'),
                                            'completed': mod.get('completed'),
                                            'description': description
                                        })
                                    
                                    result['modifications'] = modifications
                except Exception as e:
                    # If parsing fails, just return the basic result
                    result['parse_error'] = str(e)
            
            self.send_json_response(result)
            return
        
        elif path == "/api/modification/update":
            # Update a modification
            modification_id = params.get("modificationId", "")
            description = params.get("description", "")
            
            if not modification_id or not description:
                self.send_error_response("Missing modificationId or description")
                return
            
            try:
                # Find active prompt
                registry_path = _repo_root() / ".rdd-instance" / "workdir" / "work-iteration-registry.json"
                if not registry_path.exists():
                    self.send_error_response("Work iteration registry not found")
                    return
                
                with open(registry_path, 'r', encoding='utf-8') as f:
                    registry = json.load(f)
                
                active_prompt = None
                for prompt in registry.get('prompts', []):
                    if prompt.get('state') == 'active':
                        active_prompt = prompt
                        break
                
                if not active_prompt:
                    self.send_error_response("No active prompt found")
                    return
                
                prompt_id = active_prompt.get('prompt-id')
                prompt_title = active_prompt.get('prompt-title', '')
                
                # Find prompt folder
                workdir = _repo_root() / ".rdd-instance" / "workdir"
                prompt_folder = None
                for item in workdir.iterdir():
                    if item.is_dir() and item.name.startswith(f"{prompt_id}_"):
                        prompt_folder = item
                        break
                
                if not prompt_folder:
                    self.send_error_response("Prompt folder not found")
                    return
                
                # Update modification file
                mod_file = prompt_folder / f"modification-{modification_id}.md"
                if not mod_file.exists():
                    self.send_error_response(f"Modification {modification_id} not found")
                    return
                
                with open(mod_file, 'w', encoding='utf-8') as f:
                    f.write(description)
                
                self.send_json_response({"success": True, "message": "Modification updated successfully"})
            except Exception as e:
                self.send_error_response(f"Failed to update modification: {str(e)}")
            return
        
        else:
            self.send_error_response("Unknown endpoint", 404)
    
    def do_OPTIONS(self):
        """Handle OPTIONS requests for CORS."""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()


def main() -> int:
    """Start the RDD web server.
    
    Returns:
        Exit code (0 for success, 1 for error).
    """
    # Parse command line arguments
    port = 8080
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            if arg.startswith("--port="):
                try:
                    port = int(arg.split("=", 1)[1])
                except ValueError:
                    print(f"ERROR: Invalid port number: {arg}", file=sys.stderr)
                    return 1
    
    # Run seed script to ensure RDD instance structure is initialized
    print("Initializing RDD instance structure...")
    seed_script = _repo_root() / ".rdd" / "src" / "actions" / "rdd-instance_seed.py"
    try:
        result = subprocess.run(
            [sys.executable, str(seed_script)],
            capture_output=True,
            text=True,
            cwd=_repo_root()
        )
        
        # Print seed script output
        if result.stdout:
            print(result.stdout)
        
        if result.returncode != 0:
            print(f"ERROR: RDD instance seeding failed", file=sys.stderr)
            if result.stderr:
                print(result.stderr, file=sys.stderr)
            print("Remediation: Check the error messages above and ensure the framework is properly installed.", file=sys.stderr)
            return 1
        
    except Exception as e:
        print(f"ERROR: Failed to run seed script: {e}", file=sys.stderr)
        print("Remediation: Ensure .rdd/src/actions/rdd-instance_seed.py exists and is executable.", file=sys.stderr)
        return 1
    
    print()
    
    # Generate session token
    session_token = secrets.token_urlsafe(32)
    RDDWebHandler.session_token = session_token
    RDDWebHandler.shutdown_requested = False  # Reset shutdown flag
    
    # Create server with socket reuse
    try:
        # Allow immediate socket reuse to prevent "Address already in use" errors
        socketserver.TCPServer.allow_reuse_address = True
        with socketserver.TCPServer(("127.0.0.1", port), RDDWebHandler) as httpd:
            url = f"http://127.0.0.1:{port}/"
            print(f"RDD Web Interface")
            print(f"=================")
            print(f"Server running at: {url}")
            print(f"Session token: {session_token}")
            print()
            print("Press Ctrl+C to stop the server")
            print()
            
            # Open browser
            try:
                webbrowser.open(url)
                print(f"Browser opened at {url}")
            except Exception as e:
                print(f"Could not open browser automatically: {e}")
                print(f"Please open {url} manually")
            
            # Serve requests with shutdown check
            httpd.timeout = 0.5  # Check for shutdown every 0.5 seconds
            while not RDDWebHandler.shutdown_requested:
                httpd.handle_request()
            
            # Explicitly shutdown the server
            httpd.server_close()
            print("Server stopped")
            return 0
    
    except KeyboardInterrupt:
        print("\nServer stopped")
        return 0
    except OSError as e:
        print(f"ERROR: Could not start server: {e}", file=sys.stderr)
        print(f"Remediation: Check if port {port} is already in use", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"ERROR: Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
