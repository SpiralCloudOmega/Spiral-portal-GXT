"""
Notion Sync Agent for ΩΔ143 Codex Drift 5D Capsule

Provides bidirectional synchronization with Notion databases and pages,
enabling seamless integration of capsule data with Notion workspaces.
"""

import asyncio
import json
import uuid
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import aiohttp
import hashlib

# Import the omega-gpt-fleet base adapter
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'omega-gpt-fleet'))

from adapters.base_adapter import BaseAdapter


@dataclass
class NotionPage:
    """Represents a Notion page with metadata."""
    page_id: str
    title: str
    parent_id: Optional[str]
    created_time: datetime
    last_edited_time: datetime
    properties: Dict[str, Any]
    content_blocks: List[Dict[str, Any]] = field(default_factory=list)
    url: Optional[str] = None


@dataclass
class NotionDatabase:
    """Represents a Notion database with schema."""
    database_id: str
    title: str
    properties: Dict[str, Any]
    created_time: datetime
    last_edited_time: datetime
    url: Optional[str] = None


@dataclass
class SyncMapping:
    """Defines mapping between capsule data and Notion objects."""
    mapping_id: str
    capsule_component: str
    notion_object_id: str
    notion_object_type: str  # 'page' or 'database'
    sync_direction: str  # 'bidirectional', 'capsule_to_notion', 'notion_to_capsule'
    field_mappings: Dict[str, str]
    last_sync: Optional[datetime] = None
    sync_status: str = "pending"


class NotionSyncAgent(BaseAdapter):
    """
    Notion synchronization agent for the ΩΔ143 Codex Drift system.
    
    Enables bidirectional synchronization between capsule components
    and Notion databases, pages, and blocks.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the Notion sync agent."""
        super().__init__("NotionSyncAgent", config)
        self.metadata.update({
            "type": "notion_sync",
            "capabilities": [
                "notion_api_integration",
                "bidirectional_sync",
                "database_management",
                "page_management",
                "block_management",
                "real_time_updates"
            ],
            "dependencies": ["aiohttp", "notion-client"]
        })
        
        # Notion API configuration
        self.notion_token = config.get("notion_token", "") if config else ""
        self.notion_version = config.get("notion_version", "2022-06-28") if config else "2022-06-28"
        self.base_url = "https://api.notion.com/v1"
        
        # Sync configuration
        self.sync_mappings: Dict[str, SyncMapping] = {}
        self.sync_interval = config.get("sync_interval", 300) if config else 300  # 5 minutes
        self.max_retries = config.get("max_retries", 3) if config else 3
        self.batch_size = config.get("batch_size", 100) if config else 100
        
        # State tracking
        self.sync_active = False
        self.last_sync_time = None
        self.sync_statistics = {
            "total_syncs": 0,
            "successful_syncs": 0,
            "failed_syncs": 0,
            "pages_synced": 0,
            "databases_synced": 0
        }
        
        # HTTP session
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def initialize(self) -> bool:
        """Initialize the Notion sync agent."""
        try:
            if not self.notion_token:
                self.log_activity("ERROR: Notion token not provided")
                return False
            
            # Create HTTP session
            headers = {
                "Authorization": f"Bearer {self.notion_token}",
                "Notion-Version": self.notion_version,
                "Content-Type": "application/json"
            }
            
            self.session = aiohttp.ClientSession(
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=30)
            )
            
            # Test connection
            if not await self._test_connection():
                return False
            
            # Load existing sync mappings
            await self._load_sync_mappings()
            
            # Start sync loop
            self.sync_active = True
            asyncio.create_task(self._sync_loop())
            
            self.log_activity("Notion sync agent initialized successfully")
            return True
            
        except Exception as e:
            self.log_activity(f"ERROR: Failed to initialize Notion sync agent: {e}")
            return False
    
    async def _test_connection(self) -> bool:
        """Test connection to Notion API."""
        try:
            url = f"{self.base_url}/users/me"
            
            async with self.session.get(url) as response:
                if response.status == 200:
                    user_data = await response.json()
                    self.log_activity(f"Connected to Notion as user: {user_data.get('name', 'Unknown')}")
                    return True
                else:
                    self.log_activity(f"ERROR: Notion API connection failed with status {response.status}")
                    return False
                    
        except Exception as e:
            self.log_activity(f"ERROR: Failed to test Notion connection: {e}")
            return False
    
    async def _load_sync_mappings(self):
        """Load existing sync mappings from configuration."""
        # In a real implementation, this would load from persistent storage
        # For now, we'll create some default mappings
        
        # Example mapping for ScrollMath Engine data
        scrollmath_mapping = SyncMapping(
            mapping_id="scrollmath_to_notion",
            capsule_component="scrollmath_engine",
            notion_object_id="",  # To be set when database is created
            notion_object_type="database",
            sync_direction="bidirectional",
            field_mappings={
                "field_id": "Field ID",
                "vector_count": "Vector Count",
                "drift_coefficient": "Drift Coefficient",
                "field_strength": "Field Strength",
                "magnitude": "Magnitude",
                "created_at": "Created"
            }
        )
        
        self.sync_mappings["scrollmath_engine"] = scrollmath_mapping
    
    async def create_notion_database(self, 
                                   parent_page_id: str,
                                   title: str,
                                   properties: Dict[str, Any]) -> Optional[str]:
        """Create a new Notion database."""
        try:
            url = f"{self.base_url}/databases"
            
            payload = {
                "parent": {"page_id": parent_page_id},
                "title": [{"text": {"content": title}}],
                "properties": properties
            }
            
            async with self.session.post(url, json=payload) as response:
                if response.status == 200:
                    database_data = await response.json()
                    database_id = database_data["id"]
                    self.log_activity(f"Created Notion database: {title} ({database_id})")
                    return database_id
                else:
                    error_data = await response.json()
                    self.log_activity(f"ERROR: Failed to create database: {error_data}")
                    return None
                    
        except Exception as e:
            self.log_activity(f"ERROR: Failed to create Notion database: {e}")
            return None
    
    async def create_notion_page(self, 
                               parent_id: str,
                               title: str,
                               properties: Dict[str, Any] = None,
                               content_blocks: List[Dict[str, Any]] = None) -> Optional[str]:
        """Create a new Notion page."""
        try:
            url = f"{self.base_url}/pages"
            
            payload = {
                "parent": {"database_id": parent_id},
                "properties": properties or {},
                "children": content_blocks or []
            }
            
            # Add title if provided
            if title:
                payload["properties"]["title"] = {
                    "title": [{"text": {"content": title}}]
                }
            
            async with self.session.post(url, json=payload) as response:
                if response.status == 200:
                    page_data = await response.json()
                    page_id = page_data["id"]
                    self.log_activity(f"Created Notion page: {title} ({page_id})")
                    return page_id
                else:
                    error_data = await response.json()
                    self.log_activity(f"ERROR: Failed to create page: {error_data}")
                    return None
                    
        except Exception as e:
            self.log_activity(f"ERROR: Failed to create Notion page: {e}")
            return None
    
    async def get_notion_database(self, database_id: str) -> Optional[NotionDatabase]:
        """Retrieve a Notion database by ID."""
        try:
            url = f"{self.base_url}/databases/{database_id}"
            
            async with self.session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return NotionDatabase(
                        database_id=data["id"],
                        title=data["title"][0]["text"]["content"] if data["title"] else "",
                        properties=data["properties"],
                        created_time=datetime.fromisoformat(data["created_time"].replace('Z', '+00:00')),
                        last_edited_time=datetime.fromisoformat(data["last_edited_time"].replace('Z', '+00:00')),
                        url=data.get("url")
                    )
                else:
                    self.log_activity(f"ERROR: Failed to get database {database_id}: {response.status}")
                    return None
                    
        except Exception as e:
            self.log_activity(f"ERROR: Failed to get Notion database: {e}")
            return None
    
    async def query_notion_database(self, 
                                  database_id: str,
                                  filter_conditions: Dict[str, Any] = None,
                                  sorts: List[Dict[str, Any]] = None) -> List[NotionPage]:
        """Query pages from a Notion database."""
        try:
            url = f"{self.base_url}/databases/{database_id}/query"
            
            payload = {}
            if filter_conditions:
                payload["filter"] = filter_conditions
            if sorts:
                payload["sorts"] = sorts
            
            pages = []
            has_more = True
            next_cursor = None
            
            while has_more:
                if next_cursor:
                    payload["start_cursor"] = next_cursor
                
                async with self.session.post(url, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        for page_data in data["results"]:
                            page = NotionPage(
                                page_id=page_data["id"],
                                title=self._extract_title_from_properties(page_data["properties"]),
                                parent_id=page_data["parent"]["database_id"],
                                created_time=datetime.fromisoformat(page_data["created_time"].replace('Z', '+00:00')),
                                last_edited_time=datetime.fromisoformat(page_data["last_edited_time"].replace('Z', '+00:00')),
                                properties=page_data["properties"],
                                url=page_data.get("url")
                            )
                            pages.append(page)
                        
                        has_more = data["has_more"]
                        next_cursor = data.get("next_cursor")
                    else:
                        self.log_activity(f"ERROR: Failed to query database: {response.status}")
                        break
            
            return pages
            
        except Exception as e:
            self.log_activity(f"ERROR: Failed to query Notion database: {e}")
            return []
    
    def _extract_title_from_properties(self, properties: Dict[str, Any]) -> str:
        """Extract title from Notion page properties."""
        for prop_name, prop_value in properties.items():
            if prop_value.get("type") == "title":
                title_parts = prop_value.get("title", [])
                if title_parts:
                    return title_parts[0].get("text", {}).get("content", "")
        return ""
    
    async def sync_capsule_to_notion(self, component_name: str, data: Dict[str, Any]) -> bool:
        """Sync capsule component data to Notion."""
        try:
            if component_name not in self.sync_mappings:
                self.log_activity(f"No sync mapping found for component: {component_name}")
                return False
            
            mapping = self.sync_mappings[component_name]
            
            if mapping.sync_direction == "notion_to_capsule":
                return True  # Skip if sync direction is only from Notion
            
            # Create or update Notion database/page based on mapping
            if mapping.notion_object_type == "database":
                success = await self._sync_data_to_database(mapping, data)
            else:
                success = await self._sync_data_to_page(mapping, data)
            
            if success:
                mapping.last_sync = datetime.now()
                mapping.sync_status = "success"
                self.sync_statistics["successful_syncs"] += 1
                self.sync_statistics["total_syncs"] += 1
            else:
                mapping.sync_status = "failed"
                self.sync_statistics["failed_syncs"] += 1
                self.sync_statistics["total_syncs"] += 1
            
            return success
            
        except Exception as e:
            self.log_activity(f"ERROR: Failed to sync {component_name} to Notion: {e}")
            return False
    
    async def _sync_data_to_database(self, mapping: SyncMapping, data: Dict[str, Any]) -> bool:
        """Sync data to a Notion database."""
        try:
            if not mapping.notion_object_id:
                # Create database if it doesn't exist
                # This would require a parent page ID from configuration
                return False
            
            # Convert capsule data to Notion page properties
            properties = {}
            for capsule_field, notion_field in mapping.field_mappings.items():
                if capsule_field in data:
                    properties[notion_field] = self._convert_to_notion_property(
                        data[capsule_field], notion_field
                    )
            
            # Create or update page in database
            page_id = await self.create_notion_page(
                parent_id=mapping.notion_object_id,
                title=f"Capsule Data - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                properties=properties
            )
            
            if page_id:
                self.sync_statistics["pages_synced"] += 1
                return True
            else:
                return False
                
        except Exception as e:
            self.log_activity(f"ERROR: Failed to sync data to database: {e}")
            return False
    
    async def _sync_data_to_page(self, mapping: SyncMapping, data: Dict[str, Any]) -> bool:
        """Sync data to a Notion page."""
        try:
            # Convert data to Notion blocks
            blocks = []
            
            # Add heading
            blocks.append({
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"text": {"content": f"Capsule Component: {mapping.capsule_component}"}}]
                }
            })
            
            # Add data as code block
            blocks.append({
                "type": "code",
                "code": {
                    "rich_text": [{"text": {"content": json.dumps(data, indent=2)}}],
                    "language": "json"
                }
            })
            
            # Update page content
            url = f"{self.base_url}/blocks/{mapping.notion_object_id}/children"
            payload = {"children": blocks}
            
            async with self.session.patch(url, json=payload) as response:
                if response.status == 200:
                    self.sync_statistics["pages_synced"] += 1
                    return True
                else:
                    self.log_activity(f"ERROR: Failed to update page: {response.status}")
                    return False
                    
        except Exception as e:
            self.log_activity(f"ERROR: Failed to sync data to page: {e}")
            return False
    
    def _convert_to_notion_property(self, value: Any, property_name: str) -> Dict[str, Any]:
        """Convert a value to a Notion property format."""
        if isinstance(value, str):
            return {
                "rich_text": [{"text": {"content": value}}]
            }
        elif isinstance(value, (int, float)):
            return {
                "number": value
            }
        elif isinstance(value, bool):
            return {
                "checkbox": value
            }
        elif isinstance(value, datetime):
            return {
                "date": {"start": value.isoformat()}
            }
        else:
            return {
                "rich_text": [{"text": {"content": str(value)}}]
            }
    
    async def sync_notion_to_capsule(self, component_name: str) -> Optional[Dict[str, Any]]:
        """Sync Notion data to capsule component."""
        try:
            if component_name not in self.sync_mappings:
                self.log_activity(f"No sync mapping found for component: {component_name}")
                return None
            
            mapping = self.sync_mappings[component_name]
            
            if mapping.sync_direction == "capsule_to_notion":
                return None  # Skip if sync direction is only to Notion
            
            # Retrieve data from Notion
            if mapping.notion_object_type == "database":
                pages = await self.query_notion_database(mapping.notion_object_id)
                
                # Convert pages to capsule data format
                capsule_data = []
                for page in pages:
                    page_data = {}
                    for notion_field, capsule_field in mapping.field_mappings.items():
                        if notion_field in page.properties:
                            page_data[capsule_field] = self._extract_property_value(
                                page.properties[notion_field]
                            )
                    capsule_data.append(page_data)
                
                return {"pages": capsule_data}
            
            return None
            
        except Exception as e:
            self.log_activity(f"ERROR: Failed to sync {component_name} from Notion: {e}")
            return None
    
    def _extract_property_value(self, property_data: Dict[str, Any]) -> Any:
        """Extract value from Notion property data."""
        prop_type = property_data.get("type")
        
        if prop_type == "title":
            title_parts = property_data.get("title", [])
            return title_parts[0].get("text", {}).get("content", "") if title_parts else ""
        elif prop_type == "rich_text":
            text_parts = property_data.get("rich_text", [])
            return text_parts[0].get("text", {}).get("content", "") if text_parts else ""
        elif prop_type == "number":
            return property_data.get("number", 0)
        elif prop_type == "checkbox":
            return property_data.get("checkbox", False)
        elif prop_type == "date":
            date_data = property_data.get("date")
            if date_data and date_data.get("start"):
                return datetime.fromisoformat(date_data["start"].replace('Z', '+00:00'))
            return None
        else:
            return str(property_data)
    
    async def _sync_loop(self):
        """Main synchronization loop."""
        while self.sync_active:
            try:
                self.log_activity("Starting sync cycle")
                
                # Sync each mapped component
                for component_name, mapping in self.sync_mappings.items():
                    # This would integrate with actual capsule components
                    # For now, we'll simulate with dummy data
                    dummy_data = {
                        "timestamp": datetime.now().isoformat(),
                        "component": component_name,
                        "status": "active"
                    }
                    
                    await self.sync_capsule_to_notion(component_name, dummy_data)
                
                self.last_sync_time = datetime.now()
                self.log_activity("Sync cycle completed")
                
                await asyncio.sleep(self.sync_interval)
                
            except Exception as e:
                self.log_activity(f"ERROR: Sync loop error: {e}")
                await asyncio.sleep(60)  # Wait before retrying
    
    async def execute(self, command: str, parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute a sync command."""
        parameters = parameters or {}
        
        if command == "sync_component":
            component_name = parameters.get("component_name")
            data = parameters.get("data", {})
            
            if component_name:
                success = await self.sync_capsule_to_notion(component_name, data)
                return {
                    "success": success,
                    "message": f"Sync {'completed' if success else 'failed'} for {component_name}"
                }
            else:
                return {"success": False, "message": "Component name required"}
        
        elif command == "get_sync_status":
            return {
                "success": True,
                "data": {
                    "sync_active": self.sync_active,
                    "last_sync": self.last_sync_time.isoformat() if self.last_sync_time else None,
                    "statistics": self.sync_statistics.copy(),
                    "mappings": len(self.sync_mappings)
                }
            }
        
        elif command == "create_database":
            parent_page_id = parameters.get("parent_page_id")
            title = parameters.get("title")
            properties = parameters.get("properties", {})
            
            if parent_page_id and title:
                database_id = await self.create_notion_database(parent_page_id, title, properties)
                return {
                    "success": database_id is not None,
                    "data": {"database_id": database_id}
                }
            else:
                return {"success": False, "message": "Parent page ID and title required"}
        
        else:
            return {"success": False, "message": f"Unknown command: {command}"}
    
    async def validate(self) -> bool:
        """Validate the sync agent configuration."""
        try:
            # Check Notion token
            if not self.notion_token:
                return False
            
            # Test API connection
            return await self._test_connection()
            
        except Exception:
            return False
    
    async def cleanup(self):
        """Clean up resources."""
        try:
            self.sync_active = False
            
            if self.session:
                await self.session.close()
                self.session = None
            
            self.log_activity("Notion sync agent cleaned up")
            
        except Exception as e:
            self.log_activity(f"ERROR: Cleanup failed: {e}")
    
    def get_sync_statistics(self) -> Dict[str, Any]:
        """Get sync statistics."""
        return {
            "statistics": self.sync_statistics.copy(),
            "mappings": {
                mapping_id: {
                    "component": mapping.capsule_component,
                    "notion_object_type": mapping.notion_object_type,
                    "sync_direction": mapping.sync_direction,
                    "last_sync": mapping.last_sync.isoformat() if mapping.last_sync else None,
                    "status": mapping.sync_status
                }
                for mapping_id, mapping in self.sync_mappings.items()
            },
            "last_sync_time": self.last_sync_time.isoformat() if self.last_sync_time else None
        }