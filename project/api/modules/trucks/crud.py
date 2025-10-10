"""
CRUD операции для модуля trucks.
"""
from typing import List, Optional
from sqlalchemy.orm import Session

from project.models.database import Truck as TruckORM, MonthlyRow as MonthlyRowORM, FixedCostsTruck as FixedCostsTruckORM
from project.models.entities import TruckInfo


class TruckCRUD:
    """CRUD операции для траков."""
    
    def create_truck(self, db: Session, tractor_no: str) -> TruckInfo:
        """Создать новый трак."""
        # Проверка уникальности
        existing = db.query(TruckORM).filter_by(tractor_no=tractor_no.strip()).first()
        if existing:
            raise ValueError(f"Трак с номером '{tractor_no}' уже существует")
        
        # Создание нового трака
        truck_orm = TruckORM(tractor_no=tractor_no.strip())
        db.add(truck_orm)
        db.flush()  # Получаем ID
        
        return TruckInfo(
            id=truck_orm.id,
            tractor_no=truck_orm.tractor_no,
            monthly_count=0,
            has_fixed_costs=False
        )
    
    def get_truck_by_id(self, db: Session, truck_id: int) -> Optional[TruckInfo]:
        """Получить трак по ID."""
        truck_orm = db.query(TruckORM).filter_by(id=truck_id).first()
        if not truck_orm:
            return None
        
        monthly_count = db.query(MonthlyRowORM).filter_by(truck_id=truck_id).count()
        has_fixed_costs = db.query(FixedCostsTruckORM).filter_by(truck_id=truck_id).first() is not None
        
        return TruckInfo(
            id=truck_orm.id,
            tractor_no=truck_orm.tractor_no,
            monthly_count=monthly_count,
            has_fixed_costs=has_fixed_costs
        )
    
    def get_all_trucks(self, db: Session) -> List[TruckInfo]:
        """Получить все траки."""
        trucks = db.query(TruckORM).all()
        result = []
        
        for truck_orm in trucks:
            monthly_count = db.query(MonthlyRowORM).filter_by(truck_id=truck_orm.id).count()
            has_fixed_costs = db.query(FixedCostsTruckORM).filter_by(truck_id=truck_orm.id).first() is not None
            
            result.append(TruckInfo(
                id=truck_orm.id,
                tractor_no=truck_orm.tractor_no,
                monthly_count=monthly_count,
                has_fixed_costs=has_fixed_costs
            ))
        
        return result
    
    def update_truck(self, db: Session, truck_id: int, tractor_no: str) -> TruckInfo:
        """Обновить трак."""
        truck_orm = db.query(TruckORM).filter_by(id=truck_id).first()
        if not truck_orm:
            raise ValueError(f"Трак с ID {truck_id} не найден")
        
        # Проверка уникальности (исключая текущий трак)
        existing = db.query(TruckORM).filter(
            TruckORM.tractor_no == tractor_no.strip(),
            TruckORM.id != truck_id
        ).first()
        if existing:
            raise ValueError(f"Трак с номером '{tractor_no}' уже существует")
        
        truck_orm.tractor_no = tractor_no.strip()
        db.flush()
        
        monthly_count = db.query(MonthlyRowORM).filter_by(truck_id=truck_id).count()
        has_fixed_costs = db.query(FixedCostsTruckORM).filter_by(truck_id=truck_id).first() is not None
        
        return TruckInfo(
            id=truck_orm.id,
            tractor_no=truck_orm.tractor_no,
            monthly_count=monthly_count,
            has_fixed_costs=has_fixed_costs
        )
    
    def delete_truck(self, db: Session, truck_id: int) -> bool:
        """Удалить трак."""
        truck_orm = db.query(TruckORM).filter_by(id=truck_id).first()
        if not truck_orm:
            return False
        
        # Проверка наличия месячных данных
        monthly_count = db.query(MonthlyRowORM).filter_by(truck_id=truck_id).count()
        if monthly_count > 0:
            raise ValueError("Нельзя удалить трак, который имеет месячные записи")
        
        db.delete(truck_orm)
        return True


# Глобальный экземпляр CRUD
truck_crud = TruckCRUD()
