"""
Truck domain service - business logic for truck operations.
"""

from typing import List, Optional
from ..entities.truck import Truck, TruckId
from ..entities.costs import FixedCostsTruck, FixedCostsCommon
from ..repositories.truck_repository import TruckRepository
from ..repositories.costs_repository import CostsRepository


class TruckService:
    """
    Domain service for truck-related business operations.
    Coordinates between truck entities and repositories.
    """
    
    def __init__(self, 
                 truck_repo: TruckRepository,
                 costs_repo: CostsRepository):
        self._truck_repo = truck_repo
        self._costs_repo = costs_repo
    
    def can_delete_truck(self, truck_id: TruckId) -> bool:
        """
        Business rule: Check if truck can be safely deleted.
        
        A truck can be deleted only if:
        1. It exists
        2. It has no monthly data records
        """
        truck = self._truck_repo.find_by_id(truck_id)
        if not truck:
            return False
        
        has_monthly_data = self._truck_repo.has_monthly_data(truck_id)
        return truck.can_be_deleted(has_monthly_data)
    
    def get_truck_with_costs(self, truck_id: TruckId) -> Optional[tuple[Truck, FixedCostsTruck]]:
        """
        Get truck along with its specific fixed costs.
        Returns None if truck doesn't exist.
        """
        truck = self._truck_repo.find_by_id(truck_id)
        if not truck:
            return None
        
        truck_costs = self._costs_repo.find_truck_costs(truck_id)
        if not truck_costs:
            # Create default zero costs for this truck
            truck_costs = FixedCostsTruck.zero_for_truck(truck_id)
        
        return truck, truck_costs
    
    def ensure_truck_costs_exist(self, truck_id: TruckId) -> FixedCostsTruck:
        """
        Ensure that truck has fixed costs record.
        Creates zero costs if none exist.
        """
        truck_costs = self._costs_repo.find_truck_costs(truck_id)
        if not truck_costs:
            truck_costs = FixedCostsTruck.zero_for_truck(truck_id)
            self._costs_repo.save_truck_costs(truck_costs)
        
        return truck_costs
    
    def validate_unique_tractor_no(self, tractor_no: str, exclude_truck_id: Optional[TruckId] = None) -> bool:
        """
        Business rule: Tractor numbers must be unique across all trucks.
        
        Args:
            tractor_no: The tractor number to check
            exclude_truck_id: Optional truck ID to exclude from check (for updates)
            
        Returns:
            True if tractor number is unique, False otherwise
        """
        # Check both original and updated names to handle renames
        normalized_tractor_no = tractor_no.strip().upper()
        
        all_trucks = self._truck_repo.find_all()
        
        for truck in all_trucks:
            if truck.tractor_no.upper() == normalized_tractor_no:
                # If we're excluding a truck (for updates), check if it's the same truck
                if exclude_truck_id and truck.id == exclude_truck_id:
                    continue
                return False
        
        return True
    
    def list_all_trucks_with_summary(self) -> List[dict]:
        """
        Get all trucks with summary information.
        
        Returns list of dictionaries with truck info and counts.
        """
        trucks = self._truck_repo.find_all()
        result = []
        
        for truck in trucks:
            monthly_count = self._truck_repo.count_monthly_records(truck.id)
            fixed_costs_exist = self._costs_repo.find_truck_costs(truck.id) is not None
            
            result.append({
                'id': truck.id,
                'tractor_no': truck.tractor_no,
                'monthly_rows_count': monthly_count,
                'fixed_costs_count': 1 if fixed_costs_exist else 0,
            })
        
        return result
