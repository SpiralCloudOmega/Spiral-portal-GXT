#!/usr/bin/env python3
"""
Runtime Scrollmath Launcher for ΩΔ143 Codex Drift 5D Capsule

Provides runtime environment initialization, management, and control
for the capsule's scrollmath computation and mesh orchestration systems.
"""

import asyncio
import argparse
import json
import sys
import os
import signal
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

# Add the capsule core to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from capsule_core import (
    ScrollMathEngine, MeshOrchestrator, SymbolicFieldComputer,
    MemoryRecursionManager, AgentActivator
)
from capsule_core.scrollmath_engine import ScrollVector, CodexDriftField
from notion_sync import NotionSyncAgent


class RuntimeEnvironment:
    """
    Manages the runtime environment for the ΩΔ143 Codex Drift 5D Capsule.
    
    Coordinates all capsule components and provides unified control interface.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the runtime environment."""
        self.config = config
        self.logger = self._setup_logging()
        
        # Core components
        self.scrollmath_engine: Optional[ScrollMathEngine] = None
        self.mesh_orchestrator: Optional[MeshOrchestrator] = None
        self.symbolic_computer: Optional[SymbolicFieldComputer] = None
        self.memory_manager: Optional[MemoryRecursionManager] = None
        self.agent_activator: Optional[AgentActivator] = None
        self.notion_sync: Optional[NotionSyncAgent] = None
        
        # Runtime state
        self.running = False
        self.startup_time: Optional[datetime] = None
        self.component_status: Dict[str, str] = {}
        
        # Performance metrics
        self.metrics = {
            "total_computations": 0,
            "active_agents": 0,
            "mesh_nodes": 0,
            "memory_fragments": 0,
            "uptime_seconds": 0
        }
        
        # Signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging configuration."""
        log_level = self.config.get("log_level", "INFO")
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        
        logging.basicConfig(
            level=getattr(logging, log_level),
            format=log_format,
            handlers=[
                logging.StreamHandler(sys.stdout),
                logging.FileHandler("capsule_runtime.log")
            ]
        )
        
        return logging.getLogger("CapsuleRuntime")
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        self.logger.info(f"Received signal {signum}, shutting down gracefully...")
        asyncio.create_task(self.shutdown())
    
    async def initialize(self) -> bool:
        """Initialize all capsule components."""
        try:
            self.logger.info("Initializing ΩΔ143 Codex Drift 5D Capsule Runtime...")
            self.startup_time = datetime.now()
            
            # Initialize core components
            await self._initialize_scrollmath_engine()
            await self._initialize_mesh_orchestrator()
            await self._initialize_symbolic_computer()
            await self._initialize_memory_manager()
            await self._initialize_agent_activator()
            
            # Initialize integrations
            if self.config.get("notion_sync", {}).get("enabled", False):
                await self._initialize_notion_sync()
            
            # Cross-component integration
            await self._integrate_components()
            
            self.running = True
            self.logger.info("Capsule runtime initialization completed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize runtime: {e}")
            return False
    
    async def _initialize_scrollmath_engine(self):
        """Initialize the ScrollMath Engine."""
        try:
            config = self.config.get("scrollmath_engine", {})
            self.scrollmath_engine = ScrollMathEngine(config)
            self.component_status["scrollmath_engine"] = "initialized"
            self.logger.info("ScrollMath Engine initialized")
        except Exception as e:
            self.component_status["scrollmath_engine"] = "failed"
            raise Exception(f"ScrollMath Engine initialization failed: {e}")
    
    async def _initialize_mesh_orchestrator(self):
        """Initialize the Mesh Orchestrator."""
        try:
            config = self.config.get("mesh_orchestrator", {})
            self.mesh_orchestrator = MeshOrchestrator(config)
            
            success = await self.mesh_orchestrator.initialize_mesh()
            if success:
                self.component_status["mesh_orchestrator"] = "initialized"
                self.logger.info("Mesh Orchestrator initialized")
            else:
                raise Exception("Mesh initialization failed")
        except Exception as e:
            self.component_status["mesh_orchestrator"] = "failed"
            raise Exception(f"Mesh Orchestrator initialization failed: {e}")
    
    async def _initialize_symbolic_computer(self):
        """Initialize the Symbolic Field Computer."""
        try:
            config = self.config.get("symbolic_computer", {})
            self.symbolic_computer = SymbolicFieldComputer(config)
            self.component_status["symbolic_computer"] = "initialized"
            self.logger.info("Symbolic Field Computer initialized")
        except Exception as e:
            self.component_status["symbolic_computer"] = "failed"
            raise Exception(f"Symbolic Computer initialization failed: {e}")
    
    async def _initialize_memory_manager(self):
        """Initialize the Memory Recursion Manager."""
        try:
            config = self.config.get("memory_manager", {})
            self.memory_manager = MemoryRecursionManager(config)
            self.component_status["memory_manager"] = "initialized"
            self.logger.info("Memory Recursion Manager initialized")
        except Exception as e:
            self.component_status["memory_manager"] = "failed"
            raise Exception(f"Memory Manager initialization failed: {e}")
    
    async def _initialize_agent_activator(self):
        """Initialize the Agent Activator."""
        try:
            config = self.config.get("agent_activator", {})
            self.agent_activator = AgentActivator(config)
            self.component_status["agent_activator"] = "initialized"
            self.logger.info("Agent Activator initialized")
        except Exception as e:
            self.component_status["agent_activator"] = "failed"
            raise Exception(f"Agent Activator initialization failed: {e}")
    
    async def _initialize_notion_sync(self):
        """Initialize the Notion Sync Agent."""
        try:
            config = self.config.get("notion_sync", {})
            self.notion_sync = NotionSyncAgent(config)
            
            success = await self.notion_sync.initialize()
            if success:
                self.component_status["notion_sync"] = "initialized"
                self.logger.info("Notion Sync Agent initialized")
            else:
                self.component_status["notion_sync"] = "failed"
                self.logger.warning("Notion Sync Agent initialization failed")
        except Exception as e:
            self.component_status["notion_sync"] = "failed"
            self.logger.warning(f"Notion Sync initialization failed: {e}")
    
    async def _integrate_components(self):
        """Integrate components for cross-system coordination."""
        try:
            # Integrate agent activator with mesh orchestrator
            if self.agent_activator and self.mesh_orchestrator:
                self.agent_activator.integrate_with_mesh(self.mesh_orchestrator)
                self.logger.info("Integrated Agent Activator with Mesh Orchestrator")
            
            # Integrate agent activator with memory manager
            if self.agent_activator and self.memory_manager:
                self.agent_activator.integrate_with_memory(self.memory_manager)
                self.logger.info("Integrated Agent Activator with Memory Manager")
            
            self.logger.info("Component integration completed")
            
        except Exception as e:
            self.logger.error(f"Component integration failed: {e}")
    
    async def run(self):
        """Run the main runtime loop."""
        try:
            self.logger.info("Starting main runtime loop...")
            
            # Start monitoring and maintenance tasks
            asyncio.create_task(self._metrics_collector())
            asyncio.create_task(self._health_monitor())
            asyncio.create_task(self._performance_optimizer())
            
            # Example: Start some initial computations
            await self._run_initial_computations()
            
            # Main loop - keep running until shutdown
            while self.running:
                await self._runtime_cycle()
                await asyncio.sleep(1.0)  # Main loop cycle
                
        except Exception as e:
            self.logger.error(f"Runtime loop error: {e}")
        finally:
            await self.shutdown()
    
    async def _run_initial_computations(self):
        """Run initial computations to demonstrate system functionality."""
        try:
            self.logger.info("Running initial system computations...")
            
            # Create initial scroll vectors
            vectors = [
                ScrollVector(1, 0, 0, 0, 0.5),
                ScrollVector(0, 1, 0, 0.5, 0),
                ScrollVector(0, 0, 1, 0, 0.8)
            ]
            
            # Create codex drift field
            field = self.scrollmath_engine.create_drift_field(vectors, drift_coeff=1.0)
            
            # Submit mesh task
            if self.mesh_orchestrator:
                task_id = await self.mesh_orchestrator.submit_mesh_task(
                    "field_transform", field, priority=1
                )
                self.logger.info(f"Submitted initial mesh task: {task_id}")
            
            # Create symbolic field
            if self.symbolic_computer:
                field_id = self.symbolic_computer.create_symbolic_field(
                    "initial_field",
                    ["sin(x)*cos(y)", "exp(-z**2)", "t*sqrt(1+s**2)"]
                )
                self.logger.info(f"Created initial symbolic field: {field_id}")
            
            # Store memory fragment
            if self.memory_manager:
                fragment_id = self.memory_manager.store_memory_fragment(
                    content={"type": "initial_computation", "timestamp": datetime.now().isoformat()},
                    context_vector=vectors[0],
                    importance=1.0
                )
                self.logger.info(f"Stored initial memory fragment: {fragment_id}")
            
            # Activate initial agents
            if self.agent_activator:
                from capsule_core.agent_activator import AgentCapability
                
                agents = await self.agent_activator.activate_agent_swarm(
                    "compute_agent", 3,
                    [AgentCapability.SCROLLMATH_COMPUTATION, AgentCapability.FIELD_ANALYSIS],
                    ScrollVector(0, 0, 0, 0, 0)
                )
                self.logger.info(f"Activated {len(agents)} initial agents")
            
            self.logger.info("Initial computations completed")
            
        except Exception as e:
            self.logger.error(f"Initial computations failed: {e}")
    
    async def _runtime_cycle(self):
        """Execute one cycle of the runtime loop."""
        try:
            # Update metrics
            await self._update_metrics()
            
            # Check component health
            await self._check_component_health()
            
            # Sync with Notion if enabled
            if self.notion_sync and self.component_status.get("notion_sync") == "initialized":
                # Sync runtime status
                runtime_data = {
                    "timestamp": datetime.now().isoformat(),
                    "uptime": self.metrics["uptime_seconds"],
                    "active_agents": self.metrics["active_agents"],
                    "mesh_nodes": self.metrics["mesh_nodes"],
                    "component_status": self.component_status.copy()
                }
                
                await self.notion_sync.sync_capsule_to_notion("runtime_status", runtime_data)
            
        except Exception as e:
            self.logger.error(f"Runtime cycle error: {e}")
    
    async def _update_metrics(self):
        """Update runtime metrics."""
        try:
            if self.startup_time:
                self.metrics["uptime_seconds"] = (datetime.now() - self.startup_time).total_seconds()
            
            if self.agent_activator:
                status = self.agent_activator.get_activation_status()
                self.metrics["active_agents"] = status["total_agents"]
            
            if self.mesh_orchestrator:
                status = self.mesh_orchestrator.get_mesh_status()
                self.metrics["mesh_nodes"] = status["total_nodes"]
            
            if self.memory_manager:
                status = self.memory_manager.get_manager_status()
                self.metrics["memory_fragments"] = status["total_fragments"]
                
        except Exception as e:
            self.logger.error(f"Metrics update failed: {e}")
    
    async def _check_component_health(self):
        """Check health of all components."""
        try:
            # Check each component's health
            if self.scrollmath_engine:
                engine_status = self.scrollmath_engine.get_engine_status()
                if engine_status.get("active_fields", 0) >= 0:
                    self.component_status["scrollmath_engine"] = "healthy"
                else:
                    self.component_status["scrollmath_engine"] = "unhealthy"
            
            if self.mesh_orchestrator:
                mesh_status = self.mesh_orchestrator.get_mesh_status()
                if mesh_status.get("orchestration_active", False):
                    self.component_status["mesh_orchestrator"] = "healthy"
                else:
                    self.component_status["mesh_orchestrator"] = "unhealthy"
            
            # Log health status periodically
            if int(self.metrics["uptime_seconds"]) % 60 == 0:  # Every minute
                healthy_components = sum(1 for status in self.component_status.values() 
                                       if status == "healthy")
                total_components = len(self.component_status)
                self.logger.info(f"Component health: {healthy_components}/{total_components} healthy")
                
        except Exception as e:
            self.logger.error(f"Health check failed: {e}")
    
    async def _metrics_collector(self):
        """Background task for collecting detailed metrics."""
        while self.running:
            try:
                # Collect detailed metrics every 30 seconds
                await asyncio.sleep(30)
                
                if not self.running:
                    break
                
                # Log detailed status
                self.logger.info("=== Runtime Metrics ===")
                self.logger.info(f"Uptime: {self.metrics['uptime_seconds']:.0f} seconds")
                self.logger.info(f"Active Agents: {self.metrics['active_agents']}")
                self.logger.info(f"Mesh Nodes: {self.metrics['mesh_nodes']}")
                self.logger.info(f"Memory Fragments: {self.metrics['memory_fragments']}")
                
            except Exception as e:
                self.logger.error(f"Metrics collector error: {e}")
    
    async def _health_monitor(self):
        """Background task for health monitoring."""
        while self.running:
            try:
                await asyncio.sleep(60)  # Check every minute
                
                if not self.running:
                    break
                
                # Check for failed components and attempt recovery
                for component, status in self.component_status.items():
                    if status == "failed":
                        self.logger.warning(f"Component {component} is in failed state")
                        # Could implement recovery logic here
                
            except Exception as e:
                self.logger.error(f"Health monitor error: {e}")
    
    async def _performance_optimizer(self):
        """Background task for performance optimization."""
        while self.running:
            try:
                await asyncio.sleep(300)  # Optimize every 5 minutes
                
                if not self.running:
                    break
                
                # Simple optimization: adjust agent count based on load
                if self.agent_activator and self.metrics["active_agents"] < 5:
                    # Activate more agents if needed
                    from capsule_core.agent_activator import AgentCapability
                    
                    new_agents = await self.agent_activator.activate_agent_swarm(
                        "auto_agent", 2,
                        [AgentCapability.SCROLLMATH_COMPUTATION],
                        ScrollVector(0, 0, 0, 0, 0)
                    )
                    
                    if new_agents:
                        self.logger.info(f"Auto-activated {len(new_agents)} agents for optimization")
                
            except Exception as e:
                self.logger.error(f"Performance optimizer error: {e}")
    
    async def shutdown(self):
        """Gracefully shutdown the runtime."""
        try:
            if not self.running:
                return
            
            self.logger.info("Initiating graceful shutdown...")
            self.running = False
            
            # Shutdown components in reverse order
            if self.notion_sync:
                await self.notion_sync.cleanup()
                self.logger.info("Notion Sync Agent shutdown")
            
            if self.agent_activator:
                # Terminate all agents
                activation_status = self.agent_activator.get_activation_status()
                self.logger.info(f"Shutting down {activation_status['total_agents']} agents")
            
            if self.mesh_orchestrator:
                await self.mesh_orchestrator.shutdown_mesh()
                self.logger.info("Mesh Orchestrator shutdown")
            
            # Final metrics log
            uptime = (datetime.now() - self.startup_time).total_seconds() if self.startup_time else 0
            self.logger.info(f"Runtime shutdown completed. Total uptime: {uptime:.0f} seconds")
            
        except Exception as e:
            self.logger.error(f"Shutdown error: {e}")
    
    def get_runtime_status(self) -> Dict[str, Any]:
        """Get comprehensive runtime status."""
        return {
            "running": self.running,
            "startup_time": self.startup_time.isoformat() if self.startup_time else None,
            "uptime_seconds": self.metrics["uptime_seconds"],
            "component_status": self.component_status.copy(),
            "metrics": self.metrics.copy(),
            "config": {
                "log_level": self.config.get("log_level", "INFO"),
                "notion_sync_enabled": self.config.get("notion_sync", {}).get("enabled", False)
            }
        }


def load_config(config_path: str) -> Dict[str, Any]:
    """Load configuration from file."""
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return DEFAULT_CONFIG
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in config file: {e}")


DEFAULT_CONFIG = {
    "log_level": "INFO",
    "scrollmath_engine": {
        "field_resolution": 1024,
        "drift_sensitivity": 0.01
    },
    "mesh_orchestrator": {
        "max_nodes": 50,
        "heartbeat_interval": 10,
        "task_timeout": 300
    },
    "symbolic_computer": {},
    "memory_manager": {
        "max_recursion_depth": 10,
        "fragment_lifetime_days": 30,
        "coherence_threshold": 0.5
    },
    "agent_activator": {
        "max_agents": 30,
        "message_broker_size": 1000
    },
    "notion_sync": {
        "enabled": False,
        "notion_token": "",
        "sync_interval": 300
    }
}


async def main():
    """Main entry point for the runtime launcher."""
    parser = argparse.ArgumentParser(
        description="ΩΔ143 Codex Drift 5D Capsule Runtime Launcher"
    )
    parser.add_argument(
        "--config", "-c",
        default="capsule_config.json",
        help="Configuration file path"
    )
    parser.add_argument(
        "--log-level", "-l",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Logging level"
    )
    parser.add_argument(
        "--daemon", "-d",
        action="store_true",
        help="Run as daemon (background process)"
    )
    
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.config)
    config["log_level"] = args.log_level
    
    # Create and initialize runtime
    runtime = RuntimeEnvironment(config)
    
    success = await runtime.initialize()
    if not success:
        print("Failed to initialize runtime environment")
        sys.exit(1)
    
    # Run the runtime
    try:
        await runtime.run()
    except KeyboardInterrupt:
        print("\nShutdown requested by user")
    except Exception as e:
        print(f"Runtime error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())