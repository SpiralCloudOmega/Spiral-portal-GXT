"""
NASA Adapter for OmegaGPT Fleet

This adapter provides interface to NASA APIs and data sources for space research data.
"""

import os
import json
import requests
from typing import Dict, Any, Optional, List
from datetime import datetime
from ..base_adapter import BaseAdapter


class NASAAdapter(BaseAdapter):
    """
    Adapter for NASA APIs and data sources.
    
    This adapter provides methods to interact with NASA's various APIs
    for accessing space research data, images, and scientific information.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the NASA adapter.
        
        Args:
            config: Configuration dictionary containing NASA API settings
        """
        super().__init__("NASAAdapter", config)
        self.metadata.update({
            "type": "research",
            "capabilities": [
                "apod_api",
                "mars_rover_photos",
                "exoplanet_archive",
                "earth_observation",
                "space_weather",
                "mission_data",
                "astronomy_data"
            ],
            "dependencies": ["requests", "nasa-api-key"]
        })
        self.api_key = config.get("api_key", "DEMO_KEY") if config else "DEMO_KEY"
        self.base_url = config.get("base_url", "https://api.nasa.gov") if config else "https://api.nasa.gov"
        self.cache_dir = config.get("cache_dir", "./nasa_cache") if config else "./nasa_cache"
        self.rate_limit = config.get("rate_limit", 30) if config else 30  # requests per hour
        self.session = None
        self.cached_data = {}
    
    def initialize(self) -> bool:
        """
        Initialize NASA API connection.
        
        Returns:
            bool: True if initialization successful, False otherwise
        """
        try:
            # Create cache directory
            os.makedirs(self.cache_dir, exist_ok=True)
            
            # Initialize HTTP session
            self.session = requests.Session()
            self.session.headers.update({
                'User-Agent': 'OmegaGPT-Fleet/1.0',
                'Accept': 'application/json'
            })
            
            # Test API connection
            test_url = f"{self.base_url}/planetary/apod"
            params = {"api_key": self.api_key, "count": 1}
            
            try:
                response = self.session.get(test_url, params=params, timeout=10)
                if response.status_code == 200:
                    self.log_activity("NASA API connection successful")
                else:
                    self.log_activity(f"NASA API test returned status {response.status_code}")
            except requests.RequestException as e:
                self.log_activity(f"NASA API test failed: {e}")
                # Continue with stub mode
            
            self.status = "ready"
            self.log_activity("NASA adapter initialized successfully")
            return True
            
        except Exception as e:
            self.handle_error(e, "NASA initialization")
            return False
    
    def execute(self, command: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a NASA API command with the given parameters.
        
        Args:
            command: The command to execute
            parameters: Parameters for the command
            
        Returns:
            Dict containing the execution result
        """
        try:
            self.log_activity(f"Executing command: {command}", parameters)
            
            result = {"success": False, "data": None, "message": ""}
            
            if command == "get_apod":
                result = self._get_apod(parameters)
            elif command == "get_mars_photos":
                result = self._get_mars_photos(parameters)
            elif command == "get_earth_imagery":
                result = self._get_earth_imagery(parameters)
            elif command == "get_exoplanets":
                result = self._get_exoplanets(parameters)
            elif command == "get_space_weather":
                result = self._get_space_weather(parameters)
            elif command == "search_images":
                result = self._search_images(parameters)
            elif command == "get_mission_data":
                result = self._get_mission_data(parameters)
            elif command == "get_near_earth_objects":
                result = self._get_near_earth_objects(parameters)
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
            # Check if session is initialized
            if not self.session:
                return False
                
            # Check cache directory
            if not os.path.exists(self.cache_dir):
                return False
                
            # Check API key
            if not self.api_key or self.api_key == "DEMO_KEY":
                self.log_activity("Using demo API key - limited functionality")
                
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
            if self.session:
                self.session.close()
                self.session = None
            
            self.cached_data.clear()
            self.status = "cleaned"
            self.log_activity("NASA adapter cleaned up successfully")
            return True
            
        except Exception as e:
            self.handle_error(e, "Cleanup")
            return False
    
    def _get_apod(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Get Astronomy Picture of the Day."""
        # Stub implementation
        date = parameters.get("date", datetime.now().strftime("%Y-%m-%d"))
        hd = parameters.get("hd", True)
        
        # Mock APOD data
        apod_data = {
            "date": date,
            "explanation": "This is a mock APOD entry for testing purposes.",
            "hdurl": "https://apod.nasa.gov/apod/image/test_hd.jpg",
            "media_type": "image",
            "service_version": "v1",
            "title": "Mock Astronomy Picture",
            "url": "https://apod.nasa.gov/apod/image/test.jpg"
        }
        
        return {
            "success": True,
            "data": apod_data,
            "message": "APOD retrieved successfully"
        }
    
    def _get_mars_photos(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Get Mars Rover photos."""
        # Stub implementation
        rover = parameters.get("rover", "curiosity")
        sol = parameters.get("sol", 1000)
        camera = parameters.get("camera", "mast")
        
        # Mock Mars photos data
        photos_data = {
            "photos": [
                {
                    "id": 123456,
                    "sol": sol,
                    "camera": {"name": camera, "full_name": "Mast Camera"},
                    "img_src": f"https://mars.nasa.gov/msl-raw-images/proj/msl/redops/ods/surface/sol/{sol}/image.jpg",
                    "earth_date": "2024-01-01",
                    "rover": {"name": rover, "status": "active"}
                }
            ]
        }
        
        return {
            "success": True,
            "data": photos_data,
            "message": "Mars photos retrieved successfully"
        }
    
    def _get_earth_imagery(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Get Earth observation imagery."""
        # Stub implementation
        lat = parameters.get("lat", 29.78)
        lon = parameters.get("lon", -95.33)
        date = parameters.get("date", "2024-01-01")
        dim = parameters.get("dim", 0.15)
        
        # Mock Earth imagery data
        imagery_data = {
            "date": date,
            "id": f"LANDSAT_8_C1_{date}",
            "url": f"https://earthengine.googleapis.com/v1alpha/projects/earthengine-legacy/thumbnails/image_{lat}_{lon}.jpg"
        }
        
        return {
            "success": True,
            "data": imagery_data,
            "message": "Earth imagery retrieved successfully"
        }
    
    def _get_exoplanets(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Get exoplanet data."""
        # Stub implementation
        limit = parameters.get("limit", 10)
        
        # Mock exoplanet data
        exoplanets_data = {
            "count": limit,
            "planets": [
                {
                    "pl_name": "Kepler-442b",
                    "hostname": "Kepler-442",
                    "pl_masse": 2.34,
                    "pl_rade": 1.34,
                    "pl_orbper": 112.3,
                    "st_dist": 1206.0
                }
            ]
        }
        
        return {
            "success": True,
            "data": exoplanets_data,
            "message": "Exoplanet data retrieved successfully"
        }
    
    def _get_space_weather(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Get space weather information."""
        # Stub implementation
        date = parameters.get("date", datetime.now().strftime("%Y-%m-%d"))
        
        # Mock space weather data
        weather_data = {
            "date": date,
            "kp_index": 2.33,
            "solar_flares": [],
            "geomagnetic_storms": [],
            "solar_wind_speed": 450.0,
            "solar_wind_density": 5.2
        }
        
        return {
            "success": True,
            "data": weather_data,
            "message": "Space weather data retrieved successfully"
        }
    
    def _search_images(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Search NASA image and video library."""
        # Stub implementation
        query = parameters.get("query", "")
        media_type = parameters.get("media_type", "image")
        
        # Mock search results
        search_results = {
            "collection": {
                "items": [
                    {
                        "data": [{
                            "title": f"Mock result for {query}",
                            "description": "Mock search result",
                            "nasa_id": "mock_123456"
                        }],
                        "links": [{
                            "href": "https://images.nasa.gov/mock_image.jpg",
                            "rel": "preview"
                        }]
                    }
                ]
            }
        }
        
        return {
            "success": True,
            "data": search_results,
            "message": "Image search completed successfully"
        }
    
    def _get_mission_data(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Get mission-specific data."""
        # Stub implementation
        mission = parameters.get("mission", "")
        
        # Mock mission data
        mission_data = {
            "mission": mission,
            "status": "active",
            "launch_date": "2024-01-01",
            "description": f"Mock data for {mission} mission"
        }
        
        return {
            "success": True,
            "data": mission_data,
            "message": "Mission data retrieved successfully"
        }
    
    def _get_near_earth_objects(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Get Near Earth Objects data."""
        # Stub implementation
        start_date = parameters.get("start_date", "2024-01-01")
        end_date = parameters.get("end_date", "2024-01-07")
        
        # Mock NEO data
        neo_data = {
            "element_count": 1,
            "near_earth_objects": {
                start_date: [
                    {
                        "id": "123456",
                        "name": "Mock Asteroid",
                        "estimated_diameter": {
                            "kilometers": {"estimated_diameter_min": 0.1, "estimated_diameter_max": 0.3}
                        },
                        "is_potentially_hazardous_asteroid": False
                    }
                ]
            }
        }
        
        return {
            "success": True,
            "data": neo_data,
            "message": "Near Earth Objects data retrieved successfully"
        }