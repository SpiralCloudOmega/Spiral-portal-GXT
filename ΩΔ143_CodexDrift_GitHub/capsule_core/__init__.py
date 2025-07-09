"""
ΩΔ143 Codex Drift 5D Capsule Core Module

This module provides the core scrollmath logic and mesh orchestration
for the ΩΔ143 Codex Drift 5D Capsule system.
"""

from .scrollmath_engine import ScrollMathEngine
from .mesh_orchestrator import MeshOrchestrator
from .symbolic_field_computer import SymbolicFieldComputer
from .memory_recursion_manager import MemoryRecursionManager
from .agent_activator import AgentActivator

__version__ = "1.0.0"
__all__ = [
    "ScrollMathEngine",
    "MeshOrchestrator", 
    "SymbolicFieldComputer",
    "MemoryRecursionManager",
    "AgentActivator"
]