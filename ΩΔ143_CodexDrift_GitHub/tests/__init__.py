#!/usr/bin/env python3
"""
Test configuration and utilities for the ΩΔ143 Codex Drift 5D Capsule test suite.
"""

import pytest
import asyncio
import sys
import os

# Configure test environment
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Test configuration
pytest_plugins = ['pytest_asyncio']


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def sample_config():
    """Provide sample configuration for testing."""
    return {
        "log_level": "INFO",
        "scrollmath_engine": {
            "field_resolution": 512,
            "drift_sensitivity": 0.01
        },
        "mesh_orchestrator": {
            "max_nodes": 10,
            "heartbeat_interval": 5,
            "task_timeout": 60
        },
        "memory_manager": {
            "max_recursion_depth": 5,
            "fragment_lifetime_days": 7,
            "coherence_threshold": 0.5
        },
        "agent_activator": {
            "max_agents": 10,
            "message_broker_size": 100
        }
    }


@pytest.fixture
def sample_vectors():
    """Provide sample scroll vectors for testing."""
    from capsule_core.scrollmath_engine import ScrollVector
    
    return [
        ScrollVector(1, 0, 0, 0, 0.5),
        ScrollVector(0, 1, 0, 0.5, 0),
        ScrollVector(0, 0, 1, 0, 0.8),
        ScrollVector(0.5, 0.5, 0.5, 0.1, 0.3),
        ScrollVector(-1, 0, 0, 0, -0.2)
    ]