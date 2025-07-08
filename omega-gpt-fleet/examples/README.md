# OmegaGPT Fleet Examples

This directory contains example workflows, configurations, and usage patterns for the OmegaGPT Fleet automation system. These examples demonstrate how to use the various adapters and orchestrate complex multi-tool workflows.

## Available Examples

### ScrollAI & Distributed Processing

#### ΩΔ174 ScrollAI ClusterSpawn Example (`ΩΔ174_ScrollAI_ClusterSpawn.yaml`)
Comprehensive example demonstrating ScrollAI cluster spawning and management for distributed scroll chain processing.

**Features:**
- Automated cluster spawning with multiple configurations
- Dynamic scaling based on performance metrics
- Scroll chain expansion across distributed clusters
- Monitoring and alerting integration
- Resource management and cleanup

**Usage:**
```bash
# Execute the ScrollAI cluster workflow
omega-gpt-fleet run examples/ΩΔ174_ScrollAI_ClusterSpawn.yaml

# Run with custom parameters
omega-gpt-fleet run examples/ΩΔ174_ScrollAI_ClusterSpawn.yaml \
  --var cluster_prefix=demo-scroll \
  --var replicas=3
```

**Key Components:**
- Primary and secondary cluster spawning
- Performance-based auto-scaling
- Cross-cluster scroll chain distribution
- Comprehensive monitoring and logging
- Automatic cleanup on failure

## Workflow Structure

### Standard Workflow Format

All example workflows follow this structure:

```yaml
name: "Workflow_Name"
description: "Workflow description"
version: "1.0.0"
adapter: "AdapterName"

# Configuration
config:
  # Adapter-specific configuration
  
# Workflow steps
steps:
  - name: "step_name"
    command: "adapter_command"
    parameters:
      # Command parameters
    description: "Step description"
    depends_on: ["previous_step"]
    
# Variables and templating
variables:
  var_name: "{{ expression }}"

# Event handlers
on_success:
  - action: "log"
    message: "Workflow completed"

on_failure:
  - action: "cleanup"
    
# Resource management
resources:
  max_instances: 10
  timeout: "30m"
```

### Workflow Features

#### Templating and Variables
- **Dynamic Values**: Use `{{ variable }}` syntax for dynamic values
- **Built-in Functions**: Access to date, time, and utility functions
- **Environment Variables**: Reference environment variables
- **Step Outputs**: Reference outputs from previous steps

#### Dependency Management
- **Step Dependencies**: Control execution order with `depends_on`
- **Conditional Execution**: Use `condition` for conditional steps
- **Parallel Execution**: Steps without dependencies run in parallel
- **Error Handling**: Continue or halt on step failures

#### Resource Management
- **Resource Limits**: Define CPU, memory, and other resource constraints
- **Timeouts**: Set step and workflow timeouts
- **Cleanup**: Automatic resource cleanup on completion or failure
- **Monitoring**: Built-in metrics and health checks

## Usage Patterns

### Basic Workflow Execution

```bash
# Run a workflow
omega-gpt-fleet run examples/workflow.yaml

# Run with variables
omega-gpt-fleet run examples/workflow.yaml --var key=value

# Dry run (validation only)
omega-gpt-fleet run examples/workflow.yaml --dry-run

# Watch execution
omega-gpt-fleet run examples/workflow.yaml --watch
```

### Advanced Execution Options

```bash
# Run with custom config
omega-gpt-fleet run examples/workflow.yaml \
  --config custom-config.yaml \
  --var environment=production

# Run specific steps only
omega-gpt-fleet run examples/workflow.yaml \
  --steps spawn_cluster,monitor_performance

# Run with timeout
omega-gpt-fleet run examples/workflow.yaml \
  --timeout 1h
```

### Workflow Validation

```bash
# Validate workflow syntax
omega-gpt-fleet validate examples/workflow.yaml

# Check adapter compatibility
omega-gpt-fleet validate examples/workflow.yaml --check-adapters

# Verify resource requirements
omega-gpt-fleet validate examples/workflow.yaml --check-resources
```

## Multi-Domain Workflows

### CAD to Web Pipeline
```yaml
name: "CAD_Web_Pipeline"
steps:
  - name: "create_model"
    adapter: "freecad"
    command: "create_model"
    
  - name: "export_web_format"
    adapter: "freecad" 
    command: "export_model"
    depends_on: ["create_model"]
    
  - name: "deploy_web_server"
    adapter: "caddy"
    command: "deploy_site"
    depends_on: ["export_web_format"]
```

### AI/ML Training Pipeline
```yaml
name: "ML_Training_Pipeline"
steps:
  - name: "prepare_dataset"
    adapter: "pytorch_lightning"
    command: "prepare_data"
    
  - name: "train_model"
    adapter: "pytorch_lightning"
    command: "train"
    depends_on: ["prepare_dataset"]
    
  - name: "deploy_inference"
    adapter: "docker"
    command: "deploy_container"
    depends_on: ["train_model"]
```

### Infrastructure Automation
```yaml
name: "Infrastructure_Setup"
steps:
  - name: "create_network"
    adapter: "netbird"
    command: "create_network"
    
  - name: "spawn_clusters"
    adapter: "scrollai_clusterspawn"
    command: "spawn_cluster"
    depends_on: ["create_network"]
    
  - name: "setup_monitoring"
    adapter: "prometheus"
    command: "deploy_monitoring"
    depends_on: ["spawn_clusters"]
```

## Configuration Examples

### Development Environment
```yaml
# dev-config.yaml
api_endpoints:
  scrollai: "http://localhost:8080"
  docker: "unix:///var/run/docker.sock"

resources:
  max_cpu: "4"
  max_memory: "8Gi"
  
logging:
  level: "DEBUG"
  output: "console"
```

### Production Environment
```yaml
# prod-config.yaml
api_endpoints:
  scrollai: "https://scrollai.prod.example.com"
  docker: "tcp://docker.prod.example.com:2376"

resources:
  max_cpu: "32"
  max_memory: "128Gi"
  
security:
  tls_verify: true
  auth_required: true
  
monitoring:
  enabled: true
  metrics_endpoint: "https://metrics.example.com"
```

## Testing Examples

### Unit Testing Workflows
```bash
# Test individual steps
omega-gpt-fleet test examples/workflow.yaml --step spawn_cluster

# Test with mock adapters
omega-gpt-fleet test examples/workflow.yaml --mock-adapters

# Load testing
omega-gpt-fleet test examples/workflow.yaml --load-test --concurrency 10
```

### Integration Testing
```bash
# End-to-end testing
omega-gpt-fleet test examples/ --integration

# Performance benchmarking
omega-gpt-fleet benchmark examples/ΩΔ174_ScrollAI_ClusterSpawn.yaml
```

## Best Practices

### Workflow Design
1. **Modular Steps**: Break complex operations into discrete steps
2. **Error Handling**: Include comprehensive error handling and cleanup
3. **Resource Management**: Define appropriate resource limits
4. **Documentation**: Include clear descriptions and comments
5. **Validation**: Test workflows thoroughly before production use

### Configuration Management
1. **Environment Separation**: Use different configs for dev/staging/prod
2. **Secret Management**: Use secure methods for credentials and tokens
3. **Parameter Validation**: Validate all input parameters
4. **Default Values**: Provide sensible defaults for optional parameters
5. **Documentation**: Document all configuration options

### Performance Optimization
1. **Parallel Execution**: Leverage parallel step execution where possible
2. **Resource Efficiency**: Right-size resource allocations
3. **Caching**: Use caching for repeated operations
4. **Monitoring**: Implement comprehensive monitoring and alerting
5. **Cleanup**: Ensure proper resource cleanup

## Creating Custom Examples

### Example Template
```yaml
name: "Custom_Workflow"
description: "Description of what this workflow does"
version: "1.0.0"
adapter: "AdapterName"

config:
  # Adapter configuration

steps:
  - name: "step1"
    command: "command1"
    parameters:
      param1: "value1"
    description: "What this step does"

variables:
  custom_var: "{{ now() }}"

on_success:
  - action: "log"
    message: "Workflow succeeded"

tags:
  - "custom"
  - "example"
```

### Contribution Guidelines
1. **Follow Template**: Use the standard workflow template
2. **Clear Documentation**: Include comprehensive descriptions
3. **Real-world Examples**: Create practical, useful examples
4. **Test Coverage**: Ensure examples work correctly
5. **Tagging**: Use appropriate tags for organization

## Support and Resources

### Getting Help
- **Documentation**: Check adapter-specific documentation
- **Examples**: Review similar workflow examples
- **Community**: Join project discussions
- **Issues**: Report problems or request new examples

### Learning Resources
- **Workflow Guide**: Comprehensive workflow development guide
- **Adapter Documentation**: Individual adapter documentation
- **Video Tutorials**: Step-by-step workflow creation tutorials
- **Best Practices**: Workflow design and optimization guides

---

**OmegaGPT Fleet Examples** - Learn by example, automate with confidence