"""
Database utilities for Streamlit UI.

This module provides simple functions that wrap the StreamlitAdapter
for backward compatibility and easy integration with existing UI code.
"""

from typing import List, Dict, Any, Optional
from .adapters.streamlit_adapter import get_adapter


# Initialize database
def init_database():
    """Initialize database tables."""
    get_adapter().init_database()


# Truck management functions
def create_truck(tractor_no: str) -> bool:
    """Create a new truck."""
    return get_adapter().create_truck(tractor_no)


def get_all_trucks() -> List[Dict[str, Any]]:
    """Get all trucks with summary information."""
    return get_adapter().get_all_trucks()


def get_truck_by_id(truck_id: int) -> Optional[Dict[str, Any]]:
    """Get truck by ID.""" 
    return get_adapter().get_truck_by_id(truck_id)


def update_truck(truck_id: int, new_tractor_no: str) -> bool:
    """Update truck tractor number."""
    return get_adapter().update_truck(truck_id, new_tractor_no)


def delete_truck(truck_id: int) -> bool:
    """Delete truck if allowed by business rules."""
    return get_adapter().delete_truck(truck_id)


# Costs management functions  
def get_truck_costs(truck_id: int) -> Dict[str, float]:
    """Get truck-specific fixed costs."""
    return get_adapter().get_truck_costs(truck_id)


def update_truck_costs(truck_id: int, **cost_updates) -> bool:
    """Update truck-specific fixed costs."""
    return get_adapter().update_truck_costs(truck_id, **cost_updates)


def get_common_costs() -> Dict[str, float]:
    """Get common fixed costs."""
    return get_adapter().get_common_costs()


def update_common_costs(**cost_updates) -> bool:
    """Update common fixed costs."""
    return get_adapter().update_common_costs(**cost_updates)


# Utility functions for backward compatibility
def get_trucks_for_selectbox() -> Dict[str, int]:
    """
    Get trucks formatted for Streamlit selectbox.
    
    Returns:
        Dictionary mapping display names to truck IDs
    """
    trucks = get_all_trucks()
    return {
        f"{truck['tractor_no']} (ID: {truck['id']})": truck['id']
        for truck in trucks
    }
