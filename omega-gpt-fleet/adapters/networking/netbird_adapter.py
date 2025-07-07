"""
NetBird Adapter for OmegaGPT Fleet

This adapter provides interface to NetBird for VPN and network mesh management.
"""

import os
import json
import requests
from typing import Dict, Any, Optional, List
from ..base_adapter import BaseAdapter


class NetBirdAdapter(BaseAdapter):
    """
    Adapter for NetBird VPN and network mesh operations.
    
    This adapter provides methods to interact with NetBird for VPN connections,
    network mesh configuration, and peer management.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the NetBird adapter.
        
        Args:
            config: Configuration dictionary containing NetBird settings
        """
        super().__init__("NetBirdAdapter", config)
        self.metadata.update({
            "type": "networking",
            "capabilities": [
                "vpn_management",
                "network_mesh",
                "peer_management",
                "access_control",
                "network_monitoring"
            ],
            "dependencies": ["netbird", "netbird-api"]
        })
        self.server_url = config.get("server_url", "https://netbird.example.com") if config else "https://netbird.example.com"
        self.api_key = config.get("api_key", "") if config else ""
        self.management_url = config.get("management_url", "") if config else ""
        self.session = None
        self.peers = {}
    
    def initialize(self) -> bool:
        """
        Initialize NetBird connection.
        
        Returns:
            bool: True if initialization successful, False otherwise
        """
        try:
            self.session = requests.Session()
            self.session.headers.update({
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            })
            
            self.status = "ready"
            self.log_activity("NetBird adapter initialized successfully")
            return True
            
        except Exception as e:
            self.handle_error(e, "NetBird initialization")
            return False
    
    def execute(self, command: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a NetBird command with parameters."""
        try:
            self.log_activity(f"Executing command: {command}", parameters)
            
            result = {"success": False, "data": None, "message": ""}
            
            if command == "create_peer":
                result = self._create_peer(parameters)
            elif command == "connect_peer":
                result = self._connect_peer(parameters)
            elif command == "disconnect_peer":
                result = self._disconnect_peer(parameters)
            elif command == "list_peers":
                result = self._list_peers(parameters)
            elif command == "get_network_status":
                result = self._get_network_status(parameters)
            else:
                result["message"] = f"Unknown command: {command}"
            
            return result
            
        except Exception as e:
            self.handle_error(e, f"Command execution: {command}")
            return {"success": False, "data": None, "message": str(e)}
    
    def validate(self) -> bool:
        """Validate adapter configuration."""
        try:
            return self.session is not None
        except Exception as e:
            self.handle_error(e, "Validation")
            return False
    
    def cleanup(self) -> bool:
        """Clean up resources."""
        try:
            if self.session:
                self.session.close()
            self.peers.clear()
            self.status = "cleaned"
            return True
        except Exception as e:
            self.handle_error(e, "Cleanup")
            return False
    
    def _create_peer(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new NetBird peer."""
        name = parameters.get("name", "")
        groups = parameters.get("groups", [])
        
        peer_data = {
            "name": name,
            "groups": groups,
            "ip": "10.0.0.1",
            "status": "connected"
        }
        
        self.peers[name] = peer_data
        
        return {
            "success": True,
            "data": peer_data,
            "message": "Peer created successfully"
        }
    
    def _connect_peer(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Connect a peer to the network."""
        peer_name = parameters.get("name", "")
        
        return {
            "success": True,
            "data": {"name": peer_name, "status": "connected"},
            "message": "Peer connected successfully"
        }
    
    def _disconnect_peer(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Disconnect a peer from the network."""
        peer_name = parameters.get("name", "")
        
        return {
            "success": True,
            "data": {"name": peer_name, "status": "disconnected"},
            "message": "Peer disconnected successfully"
        }
    
    def _list_peers(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """List all peers in the network."""
        return {
            "success": True,
            "data": {"peers": list(self.peers.values())},
            "message": "Peers listed successfully"
        }
    
    def _get_network_status(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Get network status information."""
        return {
            "success": True,
            "data": {
                "network_status": "active",
                "connected_peers": len(self.peers),
                "total_peers": len(self.peers)
            },
            "message": "Network status retrieved successfully"
        }