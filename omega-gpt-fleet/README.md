# OmegaGPT Fleet Agent/Adapters Automation System

The OmegaGPT Fleet is a comprehensive automation system that provides standardized adapters for various tools, services, and platforms. This system enables automated orchestration, multi-repo upgrades, and seamless integration across different technology domains.

## Overview

The OmegaGPT Fleet adapter system provides a unified interface for interacting with diverse tools and services across multiple domains:

- **CAD (Computer-Aided Design)**: FreeCAD, SolveSpace, PythonOCC, Build123d, FreeCAD Library, OpenJSCAD
- **EDA (Electronic Design Automation)**: VTR (Verilog to Routing)
- **Web Infrastructure**: Caddy, Caddy Docker
- **Research**: NASA APIs and data sources
- **Networking**: NetBird, Docker, Prometheus Exporters, Diagramming, Dashboards
- **Data Storage**: Apache Cassandra
- **Vision/ML**: PyTorch3D, PyTorch Lightning, PyTorch Image Models

## Architecture

### Base Adapter Framework

All adapters inherit from the `BaseAdapter` class, providing:
- Standardized initialization and cleanup
- Consistent command execution interface
- Built-in logging and error handling
- Configuration management
- Status tracking and validation

### Domain Organization

Adapters are organized by domain for easy maintenance and discovery:

```
omega-gpt-fleet/
├── adapters/
│   ├── base_adapter.py      # Base adapter class
│   ├── cad/                 # CAD tool adapters
│   ├── eda/                 # EDA tool adapters
│   ├── web/                 # Web server adapters
│   ├── research/            # Research data adapters
│   ├── networking/          # Network tool adapters
│   ├── data/                # Database adapters
│   └── vision_ml/           # ML/AI tool adapters
├── upgrade.py               # Main upgrade script
└── meta-upgrade/            # Multi-repo upgrade system
```

## Quick Start

### Basic Usage

```python
from omega_gpt_fleet.adapters.cad import FreeCadAdapter

# Initialize adapter with configuration
config = {
    'freecad_path': '/usr/bin/freecad',
    'workspace': './cad_workspace'
}
adapter = FreeCadAdapter(config)

# Initialize and use adapter
if adapter.initialize():
    # Create a box
    result = adapter.execute('create_box', {
        'width': 10,
        'height': 10, 
        'depth': 10
    })
    
    # Check result
    if result['success']:
        print(f"Box created: {result['data']}")
    
    # Cleanup
    adapter.cleanup()
```

### Multi-Domain Workflow

```python
from omega_gpt_fleet.adapters.cad import FreeCadAdapter
from omega_gpt_fleet.adapters.web import CaddyAdapter
from omega_gpt_fleet.adapters.networking import DockerAdapter

# Initialize multiple adapters
cad_adapter = FreeCadAdapter({'workspace': './cad'})
web_adapter = CaddyAdapter({'config_path': './Caddyfile'})
docker_adapter = DockerAdapter()

# Orchestrate workflow
adapters = [cad_adapter, web_adapter, docker_adapter]

# Initialize all adapters
for adapter in adapters:
    if not adapter.initialize():
        print(f"Failed to initialize {adapter.name}")
        continue

# Execute coordinated operations
# ... workflow logic ...

# Cleanup all adapters
for adapter in adapters:
    adapter.cleanup()
```

## Installation

### Prerequisites

- Python 3.8+
- Git
- Tool-specific dependencies (see individual adapter documentation)

### Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/SpiralCloudOmega/Spiral-portal-GXT.git
   cd Spiral-portal-GXT
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt  # If available
   ```

3. **Configure adapters**:
   Each adapter can be configured with tool-specific settings. See domain-specific README files for details.

## Domain-Specific Documentation

Each adapter domain has comprehensive documentation:

- [CAD Adapters](adapters/cad/README.md) - CAD tool integration
- [EDA Adapters](adapters/eda/README.md) - Electronic design automation
- [Web Adapters](adapters/web/README.md) - Web server management
- [Research Adapters](adapters/research/README.md) - Research data access
- [Networking Adapters](adapters/networking/README.md) - Network tools and monitoring
- [Data Adapters](adapters/data/README.md) - Database and storage systems
- [Vision/ML Adapters](adapters/vision_ml/README.md) - Machine learning and computer vision

## Upgrade System

The OmegaGPT Fleet includes an automated upgrade system for maintaining adapters across multiple repositories:

### Upgrade All Repositories
```bash
python omega-gpt-fleet/upgrade.py
```

### Upgrade Specific Repositories
```bash
python omega-gpt-fleet/upgrade.py --repositories repo1 repo2
```

### Generate Upgrade Report
```bash
python omega-gpt-fleet/upgrade.py --report-only
```

See [Meta-Upgrade Documentation](meta-upgrade/README.md) for detailed information.

## Configuration

### Global Configuration

Create a configuration file for your environment:

```json
{
  "adapters": {
    "cad": {
      "freecad_path": "/usr/bin/freecad",
      "workspace": "./workspaces/cad"
    },
    "web": {
      "caddy_path": "/usr/bin/caddy",
      "config_path": "./config/Caddyfile"
    },
    "networking": {
      "docker_path": "/usr/bin/docker",
      "prometheus_url": "http://localhost:9090"
    }
  },
  "logging": {
    "level": "INFO",
    "file": "omega_gpt_fleet.log"
  }
}
```

### Environment Variables

Set environment variables for common configurations:

```bash
export OMEGA_GPT_FLEET_CONFIG="/path/to/config.json"
export OMEGA_GPT_FLEET_WORKSPACE="/path/to/workspace"
export OMEGA_GPT_FLEET_LOG_LEVEL="INFO"
```

## Advanced Features

### Agent Orchestration

The adapter system supports complex multi-tool workflows:

```python
from omega_gpt_fleet.orchestrator import AgentOrchestrator

orchestrator = AgentOrchestrator()

# Define workflow
workflow = {
    'name': 'cad_to_web_pipeline',
    'steps': [
        {'adapter': 'cad.freecad', 'action': 'create_model'},
        {'adapter': 'cad.freecad', 'action': 'export_stl'},
        {'adapter': 'web.caddy', 'action': 'serve_files'},
        {'adapter': 'networking.docker', 'action': 'deploy_container'}
    ]
}

orchestrator.execute_workflow(workflow)
```

### Event-Driven Automation

Set up event handlers for automated responses:

```python
from omega_gpt_fleet.events import EventHandler

handler = EventHandler()

@handler.on('cad.model_created')
def on_model_created(event):
    # Automatically export to web format
    web_adapter.execute('update_gallery', event.data)

@handler.on('networking.container_deployed')
def on_deployment(event):
    # Send notification
    notification_adapter.execute('send_alert', {
        'message': f"Container {event.data['name']} deployed"
    })
```

## Testing

### Run All Tests
```bash
python -m pytest omega-gpt-fleet/tests/
```

### Test Specific Domain
```bash
python -m pytest omega-gpt-fleet/tests/test_cad_adapters.py
```

### Integration Tests
```bash
python -m pytest omega-gpt-fleet/tests/integration/
```

## Contributing

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/new-adapter`
3. **Follow the adapter template** in `adapters/base_adapter.py`
4. **Add tests** for your adapter
5. **Update documentation**
6. **Submit a pull request**

### Adapter Development Guidelines

- Inherit from `BaseAdapter`
- Implement all abstract methods
- Include comprehensive docstrings
- Add domain-specific capabilities
- Handle errors gracefully
- Support configuration options

## License

This project is part of the Spiral Cloud Omega ecosystem.

## Support

- **Issues**: Report bugs and feature requests on GitHub
- **Documentation**: Check domain-specific README files
- **Community**: Join discussions in project issues

---

**OmegaGPT Fleet** - Unified automation for the modern technology stack