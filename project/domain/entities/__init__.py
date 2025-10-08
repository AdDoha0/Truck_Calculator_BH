"""
Domain entities - pure business objects.

These classes contain only business logic and have no dependencies
on databases, frameworks, or external libraries.
"""

from .common import TruckId
from .truck import Truck
from .costs import FixedCostsTruck, FixedCostsCommon, VariableCosts, TotalCosts
from .financial import Money, Period

__all__ = [
    "TruckId",
    "Truck",
    "FixedCostsTruck",
    "FixedCostsCommon",
    "VariableCosts",
    "TotalCosts",
    "Money",
    "Period",
]
