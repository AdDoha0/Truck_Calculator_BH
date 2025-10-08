"""
Truck domain entity - core business object.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, List, TYPE_CHECKING
from .financial import Money, Period
from .common import TruckId

if TYPE_CHECKING:
    from .costs import TotalCosts


@dataclass
class Truck:
    """
    Core domain entity representing a truck.
    
    Contains business logic and invariants but no persistence details.
    """
    id: Optional[TruckId]
    tractor_no: str
    
    def __post_init__(self):
        self._validate_tractor_no()
    
    def _validate_tractor_no(self) -> None:
        """Business rule: tractor number validation."""
        if not self.tractor_no or not self.tractor_no.strip():
            raise ValueError("Tractor number cannot be empty")
        
        if len(self.tractor_no.strip()) < 2:
            raise ValueError("Tractor number must be at least 2 characters")
        
        if len(self.tractor_no.strip()) > 20:
            raise ValueError("Tractor number cannot exceed 20 characters")
    
    def change_tractor_no(self, new_tractor_no: str) -> None:
        """Business method to change tractor number with validation."""
        old_tractor_no = self.tractor_no
        self.tractor_no = new_tractor_no.strip()
        
        try:
            self._validate_tractor_no()
        except ValueError:
            # Rollback on validation failure
            self.tractor_no = old_tractor_no
            raise
    
    def calculate_monthly_profit(self, 
                               revenue: Money,
                               variable_costs: Money, 
                               fixed_costs: 'TotalCosts') -> Money:
        """
        Core business logic: calculate monthly profit for this truck.
        
        Profit = Revenue - Variable Costs - Fixed Costs
        Fixed costs include both truck-specific and common costs.
        """
        total_fixed = fixed_costs.total_monthly_amount()
        return revenue - variable_costs - total_fixed
    
    def calculate_profit_margin(self,
                              revenue: Money,
                              variable_costs: Money,
                              fixed_costs: 'TotalCosts') -> float:
        """Calculate profit margin as percentage."""
        if revenue.is_zero:
            return 0.0
        
        profit = self.calculate_monthly_profit(revenue, variable_costs, fixed_costs)
        return float(profit.amount / revenue.amount * 100)
    
    def can_be_deleted(self, has_monthly_data: bool) -> bool:
        """Business rule: truck can only be deleted if it has no monthly data."""
        return not has_monthly_data
    
    def __str__(self) -> str:
        return f"Truck({self.tractor_no})"
    
    def __repr__(self) -> str:
        return f"Truck(id={self.id}, tractor_no='{self.tractor_no}')"
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Truck):
            return False
        return self.id == other.id and self.tractor_no == other.tractor_no
    
    def __hash__(self) -> int:
        return hash((self.id, self.tractor_no))
