"""
Mesh Orchestrator for ΩΔ143 Codex Drift 5D Capsule

Handles mesh orchestration and cluster runtime coordination
for distributed scrollmath processing.
"""

import asyncio
import json
import uuid
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from .scrollmath_engine import ScrollVector, CodexDriftField, ScrollMathEngine


class MeshNodeState(Enum):
    """States for mesh nodes in the orchestration network."""
    INITIALIZING = "initializing"
    ACTIVE = "active"
    COMPUTING = "computing"
    SYNCHRONIZING = "synchronizing"
    DORMANT = "dormant"
    ERROR = "error"


@dataclass
class MeshNode:
    """Represents a node in the ΩΔ143 mesh orchestration network."""
    node_id: str
    position: ScrollVector
    state: MeshNodeState = MeshNodeState.INITIALIZING
    compute_capacity: float = 1.0
    field_affinity: float = 0.5
    last_heartbeat: datetime = field(default_factory=datetime.now)
    assigned_tasks: List[str] = field(default_factory=list)
    
    def update_heartbeat(self):
        """Update the node's heartbeat timestamp."""
        self.last_heartbeat = datetime.now()
    
    def is_healthy(self, timeout_seconds: int = 30) -> bool:
        """Check if node is healthy based on heartbeat."""
        time_diff = (datetime.now() - self.last_heartbeat).total_seconds()
        return time_diff < timeout_seconds


@dataclass
class MeshTask:
    """Represents a computational task in the mesh network."""
    task_id: str
    task_type: str
    input_field: CodexDriftField
    target_nodes: List[str]
    priority: int = 1
    created_at: datetime = field(default_factory=datetime.now)
    status: str = "pending"
    result: Optional[Any] = None


class MeshOrchestrator:
    """
    Orchestrates mesh operations for ΩΔ143 Codex Drift processing.
    
    Manages distributed computation across mesh nodes, handles task
    scheduling, and coordinates symbolic field processing.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the mesh orchestrator."""
        self.config = config or {}
        self.nodes: Dict[str, MeshNode] = {}
        self.tasks: Dict[str, MeshTask] = {}
        self.scrollmath_engine = ScrollMathEngine(config.get("engine", {}) if config else {})
        self.mesh_id = str(uuid.uuid4())
        self.orchestration_active = False
        
        # Configuration parameters
        self.max_nodes = self.config.get("max_nodes", 100)
        self.heartbeat_interval = self.config.get("heartbeat_interval", 10)
        self.task_timeout = self.config.get("task_timeout", 300)
        
    async def initialize_mesh(self) -> bool:
        """Initialize the mesh orchestration network."""
        try:
            # Create initial mesh topology
            await self._create_initial_topology()
            
            # Start orchestration services
            self.orchestration_active = True
            
            # Begin heartbeat monitoring
            asyncio.create_task(self._heartbeat_monitor())
            
            return True
        except Exception as e:
            print(f"Mesh initialization failed: {e}")
            return False
    
    async def _create_initial_topology(self):
        """Create the initial mesh topology with core nodes."""
        # Create core computation nodes
        core_positions = [
            ScrollVector(0, 0, 0, 0, 0),      # Origin node
            ScrollVector(1, 0, 0, 0, 0.5),    # X-axis node
            ScrollVector(0, 1, 0, 0.5, 0),    # Y-axis node
            ScrollVector(0, 0, 1, 0, 0.8),    # Z-axis node
            ScrollVector(0, 0, 0, 1, 0.3),    # Temporal node
        ]
        
        for i, pos in enumerate(core_positions):
            node_id = f"core-{i}"
            node = MeshNode(
                node_id=node_id,
                position=pos,
                state=MeshNodeState.ACTIVE,
                compute_capacity=1.0,
                field_affinity=0.8
            )
            self.nodes[node_id] = node
    
    async def add_mesh_node(self, 
                           position: ScrollVector,
                           compute_capacity: float = 1.0,
                           field_affinity: float = 0.5) -> str:
        """Add a new node to the mesh network."""
        if len(self.nodes) >= self.max_nodes:
            raise RuntimeError("Maximum mesh node limit reached")
        
        node_id = f"node-{str(uuid.uuid4())[:8]}"
        node = MeshNode(
            node_id=node_id,
            position=position,
            compute_capacity=compute_capacity,
            field_affinity=field_affinity
        )
        
        self.nodes[node_id] = node
        
        # Perform mesh integration
        await self._integrate_node(node)
        
        return node_id
    
    async def _integrate_node(self, node: MeshNode):
        """Integrate a new node into the existing mesh topology."""
        # Find optimal position based on field resonance
        best_resonance = 0
        best_neighbors = []
        
        for existing_node in self.nodes.values():
            if existing_node.node_id != node.node_id:
                # Calculate position resonance
                resonance = self._calculate_position_resonance(
                    node.position, existing_node.position
                )
                if resonance > best_resonance:
                    best_resonance = resonance
                    best_neighbors = [existing_node.node_id]
                elif resonance == best_resonance:
                    best_neighbors.append(existing_node.node_id)
        
        # Set node state to active after integration
        node.state = MeshNodeState.ACTIVE
    
    def _calculate_position_resonance(self, 
                                    pos1: ScrollVector,
                                    pos2: ScrollVector) -> float:
        """Calculate resonance between two positions in 5D space."""
        diff = ScrollVector(
            pos1.x - pos2.x,
            pos1.y - pos2.y,
            pos1.z - pos2.z,
            pos1.temporal - pos2.temporal,
            pos1.symbolic - pos2.symbolic
        )
        
        distance = diff.magnitude()
        # Inverse relationship - closer nodes have higher resonance
        return 1.0 / (1.0 + distance)
    
    async def submit_mesh_task(self,
                              task_type: str,
                              input_field: CodexDriftField,
                              priority: int = 1) -> str:
        """Submit a computational task to the mesh network."""
        task_id = f"task-{str(uuid.uuid4())[:8]}"
        
        # Select optimal nodes for the task
        target_nodes = self._select_task_nodes(input_field, task_type)
        
        task = MeshTask(
            task_id=task_id,
            task_type=task_type,
            input_field=input_field,
            target_nodes=target_nodes,
            priority=priority
        )
        
        self.tasks[task_id] = task
        
        # Schedule task execution
        asyncio.create_task(self._execute_mesh_task(task))
        
        return task_id
    
    def _select_task_nodes(self, 
                          input_field: CodexDriftField,
                          task_type: str) -> List[str]:
        """Select optimal nodes for executing a specific task."""
        available_nodes = [
            node for node in self.nodes.values()
            if node.state == MeshNodeState.ACTIVE and node.is_healthy()
        ]
        
        # Sort by field affinity and compute capacity
        node_scores = []
        for node in available_nodes:
            # Calculate affinity score based on field gradient
            field_gradient = input_field.compute_field_gradient()
            position_affinity = self._calculate_position_resonance(
                node.position, field_gradient
            )
            
            score = (node.field_affinity * position_affinity * 
                    node.compute_capacity)
            node_scores.append((node.node_id, score))
        
        # Sort by score and select top nodes
        node_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Select top 3 nodes for redundancy
        return [node_id for node_id, _ in node_scores[:3]]
    
    async def _execute_mesh_task(self, task: MeshTask):
        """Execute a computational task across selected mesh nodes."""
        try:
            task.status = "executing"
            
            # Distribute computation across target nodes
            subtask_results = []
            
            for node_id in task.target_nodes:
                if node_id in self.nodes:
                    node = self.nodes[node_id]
                    node.state = MeshNodeState.COMPUTING
                    node.assigned_tasks.append(task.task_id)
                    
                    # Simulate computation based on task type
                    result = await self._compute_subtask(task, node)
                    subtask_results.append(result)
                    
                    # Reset node state
                    node.state = MeshNodeState.ACTIVE
                    node.assigned_tasks.remove(task.task_id)
            
            # Aggregate results
            task.result = self._aggregate_subtask_results(
                task.task_type, subtask_results
            )
            task.status = "completed"
            
        except Exception as e:
            task.status = "failed"
            task.result = {"error": str(e)}
    
    async def _compute_subtask(self, task: MeshTask, node: MeshNode) -> Any:
        """Compute a subtask on a specific mesh node."""
        # Simulate computation delay
        await asyncio.sleep(0.1)
        
        if task.task_type == "field_transform":
            # Use scrollmath engine for field transformation
            transformed = self.scrollmath_engine.compute_5d_transform(
                task.input_field, node.position
            )
            return {
                "node_id": node.node_id,
                "transformed_vector": {
                    "x": transformed.x,
                    "y": transformed.y,
                    "z": transformed.z,
                    "temporal": transformed.temporal,
                    "symbolic": transformed.symbolic
                }
            }
        
        elif task.task_type == "resonance_analysis":
            # Create a test field for resonance calculation
            test_vectors = [node.position]
            test_field = self.scrollmath_engine.create_drift_field(
                test_vectors, drift_coeff=0.5
            )
            resonance = self.scrollmath_engine.calculate_mesh_resonance(
                task.input_field, test_field
            )
            return {
                "node_id": node.node_id,
                "resonance_value": resonance
            }
        
        else:
            return {"node_id": node.node_id, "status": "unknown_task_type"}
    
    def _aggregate_subtask_results(self, 
                                  task_type: str,
                                  results: List[Any]) -> Any:
        """Aggregate results from multiple subtasks."""
        if task_type == "field_transform":
            # Average the transformed vectors
            if not results:
                return None
            
            avg_x = sum(r["transformed_vector"]["x"] for r in results) / len(results)
            avg_y = sum(r["transformed_vector"]["y"] for r in results) / len(results)
            avg_z = sum(r["transformed_vector"]["z"] for r in results) / len(results)
            avg_temporal = sum(r["transformed_vector"]["temporal"] for r in results) / len(results)
            avg_symbolic = sum(r["transformed_vector"]["symbolic"] for r in results) / len(results)
            
            return {
                "aggregated_transform": {
                    "x": avg_x,
                    "y": avg_y,
                    "z": avg_z,
                    "temporal": avg_temporal,
                    "symbolic": avg_symbolic
                },
                "contributing_nodes": [r["node_id"] for r in results]
            }
        
        elif task_type == "resonance_analysis":
            total_resonance = sum(r["resonance_value"] for r in results)
            return {
                "total_resonance": total_resonance,
                "average_resonance": total_resonance / len(results) if results else 0,
                "contributing_nodes": [r["node_id"] for r in results]
            }
        
        return {"raw_results": results}
    
    async def _heartbeat_monitor(self):
        """Monitor mesh node heartbeats and health."""
        while self.orchestration_active:
            unhealthy_nodes = []
            
            for node_id, node in self.nodes.items():
                if not node.is_healthy():
                    unhealthy_nodes.append(node_id)
                    node.state = MeshNodeState.ERROR
            
            # Remove unhealthy nodes after grace period
            for node_id in unhealthy_nodes:
                # Could implement recovery logic here
                pass
            
            await asyncio.sleep(self.heartbeat_interval)
    
    def get_mesh_status(self) -> Dict[str, Any]:
        """Get current mesh orchestration status."""
        active_nodes = sum(1 for n in self.nodes.values() 
                          if n.state == MeshNodeState.ACTIVE)
        computing_nodes = sum(1 for n in self.nodes.values() 
                             if n.state == MeshNodeState.COMPUTING)
        
        return {
            "mesh_id": self.mesh_id,
            "orchestration_active": self.orchestration_active,
            "total_nodes": len(self.nodes),
            "active_nodes": active_nodes,
            "computing_nodes": computing_nodes,
            "pending_tasks": sum(1 for t in self.tasks.values() 
                               if t.status == "pending"),
            "executing_tasks": sum(1 for t in self.tasks.values() 
                                 if t.status == "executing"),
            "completed_tasks": sum(1 for t in self.tasks.values() 
                                 if t.status == "completed")
        }
    
    async def shutdown_mesh(self):
        """Gracefully shutdown the mesh orchestration."""
        self.orchestration_active = False
        
        # Set all nodes to dormant
        for node in self.nodes.values():
            node.state = MeshNodeState.DORMANT
        
        # Wait for running tasks to complete
        running_tasks = [t for t in self.tasks.values() 
                        if t.status == "executing"]
        
        if running_tasks:
            # Wait up to 30 seconds for tasks to complete
            await asyncio.sleep(min(30, self.task_timeout))