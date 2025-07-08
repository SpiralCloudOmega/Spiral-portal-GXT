"""
Web Adapters Package

This package contains adapters for web servers and web infrastructure tools.
"""

from .caddy_adapter import CaddyAdapter
from .caddy_docker_adapter import CaddyDockerAdapter

__all__ = ["CaddyAdapter", "CaddyDockerAdapter"]