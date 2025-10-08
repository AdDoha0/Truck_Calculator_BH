"""
Costs management use cases.
"""

from typing import Optional
from ...domain.entities.truck import TruckId
from ...domain.entities.costs import FixedCostsTruck, FixedCostsCommon
from ...domain.entities.financial import Money
from ...domain.services.validation_service import ValidationService
from ...domain.repositories.costs_repository import CostsRepository
from ..dto.costs_dto import (
    FixedCostsTruckDto, 
    FixedCostsCommonDto,
    UpdateTruckCostsRequest,
    UpdateCommonCostsRequest
)


class CostsManagementUseCase:
    """
    Use case for managing fixed costs (both truck-specific and common).
    
    Handles CRUD operations for fixed costs while enforcing business rules.
    """
    
    def __init__(self, costs_repo: CostsRepository):
        self._costs_repo = costs_repo
        self._validation_service = ValidationService()
    
    # Truck-specific fixed costs
    
    def get_truck_costs(self, truck_id: TruckId) -> FixedCostsTruckDto:
        """
        Get fixed costs for a specific truck.
        Creates zero costs if none exist.
        """
        costs = self._costs_repo.find_truck_costs(truck_id)
        if not costs:
            # Create default zero costs
            costs = FixedCostsTruck.zero_for_truck(truck_id)
            costs = self._costs_repo.save_truck_costs(costs)
        
        return FixedCostsTruckDto.from_domain(costs)
    
    def update_truck_costs(self, request: UpdateTruckCostsRequest) -> FixedCostsTruckDto:
        """
        Update truck-specific fixed costs.
        
        Business flow:
        1. Validate input values
        2. Get existing costs (or create if not exist)
        3. Update values
        4. Save changes
        5. Return updated DTO
        
        Raises:
            ValueError: If validation fails
        """
        # Validate update values
        updates = request.get_updates()
        validation_result = self._validation_service.validate_fixed_costs_update(updates)
        if not validation_result.is_valid:
            raise ValueError("; ".join(validation_result.errors))
        
        # Get existing costs
        existing_costs = self._costs_repo.find_truck_costs(request.truck_id)
        if not existing_costs:
            existing_costs = FixedCostsTruck.zero_for_truck(request.truck_id)
        
        # Update values
        money_updates = {k: Money(v) for k, v in updates.items()}
        existing_costs.update_values(**money_updates)
        
        # Save changes
        if existing_costs.truck_id:
            # Update existing record
            updated_costs = self._costs_repo.update_truck_costs(existing_costs)
        else:
            # Create new record
            updated_costs = self._costs_repo.save_truck_costs(existing_costs)
        
        return FixedCostsTruckDto.from_domain(updated_costs)
    
    def delete_truck_costs(self, truck_id: TruckId) -> bool:
        """
        Delete truck-specific fixed costs.
        
        Returns:
            True if deleted, False if not found
        """
        return self._costs_repo.delete_truck_costs(truck_id)
    
    # Common fixed costs
    
    def get_common_costs(self) -> FixedCostsCommonDto:
        """
        Get common fixed costs.
        Creates zero costs if none exist.
        """
        costs = self._costs_repo.find_common_costs()
        if not costs:
            # Create default zero costs
            costs = FixedCostsCommon.zero()
            costs = self._costs_repo.save_common_costs(costs)
        
        return FixedCostsCommonDto.from_domain(costs)
    
    def update_common_costs(self, request: UpdateCommonCostsRequest) -> FixedCostsCommonDto:
        """
        Update common fixed costs.
        
        Business flow:
        1. Validate input values
        2. Get existing costs (or create if not exist)
        3. Update values
        4. Save changes
        5. Return updated DTO
        
        Raises:
            ValueError: If validation fails
        """
        # Validate update values
        updates = request.get_updates()
        validation_result = self._validation_service.validate_fixed_costs_update(updates)
        if not validation_result.is_valid:
            raise ValueError("; ".join(validation_result.errors))
        
        # Get existing costs
        existing_costs = self._costs_repo.find_common_costs()
        if not existing_costs:
            existing_costs = FixedCostsCommon.zero()
        
        # Update values
        money_updates = {k: Money(v) for k, v in updates.items()}
        existing_costs.update_values(**money_updates)
        
        # Save changes
        try:
            # Try to update existing record
            updated_costs = self._costs_repo.update_common_costs(existing_costs)
        except:
            # If update fails, create new record
            updated_costs = self._costs_repo.save_common_costs(existing_costs)
        
        return FixedCostsCommonDto.from_domain(updated_costs)
    
    # Utility methods
    
    def get_all_costs_for_truck(self, truck_id: TruckId) -> tuple[FixedCostsTruckDto, FixedCostsCommonDto]:
        """
        Get both truck-specific and common costs for complete cost picture.
        
        Returns:
            Tuple of (truck_costs, common_costs)
        """
        truck_costs = self.get_truck_costs(truck_id)
        common_costs = self.get_common_costs()
        
        return truck_costs, common_costs
