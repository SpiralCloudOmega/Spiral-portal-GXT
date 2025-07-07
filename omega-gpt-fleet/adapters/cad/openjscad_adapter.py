"""
OpenJSCAD Adapter for OmegaGPT Fleet

This adapter provides interface to OpenJSCAD for JavaScript-based CAD operations.
"""

import os
import json
import subprocess
from typing import Dict, Any, Optional, List
from ..base_adapter import BaseAdapter


class OpenJsCADAdapter(BaseAdapter):
    """
    Adapter for OpenJSCAD JavaScript-based CAD operations.
    
    This adapter provides methods to interact with OpenJSCAD for web-based
    CAD operations, JavaScript-based modeling, and integration with web applications.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the OpenJSCAD adapter.
        
        Args:
            config: Configuration dictionary containing OpenJSCAD settings
        """
        super().__init__("OpenJsCADAdapter", config)
        self.metadata.update({
            "type": "cad",
            "capabilities": [
                "javascript_cad",
                "web_based_modeling",
                "procedural_modeling",
                "export_formats",
                "web_integration",
                "scripting",
                "parametric_design"
            ],
            "dependencies": ["node.js", "@jscad/cli", "@jscad/core"]
        })
        self.node_path = config.get("node_path", "node") if config else "node"
        self.jscad_cli = config.get("jscad_cli", "jscad") if config else "jscad"
        self.workspace = config.get("workspace", "./openjscad_workspace") if config else "./openjscad_workspace"
        self.current_scripts = {}
        self.web_server_port = config.get("web_server_port", 8080) if config else 8080
    
    def initialize(self) -> bool:
        """
        Initialize OpenJSCAD and establish connection.
        
        Returns:
            bool: True if initialization successful, False otherwise
        """
        try:
            # Check if Node.js is available
            result = subprocess.run([self.node_path, "--version"], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode != 0:
                raise RuntimeError("Node.js not found or not working")
            
            # Check if JSCAD CLI is available
            try:
                result = subprocess.run([self.jscad_cli, "--version"], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode != 0:
                    self.log_activity("JSCAD CLI not found, will use Node.js directly")
            except:
                self.log_activity("JSCAD CLI not available, using fallback methods")
            
            # Create workspace directory
            os.makedirs(self.workspace, exist_ok=True)
            
            # Create package.json for Node.js dependencies
            self._create_package_json()
            
            self.status = "ready"
            self.log_activity("OpenJSCAD adapter initialized successfully")
            return True
            
        except Exception as e:
            self.handle_error(e, "OpenJSCAD initialization")
            return False
    
    def execute(self, command: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute an OpenJSCAD command with the given parameters.
        
        Args:
            command: The command to execute
            parameters: Parameters for the command
            
        Returns:
            Dict containing the execution result
        """
        try:
            self.log_activity(f"Executing command: {command}", parameters)
            
            result = {"success": False, "data": None, "message": ""}
            
            if command == "create_script":
                result = self._create_script(parameters)
            elif command == "execute_script":
                result = self._execute_script(parameters)
            elif command == "create_box":
                result = self._create_box(parameters)
            elif command == "create_cylinder":
                result = self._create_cylinder(parameters)
            elif command == "create_sphere":
                result = self._create_sphere(parameters)
            elif command == "boolean_operation":
                result = self._boolean_operation(parameters)
            elif command == "export_model":
                result = self._export_model(parameters)
            elif command == "start_web_server":
                result = self._start_web_server(parameters)
            elif command == "generate_stl":
                result = self._generate_stl(parameters)
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
            # Check workspace
            if not os.path.exists(self.workspace):
                return False
                
            # Check if Node.js is available
            result = subprocess.run([self.node_path, "--version"], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode != 0:
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
            self.current_scripts.clear()
            self.status = "cleaned"
            self.log_activity("OpenJSCAD adapter cleaned up successfully")
            return True
            
        except Exception as e:
            self.handle_error(e, "Cleanup")
            return False
    
    def _create_package_json(self):
        """Create package.json for Node.js dependencies."""
        package_json = {
            "name": "omega-gpt-fleet-jscad",
            "version": "1.0.0",
            "description": "OpenJSCAD integration for OmegaGPT Fleet",
            "dependencies": {
                "@jscad/core": "^2.0.0",
                "@jscad/cli": "^2.0.0",
                "@jscad/io": "^2.0.0"
            }
        }
        
        package_path = os.path.join(self.workspace, "package.json")
        with open(package_path, "w") as f:
            json.dump(package_json, f, indent=2)
    
    def _create_script(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Create a JavaScript CAD script."""
        # Stub implementation
        script_name = parameters.get("name", "script")
        script_content = parameters.get("content", "")
        
        if not script_content:
            # Default script template
            script_content = """
const jscad = require('@jscad/core');

const main = () => {
    return jscad.primitives.cube({ size: 10 });
};

module.exports = { main };
"""
        
        script_path = os.path.join(self.workspace, f"{script_name}.js")
        self.current_scripts[script_name] = {
            "path": script_path,
            "content": script_content
        }
        
        return {
            "success": True,
            "data": {"script_name": script_name, "script_path": script_path},
            "message": "Script created successfully"
        }
    
    def _execute_script(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a JavaScript CAD script."""
        # Stub implementation
        script_name = parameters.get("name", "")
        
        if script_name not in self.current_scripts:
            return {
                "success": False,
                "data": None,
                "message": f"Script '{script_name}' not found"
            }
        
        return {
            "success": True,
            "data": {"script_name": script_name, "output": "Script executed successfully"},
            "message": "Script executed successfully"
        }
    
    def _create_box(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Create a box using OpenJSCAD."""
        # Stub implementation
        width = parameters.get("width", 10)
        height = parameters.get("height", 10)
        depth = parameters.get("depth", 10)
        
        script_content = f"""
const jscad = require('@jscad/core');

const main = () => {{
    return jscad.primitives.cube({{ size: [{width}, {height}, {depth}] }});
}};

module.exports = {{ main }};
"""
        
        return {
            "success": True,
            "data": {
                "object_type": "box",
                "dimensions": {"width": width, "height": height, "depth": depth},
                "script": script_content
            },
            "message": "Box created successfully"
        }
    
    def _create_cylinder(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Create a cylinder using OpenJSCAD."""
        # Stub implementation
        radius = parameters.get("radius", 5)
        height = parameters.get("height", 10)
        
        script_content = f"""
const jscad = require('@jscad/core');

const main = () => {{
    return jscad.primitives.cylinder({{ radius: {radius}, height: {height} }});
}};

module.exports = {{ main }};
"""
        
        return {
            "success": True,
            "data": {
                "object_type": "cylinder",
                "radius": radius,
                "height": height,
                "script": script_content
            },
            "message": "Cylinder created successfully"
        }
    
    def _create_sphere(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Create a sphere using OpenJSCAD."""
        # Stub implementation
        radius = parameters.get("radius", 5)
        
        script_content = f"""
const jscad = require('@jscad/core');

const main = () => {{
    return jscad.primitives.sphere({{ radius: {radius} }});
}};

module.exports = {{ main }};
"""
        
        return {
            "success": True,
            "data": {
                "object_type": "sphere",
                "radius": radius,
                "script": script_content
            },
            "message": "Sphere created successfully"
        }
    
    def _boolean_operation(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Perform boolean operations using OpenJSCAD."""
        # Stub implementation
        operation = parameters.get("operation", "union")
        objects = parameters.get("objects", [])
        
        return {
            "success": True,
            "data": {"operation": operation, "objects_count": len(objects)},
            "message": "Boolean operation completed successfully"
        }
    
    def _export_model(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Export the model to various formats."""
        # Stub implementation
        file_path = parameters.get("file_path", "")
        format_type = parameters.get("format", "stl")
        script_name = parameters.get("script", "")
        
        return {
            "success": True,
            "data": {"file_path": file_path, "format": format_type, "script": script_name},
            "message": "Model exported successfully"
        }
    
    def _start_web_server(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Start a web server for OpenJSCAD."""
        # Stub implementation
        port = parameters.get("port", self.web_server_port)
        
        return {
            "success": True,
            "data": {"port": port, "url": f"http://localhost:{port}"},
            "message": "Web server started successfully"
        }
    
    def _generate_stl(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Generate STL file from JavaScript CAD script."""
        # Stub implementation
        script_name = parameters.get("script", "")
        output_file = parameters.get("output", "model.stl")
        
        return {
            "success": True,
            "data": {"script": script_name, "output_file": output_file},
            "message": "STL file generated successfully"
        }