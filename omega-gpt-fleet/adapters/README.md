# OmegaGPT Fleet Adapters

This directory contains all the specialized adapters for the OmegaGPT Fleet automation system. Each adapter provides a standardized interface to different tools, services, and platforms across various technology domains.

## Adapter Organization

Adapters are organized by domain for easy maintenance and discovery:

### Core Infrastructure
- **base_adapter.py** - Base adapter class that all adapters inherit from

### Domain-Specific Adapters

#### CAD (Computer-Aided Design) - `cad/`
- **FreeCAD Adapter** (`freecad_adapter.py`) - Professional CAD modeling and design
- **SolveSpace Adapter** (`solvespace_adapter.py`) - Parametric 2D/3D CAD
- **PythonOCC Adapter** (`pythonocc_adapter.py`) - Python-based CAD kernel
- **Build123d Adapter** (`build123d_adapter.py`) - Modern Python CAD framework
- **FreeCAD Library Adapter** (`freecad_library_adapter.py`) - CAD component library management
- **OpenJSCAD Adapter** (`openjscad_adapter.py`) - JavaScript-based CAD operations

#### EDA (Electronic Design Automation) - `eda/`
- **VTR Adapter** (`vtr_adapter.py`) - Verilog to Routing FPGA development

#### Web Infrastructure - `web/`
- **Caddy Adapter** (`caddy_adapter.py`) - Modern web server management
- **Caddy Docker Adapter** (`caddy_docker_adapter.py`) - Containerized web services

#### Research & Data - `research/`
- **NASA Adapter** (`nasa_adapter.py`) - NASA APIs and research data access

#### Networking & DevOps - `networking/`
- **NetBird Adapter** (`netbird_adapter.py`) - Secure network mesh management
- **Docker Adapter** (`docker_adapter.py`) - Container lifecycle management
- **Prometheus Exporters** - Various monitoring and metrics exporters
- **Diagramming Tools** - Network and infrastructure visualization
- **Dashboard Management** - Monitoring dashboard automation

#### Data Storage - `data/`
- **Apache Cassandra Adapter** (`cassandra_adapter.py`) - Distributed database management

#### Vision & Machine Learning - `vision_ml/`
- **PyTorch3D Adapter** (`pytorch3d_adapter.py`) - 3D computer vision and graphics
- **PyTorch Lightning Adapter** (`pytorch_lightning_adapter.py`) - ML training framework
- **PyTorch Image Models** (`timm_adapter.py`) - Pre-trained vision models

#### ScrollAI & Distributed Processing
- **ScrollAI ClusterSpawn Adapter (ΩΔ174)** (`scrollai_clusterspawn_adapter.py`) - Distributed ScrollAI cluster management for scroll chain expansion

## Base Adapter Framework

All adapters inherit from the `BaseAdapter` class, providing:

- **Standardized Interface**: Consistent initialization, execution, validation, and cleanup methods
- **Built-in Logging**: Structured activity logging and error handling
- **Configuration Management**: Flexible configuration parameter handling
- **Status Tracking**: Real-time adapter status and health monitoring
- **Metadata Support**: Capability and dependency declaration

### Standard Adapter Methods

```python
from omega_gpt_fleet.adapters.base_adapter import BaseAdapter

class ExampleAdapter(BaseAdapter):
    def initialize(self) -> bool:
        """Initialize the adapter and establish connections."""
        pass
    
    def execute(self, command: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a command with the given parameters.""" 
        pass
    
    def validate(self) -> bool:
        """Validate that the adapter is properly configured."""
        pass
    
    def cleanup(self) -> bool:
        """Clean up resources and connections."""
        pass
```

## Usage Patterns

### Basic Adapter Usage

```python
from omega_gpt_fleet.adapters.scrollai_clusterspawn_adapter import ScrollAIClusterSpawnAdapter

# Initialize adapter with configuration
config = {
    "api_endpoint": "http://localhost:8080",
    "namespace": "scrollai-clusters"
}
adapter = ScrollAIClusterSpawnAdapter(config)

# Initialize connection
if adapter.initialize():
    # Execute operations
    result = adapter.execute('spawn_cluster', {
        'name': 'my-scroll-cluster',
        'replicas': 5
    })
    
    # Check result
    if result['success']:
        print(f"Cluster spawned: {result['data']['cluster_name']}")
    
    # Cleanup
    adapter.cleanup()
```

### Multi-Adapter Workflows

```python
from omega_gpt_fleet.orchestrator import AdapterOrchestrator

orchestrator = AdapterOrchestrator()

# Load multiple adapters
orchestrator.load_adapter('scrollai', ScrollAIClusterSpawnAdapter, config)
orchestrator.load_adapter('docker', DockerAdapter, docker_config)

# Execute coordinated workflow
workflow = {
    'steps': [
        {'adapter': 'docker', 'command': 'create_network'},
        {'adapter': 'scrollai', 'command': 'spawn_cluster'},
        {'adapter': 'scrollai', 'command': 'expand_scroll_chain'}
    ]
}

orchestrator.execute_workflow(workflow)
```

## Configuration Standards

### Common Configuration Parameters

All adapters support these common configuration patterns:

- **Connection Settings**: Endpoints, ports, authentication
- **Workspace Management**: Local directories, temporary files
- **Resource Limits**: CPU, memory, timeout constraints
- **Logging Configuration**: Log levels, output formats
- **Retry Policies**: Timeout, retry attempts, backoff strategies

### Environment Integration

Adapters can be configured through:

- **Configuration Files**: JSON, YAML configuration files
- **Environment Variables**: Standard environment variable patterns
- **Runtime Parameters**: Dynamic configuration during execution
- **Config Inheritance**: Hierarchical configuration management

## Testing and Validation

### Adapter Testing

Each adapter includes comprehensive testing:

```bash
# Run adapter-specific tests
python -m pytest omega_gpt_fleet/tests/test_scrollai_clusterspawn_adapter.py

# Run all adapter tests  
python -m pytest omega_gpt_fleet/tests/adapters/

# Integration testing
python -m pytest omega_gpt_fleet/tests/integration/
```

### Validation Commands

```python
# Validate adapter configuration
adapter = ScrollAIClusterSpawnAdapter(config)
is_valid = adapter.validate()

# Check adapter capabilities
capabilities = adapter.get_capabilities()
dependencies = adapter.get_dependencies()

# Get adapter status
status = adapter.get_status()
```

## Contributing

### Adding New Adapters

1. **Inherit from BaseAdapter**: Extend the base adapter class
2. **Implement Required Methods**: initialize(), execute(), validate(), cleanup()
3. **Define Metadata**: Specify capabilities, dependencies, and adapter type
4. **Add Documentation**: Include comprehensive docstrings and examples
5. **Create Tests**: Add unit and integration tests
6. **Update Documentation**: Add to this README and domain-specific docs

### Adapter Guidelines

- **Single Responsibility**: Each adapter should focus on one tool/service
- **Error Handling**: Comprehensive error handling and logging
- **Configuration**: Flexible and well-documented configuration options
- **Performance**: Efficient resource usage and cleanup
- **Security**: Secure credential handling and validation

## Architecture Integration

The adapter system integrates with:

- **Workflow Engine**: Automated multi-step processes
- **Event System**: Event-driven automation and notifications  
- **Monitoring**: Health checks and performance metrics
- **Configuration Management**: Centralized configuration and secrets
- **Deployment**: Container and cloud deployment automation

## Support and Troubleshooting

### Common Issues

1. **Initialization Failures**: Check configuration and dependencies
2. **Permission Errors**: Verify authentication and access controls
3. **Resource Constraints**: Monitor CPU, memory, and network usage
4. **Network Connectivity**: Validate endpoints and firewall rules

### Debugging

```python
# Enable debug logging
import logging
logging.getLogger('omega_gpt_fleet').setLevel(logging.DEBUG)

# Check adapter status
status = adapter.get_status()
print(f"Adapter status: {status}")

# Review recent activity
# Check adapter logs for detailed information
```

### Getting Help

- **Documentation**: Check adapter-specific documentation files
- **Examples**: Review example workflows and configurations  
- **Issues**: Report bugs and feature requests on GitHub
- **Community**: Join project discussions and forums

---

**OmegaGPT Fleet Adapters** - Unified automation interfaces for the modern technology stack