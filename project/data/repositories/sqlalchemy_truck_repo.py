"""
SQLAlchemy implementation of TruckRepository.
"""

from typing import List, Optional
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from ...domain.entities.truck import Truck, TruckId
from ...domain.repositories.truck_repository import TruckRepository
from ..database.database import get_db_session
from ..database.models import Truck as TruckORM, MonthlyRow as MonthlyRowORM
from .mappers import TruckMapper


class SqlAlchemyTruckRepository(TruckRepository):
    """
    SQLAlchemy implementation of the TruckRepository interface.
    """
    
    def __init__(self, session: Optional[Session] = None):
        """
        Initialize repository.
        
        Args:
            session: Optional SQLAlchemy session. If None, uses context manager.
        """
        self._session = session
    
    def _get_session(self):
        """Get session - either injected or from context manager."""
        if self._session:
            return self._session
        return get_db_session()
    
    def save(self, truck: Truck) -> Truck:
        """Save truck entity to database."""
        if self._session:
            # Use injected session
            return self._save_with_session(self._session, truck)
        else:
            # Use context manager
            with get_db_session() as session:
                return self._save_with_session(session, truck)
    
    def _save_with_session(self, session: Session, truck: Truck) -> Truck:
        """Internal save method with session."""
        try:
            orm_truck = TruckMapper.to_orm(truck)
            session.add(orm_truck)
            session.flush()  # Get the ID
            
            # Update domain entity with new ID
            truck.id = TruckId(orm_truck.id)
            
            return truck
            
        except IntegrityError as e:
            session.rollback()
            if "tractor_no" in str(e):
                raise ValueError(f"Трак с номером '{truck.tractor_no}' уже существует")
            raise ValueError(f"Ошибка сохранения трака: {e}")
    
    def find_by_id(self, truck_id: TruckId) -> Optional[Truck]:
        """Find truck by ID."""
        if self._session:
            return self._find_by_id_with_session(self._session, truck_id)
        else:
            with get_db_session() as session:
                return self._find_by_id_with_session(session, truck_id)
    
    def _find_by_id_with_session(self, session: Session, truck_id: TruckId) -> Optional[Truck]:
        """Internal find by ID method with session."""
        orm_truck = session.query(TruckORM).filter(TruckORM.id == int(truck_id)).first()
        if orm_truck:
            return TruckMapper.to_domain(orm_truck)
        return None
    
    def find_by_tractor_no(self, tractor_no: str) -> Optional[Truck]:
        """Find truck by tractor number.""" 
        if self._session:
            return self._find_by_tractor_no_with_session(self._session, tractor_no)
        else:
            with get_db_session() as session:
                return self._find_by_tractor_no_with_session(session, tractor_no)
    
    def _find_by_tractor_no_with_session(self, session: Session, tractor_no: str) -> Optional[Truck]:
        """Internal find by tractor number method with session."""
        orm_truck = session.query(TruckORM).filter(TruckORM.tractor_no == tractor_no.strip()).first()
        if orm_truck:
            return TruckMapper.to_domain(orm_truck)
        return None
    
    def find_all(self) -> List[Truck]:
        """Get all trucks."""
        if self._session:
            return self._find_all_with_session(self._session)
        else:
            with get_db_session() as session:
                return self._find_all_with_session(session)
    
    def _find_all_with_session(self, session: Session) -> List[Truck]:
        """Internal find all method with session."""
        orm_trucks = session.query(TruckORM).order_by(TruckORM.tractor_no).all()
        return [TruckMapper.to_domain(orm_truck) for orm_truck in orm_trucks]
    
    def update(self, truck: Truck) -> Truck:
        """Update existing truck."""
        if not truck.id:
            raise ValueError("Cannot update truck without ID")
        
        if self._session:
            return self._update_with_session(self._session, truck)
        else:
            with get_db_session() as session:
                return self._update_with_session(session, truck)
    
    def _update_with_session(self, session: Session, truck: Truck) -> Truck:
        """Internal update method with session."""
        try:
            orm_truck = session.query(TruckORM).filter(TruckORM.id == int(truck.id)).first()
            if not orm_truck:
                raise ValueError(f"Трак с ID {truck.id} не найден")
            
            # Update ORM object
            TruckMapper.to_orm(truck, orm_truck)
            session.flush()
            
            return truck
            
        except IntegrityError as e:
            session.rollback()
            if "tractor_no" in str(e):
                raise ValueError(f"Трак с номером '{truck.tractor_no}' уже существует")
            raise ValueError(f"Ошибка обновления трака: {e}")
    
    def delete(self, truck_id: TruckId) -> bool:
        """Delete truck by ID."""
        if self._session:
            return self._delete_with_session(self._session, truck_id)
        else:
            with get_db_session() as session:
                return self._delete_with_session(session, truck_id)
    
    def _delete_with_session(self, session: Session, truck_id: TruckId) -> bool:
        """Internal delete method with session."""
        orm_truck = session.query(TruckORM).filter(TruckORM.id == int(truck_id)).first()
        if not orm_truck:
            return False
        
        # Check for constraints
        monthly_count = session.query(MonthlyRowORM).filter(MonthlyRowORM.truck_id == int(truck_id)).count()
        if monthly_count > 0:
            raise ValueError(
                f"Нельзя удалить трак с ID {truck_id}: у него есть {monthly_count} месячных записей"
            )
        
        session.delete(orm_truck)
        return True
    
    def has_monthly_data(self, truck_id: TruckId) -> bool:
        """Check if truck has monthly data."""
        if self._session:
            return self._has_monthly_data_with_session(self._session, truck_id)
        else:
            with get_db_session() as session:
                return self._has_monthly_data_with_session(session, truck_id)
    
    def _has_monthly_data_with_session(self, session: Session, truck_id: TruckId) -> bool:
        """Internal has monthly data method with session."""
        count = session.query(MonthlyRowORM).filter(MonthlyRowORM.truck_id == int(truck_id)).count()
        return count > 0
    
    def count_monthly_records(self, truck_id: TruckId) -> int:
        """Count monthly records for truck."""
        if self._session:
            return self._count_monthly_records_with_session(self._session, truck_id)
        else:
            with get_db_session() as session:
                return self._count_monthly_records_with_session(session, truck_id)
    
    def _count_monthly_records_with_session(self, session: Session, truck_id: TruckId) -> int:
        """Internal count monthly records method with session."""
        return session.query(MonthlyRowORM).filter(MonthlyRowORM.truck_id == int(truck_id)).count()
