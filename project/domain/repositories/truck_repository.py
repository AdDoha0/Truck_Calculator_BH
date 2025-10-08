"""
Truck repository interface - defines contract for truck data access.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.truck import Truck
from ..entities.common import TruckId


class TruckRepository(ABC):
    """
    Abstract base class for truck data access.
    
    This interface belongs to the domain layer and defines
    what operations are needed without specifying how they're implemented.
    """
    
    @abstractmethod
    def save(self, truck: Truck) -> Truck:
        """
        Save truck entity to persistent storage.
        
        Args:
            truck: Truck entity to save
            
        Returns:
            Saved truck with assigned ID (if new)
            
        Raises:
            ValueError: If truck data is invalid
            DuplicateError: If tractor_no already exists
        """
        pass
    
    @abstractmethod
    def find_by_id(self, truck_id: TruckId) -> Optional[Truck]:
        """
        Find truck by its unique ID.
        
        Returns:
            Truck entity if found, None otherwise
        """
        pass
    
    @abstractmethod
    def find_by_tractor_no(self, tractor_no: str) -> Optional[Truck]:
        """
        Find truck by its tractor number.
        
        Args:
            tractor_no: Tractor number to search for
            
        Returns:
            Truck entity if found, None otherwise
        """
        pass
    
    @abstractmethod
    def find_all(self) -> List[Truck]:
        """
        Get all trucks.
        
        Returns:
            List of all truck entities
        """
        pass
    
    @abstractmethod
    def update(self, truck: Truck) -> Truck:
        """
        Update existing truck.
        
        Args:
            truck: Truck entity with updated data
            
        Returns:
            Updated truck entity
            
        Raises:
            NotFoundError: If truck doesn't exist
            ValueError: If truck data is invalid
        """
        pass
    
    @abstractmethod
    def delete(self, truck_id: TruckId) -> bool:
        """
        Delete truck by ID.
        
        Args:
            truck_id: ID of truck to delete
            
        Returns:
            True if deleted, False if not found
            
        Raises:
            ConstraintError: If truck has related data that prevents deletion
        """
        pass
    
    @abstractmethod
    def has_monthly_data(self, truck_id: TruckId) -> bool:
        """
        Check if truck has any monthly data records.
        
        This is used to enforce business rule that trucks with
        monthly data cannot be deleted.
        
        Args:
            truck_id: ID of truck to check
            
        Returns:
            True if truck has monthly records, False otherwise
        """
        pass
    
    @abstractmethod
    def count_monthly_records(self, truck_id: TruckId) -> int:
        """
        Count monthly records for a truck.
        
        Args:
            truck_id: ID of truck to count records for
            
        Returns:
            Number of monthly records
        """
        pass
