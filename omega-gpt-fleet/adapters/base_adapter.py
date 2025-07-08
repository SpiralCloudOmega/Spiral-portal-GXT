"""
Base Adapter Class for OmegaGPT Fleet

This module provides the base class that all adapters should inherit from.
It defines the standard interface and common functionality.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
import logging
import json
from datetime import datetime


class BaseAdapter(ABC):
    """
    Base class for all OmegaGPT Fleet adapters.
    
    This class provides the standard interface that all adapters must implement,
    along with common functionality for logging, configuration, and error handling.
    """
    
    def __init__(self, name: str, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the adapter.
        
        Args:
            name: The name of the adapter
            config: Optional configuration dictionary
        """
        self.name = name
        self.config = config or {}
        self.logger = logging.getLogger(f"omega_gpt_fleet.{name}")
        self.status = "initialized"
        self.last_activity = datetime.now()
        self.metadata = {
            "version": "1.0.0",
            "type": "base",
            "capabilities": [],
            "dependencies": []
        }
    
    @abstractmethod
    def initialize(self) -> bool:
        """
        Initialize the adapter and establish connections.
        
        Returns:
            bool: True if initialization successful, False otherwise
        """
        pass
    
    @abstractmethod
    def execute(self, command: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a command with the given parameters.
        
        Args:
            command: The command to execute
            parameters: Parameters for the command
            
        Returns:
            Dict containing the execution result
        """
        pass
    
    @abstractmethod
    def validate(self) -> bool:
        """
        Validate that the adapter is properly configured and ready.
        
        Returns:
            bool: True if validation passes, False otherwise
        """
        pass
    
    @abstractmethod
    def cleanup(self) -> bool:
        """
        Clean up resources and connections.
        
        Returns:
            bool: True if cleanup successful, False otherwise
        """
        pass
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get the current status of the adapter.
        
        Returns:
            Dict containing status information
        """
        return {
            "name": self.name,
            "status": self.status,
            "last_activity": self.last_activity.isoformat(),
            "metadata": self.metadata
        }
    
    def log_activity(self, activity: str, details: Optional[Dict[str, Any]] = None):
        """
        Log an activity with optional details.
        
        Args:
            activity: Description of the activity
            details: Optional additional details
        """
        self.last_activity = datetime.now()
        log_entry = {
            "timestamp": self.last_activity.isoformat(),
            "activity": activity,
            "adapter": self.name
        }
        if details:
            log_entry["details"] = details
        
        self.logger.info(json.dumps(log_entry))
    
    def handle_error(self, error: Exception, context: str = ""):
        """
        Handle errors in a standardized way.
        
        Args:
            error: The exception that occurred
            context: Additional context about where the error occurred
        """
        error_info = {
            "timestamp": datetime.now().isoformat(),
            "adapter": self.name,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "context": context
        }
        
        self.logger.error(json.dumps(error_info))
        self.status = "error"
    
    def get_capabilities(self) -> List[str]:
        """
        Get the list of capabilities supported by this adapter.
        
        Returns:
            List of capability strings
        """
        return self.metadata.get("capabilities", [])
    
    def get_dependencies(self) -> List[str]:
        """
        Get the list of dependencies required by this adapter.
        
        Returns:
            List of dependency strings
        """
        return self.metadata.get("dependencies", [])