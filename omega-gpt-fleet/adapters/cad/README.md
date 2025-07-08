# CAD Adapters

This directory contains adapters for Computer-Aided Design (CAD) tools and libraries used in the OmegaGPT Fleet automation system.

## Available Adapters

### FreeCAD Adapter (`freecad_adapter.py`)
- **Purpose**: Interface with FreeCAD for 3D modeling and CAD operations
- **Capabilities**: 
  - Create and modify 3D models
  - Import/export various CAD formats
  - Parametric modeling
  - Assembly operations
- **Dependencies**: FreeCAD Python API

### SolveSpace Adapter (`solvespace_adapter.py`)
- **Purpose**: Interface with SolveSpace for 2D/3D constraint-based modeling
- **Capabilities**:
  - Constraint-based parametric modeling
  - 2D sketching and 3D operations
  - Assembly constraints
  - Export to various formats
- **Dependencies**: SolveSpace library

### PythonOCC Adapter (`pythonocc_adapter.py`)
- **Purpose**: Interface with PythonOCC for OpenCASCADE operations
- **Capabilities**:
  - Advanced geometric modeling
  - NURBS surfaces and curves
  - Boolean operations
  - CAD file format support
- **Dependencies**: pythonOCC-core

### Build123d Adapter (`build123d_adapter.py`)
- **Purpose**: Interface with Build123d for modern Python-based CAD
- **Capabilities**:
  - Modern Python CAD API
  - Parametric modeling
  - Assembly operations
  - Export capabilities
- **Dependencies**: build123d

### FreeCAD Library Adapter (`freecad_library_adapter.py`)
- **Purpose**: Interface with FreeCAD part libraries and repositories
- **Capabilities**:
  - Access to standard parts libraries
  - Part library management
  - Integration with FreeCAD workflows
- **Dependencies**: FreeCAD, library repositories

### OpenJSCAD Adapter (`openjscad_adapter.py`)
- **Purpose**: Interface with OpenJSCAD for JavaScript-based CAD
- **Capabilities**:
  - JavaScript-based CAD operations
  - Web-based CAD workflows
  - Export to various formats
  - Integration with web applications
- **Dependencies**: OpenJSCAD, Node.js

## Usage

Each adapter follows the standard BaseAdapter interface:

```python
from omega_gpt_fleet.adapters.cad import FreeCadAdapter

# Initialize adapter
adapter = FreeCadAdapter(config={'workspace': '/path/to/workspace'})

# Initialize connection
if adapter.initialize():
    # Execute operations
    result = adapter.execute('create_box', {'width': 10, 'height': 10, 'depth': 10})
    
    # Cleanup
    adapter.cleanup()
```

## Configuration

Each adapter can be configured with domain-specific parameters:

- **Workspace paths**: Directory for CAD files and projects
- **Tool paths**: Paths to CAD tool executables
- **Export settings**: Default export formats and parameters
- **Library paths**: Paths to part libraries and resources

## Integration

These adapters integrate with the OmegaGPT Fleet automation system to enable:

- Automated CAD model generation
- Batch processing of CAD operations
- Integration with design workflows
- Multi-tool CAD pipelines
- Automated testing and validation