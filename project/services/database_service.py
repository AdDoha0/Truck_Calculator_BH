"""
Сервис для работы с базой данных (UI версия).
"""
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session

from project.models.database import get_db_session, MonthlyRow as MonthlyRowORM


class DatabaseService:
    """Сервис для работы с базой данных (UI версия)."""
    
    def __init__(self):
        pass
    
    def get_monthly_data_for_truck(self, truck_id: int) -> List[Dict[str, Any]]:
        """Получить месячные данные для трака."""
        with get_db_session() as db:
            monthly_rows = db.query(MonthlyRowORM).filter_by(truck_id=truck_id).all()
            
            return [
                {
                    'id': row.id,
                    'truck_id': row.truck_id,
                    'period_month': row.period_month.isoformat() if row.period_month else None,
                    'driver_name': row.driver_name,
                    'salary': float(row.salary) if row.salary else 0.0,
                    'fuel': float(row.fuel) if row.fuel else 0.0,
                    'tolls': float(row.tolls) if row.tolls else 0.0,
                    'total_rev': float(row.total_rev) if row.total_rev else 0.0,
                    'total_miles': float(row.total_miles) if row.total_miles else 0.0,
                }
                for row in monthly_rows
            ]
    
    def get_all_monthly_data(self) -> List[Dict[str, Any]]:
        """Получить все месячные данные."""
        with get_db_session() as db:
            monthly_rows = db.query(MonthlyRowORM).all()
            
            return [
                {
                    'id': row.id,
                    'truck_id': row.truck_id,
                    'period_month': row.period_month.isoformat() if row.period_month else None,
                    'driver_name': row.driver_name,
                    'salary': float(row.salary) if row.salary else 0.0,
                    'fuel': float(row.fuel) if row.fuel else 0.0,
                    'tolls': float(row.tolls) if row.tolls else 0.0,
                    'total_rev': float(row.total_rev) if row.total_rev else 0.0,
                    'total_miles': float(row.total_miles) if row.total_miles else 0.0,
                }
                for row in monthly_rows
            ]
    
    def get_monthly_data_by_period(self, period: str) -> List[Dict[str, Any]]:
        """Получить месячные данные за период."""
        from datetime import datetime
        
        try:
            period_date = datetime.fromisoformat(period).date()
        except ValueError:
            raise ValueError(f"Неверный формат периода: {period}. Используйте YYYY-MM-DD")
        
        with get_db_session() as db:
            monthly_rows = db.query(MonthlyRowORM).filter_by(period_month=period_date).all()
            
            return [
                {
                    'id': row.id,
                    'truck_id': row.truck_id,
                    'period_month': row.period_month.isoformat() if row.period_month else None,
                    'driver_name': row.driver_name,
                    'salary': float(row.salary) if row.salary else 0.0,
                    'fuel': float(row.fuel) if row.fuel else 0.0,
                    'tolls': float(row.tolls) if row.tolls else 0.0,
                    'total_rev': float(row.total_rev) if row.total_rev else 0.0,
                    'total_miles': float(row.total_miles) if row.total_miles else 0.0,
                }
                for row in monthly_rows
            ]
    
    def get_available_periods(self) -> List[str]:
        """Получить доступные периоды."""
        with get_db_session() as db:
            periods = db.query(MonthlyRowORM.period_month).distinct().all()
            return [period[0].isoformat() for period in periods if period[0]]
    
    def get_truck_count(self) -> int:
        """Получить количество траков."""
        with get_db_session() as db:
            from project.models.database import Truck as TruckORM
            return db.query(TruckORM).count()
    
    def get_monthly_data_count(self) -> int:
        """Получить количество месячных записей."""
        with get_db_session() as db:
            return db.query(MonthlyRowORM).count()
    
    def get_monthly_data_count_for_truck(self, truck_id: int) -> int:
        """Получить количество месячных записей для трака."""
        with get_db_session() as db:
            return db.query(MonthlyRowORM).filter_by(truck_id=truck_id).count()
