"""
Data Adapters Package

This package contains adapters for data storage and management systems.
"""

from .cassandra_adapter import CassandraAdapter

__all__ = ["CassandraAdapter"]