# Web Adapters

This directory contains adapters for web servers and web infrastructure tools used in the OmegaGPT Fleet automation system.

## Available Adapters

### Caddy Adapter (`caddy_adapter.py`)
- **Purpose**: Interface with Caddy web server for automated web hosting and reverse proxy
- **Capabilities**: 
  - Automatic HTTPS with Let's Encrypt
  - Reverse proxy configuration
  - Static file serving
  - Load balancing
  - Configuration management
  - SSL certificate management
- **Dependencies**: Caddy web server

### Caddy Docker Adapter (`caddy_docker_adapter.py`)
- **Purpose**: Interface with Caddy running in Docker containers
- **Capabilities**:
  - Docker container management
  - Automated deployment
  - Container orchestration
  - Volume management
  - Network configuration
  - Health monitoring
- **Dependencies**: Docker, Caddy Docker image

## Usage

Each adapter follows the standard BaseAdapter interface:

```python
from omega_gpt_fleet.adapters.web import CaddyAdapter

# Initialize adapter
adapter = CaddyAdapter(config={
    'caddy_path': '/usr/bin/caddy',
    'config_path': '/etc/caddy/Caddyfile',
    'workspace': '/var/www'
})

# Initialize connection
if adapter.initialize():
    # Execute operations
    result = adapter.execute('add_site', {
        'domain': 'example.com',
        'root': '/var/www/example.com',
        'https': True
    })
    
    # Cleanup
    adapter.cleanup()
```

## Configuration

Web adapters can be configured with domain-specific parameters:

- **Server paths**: Paths to web server executables and configuration files
- **Document roots**: Directory paths for serving static content
- **SSL settings**: Certificate paths and SSL/TLS configuration
- **Proxy settings**: Upstream server configurations
- **Docker settings**: Container names, images, and network configurations

## Integration

These adapters integrate with the OmegaGPT Fleet automation system to enable:

- Automated web server deployment
- Dynamic site configuration
- SSL certificate automation
- Load balancer management
- Container orchestration
- Web application deployment pipelines