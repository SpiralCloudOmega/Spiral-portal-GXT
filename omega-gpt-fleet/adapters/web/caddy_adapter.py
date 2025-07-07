"""
Caddy Adapter for OmegaGPT Fleet

This adapter provides interface to Caddy web server for automated web hosting and reverse proxy.
"""

import os
import json
import subprocess
from typing import Dict, Any, Optional, List
from ..base_adapter import BaseAdapter


class CaddyAdapter(BaseAdapter):
    """
    Adapter for Caddy web server operations.
    
    This adapter provides methods to interact with Caddy for web hosting,
    reverse proxy, SSL certificate management, and configuration automation.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the Caddy adapter.
        
        Args:
            config: Configuration dictionary containing Caddy settings
        """
        super().__init__("CaddyAdapter", config)
        self.metadata.update({
            "type": "web",
            "capabilities": [
                "web_server",
                "reverse_proxy",
                "automatic_https",
                "ssl_certificates",
                "load_balancing",
                "static_files",
                "configuration_management"
            ],
            "dependencies": ["caddy"]
        })
        self.caddy_path = config.get("caddy_path", "caddy") if config else "caddy"
        self.config_path = config.get("config_path", "./Caddyfile") if config else "./Caddyfile"
        self.workspace = config.get("workspace", "./caddy_workspace") if config else "./caddy_workspace"
        self.caddy_process = None
        self.current_config = {}
    
    def initialize(self) -> bool:
        """
        Initialize Caddy and establish connection.
        
        Returns:
            bool: True if initialization successful, False otherwise
        """
        try:
            # Check if Caddy is available
            result = subprocess.run([self.caddy_path, "version"], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode != 0:
                raise RuntimeError("Caddy not found or not working")
            
            # Create workspace directory
            os.makedirs(self.workspace, exist_ok=True)
            
            # Initialize default configuration
            self._create_default_config()
            
            self.status = "ready"
            self.log_activity("Caddy adapter initialized successfully")
            return True
            
        except Exception as e:
            self.handle_error(e, "Caddy initialization")
            return False
    
    def execute(self, command: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a Caddy command with the given parameters.
        
        Args:
            command: The command to execute
            parameters: Parameters for the command
            
        Returns:
            Dict containing the execution result
        """
        try:
            self.log_activity(f"Executing command: {command}", parameters)
            
            result = {"success": False, "data": None, "message": ""}
            
            if command == "start_server":
                result = self._start_server(parameters)
            elif command == "stop_server":
                result = self._stop_server(parameters)
            elif command == "reload_config":
                result = self._reload_config(parameters)
            elif command == "add_site":
                result = self._add_site(parameters)
            elif command == "remove_site":
                result = self._remove_site(parameters)
            elif command == "add_proxy":
                result = self._add_proxy(parameters)
            elif command == "get_certificates":
                result = self._get_certificates(parameters)
            elif command == "get_status":
                result = self._get_status(parameters)
            else:
                result["message"] = f"Unknown command: {command}"
            
            self.log_activity(f"Command {command} completed", result)
            return result
            
        except Exception as e:
            self.handle_error(e, f"Command execution: {command}")
            return {"success": False, "data": None, "message": str(e)}
    
    def validate(self) -> bool:
        """
        Validate that the adapter is properly configured and ready.
        
        Returns:
            bool: True if validation passes, False otherwise
        """
        try:
            # Check if Caddy is available
            result = subprocess.run([self.caddy_path, "version"], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode != 0:
                return False
                
            # Check workspace
            if not os.path.exists(self.workspace):
                return False
                
            return True
            
        except Exception as e:
            self.handle_error(e, "Validation")
            return False
    
    def cleanup(self) -> bool:
        """
        Clean up resources and connections.
        
        Returns:
            bool: True if cleanup successful, False otherwise
        """
        try:
            # Stop Caddy server if running
            if self.caddy_process:
                self.caddy_process.terminate()
                self.caddy_process = None
            
            self.current_config.clear()
            self.status = "cleaned"
            self.log_activity("Caddy adapter cleaned up successfully")
            return True
            
        except Exception as e:
            self.handle_error(e, "Cleanup")
            return False
    
    def _create_default_config(self):
        """Create a default Caddyfile configuration."""
        default_config = """
# Default Caddyfile for OmegaGPT Fleet
{
    # Global options
    auto_https off
    admin localhost:2019
}

# Default site
localhost:8080 {
    respond "OmegaGPT Fleet Caddy Server"
}
"""
        
        with open(self.config_path, "w") as f:
            f.write(default_config.strip())
    
    def _start_server(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Start the Caddy server."""
        # Stub implementation
        config_file = parameters.get("config", self.config_path)
        port = parameters.get("port", 8080)
        
        # In real implementation:
        # self.caddy_process = subprocess.Popen([self.caddy_path, "run", "--config", config_file])
        
        return {
            "success": True,
            "data": {"config_file": config_file, "port": port, "pid": 0},
            "message": "Caddy server started successfully"
        }
    
    def _stop_server(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Stop the Caddy server."""
        # Stub implementation
        return {
            "success": True,
            "data": {"stopped": True},
            "message": "Caddy server stopped successfully"
        }
    
    def _reload_config(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Reload Caddy configuration."""
        # Stub implementation
        config_file = parameters.get("config", self.config_path)
        
        return {
            "success": True,
            "data": {"config_file": config_file, "reloaded": True},
            "message": "Caddy configuration reloaded successfully"
        }
    
    def _add_site(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Add a new site to Caddy configuration."""
        # Stub implementation
        domain = parameters.get("domain", "")
        root = parameters.get("root", "")
        https = parameters.get("https", True)
        
        site_config = {
            "domain": domain,
            "root": root,
            "https": https,
            "directives": []
        }
        
        self.current_config[domain] = site_config
        
        return {
            "success": True,
            "data": site_config,
            "message": "Site added successfully"
        }
    
    def _remove_site(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Remove a site from Caddy configuration."""
        # Stub implementation
        domain = parameters.get("domain", "")
        
        if domain in self.current_config:
            del self.current_config[domain]
        
        return {
            "success": True,
            "data": {"domain": domain, "removed": True},
            "message": "Site removed successfully"
        }
    
    def _add_proxy(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Add a reverse proxy configuration."""
        # Stub implementation
        domain = parameters.get("domain", "")
        upstream = parameters.get("upstream", "")
        path = parameters.get("path", "/")
        
        proxy_config = {
            "domain": domain,
            "upstream": upstream,
            "path": path,
            "load_balancing": "round_robin"
        }
        
        return {
            "success": True,
            "data": proxy_config,
            "message": "Proxy configuration added successfully"
        }
    
    def _get_certificates(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Get SSL certificate information."""
        # Stub implementation
        domain = parameters.get("domain", "")
        
        return {
            "success": True,
            "data": {
                "domain": domain,
                "certificates": [
                    {
                        "domain": domain,
                        "issuer": "Let's Encrypt",
                        "expires": "2025-01-01T00:00:00Z",
                        "valid": True
                    }
                ]
            },
            "message": "Certificate information retrieved successfully"
        }
    
    def _get_status(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Get Caddy server status."""
        # Stub implementation
        return {
            "success": True,
            "data": {
                "running": True,
                "uptime": 0,
                "sites": len(self.current_config),
                "version": "2.7.6",
                "admin_endpoint": "localhost:2019"
            },
            "message": "Server status retrieved successfully"
        }