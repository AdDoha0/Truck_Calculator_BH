"""
Simplified UI adapter for Streamlit interface.
Replaces ui.adapters.streamlit_adapter with direct service usage.
"""
import streamlit as st
from typing import List, Dict, Any, Optional

from project.services import TruckService, CostsService, ReportService, DatabaseService
from project.models import init_db, ensure_db_exists


class UIAdapter:
    """
    Simplified adapter for Streamlit UI.
    
    Provides user-friendly interface to business services with
    Streamlit-specific error handling and messaging.
    """
    
    def __init__(self):
        """Initialize adapter with services."""
        self._truck_service = TruckService()
        self._costs_service = CostsService()
        self._report_service = ReportService()
        self._db_service = DatabaseService()
    
    # ========== Database Initialization ==========
    
    def init_database(self) -> None:
        """Initialize database with error handling."""
        try:
            ensure_db_exists()
        except Exception as e:
            st.error(f"❌ Ошибка инициализации базы данных: {e}")
            st.stop()
    
    # ========== Truck Management ==========
    
    def create_truck(self, tractor_no: str) -> bool:
        """
        Create truck with UI feedback.
        
        Args:
            tractor_no: Tractor number to create
            
        Returns:
            True if successful, False otherwise
        """
        try:
            truck_info = self._truck_service.create_truck(tractor_no)
            st.success(f"✅ Трак '{truck_info.tractor_no}' успешно создан!")
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
            trucks = self._truck_service.get_all_trucks()
            
            return [
                {
                    'id': truck.id or 0,
                    'tractor_no': truck.tractor_no,
                    'monthly_rows_count': truck.monthly_count,
                    'fixed_costs_count': 1 if truck.has_fixed_costs else 0,
                }
                for truck in trucks
            ]
        except Exception as e:
            st.error(f"❌ Ошибка загрузки траков: {e}")
            return []
    
    def get_truck_by_id(self, truck_id: int) -> Optional[Dict[str, Any]]:
        """
        Get truck by ID formatted for Streamlit.
        
        Args:
            truck_id: ID of truck to get
            
        Returns:
            Dictionary with truck data or None if not found
        """
        try:
            truck_info = self._truck_service.get_truck_by_id(truck_id)
            if not truck_info:
                return None
            
            return {
                'id': truck_info.id,
                'tractor_no': truck_info.tractor_no,
                'monthly_rows_count': truck_info.monthly_count,
                'fixed_costs_count': 1 if truck_info.has_fixed_costs else 0,
            }
        except Exception as e:
            st.error(f"❌ Ошибка загрузки трака: {e}")
            return None
    
    def update_truck(self, truck_id: int, new_tractor_no: str) -> bool:
        """
        Update truck with UI feedback.
        
        Args:
            truck_id: ID of truck to update
            new_tractor_no: New tractor number
            
        Returns:
            True if successful, False otherwise
        """
        try:
            truck_info = self._truck_service.update_truck(truck_id, new_tractor_no)
            st.success(f"✅ Трак обновлен: '{truck_info.tractor_no}'")
            return True
        except ValueError as e:
            st.error(f"❌ Ошибка обновления трака: {e}")
            return False
        except Exception as e:
            st.error(f"❌ Неожиданная ошибка: {e}")
            return False
    
    def delete_truck(self, truck_id: int) -> bool:
        """
        Delete truck with UI feedback.
        
        Args:
            truck_id: ID of truck to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            success = self._truck_service.delete_truck(truck_id)
            if success:
                st.success("✅ Трак успешно удален!")
                return True
            else:
                st.warning("⚠️ Трак не найден")
                return False
        except ValueError as e:
            st.error(f"❌ Ошибка удаления трака: {e}")
            return False
        except Exception as e:
            st.error(f"❌ Неожиданная ошибка: {e}")
            return False
    
    # ========== Costs Management ==========
    
    def get_truck_costs(self, truck_id: int) -> Dict[str, float]:
        """
        Get truck-specific fixed costs.
        
        Args:
            truck_id: ID of truck
            
        Returns:
            Dictionary with cost fields and values
        """
        try:
            return self._costs_service.get_truck_costs(truck_id)
        except Exception as e:
            st.error(f"❌ Ошибка загрузки расходов трака: {e}")
            return {
                'truck_payment': 0.0,
                'trailer_payment': 0.0,
                'physical_damage_insurance_truck': 0.0,
                'physical_damage_insurance_trailer': 0.0,
            }
    
    def update_truck_costs(self, truck_id: int, cost_updates: Dict[str, float]) -> bool:
        """
        Update truck-specific fixed costs with UI feedback.
        
        Args:
            truck_id: ID of truck
            cost_updates: Dictionary of field -> value updates
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self._costs_service.update_truck_costs(truck_id, cost_updates)
            st.success(f"✅ Расходы трака ID {truck_id} обновлены!")
            return True
        except ValueError as e:
            st.error(f"❌ Ошибка валидации: {e}")
            return False
        except Exception as e:
            st.error(f"❌ Ошибка обновления расходов: {e}")
            return False
    
    def get_common_costs(self) -> Dict[str, float]:
        """
        Get common fixed costs.
        
        Returns:
            Dictionary with cost fields and values
        """
        try:
            return self._costs_service.get_common_costs()
        except Exception as e:
            st.error(f"❌ Ошибка загрузки общих расходов: {e}")
            return {
                'ifta': 0.0,
                'insurance': 0.0,
                'eld': 0.0,
                'tablet': 0.0,
                'tolls': 0.0,
            }
    
    def update_common_costs(self, cost_updates: Dict[str, float]) -> bool:
        """
        Update common fixed costs with UI feedback.
        
        Args:
            cost_updates: Dictionary of field -> value updates
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self._costs_service.update_common_costs(cost_updates)
            st.success("✅ Общие расходы обновлены!")
            return True
        except ValueError as e:
            st.error(f"❌ Ошибка валидации: {e}")
            return False
        except Exception as e:
            st.error(f"❌ Ошибка обновления расходов: {e}")
            return False
    
    # ========== Reporting ==========
    
    def get_trucks_full_data(self, period: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get full truck data for reporting with cost calculations.
        
        Args:
            period: Optional period filter
            
        Returns:
            List of truck records with calculated costs and profits
        """
        try:
            # Get all trucks
            trucks = self._truck_service.get_all_trucks()
            result = []
            
            for truck in trucks:
                if not truck.id:
                    continue
                
                # Get truck costs
                truck_costs = self._costs_service.get_truck_costs(truck.id)
                
                # Get monthly data for truck (simplified)
                monthly_data = self._db_service.get_monthly_data_for_truck(truck.id)
                
                # If no monthly data, create a default record
                if not monthly_data:
                    # Create default record with zero values
                    monthly_data = [{
                        'salary': 0.0,
                        'fuel': 0.0,
                        'tolls': 0.0,
                        'total_rev': 0.0,
                        'total_miles': 0.0,
                        'driver_name': ''
                    }]
                
                for monthly_record in monthly_data:
                    # Calculate profitability
                    profitability = self._costs_service.calculate_truck_profitability(
                        truck.id, monthly_record['total_rev'], {
                            'salary': monthly_record['salary'],
                            'fuel': monthly_record['fuel'],
                            'tolls': monthly_record['tolls'],
                            'repair': 0,  # Not in monthly data
                        }
                    )
                    
                    # Calculate per-mile metrics
                    miles = monthly_record['total_miles']
                    rpm = monthly_record['total_rev'] / miles if miles > 0 else 0
                    cpm = profitability.total_all / miles if miles > 0 else 0
                    
                    result.append({
                        'id': truck.id,
                        'tractor_no': truck.tractor_no,
                        'driver_name': monthly_record.get('driver_name', ''),
                        'total_rev': monthly_record['total_rev'],
                        'total_miles': miles,
                        'salary': monthly_record['salary'],
                        'fuel': monthly_record['fuel'],
                        'tolls': monthly_record['tolls'],
                        'repair': 0,
                        # Fixed costs from truck_costs
                        'truck_payment': truck_costs.get('truck_payment', 0.0),
                        'trailer_payment': truck_costs.get('trailer_payment', 0.0),
                        'truck_insurance': truck_costs.get('physical_damage_insurance_truck', 0.0),
                        'trailer_insurance': truck_costs.get('physical_damage_insurance_trailer', 0.0),
                        # Calculated totals
                        'total_variable': profitability.total_variable,
                        'total_fixed': profitability.total_fixed,
                        'gross_profit': profitability.profit,
                        'rpm': rpm,
                        'cpm': cpm,
                        # Additional metadata
                        'has_monthly_data': len(monthly_data) > 0 and monthly_record['total_rev'] > 0,
                    })
            
            return result
        except Exception as e:
            st.error(f"❌ Ошибка загрузки данных для отчета: {e}")
            return []
    
    def get_available_periods(self) -> List[str]:
        """
        Get available periods from monthly data.
        
        Returns:
            List of period strings
        """
        try:
            return self._report_service.get_available_periods()
        except Exception as e:
            st.error(f"❌ Ошибка загрузки периодов: {e}")
            return []


# ========== Global Adapter Instance ==========

_adapter_instance = None

def get_adapter() -> UIAdapter:
    """
    Get singleton adapter instance.
    
    Returns:
        UIAdapter instance
    """
    global _adapter_instance
    if _adapter_instance is None:
        _adapter_instance = UIAdapter()
    return _adapter_instance
