# Networking Adapters

This directory contains adapters for networking tools and infrastructure used in the OmegaGPT Fleet automation system.

## Available Adapters

### NetBird Adapter (`netbird_adapter.py`)
- **Purpose**: Interface with NetBird for VPN and network mesh management
- **Capabilities**: 
  - VPN connection management
  - Network mesh configuration
  - Peer-to-peer networking
  - Access control
  - Network monitoring
- **Dependencies**: NetBird client, NetBird API

### Docker Adapter (`docker_adapter.py`)
- **Purpose**: Interface with Docker for container networking and orchestration
- **Capabilities**:
  - Container management
  - Network configuration
  - Service orchestration
  - Load balancing
  - Container monitoring
- **Dependencies**: Docker Engine, Docker API

### Exporter Adapter (`exporter_adapter.py`)
- **Purpose**: Interface with Prometheus exporters for metrics collection
- **Capabilities**:
  - Metrics collection
  - Data export
  - System monitoring
  - Performance metrics
  - Custom metrics
- **Dependencies**: Prometheus, various exporters

### Diagram Adapter (`diagram_adapter.py`)
- **Purpose**: Interface with network diagramming tools
- **Capabilities**:
  - Network topology visualization
  - Automated diagram generation
  - Infrastructure mapping
  - Visual documentation
- **Dependencies**: Graphviz, Diagrams library

### Dashboard Adapter (`dashboard_adapter.py`)
- **Purpose**: Interface with monitoring and visualization dashboards
- **Capabilities**:
  - Dashboard creation
  - Real-time monitoring
  - Data visualization
  - Alert management
  - Report generation
- **Dependencies**: Grafana, Prometheus, InfluxDB

## Usage

Each adapter follows the standard BaseAdapter interface:

```python
from omega_gpt_fleet.adapters.networking import NetBirdAdapter

# Initialize adapter
adapter = NetBirdAdapter(config={
    'server_url': 'https://netbird.example.com',
    'api_key': 'your_api_key',
    'management_url': 'https://management.netbird.example.com'
})

# Initialize connection
if adapter.initialize():
    # Execute operations
    result = adapter.execute('create_peer', {
        'name': 'server-01',
        'groups': ['servers', 'production']
    })
    
    # Cleanup
    adapter.cleanup()
```

## Configuration

Networking adapters can be configured with domain-specific parameters:

- **Server URLs**: Endpoints for network services
- **API keys**: Authentication credentials
- **Network settings**: IP ranges, subnets, ports
- **Monitoring endpoints**: Metrics collection points
- **Dashboard URLs**: Visualization interfaces

## Integration

These adapters integrate with the OmegaGPT Fleet automation system to enable:

- Automated network infrastructure deployment
- Container orchestration pipelines
- Network monitoring and alerting
- Infrastructure as Code (IaC)
- Automated network documentation
- Performance optimization workflows