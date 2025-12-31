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


class RDDWebHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP request handler for RDD web interface.
    
    Handles both API endpoints and static file serving.
    """
    
    # Class-level session token (generated on server startup)
    session_token: str = ""
    
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
        token = params.get("token", [""])[0] if isinstance(params.get("token"), list) else params.get("token", "")
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
            self.send_json_response(result)
            return
        
        elif path == "/api/prompts-list":
            # List all prompts
            result = self.execute_action("prompt", "list", {})
            self.send_json_response(result)
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
        
        # Verify session token for all POST requests
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
    
    # Generate session token
    session_token = secrets.token_urlsafe(32)
    RDDWebHandler.session_token = session_token
    
    # Create server
    try:
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
            
            # Serve requests
            httpd.serve_forever()
    
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
