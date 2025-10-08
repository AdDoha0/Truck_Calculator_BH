"""
Truck-related Data Transfer Objects.
"""

from dataclasses import dataclass
from typing import Optional
from ...domain.entities.common import TruckId


@dataclass
class TruckDto:
    """
    DTO for truck data transfer between layers.
    Used for read operations and displaying truck information.
    """
    id: Optional[TruckId]
    tractor_no: str
    monthly_rows_count: Optional[int] = None
    fixed_costs_count: Optional[int] = None
    
    @classmethod
    def from_domain(cls, truck, monthly_count: int = 0, fixed_costs_count: int = 0) -> 'TruckDto':
        """Create DTO from domain entity."""
        return cls(
            id=truck.id,
            tractor_no=truck.tractor_no,
            monthly_rows_count=monthly_count,
            fixed_costs_count=fixed_costs_count
        )


@dataclass
class CreateTruckRequest:
    """
    DTO for truck creation requests.
    Contains only the data needed to create a new truck.
    """
    tractor_no: str
    
    def validate(self) -> bool:
        """Basic validation before processing."""
        return bool(self.tractor_no and self.tractor_no.strip())


@dataclass 
class UpdateTruckRequest:
    """
    DTO for truck update requests.
    """
    truck_id: TruckId
    tractor_no: str
    
    def validate(self) -> bool:
        """Basic validation before processing."""
        return bool(
            self.truck_id and 
            self.tractor_no and 
            self.tractor_no.strip()
        )
