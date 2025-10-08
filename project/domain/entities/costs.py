"""
Cost-related domain entities and value objects.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Dict, Any
from .financial import Money
from .common import TruckId


@dataclass
class VariableCosts:
    """
    Variable costs that come from uploaded files (per month per truck).
    These change monthly based on actual operations.
    """
    salary: Money
    fuel: Money
    tolls: Money
    repair: Money
    
    @classmethod
    def zero(cls) -> VariableCosts:
        """Create zero variable costs."""
        return cls(
            salary=Money(0),
            fuel=Money(0), 
            tolls=Money(0),
            repair=Money(0)
        )
    
    def total(self) -> Money:
        """Calculate total variable costs."""
        return self.salary + self.fuel + self.tolls + self.repair
    
    def __str__(self) -> str:
        return f"VariableCosts(total={self.total()})"


@dataclass
class FixedCostsTruck:
    """
    Fixed costs specific to a particular truck.
    These are set through forms and change rarely.
    """
    truck_id: Optional[TruckId]
    truck_payment: Money
    trailer_payment: Money
    physical_damage_insurance_truck: Money
    physical_damage_insurance_trailer: Money
    
    @classmethod
    def zero_for_truck(cls, truck_id: Optional[TruckId] = None) -> FixedCostsTruck:
        """Create zero fixed costs for a truck."""
        return cls(
            truck_id=truck_id,
            truck_payment=Money(0),
            trailer_payment=Money(0),
            physical_damage_insurance_truck=Money(0),
            physical_damage_insurance_trailer=Money(0)
        )
    
    def total(self) -> Money:
        """Calculate total truck-specific fixed costs."""
        return (self.truck_payment + 
                self.trailer_payment +
                self.physical_damage_insurance_truck +
                self.physical_damage_insurance_trailer)
    
    def update_values(self, **kwargs) -> None:
        """Update cost values with validation."""
        valid_fields = {
            'truck_payment', 'trailer_payment',
            'physical_damage_insurance_truck',
            'physical_damage_insurance_trailer'
        }
        
        for field, value in kwargs.items():
            if field not in valid_fields:
                raise ValueError(f"Invalid field: {field}")
            
            if not isinstance(value, Money):
                value = Money(value)
            
            setattr(self, field, value)
    
    def __str__(self) -> str:
        return f"FixedCostsTruck(truck_id={self.truck_id}, total={self.total()})"


@dataclass
class FixedCostsCommon:
    """
    Common fixed costs that apply to all trucks.
    Set through forms, minimizing human factor in Excel.
    """
    ifta: Money
    insurance: Money  # General business insurance
    eld: Money        # Electronic Logging Device
    tablet: Money     # Communication/navigation tablets
    tolls: Money      # Base toll costs
    
    @classmethod
    def zero(cls) -> FixedCostsCommon:
        """Create zero common fixed costs."""
        return cls(
            ifta=Money(0),
            insurance=Money(0),
            eld=Money(0),
            tablet=Money(0),
            tolls=Money(0)
        )
    
    def total(self) -> Money:
        """Calculate total common fixed costs."""
        return (self.ifta + self.insurance + self.eld + 
                self.tablet + self.tolls)
    
    def update_values(self, **kwargs) -> None:
        """Update cost values with validation."""
        valid_fields = {'ifta', 'insurance', 'eld', 'tablet', 'tolls'}
        
        for field, value in kwargs.items():
            if field not in valid_fields:
                raise ValueError(f"Invalid field: {field}")
            
            if not isinstance(value, Money):
                value = Money(value)
            
            setattr(self, field, value)
    
    def __str__(self) -> str:
        return f"FixedCostsCommon(total={self.total()})"


@dataclass
class TotalCosts:
    """
    Aggregate of all costs for a truck in a given period.
    
    Business rule: Total costs = Variable costs + Truck fixed costs + Common fixed costs
    """
    variable_costs: VariableCosts
    truck_fixed_costs: FixedCostsTruck
    common_fixed_costs: FixedCostsCommon
    
    def total_variable_amount(self) -> Money:
        """Get total variable costs."""
        return self.variable_costs.total()
    
    def total_fixed_amount(self) -> Money:
        """Get total fixed costs (truck-specific + common)."""
        return self.truck_fixed_costs.total() + self.common_fixed_costs.total()
    
    def total_monthly_amount(self) -> Money:
        """Get total monthly costs for this truck."""
        return self.total_variable_amount() + self.total_fixed_amount()
    
    def breakdown(self) -> Dict[str, Money]:
        """Get detailed cost breakdown."""
        return {
            # Variable costs
            'salary': self.variable_costs.salary,
            'fuel': self.variable_costs.fuel,
            'tolls_variable': self.variable_costs.tolls,
            'repair': self.variable_costs.repair,
            
            # Truck fixed costs
            'truck_payment': self.truck_fixed_costs.truck_payment,
            'trailer_payment': self.truck_fixed_costs.trailer_payment,
            'truck_insurance': self.truck_fixed_costs.physical_damage_insurance_truck,
            'trailer_insurance': self.truck_fixed_costs.physical_damage_insurance_trailer,
            
            # Common fixed costs
            'ifta': self.common_fixed_costs.ifta,
            'business_insurance': self.common_fixed_costs.insurance,
            'eld': self.common_fixed_costs.eld,
            'tablet': self.common_fixed_costs.tablet,
            'tolls_fixed': self.common_fixed_costs.tolls,
        }
    
    def __str__(self) -> str:
        return f"TotalCosts(total={self.total_monthly_amount()})"
