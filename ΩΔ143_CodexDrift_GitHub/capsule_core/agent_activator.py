"""
Agent Activator for ΩΔ143 Codex Drift 5D Capsule

Handles agent activation, coordination, and lifecycle management
within the cluster runtime environment.
"""

import asyncio
import json
import uuid
import numpy as np
from typing import Dict, List, Any, Optional, Callable, Awaitable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import inspect

from .scrollmath_engine import ScrollVector, CodexDriftField
from .mesh_orchestrator import MeshOrchestrator, MeshNode, MeshTask
from .memory_recursion_manager import MemoryRecursionManager, MemoryFragment


class AgentState(Enum):
    """States for agents in the activation system."""
    DORMANT = "dormant"
    INITIALIZING = "initializing" 
    ACTIVE = "active"
    COMPUTING = "computing"
    COMMUNICATING = "communicating"
    LEARNING = "learning"
    ERROR = "error"
    TERMINATED = "terminated"


class AgentCapability(Enum):
    """Capabilities that agents can possess."""
    SCROLLMATH_COMPUTATION = "scrollmath_computation"
    FIELD_ANALYSIS = "field_analysis"
    PATTERN_RECOGNITION = "pattern_recognition"
    MESH_COORDINATION = "mesh_coordination"
    MEMORY_PROCESSING = "memory_processing"
    SYMBOLIC_REASONING = "symbolic_reasoning"
    RECURSIVE_LEARNING = "recursive_learning"
    CLUSTER_COMMUNICATION = "cluster_communication"


@dataclass
class AgentProfile:
    """Profile defining an agent's characteristics and capabilities."""
    agent_id: str
    agent_type: str
    capabilities: List[AgentCapability]
    position: ScrollVector
    activation_threshold: float = 0.5
    learning_rate: float = 0.01
    memory_capacity: int = 1000
    communication_range: float = 10.0
    priority_level: int = 1
    creation_time: datetime = field(default_factory=datetime.now)


@dataclass
class AgentMessage:
    """Message structure for inter-agent communication."""
    message_id: str
    sender_id: str
    receiver_id: Optional[str]  # None for broadcast
    message_type: str
    content: Any
    priority: int = 1
    timestamp: datetime = field(default_factory=datetime.now)
    requires_response: bool = False


class Agent:
    """
    Individual agent in the ΩΔ143 activation system.
    
    Agents are autonomous entities that can perform computation,
    learn from experience, and coordinate with other agents.
    """
    
    def __init__(self, profile: AgentProfile):
        """Initialize an agent with the given profile."""
        self.profile = profile
        self.state = AgentState.DORMANT
        self.local_memory: List[MemoryFragment] = []
        self.message_queue: List[AgentMessage] = []
        self.task_history: List[str] = []
        self.performance_metrics = {
            "tasks_completed": 0,
            "messages_processed": 0,
            "learning_iterations": 0,
            "errors_encountered": 0
        }
        self.last_activity = datetime.now()
        self.activation_energy = 0.0
        
        # Agent-specific state
        self.custom_state: Dict[str, Any] = {}
        self.learned_patterns: Dict[str, Any] = {}
        
    async def activate(self) -> bool:
        """Activate the agent and begin operations."""
        try:
            self.state = AgentState.INITIALIZING
            
            # Initialize agent-specific systems
            await self._initialize_agent_systems()
            
            self.state = AgentState.ACTIVE
            self.last_activity = datetime.now()
            
            # Start agent main loop
            asyncio.create_task(self._agent_main_loop())
            
            return True
        except Exception as e:
            self.state = AgentState.ERROR
            self.performance_metrics["errors_encountered"] += 1
            print(f"Agent {self.profile.agent_id} activation failed: {e}")
            return False
    
    async def _initialize_agent_systems(self):
        """Initialize agent-specific systems based on capabilities."""
        for capability in self.profile.capabilities:
            if capability == AgentCapability.SCROLLMATH_COMPUTATION:
                self.custom_state["scrollmath_cache"] = {}
            elif capability == AgentCapability.PATTERN_RECOGNITION:
                self.custom_state["pattern_buffer"] = []
            elif capability == AgentCapability.MEMORY_PROCESSING:
                self.custom_state["memory_index"] = {}
    
    async def _agent_main_loop(self):
        """Main operational loop for the agent."""
        while self.state not in [AgentState.ERROR, AgentState.TERMINATED]:
            try:
                # Process pending messages
                await self._process_message_queue()
                
                # Update activation energy based on local conditions
                await self._update_activation_energy()
                
                # Perform capability-specific operations
                await self._execute_capability_operations()
                
                # Learn from recent experiences
                if AgentCapability.RECURSIVE_LEARNING in self.profile.capabilities:
                    await self._perform_learning_iteration()
                
                self.last_activity = datetime.now()
                
                # Brief pause to allow other operations
                await asyncio.sleep(0.1)
                
            except Exception as e:
                self.performance_metrics["errors_encountered"] += 1
                print(f"Agent {self.profile.agent_id} main loop error: {e}")
                await asyncio.sleep(1.0)  # Recovery pause
    
    async def _process_message_queue(self):
        """Process messages in the agent's queue."""
        while self.message_queue:
            message = self.message_queue.pop(0)
            await self._handle_message(message)
            self.performance_metrics["messages_processed"] += 1
    
    async def _handle_message(self, message: AgentMessage):
        """Handle a specific message based on its type."""
        self.state = AgentState.COMMUNICATING
        
        if message.message_type == "task_assignment":
            await self._handle_task_assignment(message)
        elif message.message_type == "coordination_request":
            await self._handle_coordination_request(message)
        elif message.message_type == "learning_data":
            await self._handle_learning_data(message)
        elif message.message_type == "status_query":
            await self._handle_status_query(message)
        
        self.state = AgentState.ACTIVE
    
    async def _handle_task_assignment(self, message: AgentMessage):
        """Handle a task assignment message."""
        task_data = message.content
        task_id = task_data.get("task_id", "unknown")
        
        self.state = AgentState.COMPUTING
        self.task_history.append(task_id)
        
        # Execute task based on agent capabilities
        result = await self._execute_assigned_task(task_data)
        
        # Send result back if response required
        if message.requires_response:
            response = AgentMessage(
                message_id=f"response_{uuid.uuid4().hex[:8]}",
                sender_id=self.profile.agent_id,
                receiver_id=message.sender_id,
                message_type="task_result",
                content={"task_id": task_id, "result": result}
            )
            # Response would be sent via activator's message system
        
        self.performance_metrics["tasks_completed"] += 1
    
    async def _execute_assigned_task(self, task_data: Dict[str, Any]) -> Any:
        """Execute an assigned task based on agent capabilities."""
        task_type = task_data.get("type", "unknown")
        
        if task_type == "scrollmath_compute" and AgentCapability.SCROLLMATH_COMPUTATION in self.profile.capabilities:
            return await self._perform_scrollmath_computation(task_data)
        elif task_type == "pattern_analyze" and AgentCapability.PATTERN_RECOGNITION in self.profile.capabilities:
            return await self._perform_pattern_analysis(task_data)
        elif task_type == "memory_process" and AgentCapability.MEMORY_PROCESSING in self.profile.capabilities:
            return await self._perform_memory_processing(task_data)
        else:
            return {"status": "unsupported_task", "task_type": task_type}
    
    async def _perform_scrollmath_computation(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform scrollmath computation task."""
        # Simulate computation
        await asyncio.sleep(0.05)
        
        input_vector = task_data.get("input_vector", {"x": 0, "y": 0, "z": 0, "temporal": 0, "symbolic": 0})
        result_vector = ScrollVector(
            input_vector["x"] * 1.1,
            input_vector["y"] * 1.1,
            input_vector["z"] * 1.1,
            input_vector["temporal"] + 0.1,
            input_vector["symbolic"] * 0.9
        )
        
        return {
            "status": "completed",
            "result_vector": {
                "x": result_vector.x,
                "y": result_vector.y,
                "z": result_vector.z,
                "temporal": result_vector.temporal,
                "symbolic": result_vector.symbolic
            },
            "computation_time": 0.05
        }
    
    async def _perform_pattern_analysis(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform pattern analysis task."""
        patterns = task_data.get("patterns", [])
        
        # Simple pattern analysis
        pattern_count = len(patterns)
        complexity_score = sum(len(str(p)) for p in patterns) / max(1, pattern_count)
        
        return {
            "status": "completed",
            "pattern_count": pattern_count,
            "complexity_score": complexity_score,
            "detected_repetitions": pattern_count // 3  # Simplified
        }
    
    async def _perform_memory_processing(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform memory processing task."""
        memory_data = task_data.get("memory_data", [])
        
        # Process memory fragments
        processed_count = 0
        for item in memory_data:
            # Add to local memory if space available
            if len(self.local_memory) < self.profile.memory_capacity:
                # Convert to MemoryFragment (simplified)
                fragment = MemoryFragment(
                    fragment_id=f"local_{uuid.uuid4().hex[:8]}",
                    content=item,
                    context_vector=self.profile.position,
                    timestamp=datetime.now()
                )
                self.local_memory.append(fragment)
                processed_count += 1
        
        return {
            "status": "completed",
            "processed_items": processed_count,
            "local_memory_size": len(self.local_memory)
        }
    
    async def _update_activation_energy(self):
        """Update the agent's activation energy based on local conditions."""
        base_energy = 0.5
        
        # Increase energy based on message queue size
        message_factor = min(0.3, len(self.message_queue) * 0.1)
        
        # Increase energy based on recent task completions
        recent_tasks = len([t for t in self.task_history[-10:]])  # Last 10 tasks
        task_factor = min(0.2, recent_tasks * 0.02)
        
        self.activation_energy = base_energy + message_factor + task_factor
    
    async def _execute_capability_operations(self):
        """Execute operations specific to agent capabilities."""
        for capability in self.profile.capabilities:
            if capability == AgentCapability.PATTERN_RECOGNITION:
                await self._scan_for_patterns()
            elif capability == AgentCapability.MESH_COORDINATION:
                await self._coordinate_with_mesh()
    
    async def _scan_for_patterns(self):
        """Scan local data for patterns."""
        if "pattern_buffer" in self.custom_state:
            buffer = self.custom_state["pattern_buffer"]
            
            # Add current state to pattern buffer
            current_state = {
                "timestamp": datetime.now().isoformat(),
                "activation_energy": self.activation_energy,
                "message_count": len(self.message_queue),
                "position": {
                    "x": self.profile.position.x,
                    "y": self.profile.position.y,
                    "z": self.profile.position.z
                }
            }
            
            buffer.append(current_state)
            
            # Limit buffer size
            if len(buffer) > 100:
                buffer.pop(0)
    
    async def _coordinate_with_mesh(self):
        """Coordinate with mesh nodes if capability exists."""
        # This would integrate with MeshOrchestrator in a real implementation
        pass
    
    async def _perform_learning_iteration(self):
        """Perform a learning iteration based on recent experiences."""
        if len(self.task_history) < 2:
            return
        
        # Simple learning: adjust activation threshold based on performance
        success_rate = (self.performance_metrics["tasks_completed"] / 
                       max(1, self.performance_metrics["tasks_completed"] + 
                           self.performance_metrics["errors_encountered"]))
        
        if success_rate > 0.8:
            # Lower threshold for higher activation
            self.profile.activation_threshold *= 0.99
        elif success_rate < 0.5:
            # Raise threshold to be more selective
            self.profile.activation_threshold *= 1.01
        
        # Clamp threshold
        self.profile.activation_threshold = max(0.1, min(0.9, self.profile.activation_threshold))
        
        self.performance_metrics["learning_iterations"] += 1
    
    def add_message(self, message: AgentMessage):
        """Add a message to the agent's queue."""
        self.message_queue.append(message)
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get current agent status."""
        return {
            "agent_id": self.profile.agent_id,
            "agent_type": self.profile.agent_type,
            "state": self.state.value,
            "capabilities": [cap.value for cap in self.profile.capabilities],
            "position": {
                "x": self.profile.position.x,
                "y": self.profile.position.y,
                "z": self.profile.position.z,
                "temporal": self.profile.position.temporal,
                "symbolic": self.profile.position.symbolic
            },
            "activation_energy": self.activation_energy,
            "activation_threshold": self.profile.activation_threshold,
            "message_queue_size": len(self.message_queue),
            "local_memory_size": len(self.local_memory),
            "performance_metrics": self.performance_metrics.copy(),
            "last_activity": self.last_activity.isoformat()
        }
    
    async def terminate(self):
        """Terminate the agent gracefully."""
        self.state = AgentState.TERMINATED


class AgentActivator:
    """
    Manages agent activation, coordination, and lifecycle in the ΩΔ143 system.
    
    Coordinates multiple agents, handles inter-agent communication,
    and manages the overall agent ecosystem.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the agent activator."""
        self.config = config or {}
        self.agents: Dict[str, Agent] = {}
        self.agent_profiles: Dict[str, AgentProfile] = {}
        self.message_broker: List[AgentMessage] = []
        self.activation_rules: List[Callable[[Agent], bool]] = []
        
        # Integration with other systems
        self.mesh_orchestrator: Optional[MeshOrchestrator] = None
        self.memory_manager: Optional[MemoryRecursionManager] = None
        
        # Configuration parameters
        self.max_agents = self.config.get("max_agents", 50)
        self.message_broker_size = self.config.get("message_broker_size", 1000)
        self.agent_cleanup_interval = self.config.get("agent_cleanup_interval", 300)  # seconds
        
        # Start background services
        asyncio.create_task(self._message_broker_loop())
        asyncio.create_task(self._agent_lifecycle_manager())
    
    def register_agent_profile(self, 
                             agent_type: str,
                             capabilities: List[AgentCapability],
                             position: ScrollVector,
                             **kwargs) -> str:
        """Register a new agent profile for potential activation."""
        profile_id = f"profile_{agent_type}_{uuid.uuid4().hex[:8]}"
        
        profile = AgentProfile(
            agent_id="",  # Will be set when agent is created
            agent_type=agent_type,
            capabilities=capabilities,
            position=position,
            **kwargs
        )
        
        self.agent_profiles[profile_id] = profile
        return profile_id
    
    async def activate_agent(self, profile_id: str) -> Optional[str]:
        """Activate an agent from a registered profile."""
        if profile_id not in self.agent_profiles:
            return None
        
        if len(self.agents) >= self.max_agents:
            # Remove least active agent to make room
            await self._cleanup_inactive_agents(1)
        
        profile = self.agent_profiles[profile_id]
        agent_id = f"agent_{uuid.uuid4().hex[:8]}"
        
        # Create a new profile with the same data but updated agent_id
        agent_profile = AgentProfile(
            agent_id=agent_id,
            agent_type=profile.agent_type,
            capabilities=profile.capabilities,
            position=profile.position,
            activation_threshold=profile.activation_threshold,
            learning_rate=profile.learning_rate,
            memory_capacity=profile.memory_capacity,
            communication_range=profile.communication_range,
            priority_level=profile.priority_level,
            creation_time=profile.creation_time
        )
        
        agent = Agent(agent_profile)
        success = await agent.activate()
        
        if success:
            self.agents[agent_id] = agent
            return agent_id
        else:
            return None
    
    async def activate_agent_swarm(self, 
                                 agent_type: str,
                                 count: int,
                                 capabilities: List[AgentCapability],
                                 center_position: ScrollVector,
                                 spread_radius: float = 1.0) -> List[str]:
        """Activate a swarm of similar agents around a center position."""
        activated_agents = []
        
        for i in range(count):
            # Generate position around center
            angle = (2 * np.pi * i) / count
            radius = spread_radius * (0.5 + 0.5 * (i / count))  # Varying radius
            
            position = ScrollVector(
                center_position.x + radius * np.cos(angle),
                center_position.y + radius * np.sin(angle),
                center_position.z + (radius * 0.1 * np.sin(angle * 2)),
                center_position.temporal,
                center_position.symbolic + (i * 0.1)
            )
            
            profile_id = self.register_agent_profile(
                agent_type=f"{agent_type}_swarm_{i}",
                capabilities=capabilities,
                position=position
            )
            
            agent_id = await self.activate_agent(profile_id)
            if agent_id:
                activated_agents.append(agent_id)
        
        return activated_agents
    
    def send_message(self, 
                    sender_id: str,
                    receiver_id: Optional[str],
                    message_type: str,
                    content: Any,
                    priority: int = 1,
                    requires_response: bool = False) -> str:
        """Send a message between agents or broadcast."""
        message = AgentMessage(
            message_id=f"msg_{uuid.uuid4().hex[:8]}",
            sender_id=sender_id,
            receiver_id=receiver_id,
            message_type=message_type,
            content=content,
            priority=priority,
            requires_response=requires_response
        )
        
        self.message_broker.append(message)
        return message.message_id
    
    async def _message_broker_loop(self):
        """Main loop for the message broker."""
        while True:
            try:
                # Process messages in priority order
                self.message_broker.sort(key=lambda m: m.priority, reverse=True)
                
                while self.message_broker:
                    message = self.message_broker.pop(0)
                    await self._deliver_message(message)
                
                await asyncio.sleep(0.05)  # Message broker cycle
                
            except Exception as e:
                print(f"Message broker error: {e}")
                await asyncio.sleep(1.0)
    
    async def _deliver_message(self, message: AgentMessage):
        """Deliver a message to its intended recipient(s)."""
        if message.receiver_id is None:
            # Broadcast message
            for agent in self.agents.values():
                if agent.profile.agent_id != message.sender_id:
                    agent.add_message(message)
        else:
            # Direct message
            if message.receiver_id in self.agents:
                self.agents[message.receiver_id].add_message(message)
    
    async def _agent_lifecycle_manager(self):
        """Manage agent lifecycle and cleanup."""
        while True:
            try:
                await asyncio.sleep(self.agent_cleanup_interval)
                
                # Check for inactive or errored agents
                inactive_agents = []
                current_time = datetime.now()
                
                for agent_id, agent in self.agents.items():
                    time_since_activity = (current_time - agent.last_activity).total_seconds()
                    
                    if (agent.state == AgentState.ERROR or 
                        agent.state == AgentState.TERMINATED or
                        time_since_activity > 3600):  # 1 hour inactive
                        inactive_agents.append(agent_id)
                
                # Remove inactive agents
                for agent_id in inactive_agents:
                    await self._remove_agent(agent_id)
                
            except Exception as e:
                print(f"Agent lifecycle manager error: {e}")
    
    async def _cleanup_inactive_agents(self, count: int = 1):
        """Remove the least active agents to make room for new ones."""
        if not self.agents:
            return
        
        # Sort agents by activity
        agents_by_activity = sorted(
            self.agents.items(),
            key=lambda x: x[1].last_activity
        )
        
        removed_count = 0
        for agent_id, agent in agents_by_activity:
            if removed_count >= count:
                break
            
            await self._remove_agent(agent_id)
            removed_count += 1
    
    async def _remove_agent(self, agent_id: str):
        """Remove an agent from the system."""
        if agent_id in self.agents:
            agent = self.agents[agent_id]
            await agent.terminate()
            del self.agents[agent_id]
    
    def integrate_with_mesh(self, mesh_orchestrator: MeshOrchestrator):
        """Integrate with mesh orchestrator for distributed operations."""
        self.mesh_orchestrator = mesh_orchestrator
    
    def integrate_with_memory(self, memory_manager: MemoryRecursionManager):
        """Integrate with memory recursion manager."""
        self.memory_manager = memory_manager
    
    def get_activation_status(self) -> Dict[str, Any]:
        """Get current activation system status."""
        agent_states = {}
        for state in AgentState:
            agent_states[state.value] = sum(1 for a in self.agents.values() if a.state == state)
        
        capability_distribution = {}
        for capability in AgentCapability:
            count = sum(1 for a in self.agents.values() 
                       if capability in a.profile.capabilities)
            capability_distribution[capability.value] = count
        
        return {
            "total_agents": len(self.agents),
            "registered_profiles": len(self.agent_profiles),
            "message_broker_size": len(self.message_broker),
            "agent_states": agent_states,
            "capability_distribution": capability_distribution,
            "max_agents": self.max_agents,
            "system_integrations": {
                "mesh_orchestrator": self.mesh_orchestrator is not None,
                "memory_manager": self.memory_manager is not None
            }
        }
    
    async def coordinate_cluster_activation(self, 
                                          activation_pattern: str,
                                          target_capabilities: List[AgentCapability],
                                          cluster_size: int = 10) -> Dict[str, Any]:
        """Coordinate activation of agent clusters for specific tasks."""
        if activation_pattern == "distributed_computation":
            # Activate agents optimized for distributed computation
            center = ScrollVector(0, 0, 0, 0, 0)
            agents = await self.activate_agent_swarm(
                "compute_agent",
                cluster_size,
                target_capabilities,
                center,
                spread_radius=2.0
            )
            
            return {
                "pattern": activation_pattern,
                "activated_agents": agents,
                "cluster_size": len(agents),
                "status": "activated"
            }
        
        elif activation_pattern == "learning_collective":
            # Activate learning-focused agents
            learning_caps = [cap for cap in target_capabilities 
                           if cap in [AgentCapability.RECURSIVE_LEARNING, 
                                     AgentCapability.PATTERN_RECOGNITION,
                                     AgentCapability.MEMORY_PROCESSING]]
            
            center = ScrollVector(0, 0, 0, 1, 1)  # Temporal/symbolic focus
            agents = await self.activate_agent_swarm(
                "learning_agent",
                cluster_size,
                learning_caps,
                center,
                spread_radius=1.5
            )
            
            return {
                "pattern": activation_pattern,
                "activated_agents": agents,
                "cluster_size": len(agents),
                "status": "activated"
            }
        
        else:
            return {
                "pattern": activation_pattern,
                "status": "unknown_pattern"
            }