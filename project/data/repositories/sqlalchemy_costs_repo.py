"""
SQLAlchemy implementation of CostsRepository.
"""

from typing import Optional
from sqlalchemy.orm import Session
from ...domain.entities.truck import TruckId
from ...domain.entities.costs import FixedCostsTruck, FixedCostsCommon
from ...domain.repositories.costs_repository import CostsRepository
from ..database.database import get_db_session
from ..database.models import FixedCostsTruck as FixedCostsTruckORM, FixedCostsCommon as FixedCostsCommonORM
from .mappers import CostsMapper


class SqlAlchemyCostsRepository(CostsRepository):
    """
    SQLAlchemy implementation of the CostsRepository interface.
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
    
    # Truck-specific fixed costs
    
    def save_truck_costs(self, costs: FixedCostsTruck) -> FixedCostsTruck:
        """Save truck-specific fixed costs."""
        if self._session:
            return self._save_truck_costs_with_session(self._session, costs)
        else:
            with get_db_session() as session:
                return self._save_truck_costs_with_session(session, costs)
    
    def _save_truck_costs_with_session(self, session: Session, costs: FixedCostsTruck) -> FixedCostsTruck:
        """Internal save truck costs method with session."""
        orm_costs = CostsMapper.truck_costs_to_orm(costs)
        session.add(orm_costs)
        session.flush()
        
        return costs
    
    def find_truck_costs(self, truck_id: TruckId) -> Optional[FixedCostsTruck]:
        """Find fixed costs for specific truck."""
        if self._session:
            return self._find_truck_costs_with_session(self._session, truck_id)
        else:
            with get_db_session() as session:
                return self._find_truck_costs_with_session(session, truck_id)
    
    def _find_truck_costs_with_session(self, session: Session, truck_id: TruckId) -> Optional[FixedCostsTruck]:
        """Internal find truck costs method with session."""
        orm_costs = session.query(FixedCostsTruckORM).filter(
            FixedCostsTruckORM.truck_id == int(truck_id)
        ).first()
        
        if orm_costs:
            return CostsMapper.truck_costs_to_domain(orm_costs)
        return None
    
    def update_truck_costs(self, costs: FixedCostsTruck) -> FixedCostsTruck:
        """Update existing truck-specific costs."""
        if not costs.truck_id:
            raise ValueError("Cannot update truck costs without truck_id")
        
        if self._session:
            return self._update_truck_costs_with_session(self._session, costs)
        else:
            with get_db_session() as session:
                return self._update_truck_costs_with_session(session, costs)
    
    def _update_truck_costs_with_session(self, session: Session, costs: FixedCostsTruck) -> FixedCostsTruck:
        """Internal update truck costs method with session."""
        orm_costs = session.query(FixedCostsTruckORM).filter(
            FixedCostsTruckORM.truck_id == int(costs.truck_id)
        ).first()
        
        if not orm_costs:
            # If not found, create new record
            return self._save_truck_costs_with_session(session, costs)
        
        # Update existing record
        CostsMapper.truck_costs_to_orm(costs, orm_costs)
        session.flush()
        
        return costs
    
    def delete_truck_costs(self, truck_id: TruckId) -> bool:
        """Delete truck-specific fixed costs."""
        if self._session:
            return self._delete_truck_costs_with_session(self._session, truck_id)
        else:
            with get_db_session() as session:
                return self._delete_truck_costs_with_session(session, truck_id)
    
    def _delete_truck_costs_with_session(self, session: Session, truck_id: TruckId) -> bool:
        """Internal delete truck costs method with session."""
        orm_costs = session.query(FixedCostsTruckORM).filter(
            FixedCostsTruckORM.truck_id == int(truck_id)
        ).first()
        
        if not orm_costs:
            return False
        
        session.delete(orm_costs)
        return True
    
    # Common fixed costs
    
    def save_common_costs(self, costs: FixedCostsCommon) -> FixedCostsCommon:
        """Save common fixed costs."""
        if self._session:
            return self._save_common_costs_with_session(self._session, costs)
        else:
            with get_db_session() as session:
                return self._save_common_costs_with_session(session, costs)
    
    def _save_common_costs_with_session(self, session: Session, costs: FixedCostsCommon) -> FixedCostsCommon:
        """Internal save common costs method with session."""
        orm_costs = CostsMapper.common_costs_to_orm(costs)
        session.add(orm_costs)
        session.flush()
        
        return costs
    
    def find_common_costs(self) -> Optional[FixedCostsCommon]:
        """Find current common fixed costs."""
        if self._session:
            return self._find_common_costs_with_session(self._session)
        else:
            with get_db_session() as session:
                return self._find_common_costs_with_session(session)
    
    def _find_common_costs_with_session(self, session: Session) -> Optional[FixedCostsCommon]:
        """Internal find common costs method with session."""
        # For now, we assume there's only one common costs record
        # In the future, we could add versioning/dating
        orm_costs = session.query(FixedCostsCommonORM).first()
        
        if orm_costs:
            return CostsMapper.common_costs_to_domain(orm_costs)
        return None
    
    def update_common_costs(self, costs: FixedCostsCommon) -> FixedCostsCommon:
        """Update existing common costs."""
        if self._session:
            return self._update_common_costs_with_session(self._session, costs)
        else:
            with get_db_session() as session:
                return self._update_common_costs_with_session(session, costs)
    
    def _update_common_costs_with_session(self, session: Session, costs: FixedCostsCommon) -> FixedCostsCommon:
        """Internal update common costs method with session."""
        # Find existing record (assume only one for now)
        orm_costs = session.query(FixedCostsCommonORM).first()
        
        if not orm_costs:
            # If not found, create new record
            return self._save_common_costs_with_session(session, costs)
        
        # Update existing record
        CostsMapper.common_costs_to_orm(costs, orm_costs)
        session.flush()
        
        return costs
