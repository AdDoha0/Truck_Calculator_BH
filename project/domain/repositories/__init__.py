"""
Repository interfaces (abstractions) for the domain layer.

These are abstract base classes that define contracts for data access.
Concrete implementations live in the infrastructure layer.
"""

from .truck_repository import TruckRepository
from .costs_repository import CostsRepository

__all__ = [
    "TruckRepository",
    "CostsRepository", 
]
