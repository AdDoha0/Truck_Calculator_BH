"""
Common types and constants used across the application.
"""
from typing import NewType
from dataclasses import dataclass
from typing import Optional, Dict, Any

# Strong typing for identifiers
TruckId = NewType('TruckId', int)

# Simple data classes for UI/service communication (replacing complex DTOs)
@dataclass
class TruckInfo:
    """Simple truck data for UI display."""
    id: Optional[int]
    tractor_no: str
    monthly_count: int = 0
    has_fixed_costs: bool = False

@dataclass
class CostsSummary:
    """Summary of costs for reporting."""
    total_variable: float
    total_fixed: float
    total_all: float
    profit: float
    margin_percent: float

@dataclass 
class TruckCostsUpdate:
    """Data for updating truck costs."""
    truck_id: int
    truck_payment: Optional[float] = None
    trailer_payment: Optional[float] = None
    physical_damage_insurance_truck: Optional[float] = None
    physical_damage_insurance_trailer: Optional[float] = None
    
    def get_updates(self) -> Dict[str, float]:
        """Get non-None updates as dictionary."""
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
class CommonCostsUpdate:
    """Data for updating common costs."""
    ifta: Optional[float] = None
    insurance: Optional[float] = None
    eld: Optional[float] = None
    tablet: Optional[float] = None
    tolls: Optional[float] = None
    
    def get_updates(self) -> Dict[str, float]:
        """Get non-None updates as dictionary."""
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
