#!/usr/bin/env python3
"""
ΩΔ143 Codex Drift 5D Capsule Demonstration

A simple demonstration of the core functionality.
"""

import asyncio
import json
from datetime import datetime

# Import core components
from capsule_core import (
    ScrollMathEngine, MeshOrchestrator, SymbolicFieldComputer,
    MemoryRecursionManager, AgentActivator
)
from capsule_core.scrollmath_engine import ScrollVector
from capsule_core.agent_activator import AgentCapability


async def demonstrate_capsule():
    """Demonstrate the ΩΔ143 Codex Drift 5D Capsule functionality."""
    
    print("🌀 ΩΔ143 Codex Drift 5D Capsule Demonstration")
    print("=" * 50)
    
    # 1. ScrollMath Engine Demo
    print("\n📐 ScrollMath Engine Demo")
    print("-" * 25)
    
    engine = ScrollMathEngine()
    
    # Create 5D vectors
    vectors = [
        ScrollVector(1, 0, 0, 0, 0.5),
        ScrollVector(0, 1, 0, 0.5, 0),
        ScrollVector(0, 0, 1, 0, 0.8)
    ]
    print(f"Created {len(vectors)} 5D scroll vectors")
    
    # Create codex drift field
    field = engine.create_drift_field(vectors, drift_coeff=1.0, field_strength=1.2)
    print(f"Created codex drift field with {len(field.vectors)} vectors")
    
    # Perform 5D transformation
    target = ScrollVector(0.5, 0.5, 0.5, 0.1, 0.3)
    transformed = engine.compute_5d_transform(field, target)
    print(f"5D transformation: magnitude {transformed.magnitude():.3f}")
    
    # Calculate resonance
    field2 = engine.create_drift_field([ScrollVector(0.8, 0.6, 0, 0, 0.4)])
    resonance = engine.calculate_mesh_resonance(field, field2)
    print(f"Mesh resonance between fields: {resonance:.3f}")
    
    # 2. Symbolic Field Computer Demo
    print("\n🔣 Symbolic Field Computer Demo")
    print("-" * 32)
    
    computer = SymbolicFieldComputer()
    
    # Create symbolic field
    expressions = [
        "sin(x)*cos(y)",
        "exp(-z**2/2)",
        "t*sqrt(1+s**2)",
        "x**2 + y**2 - z**2"
    ]
    field_id = computer.create_symbolic_field("demo_field", expressions)
    print(f"Created symbolic field '{field_id}' with {len(expressions)} expressions")
    
    # Evaluate field
    eval_vector = ScrollVector(1, 1, 0.5, 0.2, 0.3)
    results = computer.compute_field_at_vector(field_id, eval_vector)
    print(f"Field evaluation at vector: {len(results)} results")
    
    # Compute gradient
    gradient = computer.compute_field_gradient(field_id, eval_vector)
    print(f"5D gradient computed with {len(gradient)} partial derivatives")
    
    # 3. Memory Recursion Manager Demo
    print("\n🧠 Memory Recursion Manager Demo")
    print("-" * 34)
    
    memory_manager = MemoryRecursionManager()
    
    # Store memory fragments
    for i in range(5):
        content = {
            "computation_id": f"comp_{i}",
            "result": f"result_{i}",
            "timestamp": datetime.now().isoformat()
        }
        context = ScrollVector(i*0.2, i*0.3, 0, i*0.1, i*0.05)
        fragment_id = memory_manager.store_memory_fragment(content, context, importance=0.8)
        print(f"Stored memory fragment {i+1}: {fragment_id[:12]}...")
    
    # Retrieve similar memories
    query_vector = ScrollVector(0.4, 0.6, 0, 0.2, 0.1)
    retrieved = memory_manager.retrieve_memory_fragments(query_vector, max_results=3)
    print(f"Retrieved {len(retrieved)} similar memory fragments")
    
    # Start recursive computation
    recursion_id = memory_manager.start_recursive_computation(
        query_vector, "field_convergence", max_iterations=50
    )
    print(f"Started recursive computation: {recursion_id[:12]}...")
    
    # 4. Mesh Orchestrator Demo
    print("\n🕸️ Mesh Orchestrator Demo")
    print("-" * 26)
    
    orchestrator = MeshOrchestrator()
    success = await orchestrator.initialize_mesh()
    print(f"Mesh initialization: {'✅ Success' if success else '❌ Failed'}")
    
    if success:
        # Add mesh nodes
        for i in range(3):
            pos = ScrollVector(i, i*0.5, 0, 0, i*0.2)
            node_id = await orchestrator.add_mesh_node(pos, compute_capacity=1.0)
            print(f"Added mesh node {i+1}: {node_id[:12]}...")
        
        # Submit mesh tasks
        task_id = await orchestrator.submit_mesh_task("field_transform", field, priority=1)
        print(f"Submitted mesh task: {task_id[:12]}...")
        
        # Wait for task processing
        await asyncio.sleep(0.5)
        
        status = orchestrator.get_mesh_status()
        print(f"Mesh status: {status['active_nodes']} active nodes, {status['completed_tasks']} completed tasks")
    
    # 5. Agent Activator Demo
    print("\n🤖 Agent Activator Demo")
    print("-" * 22)
    
    activator = AgentActivator()
    
    # Activate agent swarm
    capabilities = [
        AgentCapability.SCROLLMATH_COMPUTATION,
        AgentCapability.FIELD_ANALYSIS,
        AgentCapability.PATTERN_RECOGNITION
    ]
    center = ScrollVector(0, 0, 0, 0, 0)
    
    agents = await activator.activate_agent_swarm(
        "demo_agent", 4, capabilities, center, spread_radius=1.0
    )
    print(f"Activated agent swarm: {len(agents)} agents")
    
    # Send inter-agent message
    if len(agents) >= 2:
        message_id = activator.send_message(
            agents[0], agents[1], "coordination_request",
            {"task": "field_analysis", "priority": 1}
        )
        print(f"Sent inter-agent message: {message_id[:12]}...")
    
    # Get activation status
    activation_status = activator.get_activation_status()
    print(f"Activation status: {activation_status['total_agents']} total agents")
    
    # 6. System Integration Demo
    print("\n🔗 System Integration Demo")
    print("-" * 27)
    
    # Integrate components
    activator.integrate_with_mesh(orchestrator)
    activator.integrate_with_memory(memory_manager)
    print("✅ Integrated Agent Activator with Mesh Orchestrator and Memory Manager")
    
    # Coordinate cluster activation
    cluster_result = await activator.coordinate_cluster_activation(
        "distributed_computation",
        [AgentCapability.SCROLLMATH_COMPUTATION, AgentCapability.MESH_COORDINATION],
        cluster_size=3
    )
    print(f"Cluster activation: {cluster_result['status']}, {cluster_result.get('cluster_size', 0)} agents")
    
    # Wait for system interaction
    await asyncio.sleep(1.0)
    
    # 7. Final Status Report
    print("\n📊 Final System Status")
    print("-" * 22)
    
    engine_status = engine.get_engine_status()
    print(f"ScrollMath Engine: {engine_status['active_fields']} active fields")
    
    computer_status = computer.get_computer_status()
    print(f"Symbolic Computer: {computer_status['active_fields']} active fields")
    
    memory_status = memory_manager.get_manager_status()
    print(f"Memory Manager: {memory_status['total_fragments']} total fragments")
    
    if success:
        mesh_status = orchestrator.get_mesh_status()
        print(f"Mesh Orchestrator: {mesh_status['total_nodes']} total nodes")
    
    final_activation_status = activator.get_activation_status()
    print(f"Agent Activator: {final_activation_status['total_agents']} total agents")
    
    print("\n🎉 ΩΔ143 Codex Drift 5D Capsule Demonstration Complete!")
    print("Advanced scrollmath mesh orchestration, symbolic field computation,")
    print("memory recursion, and agent activation successfully demonstrated.")
    
    # Cleanup
    print("\n🧹 Cleaning up...")
    
    # Terminate agents
    for agent_id in activator.agents:
        await activator.agents[agent_id].terminate()
    
    # Shutdown mesh
    if success:
        await orchestrator.shutdown_mesh()
    
    print("✅ Cleanup complete")


if __name__ == "__main__":
    print("Starting ΩΔ143 Codex Drift 5D Capsule Demonstration...")
    asyncio.run(demonstrate_capsule())