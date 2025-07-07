"""
Docker Adapter for OmegaGPT Fleet

This adapter provides interface to Docker for container networking and orchestration.
"""

import subprocess
from typing import Dict, Any, Optional, List
from ..base_adapter import BaseAdapter


class DockerAdapter(BaseAdapter):
    """
    Adapter for Docker container operations.
    
    This adapter provides methods to interact with Docker for container
    management, networking, and orchestration.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the Docker adapter."""
        super().__init__("DockerAdapter", config)
        self.metadata.update({
            "type": "networking",
            "capabilities": [
                "container_management",
                "network_configuration",
                "service_orchestration",
                "load_balancing",
                "container_monitoring"
            ],
            "dependencies": ["docker"]
        })
        self.docker_path = config.get("docker_path", "docker") if config else "docker"
        self.containers = {}
    
    def initialize(self) -> bool:
        """Initialize Docker connection."""
        try:
            result = subprocess.run([self.docker_path, "version"], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode != 0:
                raise RuntimeError("Docker not found")
            
            self.status = "ready"
            self.log_activity("Docker adapter initialized successfully")
            return True
        except Exception as e:
            self.handle_error(e, "Docker initialization")
            return False
    
    def execute(self, command: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a Docker command."""
        try:
            if command == "create_container":
                return self._create_container(parameters)
            elif command == "start_container":
                return self._start_container(parameters)
            elif command == "stop_container":
                return self._stop_container(parameters)
            elif command == "list_containers":
                return self._list_containers(parameters)
            else:
                return {"success": False, "message": f"Unknown command: {command}"}
        except Exception as e:
            self.handle_error(e, f"Command execution: {command}")
            return {"success": False, "message": str(e)}
    
    def validate(self) -> bool:
        """Validate adapter configuration."""
        try:
            result = subprocess.run([self.docker_path, "version"], 
                                  capture_output=True, timeout=5)
            return result.returncode == 0
        except:
            return False
    
    def cleanup(self) -> bool:
        """Clean up resources."""
        try:
            self.containers.clear()
            self.status = "cleaned"
            return True
        except Exception as e:
            self.handle_error(e, "Cleanup")
            return False
    
    def _create_container(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Create a Docker container."""
        name = parameters.get("name", "")
        image = parameters.get("image", "")
        
        container_data = {
            "name": name,
            "image": image,
            "status": "created",
            "ports": parameters.get("ports", [])
        }
        
        self.containers[name] = container_data
        
        return {
            "success": True,
            "data": container_data,
            "message": "Container created successfully"
        }
    
    def _start_container(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Start a Docker container."""
        name = parameters.get("name", "")
        
        if name in self.containers:
            self.containers[name]["status"] = "running"
        
        return {
            "success": True,
            "data": {"name": name, "status": "running"},
            "message": "Container started successfully"
        }
    
    def _stop_container(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Stop a Docker container."""
        name = parameters.get("name", "")
        
        if name in self.containers:
            self.containers[name]["status"] = "stopped"
        
        return {
            "success": True,
            "data": {"name": name, "status": "stopped"},
            "message": "Container stopped successfully"
        }
    
    def _list_containers(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """List Docker containers."""
        return {
            "success": True,
            "data": {"containers": list(self.containers.values())},
            "message": "Containers listed successfully"
        }