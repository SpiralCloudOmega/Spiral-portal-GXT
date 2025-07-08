# Data Adapters

This directory contains adapters for data storage and management systems used in the OmegaGPT Fleet automation system.

## Available Adapters

### Cassandra Adapter (`cassandra_adapter.py`)
- **Purpose**: Interface with Apache Cassandra for distributed data storage
- **Capabilities**: 
  - Distributed database operations
  - High-availability data storage
  - Scalable data management
  - CQL query execution
  - Cluster management
  - Data modeling
- **Dependencies**: cassandra-driver, Apache Cassandra

## Usage

```python
from omega_gpt_fleet.adapters.data import CassandraAdapter

# Initialize adapter
adapter = CassandraAdapter(config={
    'hosts': ['127.0.0.1'],
    'keyspace': 'omega_gpt_fleet',
    'port': 9042
})

# Initialize connection
if adapter.initialize():
    # Execute operations
    result = adapter.execute('create_table', {
        'table_name': 'metrics',
        'schema': 'id UUID, timestamp TIMESTAMP, value DOUBLE'
    })
    
    # Cleanup
    adapter.cleanup()
```

## Configuration

- **Hosts**: Cassandra cluster node addresses
- **Keyspace**: Database keyspace for operations
- **Credentials**: Authentication parameters
- **Connection pooling**: Connection management settings

## Integration

Enables automated data management, analytics pipelines, and distributed storage solutions.