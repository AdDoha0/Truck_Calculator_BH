"""
CRUD операции для модуля costs.
"""
from typing import Dict
from sqlalchemy.orm import Session

from project.models.database import FixedCostsTruck as FixedCostsTruckORM, FixedCostsCommon as FixedCostsCommonORM


class CostsCRUD:
    """CRUD операции для затрат."""
    
    def get_truck_costs(self, db: Session, truck_id: int) -> Dict[str, float]:
        """Получить затраты трака."""
        costs_orm = db.query(FixedCostsTruckORM).filter_by(truck_id=truck_id).first()
        
        if not costs_orm:
            return {
                'truck_payment': 0.0,
                'trailer_payment': 0.0,
                'physical_damage_insurance_truck': 0.0,
                'physical_damage_insurance_trailer': 0.0,
            }
        
        return {
            'truck_payment': float(costs_orm.truck_payment),
            'trailer_payment': float(costs_orm.trailer_payment),
            'physical_damage_insurance_truck': float(costs_orm.physical_damage_insurance_truck),
            'physical_damage_insurance_trailer': float(costs_orm.physical_damage_insurance_trailer),
        }
    
    def update_truck_costs(self, db: Session, truck_id: int, cost_updates: Dict[str, float]) -> Dict[str, float]:
        """Обновить затраты трака."""
        costs_orm = db.query(FixedCostsTruckORM).filter_by(truck_id=truck_id).first()
        
        if not costs_orm:
            # Создать новую запись
            costs_orm = FixedCostsTruckORM(truck_id=truck_id)
            db.add(costs_orm)
        
        # Обновить значения
        for field, value in cost_updates.items():
            if hasattr(costs_orm, field):
                setattr(costs_orm, field, value)
        
        db.flush()
        
        return {
            'truck_payment': float(costs_orm.truck_payment),
            'trailer_payment': float(costs_orm.trailer_payment),
            'physical_damage_insurance_truck': float(costs_orm.physical_damage_insurance_truck),
            'physical_damage_insurance_trailer': float(costs_orm.physical_damage_insurance_trailer),
        }
    
    def get_common_costs(self, db: Session) -> Dict[str, float]:
        """Получить общие затраты."""
        costs_orm = db.query(FixedCostsCommonORM).first()
        
        if not costs_orm:
            return {
                'ifta': 0.0,
                'insurance': 0.0,
                'eld': 0.0,
                'tablet': 0.0,
                'tolls': 0.0,
            }
        
        return {
            'ifta': float(costs_orm.ifta),
            'insurance': float(costs_orm.insurance),
            'eld': float(costs_orm.eld),
            'tablet': float(costs_orm.tablet),
            'tolls': float(costs_orm.tolls),
        }
    
    def update_common_costs(self, db: Session, cost_updates: Dict[str, float]) -> Dict[str, float]:
        """Обновить общие затраты."""
        costs_orm = db.query(FixedCostsCommonORM).first()
        
        if not costs_orm:
            # Создать новую запись
            costs_orm = FixedCostsCommonORM()
            db.add(costs_orm)
        
        # Обновить значения
        for field, value in cost_updates.items():
            if hasattr(costs_orm, field):
                setattr(costs_orm, field, value)
        
        db.flush()
        
        return {
            'ifta': float(costs_orm.ifta),
            'insurance': float(costs_orm.insurance),
            'eld': float(costs_orm.eld),
            'tablet': float(costs_orm.tablet),
            'tolls': float(costs_orm.tolls),
        }


# Глобальный экземпляр CRUD
costs_crud = CostsCRUD()
