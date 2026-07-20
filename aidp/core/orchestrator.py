"""Core orchestration utilities for AIDP.

Provide entry points for running pipelines and managing service container.
"""

from .container import ServiceContainer

__all__ = ["ServiceContainer"]
