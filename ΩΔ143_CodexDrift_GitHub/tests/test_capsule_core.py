#!/usr/bin/env python3
"""
Test Suite for ΩΔ143 Codex Drift 5D Capsule

Basic tests to validate core functionality and integration.
"""

import pytest
import asyncio
import numpy as np
from datetime import datetime
import sys
import os

# Add the capsule core to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from capsule_core import (
    ScrollMathEngine, MeshOrchestrator, SymbolicFieldComputer,
    MemoryRecursionManager, AgentActivator
)
from capsule_core.scrollmath_engine import ScrollVector, CodexDriftField
from capsule_core.agent_activator import AgentCapability


class TestScrollMathEngine:
    """Test the ScrollMath Engine component."""
    
    def test_scroll_vector_creation(self):
        """Test ScrollVector creation and basic operations."""
        vector = ScrollVector(1, 2, 3, 4, 5)
        assert vector.x == 1
        assert vector.y == 2
        assert vector.z == 3
        assert vector.temporal == 4
        assert vector.symbolic == 5
        
    def test_scroll_vector_magnitude(self):
        """Test ScrollVector magnitude calculation."""
        vector = ScrollVector(3, 4, 0, 0, 0)
        magnitude = vector.magnitude()
        assert magnitude == 5.0
        
    def test_scroll_vector_normalization(self):
        """Test ScrollVector normalization."""
        vector = ScrollVector(3, 4, 0, 0, 0)
        normalized = vector.normalize()
        assert abs(normalized.magnitude() - 1.0) < 1e-10
        
    def test_scrollmath_engine_initialization(self):
        """Test ScrollMath Engine initialization."""
        engine = ScrollMathEngine()
        assert engine.field_resolution == 1024
        assert engine.drift_sensitivity == 0.01
        assert len(engine.drift_fields) == 0
        
    def test_drift_field_creation(self):
        """Test codex drift field creation."""
        engine = ScrollMathEngine()
        vectors = [
            ScrollVector(1, 0, 0, 0, 0.5),
            ScrollVector(0, 1, 0, 0.5, 0)
        ]
        
        field = engine.create_drift_field(vectors, drift_coeff=1.0)
        assert isinstance(field, CodexDriftField)
        assert len(field.vectors) == 2
        assert field.drift_coefficient == 1.0
        
    def test_5d_transformation(self):
        """Test 5D transformation computation."""
        engine = ScrollMathEngine()
        vectors = [ScrollVector(1, 0, 0, 0, 0)]
        field = engine.create_drift_field(vectors)
        
        target = ScrollVector(0.5, 0.5, 0.5, 0.1, 0.3)
        transformed = engine.compute_5d_transform(field, target)
        
        assert isinstance(transformed, ScrollVector)
        assert transformed.magnitude() <= 1.0  # Should be normalized
        
    def test_field_manifest_export(self):
        """Test field manifest export."""
        engine = ScrollMathEngine()
        vectors = [ScrollVector(1, 0, 0, 0, 0)]
        field = engine.create_drift_field(vectors)
        
        manifest = engine.export_field_manifest(field)
        assert "field_id" in manifest
        assert "vector_count" in manifest
        assert manifest["vector_count"] == 1


class TestMeshOrchestrator:
    """Test the Mesh Orchestrator component."""
    
    @pytest.mark.asyncio
    async def test_mesh_initialization(self):
        """Test mesh orchestrator initialization."""
        orchestrator = MeshOrchestrator()
        success = await orchestrator.initialize_mesh()
        assert success
        assert orchestrator.orchestration_active
        assert len(orchestrator.nodes) > 0
        
        # Clean up
        await orchestrator.shutdown_mesh()
    
    @pytest.mark.asyncio
    async def test_mesh_node_addition(self):
        """Test adding nodes to mesh."""
        orchestrator = MeshOrchestrator()
        await orchestrator.initialize_mesh()
        
        position = ScrollVector(1, 1, 0, 0, 0)
        node_id = await orchestrator.add_mesh_node(position)
        
        assert node_id in orchestrator.nodes
        assert orchestrator.nodes[node_id].position == position
        
        # Clean up
        await orchestrator.shutdown_mesh()
    
    @pytest.mark.asyncio
    async def test_mesh_task_submission(self):
        """Test mesh task submission."""
        orchestrator = MeshOrchestrator()
        await orchestrator.initialize_mesh()
        
        # Create test field
        vectors = [ScrollVector(1, 0, 0, 0, 0)]
        field = CodexDriftField(vectors, 1.0, 1.0, 0.95, datetime.now())
        
        task_id = await orchestrator.submit_mesh_task("field_transform", field)
        assert task_id in orchestrator.tasks
        
        # Wait briefly for task processing
        await asyncio.sleep(0.5)
        
        # Clean up
        await orchestrator.shutdown_mesh()


class TestSymbolicFieldComputer:
    """Test the Symbolic Field Computer component."""
    
    def test_symbolic_computer_initialization(self):
        """Test symbolic field computer initialization."""
        computer = SymbolicFieldComputer()
        assert len(computer.symbolic_fields) == 0
        assert len(computer.expression_cache) > 0  # Should have fundamental expressions
        
    def test_symbolic_field_creation(self):
        """Test symbolic field creation."""
        computer = SymbolicFieldComputer()
        
        expressions = ["sin(x)*cos(y)", "exp(-z**2)", "t*sqrt(1+s**2)"]
        field_id = computer.create_symbolic_field("test_field", expressions)
        
        assert field_id in computer.symbolic_fields
        field = computer.symbolic_fields[field_id]
        assert len(field.expressions) == 3
        
    def test_field_evaluation(self):
        """Test field evaluation at vector."""
        computer = SymbolicFieldComputer()
        
        expressions = ["x**2", "y**2", "z**2"]
        field_id = computer.create_symbolic_field("test_field", expressions)
        
        vector = ScrollVector(2, 3, 4, 0, 0)
        results = computer.compute_field_at_vector(field_id, vector)
        
        assert len(results) == 3
        assert "expr_0" in results
        assert abs(results["expr_0"] - 4.0) < 1e-10  # x^2 = 2^2 = 4
        assert abs(results["expr_1"] - 9.0) < 1e-10  # y^2 = 3^2 = 9
        assert abs(results["expr_2"] - 16.0) < 1e-10  # z^2 = 4^2 = 16


class TestMemoryRecursionManager:
    """Test the Memory Recursion Manager component."""
    
    def test_memory_manager_initialization(self):
        """Test memory manager initialization."""
        manager = MemoryRecursionManager()
        assert len(manager.recursion_layers) == 10  # Default depth
        assert manager.max_recursion_depth == 10
        
    def test_memory_fragment_storage(self):
        """Test memory fragment storage."""
        manager = MemoryRecursionManager()
        
        content = {"test": "data", "timestamp": datetime.now().isoformat()}
        context_vector = ScrollVector(1, 0, 0, 0, 0)
        
        fragment_id = manager.store_memory_fragment(content, context_vector)
        assert fragment_id.startswith("frag_")
        
        # Check if fragment was stored in appropriate layer
        found = False
        for layer in manager.recursion_layers.values():
            if fragment_id in layer.fragments:
                found = True
                break
        assert found
        
    def test_memory_fragment_retrieval(self):
        """Test memory fragment retrieval."""
        manager = MemoryRecursionManager()
        
        # Store test fragment
        content = {"test": "data"}
        context_vector = ScrollVector(1, 0, 0, 0, 0)
        fragment_id = manager.store_memory_fragment(content, context_vector)
        
        # Retrieve similar fragments
        query_vector = ScrollVector(1.1, 0.1, 0, 0, 0)  # Similar to stored vector
        retrieved = manager.retrieve_memory_fragments(query_vector, max_results=5)
        
        assert len(retrieved) > 0
        assert any(f.fragment_id == fragment_id for f in retrieved)
        
    @pytest.mark.asyncio
    async def test_recursive_computation(self):
        """Test recursive computation."""
        manager = MemoryRecursionManager()
        
        initial_vector = ScrollVector(1, 1, 0, 0, 0)
        recursion_id = manager.start_recursive_computation(
            initial_vector, "field_convergence", max_iterations=10
        )
        
        assert recursion_id in manager.active_recursions
        
        # Wait for computation to complete
        await asyncio.sleep(0.5)
        
        status = manager.get_recursion_status(recursion_id)
        assert status is not None
        assert status["status"] in ["running", "converged", "max_iterations_reached"]


class TestAgentActivator:
    """Test the Agent Activator component."""
    
    def test_agent_activator_initialization(self):
        """Test agent activator initialization."""
        activator = AgentActivator()
        assert len(activator.agents) == 0
        assert len(activator.agent_profiles) == 0
        assert activator.max_agents == 50
        
    def test_agent_profile_registration(self):
        """Test agent profile registration."""
        activator = AgentActivator()
        
        capabilities = [AgentCapability.SCROLLMATH_COMPUTATION, AgentCapability.FIELD_ANALYSIS]
        position = ScrollVector(0, 0, 0, 0, 0)
        
        profile_id = activator.register_agent_profile(
            "test_agent", capabilities, position
        )
        
        assert profile_id in activator.agent_profiles
        profile = activator.agent_profiles[profile_id]
        assert profile.agent_type == "test_agent"
        assert len(profile.capabilities) == 2
        
    @pytest.mark.asyncio
    async def test_agent_activation(self):
        """Test agent activation."""
        activator = AgentActivator()
        
        # Register profile
        capabilities = [AgentCapability.SCROLLMATH_COMPUTATION]
        position = ScrollVector(0, 0, 0, 0, 0)
        profile_id = activator.register_agent_profile("test_agent", capabilities, position)
        
        # Activate agent
        agent_id = await activator.activate_agent(profile_id)
        assert agent_id is not None
        assert agent_id in activator.agents
        
        # Check agent status
        agent = activator.agents[agent_id]
        assert agent.profile.agent_type == "test_agent"
        
        # Clean up
        await agent.terminate()
        
    @pytest.mark.asyncio
    async def test_agent_swarm_activation(self):
        """Test agent swarm activation."""
        activator = AgentActivator()
        
        capabilities = [AgentCapability.SCROLLMATH_COMPUTATION, AgentCapability.FIELD_ANALYSIS]
        center_position = ScrollVector(0, 0, 0, 0, 0)
        
        agents = await activator.activate_agent_swarm(
            "swarm_agent", 3, capabilities, center_position
        )
        
        assert len(agents) == 3
        for agent_id in agents:
            assert agent_id in activator.agents
            
        # Clean up
        for agent_id in agents:
            if agent_id in activator.agents:
                await activator.agents[agent_id].terminate()


class TestIntegration:
    """Integration tests for component interaction."""
    
    @pytest.mark.asyncio
    async def test_scrollmath_to_mesh_integration(self):
        """Test integration between ScrollMath Engine and Mesh Orchestrator."""
        # Initialize components
        engine = ScrollMathEngine()
        orchestrator = MeshOrchestrator()
        
        await orchestrator.initialize_mesh()
        
        # Create drift field
        vectors = [ScrollVector(1, 0, 0, 0, 0), ScrollVector(0, 1, 0, 0, 0)]
        field = engine.create_drift_field(vectors)
        
        # Submit to mesh
        task_id = await orchestrator.submit_mesh_task("field_transform", field)
        
        # Wait for processing
        await asyncio.sleep(0.5)
        
        # Check task status
        task = orchestrator.tasks[task_id]
        assert task.status in ["executing", "completed"]
        
        # Clean up
        await orchestrator.shutdown_mesh()
        
    def test_engine_status_reporting(self):
        """Test comprehensive status reporting."""
        engine = ScrollMathEngine()
        
        # Create some drift fields
        vectors = [ScrollVector(1, 0, 0, 0, 0)]
        field1 = engine.create_drift_field(vectors)
        field2 = engine.create_drift_field(vectors)
        
        status = engine.get_engine_status()
        assert status["active_fields"] == 2
        assert "engine_version" in status
        assert status["engine_version"] == "ΩΔ143-1.0.0"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])