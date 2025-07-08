"""
OmegaGPT Fleet Adapters Package

This package contains all adapters for the OmegaGPT Fleet automation system.
Adapters are organized by domain (CAD, EDA, Web, Research, Networking, Data, Vision/ML).

Each adapter provides a standardized interface for interacting with external tools
and services as part of the automated workflow orchestration.
"""

from .base_adapter import BaseAdapter

__version__ = "1.0.0"
__all__ = ["BaseAdapter"]