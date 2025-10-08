"""
Data Transfer Objects for application layer boundaries.

DTOs are simple data structures used to transfer data between layers.
They have no business logic and serve as contracts between layers.
"""

from .truck_dto import TruckDto, CreateTruckRequest, UpdateTruckRequest
from .costs_dto import (
    FixedCostsTruckDto, 
    FixedCostsCommonDto,
    UpdateTruckCostsRequest,
    UpdateCommonCostsRequest
)

__all__ = [
    "TruckDto",
    "CreateTruckRequest", 
    "UpdateTruckRequest",
    "FixedCostsTruckDto",
    "FixedCostsCommonDto",
    "UpdateTruckCostsRequest",
    "UpdateCommonCostsRequest",
]
