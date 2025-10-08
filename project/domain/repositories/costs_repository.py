"""
Costs repository interface - defines contract for costs data access.
"""

from abc import ABC, abstractmethod
from typing import Optional
from ..entities.common import TruckId
from ..entities.costs import FixedCostsTruck, FixedCostsCommon


class CostsRepository(ABC):
    """
    Abstract base class for costs data access.
    
    Handles both truck-specific fixed costs and common fixed costs.
    """
    
    # Truck-specific fixed costs
    
    @abstractmethod
    def save_truck_costs(self, costs: FixedCostsTruck) -> FixedCostsTruck:
        """
        Save truck-specific fixed costs.
        
        Args:
            costs: FixedCostsTruck entity to save
            
        Returns:
            Saved costs entity
        """
        pass
    
    @abstractmethod
    def find_truck_costs(self, truck_id: TruckId) -> Optional[FixedCostsTruck]:
        """
        Find fixed costs for a specific truck.
        
        Args:
            truck_id: ID of the truck
            
        Returns:
            FixedCostsTruck entity if found, None otherwise
        """
        pass
    
    @abstractmethod
    def update_truck_costs(self, costs: FixedCostsTruck) -> FixedCostsTruck:
        """
        Update existing truck-specific costs.
        
        Args:
            costs: Updated FixedCostsTruck entity
            
        Returns:
            Updated costs entity
            
        Raises:
            NotFoundError: If costs record doesn't exist
        """
        pass
    
    @abstractmethod
    def delete_truck_costs(self, truck_id: TruckId) -> bool:
        """
        Delete truck-specific fixed costs.
        
        Args:
            truck_id: ID of the truck whose costs to delete
            
        Returns:
            True if deleted, False if not found
        """
        pass
    
    # Common fixed costs
    
    @abstractmethod
    def save_common_costs(self, costs: FixedCostsCommon) -> FixedCostsCommon:
        """
        Save common fixed costs.
        
        Args:
            costs: FixedCostsCommon entity to save
            
        Returns:
            Saved costs entity
        """
        pass
    
    @abstractmethod
    def find_common_costs(self) -> Optional[FixedCostsCommon]:
        """
        Find current common fixed costs.
        
        Note: In this implementation, we assume there's only one
        active common costs record at a time.
        
        Returns:
            FixedCostsCommon entity if found, None otherwise
        """
        pass
    
    @abstractmethod
    def update_common_costs(self, costs: FixedCostsCommon) -> FixedCostsCommon:
        """
        Update existing common costs.
        
        Args:
            costs: Updated FixedCostsCommon entity
            
        Returns:
            Updated costs entity
            
        Raises:
            NotFoundError: If costs record doesn't exist
        """
        pass
