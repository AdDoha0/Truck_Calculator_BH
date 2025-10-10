"""
Сервис для управления расходами (UI версия).
"""
from typing import Dict, List, Tuple
from sqlalchemy.orm import Session

from project.models.validation import ValidationService
from project.api.modules.costs.crud import costs_crud
from project.models.database import get_db_session


class CostsService:
    """Сервис для управления расходами (UI версия)."""
    
    def __init__(self):
        self._validation_service = ValidationService()
    
    def get_truck_costs(self, truck_id: int) -> Dict[str, float]:
        """Получить затраты трака."""
        with get_db_session() as db:
            return costs_crud.get_truck_costs(db, truck_id)
    
    def update_truck_costs(self, truck_id: int, cost_updates: Dict[str, float]) -> Dict[str, float]:
        """Обновить затраты трака с валидацией."""
        with get_db_session() as db:
            # Валидация обновлений
            validation_result = self._validation_service.validate_fixed_costs_update(cost_updates)
            if not validation_result.is_valid:
                raise ValueError("; ".join(validation_result.errors))
            
            return costs_crud.update_truck_costs(db, truck_id, cost_updates)
    
    def get_common_costs(self) -> Dict[str, float]:
        """Получить общие затраты."""
        with get_db_session() as db:
            return costs_crud.get_common_costs(db)
    
    def update_common_costs(self, cost_updates: Dict[str, float]) -> Dict[str, float]:
        """Обновить общие затраты с валидацией."""
        with get_db_session() as db:
            # Валидация обновлений
            validation_result = self._validation_service.validate_fixed_costs_update(cost_updates)
            if not validation_result.is_valid:
                raise ValueError("; ".join(validation_result.errors))
            
            return costs_crud.update_common_costs(db, cost_updates)
    
    def calculate_truck_profitability(self, truck_id: int, revenue: float, variable_costs: Dict[str, float]) -> Dict:
        """Рассчитать прибыльность трака."""
        with get_db_session() as db:
            # Получаем фиксированные затраты трака
            truck_costs = costs_crud.get_truck_costs(db, truck_id)
            
            # Получаем общие затраты
            common_costs = costs_crud.get_common_costs(db)
            
            # Рассчитываем переменные затраты
            total_variable = sum(variable_costs.values())
            
            # Рассчитываем фиксированные затраты
            total_fixed = sum(truck_costs.values()) + sum(common_costs.values())
            
            # Общие затраты
            total_all = total_variable + total_fixed
            
            # Прибыль
            profit = revenue - total_all
            
            # Маржа в процентах
            margin_percent = (profit / revenue * 100) if revenue > 0 else 0
            
            return {
                'total_variable': total_variable,
                'total_fixed': total_fixed,
                'total_all': total_all,
                'profit': profit,
                'margin_percent': margin_percent
            }
    
    def get_cost_breakdown_for_truck(self, truck_id: int, variable_costs: Dict[str, float]) -> Dict:
        """Получить детальную разбивку затрат для трака."""
        with get_db_session() as db:
            truck_costs = costs_crud.get_truck_costs(db, truck_id)
            common_costs = costs_crud.get_common_costs(db)
            
            return {
                'variable_costs': variable_costs,
                'truck_fixed_costs': truck_costs,
                'common_fixed_costs': common_costs,
                'total_variable': sum(variable_costs.values()),
                'total_truck_fixed': sum(truck_costs.values()),
                'total_common_fixed': sum(common_costs.values()),
                'total_fixed': sum(truck_costs.values()) + sum(common_costs.values())
            }
    
    def calculate_fleet_summary(self, truck_data: List[Tuple[int, float, Dict[str, float]]]) -> Dict:
        """Рассчитать флотовый отчет."""
        total_revenue = 0.0
        total_variable_costs = 0.0
        total_fixed_costs = 0.0
        
        for truck_id, revenue, variable_costs in truck_data:
            total_revenue += revenue
            total_variable_costs += sum(variable_costs.values())
            
            # Получаем фиксированные затраты для каждого трака
            with get_db_session() as db:
                truck_costs = costs_crud.get_truck_costs(db, truck_id)
                common_costs = costs_crud.get_common_costs(db)
                total_fixed_costs += sum(truck_costs.values()) + sum(common_costs.values())
        
        total_profit = total_revenue - total_variable_costs - total_fixed_costs
        
        return {
            'total_revenue': total_revenue,
            'total_variable_costs': total_variable_costs,
            'total_fixed_costs': total_fixed_costs,
            'total_profit': total_profit
        }
