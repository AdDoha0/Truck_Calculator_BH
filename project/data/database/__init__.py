"""
Database package for Truck Calculate application.

Main components:
- models: SQLAlchemy models (Truck, MonthlyRow, FixedCostsTruck, FixedCostsCommon)
- database: Database initialization and session management

Usage:
    from project.data.database import get_db_session, Truck
    
    with get_db_session() as session:
        truck = Truck(tractor_no="ABC123")
        session.add(truck)
"""

from .database import (
    get_db_session,
    get_engine,
    get_session_factory,
    init_db,
    ensure_db_exists,
    drop_all_tables,
    DB_PATH,
)

from .models import (
    Base,
    Truck,
    MonthlyRow,
    FixedCostsTruck,
    FixedCostsCommon,
)

__all__ = [
    # Session management
    "get_db_session",
    "get_engine",
    "get_session_factory",
    "init_db",
    "ensure_db_exists",
    "drop_all_tables",
    "DB_PATH",
    # Models
    "Base",
    "Truck",
    "MonthlyRow",
    "FixedCostsTruck",
    "FixedCostsCommon",
]

