# Research Adapters

This directory contains adapters for research institutions and data sources used in the OmegaGPT Fleet automation system.

## Available Adapters

### NASA Adapter (`nasa_adapter.py`)
- **Purpose**: Interface with NASA APIs and data sources for space research data
- **Capabilities**: 
  - Access to NASA Open Data API
  - Astronomy Picture of the Day (APOD)
  - Mars Rover photo data
  - Exoplanet archive access
  - Earth observation data
  - Space weather information
  - Mission data access
- **Dependencies**: requests, NASA API keys

## Usage

Each adapter follows the standard BaseAdapter interface:

```python
from omega_gpt_fleet.adapters.research import NASAAdapter

# Initialize adapter
adapter = NASAAdapter(config={
    'api_key': 'your_nasa_api_key',
    'base_url': 'https://api.nasa.gov',
    'cache_dir': '/tmp/nasa_cache'
})

# Initialize connection
if adapter.initialize():
    # Execute operations
    result = adapter.execute('get_apod', {'date': '2024-01-01'})
    
    # Cleanup
    adapter.cleanup()
```

## Configuration

Research adapters can be configured with domain-specific parameters:

- **API keys**: Authentication credentials for research APIs
- **Base URLs**: Endpoints for research data services
- **Cache directories**: Local storage for downloaded data
- **Rate limiting**: Request throttling settings
- **Data formats**: Preferred data formats (JSON, CSV, etc.)

## Integration

These adapters integrate with the OmegaGPT Fleet automation system to enable:

- Automated research data collection
- Scientific data processing pipelines
- Research workflow automation
- Data analysis and visualization
- Multi-source data aggregation
- Research collaboration tools