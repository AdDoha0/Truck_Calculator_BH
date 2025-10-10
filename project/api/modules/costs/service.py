"""
Бизнес-логика для модуля costs.
"""
from typing import Dict, List, Tuple
from sqlalchemy.orm import Session

from project.models.validation import ValidationService
from project.models.entities import Money, VariableCosts, FixedCostsTruck, FixedCostsCommon, TotalCosts
from .crud import costs_crud


class CostsAPIService:
    """API сервис для управления затратами."""
    
    def __init__(self):
        self._validation_service = ValidationService()
    
    def get_truck_costs(self, db: Session, truck_id: int) -> Dict[str, float]:
        """Получить затраты трака."""
        return costs_crud.get_truck_costs(db, truck_id)
    
    def update_truck_costs(self, db: Session, truck_id: int, cost_updates: Dict[str, float]) -> Dict[str, float]:
        """Обновить затраты трака с валидацией."""
        # Валидация обновлений
        validation_result = self._validation_service.validate_fixed_costs_update(cost_updates)
        if not validation_result.is_valid:
            raise ValueError("; ".join(validation_result.errors))
        
        return costs_crud.update_truck_costs(db, truck_id, cost_updates)
    
    def get_common_costs(self, db: Session) -> Dict[str, float]:
        """Получить общие затраты."""
        return costs_crud.get_common_costs(db)
    
    def update_common_costs(self, db: Session, cost_updates: Dict[str, float]) -> Dict[str, float]:
        """Обновить общие затраты с валидацией."""
        # Валидация обновлений
        validation_result = self._validation_service.validate_fixed_costs_update(cost_updates)
        if not validation_result.is_valid:
            raise ValueError("; ".join(validation_result.errors))
        
        return costs_crud.update_common_costs(db, cost_updates)
    
    def calculate_costs(self, db: Session, truck_id: int, revenue: float, variable_costs: Dict[str, float]) -> Dict:
        """Рассчитать затраты и прибыль для трака."""
        # Используем существующий сервис для расчетов
        costs_summary = self._costs_service.calculate_truck_profitability(
            truck_id, revenue, variable_costs
        )
        
        # Получаем детальную разбивку затрат
        cost_breakdown = self._costs_service.get_cost_breakdown_for_truck(truck_id, variable_costs)
        
        return {
            "truck_id": truck_id,
            "revenue": revenue,
            "total_variable_costs": costs_summary.total_variable,
            "total_fixed_costs": costs_summary.total_fixed,
            "total_all_costs": costs_summary.total_all,
            "profit": costs_summary.profit,
            "margin_percent": costs_summary.margin_percent,
            "cost_breakdown": cost_breakdown
        }
    
    def calculate_fleet_summary(self, db: Session, truck_data: List[Tuple[int, float, Dict[str, float]]]) -> Dict:
        """Рассчитать флотовый отчет."""
        # Используем существующий сервис
        fleet_summary = self._costs_service.calculate_fleet_summary(truck_data)
        
        return {
            "total_revenue": fleet_summary['total_revenue'],
            "total_variable_costs": fleet_summary['total_variable_costs'],
            "total_fixed_costs": fleet_summary['total_fixed_costs'],
            "total_profit": fleet_summary['total_profit'],
            "truck_count": len(truck_data)
        }
    
    def get_common_costs_impact_per_truck(self, db: Session) -> float:
        """Получить влияние общих затрат на каждый трак."""
        common_costs = costs_crud.get_common_costs(db)
        return sum(common_costs.values())


# Глобальный экземпляр сервиса
costs_api_service = CostsAPIService()
