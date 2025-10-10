"""
Streamlit adapter - handles UI-specific concerns.
"""

import streamlit as st
from typing import List, Dict, Any, Optional
from decimal import Decimal
import sys
import os

# Добавляем корневую директорию проекта в Python path
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from project.application.use_cases.truck_management import TruckManagementUseCase
from project.application.use_cases.costs_management import CostsManagementUseCase
from project.application.use_cases.reporting import ReportingUseCase
from project.application.dto.truck_dto import CreateTruckRequest, UpdateTruckRequest, TruckDto
from project.application.dto.costs_dto import UpdateTruckCostsRequest, UpdateCommonCostsRequest
from project.data.repositories.sqlalchemy_truck_repo import SqlAlchemyTruckRepository
from project.data.repositories.sqlalchemy_costs_repo import SqlAlchemyCostsRepository
from project.domain.entities.truck import TruckId


class StreamlitAdapter:
    """
    Adapter that coordinates between Streamlit UI and application use cases.
    
    This class handles:
    - Dependency injection setup
    - Error handling with user-friendly messages
    - Data format conversion between UI and domain
    - Streamlit-specific display logic
    """
    
    def __init__(self):
        """Initialize adapter with repositories and use cases."""
        # Repository instances
        self._truck_repo = SqlAlchemyTruckRepository()
        self._costs_repo = SqlAlchemyCostsRepository()
        
        # Use case instances
        self._truck_use_case = TruckManagementUseCase(self._truck_repo, self._costs_repo)
        self._costs_use_case = CostsManagementUseCase(self._costs_repo)
        self._reporting_use_case = ReportingUseCase(self._costs_repo)
    
    # Truck management methods
    
    def create_truck(self, tractor_no: str) -> bool:
        """
        Create a new truck with Streamlit error handling.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            request = CreateTruckRequest(tractor_no=tractor_no)
            truck_dto = self._truck_use_case.create_truck(request)
            st.success(f"✅ Трак '{truck_dto.tractor_no}' успешно создан!")
            return True
            
        except ValueError as e:
            st.error(f"❌ Ошибка создания трака: {e}")
            return False
        except Exception as e:
            st.error(f"❌ Неожиданная ошибка: {e}")
            return False
    
    def get_all_trucks(self) -> List[Dict[str, Any]]:
        """
        Get all trucks formatted for Streamlit display.
        
        Returns:
            List of dictionaries suitable for st.dataframe()
        """
        try:
            trucks_dto = self._truck_use_case.get_all_trucks()
            
            return [
                {
                    'id': int(truck.id) if truck.id else 0,
                    'tractor_no': truck.tractor_no,
                    'monthly_rows_count': truck.monthly_rows_count or 0,
                    'fixed_costs_count': truck.fixed_costs_count or 0,
                }
                for truck in trucks_dto
            ]
            
        except Exception as e:
            st.error(f"❌ Ошибка загрузки траков: {e}")
            return []
    
    def get_truck_by_id(self, truck_id: int) -> Optional[Dict[str, Any]]:
        """
        Get truck by ID formatted for Streamlit.
        
        Returns:
            Dictionary with truck data or None if not found
        """
        try:
            truck_dto = self._truck_use_case.get_truck(TruckId(truck_id))
            
            if not truck_dto:
                return None
            
            return {
                'id': int(truck_dto.id) if truck_dto.id else 0,
                'tractor_no': truck_dto.tractor_no,
                'monthly_rows_count': truck_dto.monthly_rows_count or 0,
                'fixed_costs_count': truck_dto.fixed_costs_count or 0,
            }
            
        except Exception as e:
            st.error(f"❌ Ошибка загрузки трака: {e}")
            return None
    
    def update_truck(self, truck_id: int, new_tractor_no: str) -> bool:
        """
        Update truck with Streamlit error handling.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            request = UpdateTruckRequest(
                truck_id=TruckId(truck_id),
                tractor_no=new_tractor_no
            )
            truck_dto = self._truck_use_case.update_truck(request)
            st.success(f"✅ Трак обновлен: '{truck_dto.tractor_no}'")
            return True
            
        except ValueError as e:
            st.error(f"❌ Ошибка обновления трака: {e}")
            return False
        except Exception as e:
            st.error(f"❌ Неожиданная ошибка: {e}")
            return False
    
    def delete_truck(self, truck_id: int) -> bool:
        """
        Delete truck with Streamlit error handling.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            success = self._truck_use_case.delete_truck(TruckId(truck_id))
            
            if success:
                st.success("✅ Трак успешно удален!")
                return True
            else:
                st.warning("⚠️ Трак не найден")
                return False
                
        except ValueError as e:
            st.error(f"❌ Нельзя удалить трак: {e}")
            return False
        except Exception as e:
            st.error(f"❌ Неожиданная ошибка: {e}")
            return False
    
    # Costs management methods
    
    def get_truck_costs(self, truck_id: int) -> Dict[str, float]:
        """
        Get truck-specific costs formatted for Streamlit forms.
        
        Returns:
            Dictionary with cost values as floats
        """
        try:
            costs_dto = self._costs_use_case.get_truck_costs(TruckId(truck_id))
            
            return {
                'truck_payment': float(costs_dto.truck_payment),
                'trailer_payment': float(costs_dto.trailer_payment),
                'physical_damage_insurance_truck': float(costs_dto.physical_damage_insurance_truck),
                'physical_damage_insurance_trailer': float(costs_dto.physical_damage_insurance_trailer),
            }
            
        except Exception as e:
            st.error(f"❌ Ошибка загрузки расходов трака: {e}")
            return {
                'truck_payment': 0.0,
                'trailer_payment': 0.0,
                'physical_damage_insurance_truck': 0.0,
                'physical_damage_insurance_trailer': 0.0,
            }
    
    def update_truck_costs(self, truck_id: int, **cost_updates) -> bool:
        """
        Update truck-specific costs.
        
        Args:
            truck_id: ID of the truck
            **cost_updates: Keyword arguments with cost field updates
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Convert to Decimal and filter None values
            decimal_updates = {}
            for key, value in cost_updates.items():
                if value is not None:
                    decimal_updates[key] = Decimal(str(value))
            
            request = UpdateTruckCostsRequest(
                truck_id=TruckId(truck_id),
                **decimal_updates
            )
            
            costs_dto = self._costs_use_case.update_truck_costs(request)
            st.success(f"✅ Расходы трака обновлены (общая сумма: ${costs_dto.total_amount():,.2f})")
            return True
            
        except ValueError as e:
            st.error(f"❌ Ошибка обновления расходов: {e}")
            return False
        except Exception as e:
            st.error(f"❌ Неожиданная ошибка: {e}")
            return False
    
    def get_common_costs(self) -> Dict[str, float]:
        """
        Get common costs formatted for Streamlit forms.
        
        Returns:
            Dictionary with cost values as floats
        """
        try:
            costs_dto = self._costs_use_case.get_common_costs()
            
            return {
                'ifta': float(costs_dto.ifta),
                'insurance': float(costs_dto.insurance),
                'eld': float(costs_dto.eld),
                'tablet': float(costs_dto.tablet),
                'tolls': float(costs_dto.tolls),
            }
            
        except Exception as e:
            st.error(f"❌ Ошибка загрузки общих расходов: {e}")
            return {
                'ifta': 0.0,
                'insurance': 0.0,
                'eld': 0.0,
                'tablet': 0.0,
                'tolls': 0.0,
            }
    
    def update_common_costs(self, **cost_updates) -> bool:
        """
        Update common costs.
        
        Args:
            **cost_updates: Keyword arguments with cost field updates
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Convert to Decimal and filter None values
            decimal_updates = {}
            for key, value in cost_updates.items():
                if value is not None:
                    decimal_updates[key] = Decimal(str(value))
            
            request = UpdateCommonCostsRequest(**decimal_updates)
            
            costs_dto = self._costs_use_case.update_common_costs(request)
            st.success(f"✅ Общие расходы обновлены (общая сумма: ${costs_dto.total_amount():,.2f})")
            return True
            
        except ValueError as e:
            st.error(f"❌ Ошибка обновления общих расходов: {e}")
            return False
        except Exception as e:
            st.error(f"❌ Неожиданная ошибка: {e}")
            return False
    
    # Advanced truck data methods
    
    def get_trucks_with_costs_and_period(self, period_month: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get all trucks with fixed costs and variable costs for a specific period.
        
        Args:
            period_month: Period in format 'YYYY-MM-DD' or None for latest/all
            
        Returns:
            List of dictionaries with complete truck and cost data
        """
        try:
            from project.data.database.database import get_db_session
            from project.data.database.models import Truck as TruckORM, MonthlyRow as MonthlyRowORM, FixedCostsTruck as FixedCostsTruckORM
            from datetime import datetime
            
            result = []
            
            with get_db_session() as session:
                trucks = session.query(TruckORM).all()
                
                for truck in trucks:
                    # Get fixed costs for truck
                    fixed_costs_orm = session.query(FixedCostsTruckORM).filter(
                        FixedCostsTruckORM.truck_id == truck.id
                    ).first()
                    
                    # Get variable costs for period
                    monthly_data = None
                    if period_month:
                        try:
                            period_date = datetime.strptime(period_month, '%Y-%m-%d').date()
                            monthly_data = session.query(MonthlyRowORM).filter(
                                MonthlyRowORM.truck_id == truck.id,
                                MonthlyRowORM.period_month == period_date
                            ).first()
                        except ValueError:
                            pass
                    
                    # Build result dictionary with safe attribute access
                    truck_data = {
                        'id': truck.id,
                        'tractor_no': truck.tractor_no,
                        # Fixed costs
                        'truck_payment': float(fixed_costs_orm.truck_payment) if fixed_costs_orm else 0.0,
                        'trailer_payment': float(fixed_costs_orm.trailer_payment) if fixed_costs_orm else 0.0,
                        'truck_insurance': float(fixed_costs_orm.physical_damage_insurance_truck) if fixed_costs_orm else 0.0,
                        'trailer_insurance': float(fixed_costs_orm.physical_damage_insurance_trailer) if fixed_costs_orm else 0.0,
                        # Variable costs
                        'salary': float(monthly_data.salary) if monthly_data else 0.0,
                        'fuel': float(monthly_data.fuel) if monthly_data else 0.0,
                        'tolls': float(monthly_data.tolls) if monthly_data else 0.0,
                        # Metadata
                        'has_monthly_data': monthly_data is not None,
                        'monthly_row_id': monthly_data.id if monthly_data else None,
                    }
                    
                    result.append(truck_data)
            
            return result
            
        except Exception as e:
            st.error(f"❌ Ошибка загрузки данных траков: {e}")
            return []
    
    def update_truck_costs_from_table(self, truck_id: int, **cost_updates) -> bool:
        """
        Update truck-specific fixed costs from table editing.
        
        Args:
            truck_id: ID of the truck
            **cost_updates: Cost fields to update (truck_payment, trailer_payment, etc.)
            
        Returns:
            True if successful, False otherwise
        """
        # Reuse existing update_truck_costs method
        return self.update_truck_costs(truck_id, **cost_updates)
    
    def update_variable_costs(self, truck_id: int, period_month: str, **cost_updates) -> bool:
        """
        Update variable costs for a specific truck and period.
        
        Args:
            truck_id: ID of the truck
            period_month: Period in format 'YYYY-MM-DD'
            **cost_updates: Variable cost fields to update (salary, fuel, tolls, repair)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            from project.data.database.database import get_db_session
            from project.data.database.models import MonthlyRow as MonthlyRowORM
            from datetime import datetime
            
            period_date = datetime.strptime(period_month, '%Y-%m-%d').date()
            
            with get_db_session() as session:
                # Find existing monthly row
                monthly_row = session.query(MonthlyRowORM).filter(
                    MonthlyRowORM.truck_id == truck_id,
                    MonthlyRowORM.period_month == period_date
                ).first()
                
                if not monthly_row:
                    # Create new monthly row if not exists
                    monthly_row = MonthlyRowORM(
                        truck_id=truck_id,
                        period_month=period_date,
                        total_rev=0,
                        total_miles=0,
                        salary=0,
                        fuel=0,
                        tolls=0
                    )
                    session.add(monthly_row)
                
                # Update fields
                valid_fields = {'salary', 'fuel', 'tolls'}
                for field, value in cost_updates.items():
                    if field in valid_fields and value is not None:
                        setattr(monthly_row, field, float(value))
                
                session.flush()
                
            st.success(f"✅ Переменные расходы обновлены для трака ID {truck_id}")
            return True
            
        except Exception as e:
            st.error(f"❌ Ошибка обновления переменных расходов: {e}")
            return False
    
    def get_available_periods(self) -> List[str]:
        """
        Get list of available periods from monthly data.
        
        Returns:
            List of period strings in format 'YYYY-MM-DD'
        """
        try:
            from project.data.database.database import get_db_session
            from project.data.database.models import MonthlyRow as MonthlyRowORM
            from sqlalchemy import distinct
            
            with get_db_session() as session:
                periods = session.query(distinct(MonthlyRowORM.period_month))\
                    .order_by(MonthlyRowORM.period_month.desc())\
                    .all()
                
                return [str(period[0]) for period in periods]
            
        except Exception as e:
            st.error(f"❌ Ошибка загрузки периодов: {e}")
            return []
    
    # Database initialization
    
    @staticmethod
    def init_database():
        """Initialize database tables."""
        try:
            from project.data.database.database import init_db
            init_db()
            
        except Exception as e:
            st.error(f"❌ Ошибка инициализации базы данных: {e}")
            st.stop()


# Global adapter instance for use across UI modules
_adapter_instance = None

def get_adapter() -> StreamlitAdapter:
    """
    Get singleton adapter instance.
    
    This ensures we reuse the same repositories and use cases
    across different UI components.
    """
    global _adapter_instance
    if _adapter_instance is None:
        _adapter_instance = StreamlitAdapter()
    return _adapter_instance
