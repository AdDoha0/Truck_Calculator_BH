"""
Costs-related Data Transfer Objects.
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any
from decimal import Decimal
from ...domain.entities.common import TruckId


@dataclass
class FixedCostsTruckDto:
    """
    DTO for truck-specific fixed costs.
    Used for transferring cost data between layers.
    """
    truck_id: Optional[TruckId] 
    truck_payment: Decimal
    trailer_payment: Decimal
    physical_damage_insurance_truck: Decimal
    physical_damage_insurance_trailer: Decimal
    
    @classmethod
    def from_domain(cls, costs) -> 'FixedCostsTruckDto':
        """Create DTO from domain entity."""
        return cls(
            truck_id=costs.truck_id,
            truck_payment=costs.truck_payment.amount,
            trailer_payment=costs.trailer_payment.amount,
            physical_damage_insurance_truck=costs.physical_damage_insurance_truck.amount,
            physical_damage_insurance_trailer=costs.physical_damage_insurance_trailer.amount
        )
    
    def total_amount(self) -> Decimal:
        """Calculate total truck costs."""
        return (self.truck_payment + 
                self.trailer_payment + 
                self.physical_damage_insurance_truck + 
                self.physical_damage_insurance_trailer)


@dataclass
class FixedCostsCommonDto:
    """
    DTO for common fixed costs.
    """
    ifta: Decimal
    insurance: Decimal
    eld: Decimal
    tablet: Decimal
    tolls: Decimal
    
    @classmethod
    def from_domain(cls, costs) -> 'FixedCostsCommonDto':
        """Create DTO from domain entity.""" 
        return cls(
            ifta=costs.ifta.amount,
            insurance=costs.insurance.amount,
            eld=costs.eld.amount,
            tablet=costs.tablet.amount,
            tolls=costs.tolls.amount
        )
    
    def total_amount(self) -> Decimal:
        """Calculate total common costs."""
        return (self.ifta + self.insurance + self.eld + 
                self.tablet + self.tolls)


@dataclass
class UpdateTruckCostsRequest:
    """
    DTO for updating truck-specific fixed costs.
    """
    truck_id: TruckId
    truck_payment: Optional[Decimal] = None
    trailer_payment: Optional[Decimal] = None
    physical_damage_insurance_truck: Optional[Decimal] = None
    physical_damage_insurance_trailer: Optional[Decimal] = None
    
    def get_updates(self) -> Dict[str, Decimal]:
        """Get non-None update fields."""
        updates = {}
        if self.truck_payment is not None:
            updates['truck_payment'] = self.truck_payment
        if self.trailer_payment is not None:
            updates['trailer_payment'] = self.trailer_payment
        if self.physical_damage_insurance_truck is not None:
            updates['physical_damage_insurance_truck'] = self.physical_damage_insurance_truck
        if self.physical_damage_insurance_trailer is not None:
            updates['physical_damage_insurance_trailer'] = self.physical_damage_insurance_trailer
        return updates


@dataclass
class UpdateCommonCostsRequest:
    """
    DTO for updating common fixed costs.
    """
    ifta: Optional[Decimal] = None
    insurance: Optional[Decimal] = None
    eld: Optional[Decimal] = None
    tablet: Optional[Decimal] = None
    tolls: Optional[Decimal] = None
    
    def get_updates(self) -> Dict[str, Decimal]:
        """Get non-None update fields."""
        updates = {}
        if self.ifta is not None:
            updates['ifta'] = self.ifta
        if self.insurance is not None:
            updates['insurance'] = self.insurance
        if self.eld is not None:
            updates['eld'] = self.eld
        if self.tablet is not None:
            updates['tablet'] = self.tablet
        if self.tolls is not None:
            updates['tolls'] = self.tolls
        return updates
