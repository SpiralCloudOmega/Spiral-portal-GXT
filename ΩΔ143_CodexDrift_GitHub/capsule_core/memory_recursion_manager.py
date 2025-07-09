"""
Memory Recursion Manager for ΩΔ143 Codex Drift 5D Capsule

Handles memory recursion, pattern storage, and recursive
computation across the 5D symbolic field space.
"""

import json
import pickle
import hashlib
import numpy as np
from typing import Dict, List, Any, Optional, Union, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import deque
import asyncio

from .scrollmath_engine import ScrollVector, CodexDriftField
from .symbolic_field_computer import SymbolicField, SymbolicExpression


@dataclass
class MemoryFragment:
    """Represents a fragment of memory in the recursion system."""
    fragment_id: str
    content: Any
    context_vector: ScrollVector
    timestamp: datetime
    access_count: int = 0
    importance: float = 1.0
    parent_fragments: List[str] = field(default_factory=list)
    child_fragments: List[str] = field(default_factory=list)
    
    def update_access(self):
        """Update access statistics."""
        self.access_count += 1
        # Decay importance over time
        time_decay = (datetime.now() - self.timestamp).total_seconds() / 86400  # days
        self.importance *= max(0.1, 1.0 - time_decay * 0.01)


@dataclass 
class RecursionLayer:
    """Represents a layer in the memory recursion hierarchy."""
    layer_id: str
    depth: int
    fragments: Dict[str, MemoryFragment]
    coherence_threshold: float = 0.5
    max_fragments: int = 1000
    
    def add_fragment(self, fragment: MemoryFragment) -> bool:
        """Add a memory fragment to this layer."""
        if len(self.fragments) >= self.max_fragments:
            # Remove least important fragment
            least_important = min(self.fragments.values(), 
                                key=lambda f: f.importance * f.access_count)
            del self.fragments[least_important.fragment_id]
        
        self.fragments[fragment.fragment_id] = fragment
        return True
    
    def find_similar_fragments(self, 
                              context_vector: ScrollVector,
                              threshold: float = None) -> List[MemoryFragment]:
        """Find fragments similar to the given context vector."""
        threshold = threshold or self.coherence_threshold
        similar = []
        
        for fragment in self.fragments.values():
            similarity = self._calculate_vector_similarity(
                context_vector, fragment.context_vector
            )
            if similarity >= threshold:
                similar.append(fragment)
        
        return sorted(similar, key=lambda f: f.importance, reverse=True)
    
    def _calculate_vector_similarity(self, 
                                   v1: ScrollVector,
                                   v2: ScrollVector) -> float:
        """Calculate similarity between two scroll vectors."""
        diff = ScrollVector(
            v1.x - v2.x, v1.y - v2.y, v1.z - v2.z,
            v1.temporal - v2.temporal, v1.symbolic - v2.symbolic
        )
        distance = diff.magnitude()
        return max(0.0, 1.0 - distance / 5.0)  # Normalize to [0,1]


class MemoryRecursionManager:
    """
    Manages memory recursion and pattern storage for the ΩΔ143 system.
    
    Implements hierarchical memory with recursive pattern recognition
    and temporal persistence across the 5D symbolic field space.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the memory recursion manager."""
        self.config = config or {}
        self.recursion_layers: Dict[int, RecursionLayer] = {}
        self.active_recursions: Dict[str, Any] = {}
        self.memory_cache: Dict[str, Any] = {}
        
        # Configuration parameters
        self.max_recursion_depth = self.config.get("max_recursion_depth", 10)
        self.fragment_lifetime_days = self.config.get("fragment_lifetime_days", 30)
        self.coherence_threshold = self.config.get("coherence_threshold", 0.5)
        self.auto_cleanup_interval = self.config.get("auto_cleanup_interval", 3600)  # seconds
        
        # Initialize recursion layers
        self._initialize_recursion_layers()
        
        # Start background cleanup task
        asyncio.create_task(self._background_cleanup())
    
    def _initialize_recursion_layers(self):
        """Initialize the hierarchical recursion layers."""
        for depth in range(self.max_recursion_depth):
            layer = RecursionLayer(
                layer_id=f"layer_{depth}",
                depth=depth,
                fragments={},
                coherence_threshold=self.coherence_threshold * (0.9 ** depth),
                max_fragments=max(100, 1000 - depth * 100)
            )
            self.recursion_layers[depth] = layer
    
    def store_memory_fragment(self, 
                            content: Any,
                            context_vector: ScrollVector,
                            importance: float = 1.0,
                            target_depth: Optional[int] = None) -> str:
        """Store a memory fragment in the recursion hierarchy."""
        # Generate unique fragment ID
        content_hash = hashlib.md5(str(content).encode()).hexdigest()[:8]
        fragment_id = f"frag_{content_hash}_{int(datetime.now().timestamp())}"
        
        fragment = MemoryFragment(
            fragment_id=fragment_id,
            content=content,
            context_vector=context_vector,
            timestamp=datetime.now(),
            importance=importance
        )
        
        # Determine target depth if not specified
        if target_depth is None:
            target_depth = self._calculate_optimal_depth(content, context_vector)
        
        target_depth = min(target_depth, self.max_recursion_depth - 1)
        
        # Store in target layer
        if target_depth in self.recursion_layers:
            self.recursion_layers[target_depth].add_fragment(fragment)
        
        # Create recursive connections
        self._create_recursive_connections(fragment, target_depth)
        
        return fragment_id
    
    def _calculate_optimal_depth(self, 
                               content: Any,
                               context_vector: ScrollVector) -> int:
        """Calculate optimal recursion depth for storing content."""
        # Simple heuristic based on content complexity and vector properties
        content_complexity = len(str(content)) / 1000.0  # Normalize
        vector_magnitude = context_vector.magnitude()
        
        # Higher complexity and magnitude -> deeper storage
        depth_factor = (content_complexity + vector_magnitude) / 2.0
        optimal_depth = int(depth_factor * self.max_recursion_depth)
        
        return min(max(0, optimal_depth), self.max_recursion_depth - 1)
    
    def _create_recursive_connections(self, 
                                    fragment: MemoryFragment,
                                    depth: int):
        """Create recursive connections between fragments."""
        current_layer = self.recursion_layers[depth]
        
        # Find similar fragments in the same layer
        similar_fragments = current_layer.find_similar_fragments(
            fragment.context_vector, threshold=0.7
        )
        
        # Create connections to most similar fragments
        for similar in similar_fragments[:3]:  # Limit connections
            if similar.fragment_id != fragment.fragment_id:
                fragment.parent_fragments.append(similar.fragment_id)
                similar.child_fragments.append(fragment.fragment_id)
        
        # Try to connect to parent layer (if exists)
        if depth > 0:
            parent_layer = self.recursion_layers[depth - 1]
            parent_candidates = parent_layer.find_similar_fragments(
                fragment.context_vector, threshold=0.6
            )
            
            if parent_candidates:
                parent = parent_candidates[0]  # Most similar parent
                fragment.parent_fragments.append(parent.fragment_id)
                parent.child_fragments.append(fragment.fragment_id)
    
    def retrieve_memory_fragments(self, 
                                query_vector: ScrollVector,
                                max_results: int = 10,
                                similarity_threshold: float = 0.5) -> List[MemoryFragment]:
        """Retrieve memory fragments similar to the query vector."""
        all_candidates = []
        
        # Search across all layers
        for layer in self.recursion_layers.values():
            similar_fragments = layer.find_similar_fragments(
                query_vector, threshold=similarity_threshold
            )
            all_candidates.extend(similar_fragments)
        
        # Sort by importance and similarity
        all_candidates.sort(
            key=lambda f: f.importance * f.access_count, 
            reverse=True
        )
        
        # Update access counts
        for fragment in all_candidates[:max_results]:
            fragment.update_access()
        
        return all_candidates[:max_results]
    
    def start_recursive_computation(self, 
                                  initial_vector: ScrollVector,
                                  computation_type: str,
                                  max_iterations: int = 100) -> str:
        """Start a recursive computation process."""
        recursion_id = f"rec_{int(datetime.now().timestamp())}_{computation_type}"
        
        recursion_state = {
            "recursion_id": recursion_id,
            "current_vector": initial_vector,
            "computation_type": computation_type,
            "iteration": 0,
            "max_iterations": max_iterations,
            "history": [initial_vector],
            "convergence_threshold": 1e-6,
            "status": "running"
        }
        
        self.active_recursions[recursion_id] = recursion_state
        
        # Start async computation
        asyncio.create_task(self._execute_recursive_computation(recursion_id))
        
        return recursion_id
    
    async def _execute_recursive_computation(self, recursion_id: str):
        """Execute a recursive computation asynchronously."""
        if recursion_id not in self.active_recursions:
            return
        
        state = self.active_recursions[recursion_id]
        
        while (state["iteration"] < state["max_iterations"] and 
               state["status"] == "running"):
            
            current_vector = state["current_vector"]
            
            # Retrieve relevant memory fragments
            relevant_memories = self.retrieve_memory_fragments(
                current_vector, max_results=5, similarity_threshold=0.3
            )
            
            # Compute next iteration based on computation type
            next_vector = await self._compute_next_iteration(
                current_vector, relevant_memories, state["computation_type"]
            )
            
            # Check for convergence
            diff = ScrollVector(
                next_vector.x - current_vector.x,
                next_vector.y - current_vector.y,
                next_vector.z - current_vector.z,
                next_vector.temporal - current_vector.temporal,
                next_vector.symbolic - current_vector.symbolic
            )
            
            if diff.magnitude() < state["convergence_threshold"]:
                state["status"] = "converged"
                break
            
            # Update state
            state["current_vector"] = next_vector
            state["history"].append(next_vector)
            state["iteration"] += 1
            
            # Store intermediate result as memory
            self.store_memory_fragment(
                content={"iteration": state["iteration"], "vector": next_vector},
                context_vector=next_vector,
                importance=0.5
            )
            
            # Brief pause to allow other operations
            await asyncio.sleep(0.001)
        
        if state["status"] == "running":
            state["status"] = "max_iterations_reached"
    
    async def _compute_next_iteration(self, 
                                    current_vector: ScrollVector,
                                    memories: List[MemoryFragment],
                                    computation_type: str) -> ScrollVector:
        """Compute the next iteration in the recursive computation."""
        if computation_type == "field_convergence":
            # Converge towards memory-weighted center
            if memories:
                weight_sum = sum(m.importance for m in memories)
                if weight_sum > 0:
                    weighted_x = sum(m.context_vector.x * m.importance for m in memories) / weight_sum
                    weighted_y = sum(m.context_vector.y * m.importance for m in memories) / weight_sum
                    weighted_z = sum(m.context_vector.z * m.importance for m in memories) / weight_sum
                    weighted_t = sum(m.context_vector.temporal * m.importance for m in memories) / weight_sum
                    weighted_s = sum(m.context_vector.symbolic * m.importance for m in memories) / weight_sum
                    
                    # Move towards weighted center with damping
                    damping = 0.1
                    return ScrollVector(
                        current_vector.x + damping * (weighted_x - current_vector.x),
                        current_vector.y + damping * (weighted_y - current_vector.y),
                        current_vector.z + damping * (weighted_z - current_vector.z),
                        current_vector.temporal + damping * (weighted_t - current_vector.temporal),
                        current_vector.symbolic + damping * (weighted_s - current_vector.symbolic)
                    )
            
            # Default: simple decay towards origin
            decay = 0.95
            return ScrollVector(
                current_vector.x * decay,
                current_vector.y * decay,
                current_vector.z * decay,
                current_vector.temporal * decay,
                current_vector.symbolic * decay
            )
        
        elif computation_type == "spiral_drift":
            # Spiral pattern with memory influence
            angle = current_vector.magnitude() * 0.1
            spiral_x = current_vector.x * 0.9 + 0.1 * np.cos(angle)
            spiral_y = current_vector.y * 0.9 + 0.1 * np.sin(angle)
            
            return ScrollVector(
                spiral_x,
                spiral_y,
                current_vector.z * 0.98,
                current_vector.temporal + 0.01,
                current_vector.symbolic * 1.01
            )
        
        else:
            # Default: identity transformation
            return current_vector
    
    def get_recursion_status(self, recursion_id: str) -> Optional[Dict[str, Any]]:
        """Get the status of a recursive computation."""
        if recursion_id not in self.active_recursions:
            return None
        
        state = self.active_recursions[recursion_id]
        return {
            "recursion_id": recursion_id,
            "status": state["status"],
            "iteration": state["iteration"],
            "max_iterations": state["max_iterations"],
            "current_vector": {
                "x": state["current_vector"].x,
                "y": state["current_vector"].y,
                "z": state["current_vector"].z,
                "temporal": state["current_vector"].temporal,
                "symbolic": state["current_vector"].symbolic
            },
            "convergence_magnitude": state["current_vector"].magnitude(),
            "history_length": len(state["history"])
        }
    
    def analyze_memory_patterns(self) -> Dict[str, Any]:
        """Analyze patterns in the stored memory fragments."""
        analysis = {
            "total_fragments": 0,
            "fragments_by_depth": {},
            "importance_distribution": {"low": 0, "medium": 0, "high": 0},
            "temporal_distribution": {"recent": 0, "old": 0, "ancient": 0},
            "connectivity_stats": {"isolated": 0, "connected": 0, "hubs": 0}
        }
        
        now = datetime.now()
        
        for depth, layer in self.recursion_layers.items():
            fragment_count = len(layer.fragments)
            analysis["total_fragments"] += fragment_count
            analysis["fragments_by_depth"][str(depth)] = fragment_count
            
            for fragment in layer.fragments.values():
                # Importance distribution
                if fragment.importance < 0.3:
                    analysis["importance_distribution"]["low"] += 1
                elif fragment.importance < 0.7:
                    analysis["importance_distribution"]["medium"] += 1
                else:
                    analysis["importance_distribution"]["high"] += 1
                
                # Temporal distribution
                age_hours = (now - fragment.timestamp).total_seconds() / 3600
                if age_hours < 24:
                    analysis["temporal_distribution"]["recent"] += 1
                elif age_hours < 168:  # 1 week
                    analysis["temporal_distribution"]["old"] += 1
                else:
                    analysis["temporal_distribution"]["ancient"] += 1
                
                # Connectivity
                total_connections = len(fragment.parent_fragments) + len(fragment.child_fragments)
                if total_connections == 0:
                    analysis["connectivity_stats"]["isolated"] += 1
                elif total_connections <= 3:
                    analysis["connectivity_stats"]["connected"] += 1
                else:
                    analysis["connectivity_stats"]["hubs"] += 1
        
        return analysis
    
    async def _background_cleanup(self):
        """Background task for cleaning up old memory fragments."""
        while True:
            try:
                current_time = datetime.now()
                cleanup_threshold = current_time - timedelta(days=self.fragment_lifetime_days)
                
                for layer in self.recursion_layers.values():
                    fragments_to_remove = []
                    
                    for frag_id, fragment in layer.fragments.items():
                        # Remove old, unimportant fragments
                        if (fragment.timestamp < cleanup_threshold and 
                            fragment.importance < 0.1 and 
                            fragment.access_count < 2):
                            fragments_to_remove.append(frag_id)
                    
                    # Remove fragments
                    for frag_id in fragments_to_remove:
                        del layer.fragments[frag_id]
                
                await asyncio.sleep(self.auto_cleanup_interval)
                
            except Exception as e:
                print(f"Background cleanup error: {e}")
                await asyncio.sleep(self.auto_cleanup_interval)
    
    def export_memory_state(self, include_content: bool = False) -> Dict[str, Any]:
        """Export the current memory state for persistence."""
        export_data = {
            "config": self.config,
            "layers": {},
            "active_recursions": len(self.active_recursions),
            "export_timestamp": datetime.now().isoformat()
        }
        
        for depth, layer in self.recursion_layers.items():
            layer_data = {
                "layer_id": layer.layer_id,
                "depth": layer.depth,
                "fragment_count": len(layer.fragments),
                "fragments": {}
            }
            
            for frag_id, fragment in layer.fragments.items():
                fragment_data = {
                    "fragment_id": fragment.fragment_id,
                    "context_vector": {
                        "x": fragment.context_vector.x,
                        "y": fragment.context_vector.y,
                        "z": fragment.context_vector.z,
                        "temporal": fragment.context_vector.temporal,
                        "symbolic": fragment.context_vector.symbolic
                    },
                    "timestamp": fragment.timestamp.isoformat(),
                    "access_count": fragment.access_count,
                    "importance": fragment.importance,
                    "parent_fragments": fragment.parent_fragments,
                    "child_fragments": fragment.child_fragments
                }
                
                if include_content:
                    fragment_data["content"] = str(fragment.content)
                
                layer_data["fragments"][frag_id] = fragment_data
            
            export_data["layers"][str(depth)] = layer_data
        
        return export_data
    
    def get_manager_status(self) -> Dict[str, Any]:
        """Get current memory recursion manager status."""
        return {
            "max_recursion_depth": self.max_recursion_depth,
            "active_layers": len(self.recursion_layers),
            "total_fragments": sum(len(layer.fragments) for layer in self.recursion_layers.values()),
            "active_recursions": len(self.active_recursions),
            "cache_size": len(self.memory_cache),
            "coherence_threshold": self.coherence_threshold
        }