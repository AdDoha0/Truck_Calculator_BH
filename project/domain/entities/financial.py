"""
Financial domain entities and value objects.
"""

from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal
from datetime import date
from typing import Union


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
