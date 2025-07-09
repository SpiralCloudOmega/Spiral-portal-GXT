# ΩΔ143 Codex Drift 5D Capsule

A comprehensive standalone package for advanced scrollmath mesh orchestration, symbolic field computation, memory recursion, and agent activation in cluster runtimes.

## Overview

The ΩΔ143 Codex Drift 5D Capsule is a sophisticated computational system that operates in 5-dimensional space (x, y, z, temporal, symbolic) to enable:

- **Advanced Scrollmath Computation**: 5D vector operations and codex drift field processing
- **Mesh Orchestration**: Distributed computation across mesh nodes with intelligent task routing
- **Symbolic Field Processing**: Mathematical symbolic computation with pattern recognition
- **Memory Recursion**: Hierarchical memory management with recursive pattern storage
- **Agent Activation**: Autonomous agent coordination with adaptive behavior
- **Notion Integration**: Bidirectional synchronization with Notion databases and pages
- **Runtime Management**: Complete lifecycle management and monitoring

## Architecture

### Core Components

#### 1. ScrollMath Engine (`capsule_core/scrollmath_engine.py`)
- **Purpose**: Core 5D mathematical computation engine
- **Capabilities**:
  - 5D vector operations (addition, multiplication, normalization)
  - Codex drift field creation and manipulation
  - Field transformation and resonance calculation
  - Symbolic sequence generation
  - Field manifests and status reporting

#### 2. Mesh Orchestrator (`capsule_core/mesh_orchestrator.py`)
- **Purpose**: Distributed mesh coordination and task orchestration
- **Capabilities**:
  - Dynamic mesh topology management
  - Node health monitoring and heartbeat tracking
  - Task distribution and load balancing
  - Fault tolerance and recovery
  - Performance optimization

#### 3. Symbolic Field Computer (`capsule_core/symbolic_field_computer.py`)
- **Purpose**: Advanced symbolic mathematics in 5D space
- **Capabilities**:
  - Symbolic expression parsing and evaluation
  - Field gradient computation
  - Symmetry analysis and pattern detection
  - Mathematical optimization
  - Domain-specific computation (mathematical, logical, geometric, temporal, quantum)

#### 4. Memory Recursion Manager (`capsule_core/memory_recursion_manager.py`)
- **Purpose**: Hierarchical memory management with recursive computation
- **Capabilities**:
  - Multi-level memory hierarchy (10 levels by default)
  - Fragment storage with context vectors
  - Recursive computation patterns
  - Temporal persistence and cleanup
  - Pattern recognition and retrieval

#### 5. Agent Activator (`capsule_core/agent_activator.py`)
- **Purpose**: Agent lifecycle management and coordination
- **Capabilities**:
  - Agent spawning and termination
  - Inter-agent communication
  - Capability matching and task assignment
  - Swarm coordination
  - Adaptive learning and behavior

### Integration Components

#### 6. Notion Sync Agent (`notion_sync/notion_sync_agent.py`)
- **Purpose**: Bidirectional synchronization with Notion
- **Capabilities**:
  - Database and page management
  - Real-time synchronization
  - Field mapping and data transformation
  - Error handling and retry logic

#### 7. Runtime Launcher (`runtime_launcher/capsule_launcher.py`)
- **Purpose**: Complete runtime environment management
- **Capabilities**:
  - Component initialization and integration
  - Health monitoring and metrics collection
  - Performance optimization
  - Graceful shutdown and cleanup

## Quick Start

### Prerequisites

- Python 3.8+
- Docker (optional, for containerized deployment)
- Kubernetes (optional, for cluster deployment)

### Installation

```bash
# Clone the repository
git clone https://github.com/SpiralCloudOmega/Spiral-portal-GXT.git
cd Spiral-portal-GXT/ΩΔ143_CodexDrift_GitHub

# Install dependencies
pip install -r requirements.txt

# Run the capsule
python runtime_launcher/capsule_launcher.py
```

### Configuration

Create a `capsule_config.json` file:

```json
{
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
    "enabled": false,
    "notion_token": "your_notion_token_here",
    "sync_interval": 300
  }
}
```

## Usage Examples

### Basic Scrollmath Computation

```python
from capsule_core import ScrollMathEngine, ScrollVector

# Initialize engine
engine = ScrollMathEngine()

# Create scroll vectors
vectors = [
    ScrollVector(1, 0, 0, 0, 0.5),
    ScrollVector(0, 1, 0, 0.5, 0),
    ScrollVector(0, 0, 1, 0, 0.8)
]

# Create codex drift field
field = engine.create_drift_field(vectors, drift_coeff=1.0)

# Perform 5D transformation
target = ScrollVector(0.5, 0.5, 0.5, 0.1, 0.3)
transformed = engine.compute_5d_transform(field, target)

print(f"Transformed vector: {transformed}")
```

### Mesh Orchestration

```python
import asyncio
from capsule_core import MeshOrchestrator

async def main():
    # Initialize mesh
    orchestrator = MeshOrchestrator()
    await orchestrator.initialize_mesh()
    
    # Submit task
    task_id = await orchestrator.submit_mesh_task(
        "field_transform", field, priority=1
    )
    
    # Get status
    status = orchestrator.get_mesh_status()
    print(f"Mesh status: {status}")

asyncio.run(main())
```

### Symbolic Field Computation

```python
from capsule_core import SymbolicFieldComputer

# Initialize computer
computer = SymbolicFieldComputer()

# Create symbolic field
field_id = computer.create_symbolic_field(
    "wave_field",
    ["sin(x)*cos(y)", "exp(-z**2)", "t*sqrt(1+s**2)"]
)

# Compute field at vector
vector = ScrollVector(1, 1, 0, 0.5, 0.3)
values = computer.compute_field_at_vector(field_id, vector)
print(f"Field values: {values}")
```

### Agent Activation

```python
import asyncio
from capsule_core import AgentActivator, AgentCapability

async def main():
    # Initialize activator
    activator = AgentActivator()
    
    # Activate agent swarm
    agents = await activator.activate_agent_swarm(
        "compute_agent", 5,
        [AgentCapability.SCROLLMATH_COMPUTATION, AgentCapability.FIELD_ANALYSIS],
        ScrollVector(0, 0, 0, 0, 0)
    )
    
    print(f"Activated {len(agents)} agents")

asyncio.run(main())
```

## Docker Deployment

### Build Image

```bash
docker build -t codex-drift-5d:latest .
```

### Run Container

```bash
docker run -d \
  --name codex-drift-capsule \
  -p 8080:8080 \
  -p 8081:8081 \
  -p 8082:8082 \
  -p 8083:8083 \
  -v $(pwd)/config:/app/config \
  -v $(pwd)/data:/app/data \
  codex-drift-5d:latest
```

### Docker Compose

```yaml
version: '3.8'
services:
  codex-drift-capsule:
    image: codex-drift-5d:latest
    ports:
      - "8080:8080"
      - "8081:8081"
      - "8082:8082"
      - "8083:8083"
    environment:
      - CAPSULE_MODE=standalone
      - LOG_LEVEL=INFO
    volumes:
      - ./config:/app/config
      - ./data:/app/data
    restart: unless-stopped
```

## Kubernetes Deployment

### Apply Manifests

```bash
cd workflows/k8s
export ENVIRONMENT=production
export NAMESPACE=omega-delta-143
export IMAGE_TAG=latest

envsubst < deployment-template.yaml > deployment.yaml
kubectl apply -f deployment.yaml
```

### Monitor Deployment

```bash
kubectl get pods -n omega-delta-143
kubectl logs -f deployment/codex-drift-capsule -n omega-delta-143
kubectl port-forward service/codex-drift-capsule-service 8080:8080 -n omega-delta-143
```

## API Endpoints

### Health and Status

- `GET /health` - Health check endpoint
- `GET /ready` - Readiness check endpoint
- `GET /status` - Comprehensive status information
- `GET /metrics` - Prometheus-compatible metrics

### ScrollMath Engine

- `POST /api/v1/scrollmath/compute` - Perform scrollmath computation
- `GET /api/v1/scrollmath/fields` - List active drift fields
- `POST /api/v1/scrollmath/transform` - Execute 5D transformation

### Mesh Orchestrator

- `GET /api/v1/mesh/status` - Get mesh status
- `POST /api/v1/mesh/tasks` - Submit mesh task
- `GET /api/v1/mesh/nodes` - List mesh nodes

### Agent Activator

- `GET /api/v1/agents/status` - Get agent activation status
- `POST /api/v1/agents/activate` - Activate agents
- `POST /api/v1/agents/message` - Send inter-agent message

### Notion Sync

- `GET /api/v1/notion/status` - Get sync status
- `POST /api/v1/notion/sync` - Trigger manual sync
- `POST /api/v1/notion/create-database` - Create Notion database

## Configuration Reference

### Environment Variables

- `CAPSULE_MODE`: Runtime mode (`standalone`, `cluster`)
- `LOG_LEVEL`: Logging level (`DEBUG`, `INFO`, `WARNING`, `ERROR`)
- `ENVIRONMENT`: Deployment environment (`development`, `staging`, `production`)

### ScrollMath Engine Configuration

```json
{
  "scrollmath_engine": {
    "field_resolution": 1024,      // Field computation resolution
    "drift_sensitivity": 0.01      // Drift calculation sensitivity
  }
}
```

### Mesh Orchestrator Configuration

```json
{
  "mesh_orchestrator": {
    "max_nodes": 100,              // Maximum mesh nodes
    "heartbeat_interval": 10,      // Heartbeat interval (seconds)
    "task_timeout": 300            // Task timeout (seconds)
  }
}
```

### Memory Manager Configuration

```json
{
  "memory_manager": {
    "max_recursion_depth": 10,     // Maximum recursion levels
    "fragment_lifetime_days": 30,  // Fragment retention period
    "coherence_threshold": 0.5     // Coherence threshold for retrieval
  }
}
```

### Agent Activator Configuration

```json
{
  "agent_activator": {
    "max_agents": 50,              // Maximum active agents
    "message_broker_size": 1000,   // Message queue size
    "agent_cleanup_interval": 300  // Cleanup interval (seconds)
  }
}
```

### Notion Sync Configuration

```json
{
  "notion_sync": {
    "enabled": true,               // Enable Notion integration
    "notion_token": "secret_...",  // Notion API token
    "notion_version": "2022-06-28", // Notion API version
    "sync_interval": 300,          // Sync interval (seconds)
    "max_retries": 3,              // Maximum retry attempts
    "batch_size": 100              // Batch processing size
  }
}
```

## Monitoring and Observability

### Metrics

The capsule exposes the following metrics:

- `scrollmath_computations_per_second` - Rate of scrollmath computations
- `active_mesh_nodes` - Number of active mesh nodes
- `memory_fragments_stored` - Total memory fragments across all levels
- `active_agents` - Number of active agents
- `field_coherence_average` - Average field coherence

### Logging

Structured logging with configurable levels:

```
2024-01-01 12:00:00 - CapsuleRuntime - INFO - Capsule runtime initialization completed
2024-01-01 12:00:01 - ScrollMathEngine - INFO - Created drift field with 3 vectors
2024-01-01 12:00:02 - MeshOrchestrator - INFO - Mesh topology initialized with 5 nodes
```

### Health Checks

- **Liveness Probe**: `/health` - Verifies the capsule is running
- **Readiness Probe**: `/ready` - Verifies the capsule is ready to serve traffic

## Testing

### Unit Tests

```bash
python -m pytest tests/ -v --cov=capsule_core
```

### Integration Tests

```bash
python -m pytest tests/integration/ -v
```

### Performance Tests

```bash
python -m pytest tests/performance/ -v --benchmark-only
```

## Development

### Code Style

```bash
# Format code
black .
isort .

# Lint code
flake8 .

# Security scan
bandit -r .
```

### Pre-commit Hooks

```bash
pip install pre-commit
pre-commit install
```

## Troubleshooting

### Common Issues

#### High Memory Usage
- Reduce `max_recursion_depth` in memory manager
- Decrease `fragment_lifetime_days`
- Adjust `field_resolution` in scrollmath engine

#### Mesh Node Connection Issues
- Check `heartbeat_interval` configuration
- Verify network connectivity between nodes
- Review mesh orchestrator logs

#### Agent Communication Problems
- Increase `message_broker_size`
- Check agent capability matching
- Review agent activator status

#### Notion Sync Failures
- Verify Notion API token validity
- Check rate limit configurations
- Review sync mapping configurations

### Log Analysis

```bash
# Filter by component
kubectl logs deployment/codex-drift-capsule -n omega-delta-143 | grep "MeshOrchestrator"

# Monitor real-time logs
kubectl logs -f deployment/codex-drift-capsule -n omega-delta-143

# Export logs for analysis
kubectl logs deployment/codex-drift-capsule -n omega-delta-143 > capsule.log
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-capability`
3. Make changes and add tests
4. Run the test suite: `python -m pytest`
5. Format code: `black .` and `isort .`
6. Submit a pull request

## License

This project is part of the Spiral Cloud Omega ecosystem. All rights reserved.

## Support

- **Issues**: Report bugs and feature requests on GitHub
- **Documentation**: Check component-specific README files
- **Community**: Join discussions in project issues

---

**ΩΔ143 Codex Drift 5D Capsule** - Advanced scrollmath mesh orchestration for the modern computational stack