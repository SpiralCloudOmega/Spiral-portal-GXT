# Vision/ML Adapters

This directory contains adapters for computer vision and machine learning tools used in the OmegaGPT Fleet automation system.

## Available Adapters

### PyTorch3D Adapter (`pytorch3d_adapter.py`)
- **Purpose**: Interface with PyTorch3D for 3D computer vision and graphics
- **Capabilities**: 
  - 3D object detection and segmentation
  - 3D scene understanding
  - Neural rendering
  - 3D shape analysis
  - Mesh processing
- **Dependencies**: pytorch3d, torch, torchvision

### PyTorch Lightning Adapter (`pytorch_lightning_adapter.py`)
- **Purpose**: Interface with PyTorch Lightning for ML training workflows
- **Capabilities**:
  - Model training orchestration
  - Distributed training
  - Experiment tracking
  - Hyperparameter optimization
  - Model deployment
- **Dependencies**: pytorch-lightning, torch

### PyTorch Image Models Adapter (`pytorch_image_models_adapter.py`)
- **Purpose**: Interface with timm (PyTorch Image Models) for pre-trained models
- **Capabilities**:
  - Pre-trained model access
  - Image classification
  - Feature extraction
  - Transfer learning
  - Model fine-tuning
- **Dependencies**: timm, torch, torchvision

## Usage

```python
from omega_gpt_fleet.adapters.vision_ml import PyTorch3DAdapter

# Initialize adapter
adapter = PyTorch3DAdapter(config={
    'device': 'cuda',
    'model_path': '/models',
    'cache_dir': '/cache'
})

# Initialize connection
if adapter.initialize():
    # Execute operations
    result = adapter.execute('load_mesh', {'file_path': 'model.obj'})
    
    # Cleanup
    adapter.cleanup()
```

## Configuration

- **Device**: Computing device (CPU/GPU)
- **Model paths**: Pre-trained model locations
- **Cache directories**: Temporary storage locations
- **Training parameters**: Learning rates, batch sizes, etc.

## Integration

Enables automated ML pipelines, computer vision workflows, and AI-powered automation.