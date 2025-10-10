"""
Models layer - Data models, entities and database management.

This layer contains:
- SQLAlchemy database models and connection management
- Business entities and value objects  
- Validation logic for business rules
- Common types and data structures

Replaces the original domain/entities and data/database layers.
"""
from .database import (
    # Database models
    Truck, MonthlyRow, FixedCostsTruck, FixedCostsCommon,
    # Database functions
    get_db_session, init_db, ensure_db_exists
)
from .entities import (
    # Value objects
    Money, Period,
    # Business entities  
    Truck as TruckEntity, VariableCosts, FixedCostsTruck as FixedCostsTruckEntity,
    FixedCostsCommon as FixedCostsCommonEntity, TotalCosts
)
from .validation import ValidationService, ValidationResult
from .types import TruckId, TruckInfo, CostsSummary, TruckCostsUpdate, CommonCostsUpdate

__all__ = [
    # Database
    "Truck", "MonthlyRow", "FixedCostsTruck", "FixedCostsCommon",
    "get_db_session", "init_db", "ensure_db_exists",
    
    # Entities
    "Money", "Period", "TruckEntity", "VariableCosts", 
    "FixedCostsTruckEntity", "FixedCostsCommonEntity", "TotalCosts",
    
    # Validation
    "ValidationService", "ValidationResult",
    
    # Types
    "TruckId", "TruckInfo", "CostsSummary", "TruckCostsUpdate", "CommonCostsUpdate",
]
