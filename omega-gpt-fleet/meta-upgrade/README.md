# Meta-Upgrade System

This directory contains the meta-upgrade system for automated propagation of OmegaGPT Fleet adapters and updates across multiple repositories.

## Overview

The meta-upgrade system enables automated distribution and synchronization of adapter updates across the entire OmegaGPT Fleet ecosystem. This ensures consistent adapter versions and capabilities across all repositories and deployments.

## Components

### Upgrade Script (`../upgrade.py`)
The main upgrade script that handles:
- Repository synchronization
- Adapter distribution
- Version management
- Validation testing
- Backup creation

### Configuration (`upgrade_config.json`)
Configuration file that defines:
- Target repositories
- Adapter mappings
- Upgrade options
- Validation settings

## Usage

### Basic Upgrade
```bash
# Upgrade all repositories
python omega-gpt-fleet/upgrade.py

# Upgrade specific repositories
python omega-gpt-fleet/upgrade.py --repositories repo1 repo2

# Generate upgrade report only
python omega-gpt-fleet/upgrade.py --report-only
```

### Configuration
```json
{
  "version": "1.0.0",
  "repositories": [
    {
      "name": "spiral-portal-gxt",
      "url": "https://github.com/SpiralCloudOmega/Spiral-portal-GXT.git",
      "branch": "main",
      "adapter_path": "omega-gpt-fleet/adapters"
    }
  ],
  "adapters": {
    "cad": ["freecad", "solvespace", "pythonocc", "build123d"],
    "eda": ["vtr"],
    "web": ["caddy", "caddy_docker"],
    "research": ["nasa"],
    "networking": ["netbird", "docker", "exporter", "diagram", "dashboard"],
    "data": ["cassandra"],
    "vision_ml": ["pytorch3d", "pytorch_lightning", "pytorch_image_models"]
  },
  "upgrade_options": {
    "backup_before_upgrade": true,
    "run_tests": true,
    "auto_commit": false,
    "notification_webhook": ""
  }
}
```

## Workflow

1. **Pre-upgrade Checks**
   - Validate configuration
   - Check repository access
   - Create backups if enabled

2. **Repository Updates**
   - Clone or pull latest changes
   - Copy updated adapters
   - Update configuration files

3. **Validation**
   - Test adapter imports
   - Run validation tests
   - Check dependencies

4. **Post-upgrade**
   - Generate reports
   - Send notifications
   - Log results

## Features

### Automated Synchronization
- Keeps all repositories in sync with latest adapter versions
- Handles dependencies and compatibility
- Manages version conflicts

### Backup and Recovery
- Creates backups before upgrades
- Enables rollback on failures
- Preserves local configurations

### Validation and Testing
- Runs automated tests after upgrades
- Validates adapter functionality
- Reports issues and conflicts

### Multi-Repository Support
- Supports multiple Git repositories
- Handles different branch strategies
- Manages repository-specific configurations

## Integration with CI/CD

The meta-upgrade system can be integrated with CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
name: OmegaGPT Fleet Upgrade
on:
  schedule:
    - cron: '0 2 * * 0'  # Weekly on Sunday at 2 AM
  workflow_dispatch:

jobs:
  upgrade:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - name: Run OmegaGPT Fleet Upgrade
        run: python omega-gpt-fleet/upgrade.py
```

## Monitoring and Alerts

The system provides monitoring capabilities:
- Upgrade success/failure tracking
- Performance metrics
- Error reporting
- Webhook notifications

## Security Considerations

- Repository access controls
- Secure credential management
- Audit logging
- Change validation

## Best Practices

1. **Testing**: Always test upgrades in staging environments first
2. **Backups**: Enable automatic backups before upgrades
3. **Monitoring**: Set up alerts for upgrade failures
4. **Documentation**: Keep upgrade logs and documentation current
5. **Gradual Rollout**: Use phased deployment for large ecosystems

## Troubleshooting

### Common Issues

1. **Permission Errors**
   - Check repository access permissions
   - Verify authentication credentials

2. **Merge Conflicts**
   - Resolve conflicts manually
   - Update configuration files

3. **Dependency Issues**
   - Update dependency versions
   - Check compatibility matrices

4. **Test Failures**
   - Review test logs
   - Update test configurations

### Recovery Procedures

1. **Rollback**: Use backup directories to restore previous state
2. **Manual Sync**: Manually synchronize specific repositories
3. **Selective Upgrade**: Upgrade only specific adapters or domains

## Future Enhancements

- **Semantic Versioning**: Automatic version management
- **Dependency Resolution**: Smart dependency handling
- **Performance Optimization**: Parallel processing
- **Advanced Testing**: Comprehensive test suites
- **UI Dashboard**: Web-based monitoring interface