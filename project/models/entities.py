"""
Business entities and value objects.
Combines all domain entities from the original domain layer.
"""
from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal
from datetime import date
from typing import Union, Optional, Dict, NewType, TYPE_CHECKING

if TYPE_CHECKING:
    pass

# ========== Common Types ==========

# Strong typing for truck ID
TruckId = NewType('TruckId', int)


# ========== Financial Value Objects ==========

@dataclass(frozen=True)
class Money:
    """
    Value object representing monetary amount.
    Uses Decimal for precise financial calculations.
    """
    amount: Decimal
    
    def __init__(self, amount: Union[float, int, str, Decimal]):
        # Use object.__setattr__ since dataclass is frozen
        object.__setattr__(self, 'amount', Decimal(str(amount)))
    
    def __add__(self, other: Money) -> Money:
        return Money(self.amount + other.amount)
    
    def __sub__(self, other: Money) -> Money:
        return Money(self.amount - other.amount)
    
    def __mul__(self, factor: Union[int, float, Decimal]) -> Money:
        return Money(self.amount * Decimal(str(factor)))
    
    def __truediv__(self, divisor: Union[int, float, Decimal]) -> Money:
        return Money(self.amount / Decimal(str(divisor)))
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Money):
            return False
        return self.amount == other.amount
    
    def __lt__(self, other: Money) -> bool:
        return self.amount < other.amount
    
    def __gt__(self, other: Money) -> bool:
        return self.amount > other.amount
    
    def __str__(self) -> str:
        return f"${self.amount:,.2f}"
    
    def __repr__(self) -> str:
        return f"Money({self.amount})"
    
    @property
    def is_positive(self) -> bool:
        return self.amount > 0
    
    @property 
    def is_negative(self) -> bool:
        return self.amount < 0
    
    @property
    def is_zero(self) -> bool:
        return self.amount == 0


@dataclass(frozen=True)
class Period:
    """
    Value object representing a time period (month/year).
    """
    year: int
    month: int
    
    def __post_init__(self):
        if not (1 <= self.month <= 12):
            raise ValueError(f"Month must be between 1 and 12, got {self.month}")
        if self.year < 1900:
            raise ValueError(f"Year must be >= 1900, got {self.year}")
    
    @classmethod
    def from_date(cls, date_value: date) -> Period:
        return cls(year=date_value.year, month=date_value.month)
    
    def to_date(self) -> date:
        """Returns first day of the period month."""
        return date(self.year, self.month, 1)
    
    def next_month(self) -> Period:
        if self.month == 12:
            return Period(year=self.year + 1, month=1)
        return Period(year=self.year, month=self.month + 1)
    
    def previous_month(self) -> Period:
        if self.month == 1:
            return Period(year=self.year - 1, month=12)
        return Period(year=self.year, month=self.month - 1)
    
    def __str__(self) -> str:
        return f"{self.year}-{self.month:02d}"
    
    def __lt__(self, other: Period) -> bool:
        if self.year != other.year:
            return self.year < other.year
        return self.month < other.month


# ========== Core Business Entities ==========

@dataclass
class TruckInfo:
    """
    Data transfer object for truck information.
    Used by API layer to return truck data with additional metadata.
    """
    id: int
    tractor_no: str
    monthly_count: int
    has_fixed_costs: bool
    
    def __str__(self) -> str:
        return f"TruckInfo(id={self.id}, tractor_no='{self.tractor_no}', monthly_count={self.monthly_count})"


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


# ========== Cost Entities ==========

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
