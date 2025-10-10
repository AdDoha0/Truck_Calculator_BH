"""
CRUD операции для модуля monthly.
"""
from typing import List, Optional, Dict, Any
from datetime import date
from sqlalchemy.orm import Session

from project.models.database import MonthlyRow as MonthlyRowORM


class MonthlyCRUD:
    """CRUD операции для месячных данных."""
    
    def get_monthly_data_for_truck(self, db: Session, truck_id: int) -> List[Dict[str, Any]]:
        """Получить месячные данные для трака."""
        monthly_rows = db.query(MonthlyRowORM).filter_by(truck_id=truck_id).all()
        
        return [
            {
                'id': row.id,
                'period_month': row.period_month,
                'truck_id': row.truck_id,
                'driver_name': row.driver_name,
                'total_rev': float(row.total_rev),
                'total_miles': row.total_miles,
                'salary': float(row.salary),
                'fuel': float(row.fuel),
                'tolls': float(row.tolls),
            }
            for row in monthly_rows
        ]
    
    def get_monthly_data_by_id(self, db: Session, monthly_id: int) -> Optional[Dict[str, Any]]:
        """Получить месячные данные по ID."""
        row = db.query(MonthlyRowORM).filter_by(id=monthly_id).first()
        
        if not row:
            return None
        
        return {
            'id': row.id,
            'period_month': row.period_month,
            'truck_id': row.truck_id,
            'driver_name': row.driver_name,
            'total_rev': float(row.total_rev),
            'total_miles': row.total_miles,
            'salary': float(row.salary),
            'fuel': float(row.fuel),
            'tolls': float(row.tolls),
        }
    
    def create_monthly_data(self, db: Session, data: Dict[str, Any]) -> Dict[str, Any]:
        """Создать месячные данные."""
        # Проверка уникальности (период + трак)
        existing = db.query(MonthlyRowORM).filter_by(
            period_month=data['period_month'],
            truck_id=data['truck_id']
        ).first()
        
        if existing:
            raise ValueError(
                f"Данные за период {data['period_month']} для трака {data['truck_id']} уже существуют"
            )
        
        monthly_row = MonthlyRowORM(**data)
        db.add(monthly_row)
        db.flush()  # Получаем ID
        
        return {
            'id': monthly_row.id,
            'period_month': monthly_row.period_month,
            'truck_id': monthly_row.truck_id,
            'driver_name': monthly_row.driver_name,
            'total_rev': float(monthly_row.total_rev),
            'total_miles': monthly_row.total_miles,
            'salary': float(monthly_row.salary),
            'fuel': float(monthly_row.fuel),
            'tolls': float(monthly_row.tolls),
        }
    
    def update_monthly_data(self, db: Session, monthly_id: int, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Обновить месячные данные."""
        row = db.query(MonthlyRowORM).filter_by(id=monthly_id).first()
        
        if not row:
            raise ValueError(f"Месячные данные с ID {monthly_id} не найдены")
        
        # Обновить поля
        for field, value in updates.items():
            if hasattr(row, field):
                setattr(row, field, value)
        
        db.flush()
        
        return {
            'id': row.id,
            'period_month': row.period_month,
            'truck_id': row.truck_id,
            'driver_name': row.driver_name,
            'total_rev': float(row.total_rev),
            'total_miles': row.total_miles,
            'salary': float(row.salary),
            'fuel': float(row.fuel),
            'tolls': float(row.tolls),
        }
    
    def delete_monthly_data(self, db: Session, monthly_id: int) -> bool:
        """Удалить месячные данные."""
        row = db.query(MonthlyRowORM).filter_by(id=monthly_id).first()
        
        if not row:
            return False
        
        db.delete(row)
        return True
    
    def get_available_periods(self, db: Session) -> List[str]:
        """Получить доступные периоды."""
        periods = db.query(MonthlyRowORM.period_month).distinct().all()
        return [str(period[0]) for period in periods]
    
    def get_all_monthly_data(self, db: Session) -> List[Dict[str, Any]]:
        """Получить все месячные данные."""
        monthly_rows = db.query(MonthlyRowORM).all()
        
        return [
            {
                'id': row.id,
                'period_month': row.period_month,
                'truck_id': row.truck_id,
                'driver_name': row.driver_name,
                'total_rev': float(row.total_rev),
                'total_miles': row.total_miles,
                'salary': float(row.salary),
                'fuel': float(row.fuel),
                'tolls': float(row.tolls),
            }
            for row in monthly_rows
        ]


# Глобальный экземпляр CRUD
monthly_crud = MonthlyCRUD()
