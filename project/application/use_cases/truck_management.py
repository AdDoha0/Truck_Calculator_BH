"""
Truck management use cases.
"""

from typing import List, Optional
from ...domain.entities.truck import Truck, TruckId
from ...domain.services.truck_service import TruckService
from ...domain.services.validation_service import ValidationService
from ...domain.repositories.truck_repository import TruckRepository
from ...domain.repositories.costs_repository import CostsRepository
from ..dto.truck_dto import TruckDto, CreateTruckRequest, UpdateTruckRequest


class TruckManagementUseCase:
    """
    Use case for truck management operations.
    
    Coordinates domain services to handle truck CRUD operations
    while enforcing business rules and validation.
    """
    
    def __init__(self, 
                 truck_repo: TruckRepository,
                 costs_repo: CostsRepository):
        self._truck_service = TruckService(truck_repo, costs_repo)
        self._validation_service = ValidationService()
        self._truck_repo = truck_repo
    
    def create_truck(self, request: CreateTruckRequest) -> TruckDto:
        """
        Create a new truck.
        
        Business flow:
        1. Validate request data
        2. Check tractor number uniqueness
        3. Create truck entity
        4. Save to repository
        5. Return DTO
        
        Raises:
            ValueError: If validation fails or tractor number is not unique
        """
        # Validate request
        if not request.validate():
            raise ValueError("Invalid truck creation request")
        
        # Validate tractor number format
        validation_result = self._validation_service.validate_truck_creation(request.tractor_no)
        if not validation_result.is_valid:
            raise ValueError("; ".join(validation_result.errors))
        
        # Check uniqueness
        is_unique = self._truck_service.validate_unique_tractor_no(request.tractor_no)
        if not is_unique:
            raise ValueError(f"Трак с номером '{request.tractor_no}' уже существует")
        
        # Create domain entity
        truck = Truck(id=None, tractor_no=request.tractor_no.strip())
        
        # Save via repository
        saved_truck = self._truck_repo.save(truck)
        
        # Return DTO
        return TruckDto.from_domain(saved_truck)
    
    def get_truck(self, truck_id: TruckId) -> Optional[TruckDto]:
        """
        Get truck by ID.
        
        Returns:
            TruckDto if found, None otherwise
        """
        truck = self._truck_repo.find_by_id(truck_id)
        if not truck:
            return None
        
        # Get additional counts for the DTO
        monthly_count = self._truck_repo.count_monthly_records(truck_id)
        
        return TruckDto.from_domain(
            truck, 
            monthly_count=monthly_count,
            fixed_costs_count=1  # Simplified for now
        )
    
    def get_all_trucks(self) -> List[TruckDto]:
        """
        Get all trucks with summary information.
        
        Returns:
            List of TruckDto objects with counts
        """
        trucks_summary = self._truck_service.list_all_trucks_with_summary()
        
        return [
            TruckDto(
                id=TruckId(item['id']),
                tractor_no=item['tractor_no'],
                monthly_rows_count=item['monthly_rows_count'],
                fixed_costs_count=item['fixed_costs_count']
            )
            for item in trucks_summary
        ]
    
    def update_truck(self, request: UpdateTruckRequest) -> TruckDto:
        """
        Update existing truck.
        
        Business flow:
        1. Find existing truck
        2. Validate new data
        3. Check uniqueness (excluding current truck)
        4. Update truck entity
        5. Save changes
        6. Return updated DTO
        
        Raises:
            ValueError: If validation fails or truck not found
        """
        # Validate request
        if not request.validate():
            raise ValueError("Invalid truck update request")
        
        # Find existing truck
        existing_truck = self._truck_repo.find_by_id(request.truck_id)
        if not existing_truck:
            raise ValueError(f"Трак с ID {request.truck_id} не найден")
        
        # Validate new tractor number
        validation_result = self._validation_service.validate_truck_update(
            existing_truck, request.tractor_no
        )
        if not validation_result.is_valid:
            raise ValueError("; ".join(validation_result.errors))
        
        # Check uniqueness (excluding current truck)
        is_unique = self._truck_service.validate_unique_tractor_no(
            request.tractor_no, exclude_truck_id=request.truck_id
        )
        if not is_unique:
            raise ValueError(f"Трак с номером '{request.tractor_no}' уже существует")
        
        # Update truck entity
        existing_truck.change_tractor_no(request.tractor_no)
        
        # Save changes
        updated_truck = self._truck_repo.update(existing_truck)
        
        # Return DTO
        monthly_count = self._truck_repo.count_monthly_records(request.truck_id)
        return TruckDto.from_domain(
            updated_truck,
            monthly_count=monthly_count,
            fixed_costs_count=1
        )
    
    def delete_truck(self, truck_id: TruckId) -> bool:
        """
        Delete truck if allowed by business rules.
        
        Business flow:
        1. Check if truck exists
        2. Verify deletion is allowed (no monthly data)
        3. Delete truck and related data
        
        Returns:
            True if deleted successfully, False if not found
            
        Raises:
            ValueError: If truck cannot be deleted due to business rules
        """
        # Check if truck exists
        truck = self._truck_repo.find_by_id(truck_id)
        if not truck:
            return False
        
        # Check business rules for deletion
        can_delete = self._truck_service.can_delete_truck(truck_id)
        if not can_delete:
            raise ValueError(
                "Нельзя удалить трак, который имеет месячные записи. "
                "Сначала удалите все связанные данные."
            )
        
        # Perform deletion
        return self._truck_repo.delete(truck_id)
