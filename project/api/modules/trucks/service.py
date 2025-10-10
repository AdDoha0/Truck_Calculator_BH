"""
Бизнес-логика для модуля trucks.
"""
from typing import List, Optional
from sqlalchemy.orm import Session

from project.models.validation import ValidationService
from project.models.entities import TruckInfo
from .crud import truck_crud


class TruckService:
    """Сервис для управления траками."""
    
    def __init__(self):
        self._validation_service = ValidationService()
    
    def create_truck(self, db: Session, tractor_no: str) -> TruckInfo:
        """Создать трак с валидацией."""
        # Валидация номера трактора
        validation_result = self._validation_service.validate_truck_creation(tractor_no)
        if not validation_result.is_valid:
            raise ValueError("; ".join(validation_result.errors))
        
        return truck_crud.create_truck(db, tractor_no)
    
    def get_truck_by_id(self, db: Session, truck_id: int) -> Optional[TruckInfo]:
        """Получить трак по ID."""
        return truck_crud.get_truck_by_id(db, truck_id)
    
    def get_all_trucks(self, db: Session) -> List[TruckInfo]:
        """Получить все траки."""
        return truck_crud.get_all_trucks(db)
    
    def update_truck(self, db: Session, truck_id: int, tractor_no: str) -> TruckInfo:
        """Обновить трак с валидацией."""
        # Валидация нового номера трактора
        validation_result = self._validation_service.validate_truck_creation(tractor_no)
        if not validation_result.is_valid:
            raise ValueError("; ".join(validation_result.errors))
        
        return truck_crud.update_truck(db, truck_id, tractor_no)
    
    def delete_truck(self, db: Session, truck_id: int) -> bool:
        """Удалить трак с проверкой бизнес-правил."""
        # Получаем информацию о траке
        truck_info = truck_crud.get_truck_by_id(db, truck_id)
        if not truck_info:
            return False
        
        # Бизнес-правило: нельзя удалить трак с месячными данными
        if truck_info.monthly_count > 0:
            raise ValueError(
                "Нельзя удалить трак, который имеет месячные записи. "
                "Сначала удалите все связанные данные."
            )
        
        return truck_crud.delete_truck(db, truck_id)
    
    def can_delete_truck(self, db: Session, truck_id: int) -> bool:
        """Проверить, можно ли удалить трак."""
        truck_info = truck_crud.get_truck_by_id(db, truck_id)
        if not truck_info:
            return False
        
        return truck_info.monthly_count == 0


# Глобальный экземпляр сервиса
truck_service = TruckService()
