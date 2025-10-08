"""
Domain layer for Truck Calculate application.

This layer contains:
- Business entities (pure domain objects)
- Domain services (business logic)
- Repository interfaces (abstractions)

Domain layer has NO dependencies on infrastructure or UI layers.
All dependencies point inward to the domain.
"""

from .entities import *
from .services import *
from .repositories import *

__all__ = [
    # Re-export all domain components
    "entities",
    "services", 
    "repositories",
]
