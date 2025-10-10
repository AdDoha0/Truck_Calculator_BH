"""
Бизнес-логика для модуля monthly.
"""
from typing import List, Dict, Any, Optional
from datetime import date
import pandas as pd
from sqlalchemy.orm import Session

from project.models.validation import ValidationService
from .crud import monthly_crud


class MonthlyAPIService:
    """API сервис для месячных данных."""
    
    def __init__(self):
        self._validation_service = ValidationService()
    
    def get_monthly_data_for_truck(self, db: Session, truck_id: int) -> List[Dict[str, Any]]:
        """Получить месячные данные для трака."""
        return monthly_crud.get_monthly_data_for_truck(db, truck_id)
    
    def get_monthly_data_by_id(self, db: Session, monthly_id: int) -> Optional[Dict[str, Any]]:
        """Получить месячные данные по ID."""
        return monthly_crud.get_monthly_data_by_id(db, monthly_id)
    
    def create_monthly_data(self, db: Session, data: Dict[str, Any]) -> Dict[str, Any]:
        """Создать месячные данные с валидацией."""
        # Валидация данных
        self._validate_monthly_data(data)
        
        return monthly_crud.create_monthly_data(db, data)
    
    def update_monthly_data(self, db: Session, monthly_id: int, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Обновить месячные данные с валидацией."""
        # Валидация обновлений
        if updates:
            self._validate_monthly_data(updates, is_update=True)
        
        return monthly_crud.update_monthly_data(db, monthly_id, updates)
    
    def delete_monthly_data(self, db: Session, monthly_id: int) -> bool:
        """Удалить месячные данные."""
        return monthly_crud.delete_monthly_data(db, monthly_id)
    
    def get_available_periods(self, db: Session) -> List[str]:
        """Получить доступные периоды."""
        return monthly_crud.get_available_periods(db)
    
    def get_all_monthly_data(self, db: Session) -> List[Dict[str, Any]]:
        """Получить все месячные данные."""
        return monthly_crud.get_all_monthly_data(db)
    
    def process_uploaded_file(self, db: Session, file_content: bytes, filename: str) -> Dict[str, Any]:
        """Обработать загруженный файл с месячными данными."""
        try:
            # Определить тип файла и загрузить
            if filename.endswith('.xlsx') or filename.endswith('.xls'):
                df = pd.read_excel(file_content)
            elif filename.endswith('.csv'):
                df = pd.read_csv(file_content)
            else:
                raise ValueError("Неподдерживаемый формат файла. Используйте .xlsx, .xls или .csv")
            
            # Валидация структуры файла
            required_columns = ['period_month', 'truck_id', 'total_rev', 'total_miles', 'salary', 'fuel', 'tolls']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                raise ValueError(f"Отсутствуют обязательные колонки: {', '.join(missing_columns)}")
            
            records_processed = 0
            records_created = 0
            errors = []
            
            # Обработка каждой строки
            for index, row in df.iterrows():
                try:
                    records_processed += 1
                    
                    # Подготовка данных
                    data = {
                        'period_month': pd.to_datetime(row['period_month']).date(),
                        'truck_id': int(row['truck_id']),
                        'driver_name': row.get('driver_name'),
                        'total_rev': float(row['total_rev']),
                        'total_miles': int(row['total_miles']),
                        'salary': float(row['salary']),
                        'fuel': float(row['fuel']),
                        'tolls': float(row['tolls']),
                    }
                    
                    # Валидация и создание
                    self._validate_monthly_data(data)
                    monthly_crud.create_monthly_data(db, data)
                    records_created += 1
                    
                except Exception as e:
                    errors.append(f"Строка {index + 1}: {str(e)}")
                    continue
            
            return {
                'message': f"Обработано {records_processed} записей, создано {records_created}",
                'records_processed': records_processed,
                'records_created': records_created,
                'errors': errors
            }
            
        except Exception as e:
            raise ValueError(f"Ошибка обработки файла: {str(e)}")
    
    def _validate_monthly_data(self, data: Dict[str, Any], is_update: bool = False) -> None:
        """Валидация месячных данных."""
        # Проверка обязательных полей
        if not is_update:
            required_fields = ['period_month', 'truck_id', 'total_rev', 'total_miles', 'salary', 'fuel', 'tolls']
            for field in required_fields:
                if field not in data:
                    raise ValueError(f"Отсутствует обязательное поле: {field}")
        
        # Валидация числовых полей
        numeric_fields = ['total_rev', 'total_miles', 'salary', 'fuel', 'tolls']
        for field in numeric_fields:
            if field in data:
                value = data[field]
                if not isinstance(value, (int, float)) or value < 0:
                    raise ValueError(f"Поле {field} должно быть неотрицательным числом")
        
        # Валидация даты
        if 'period_month' in data:
            if not isinstance(data['period_month'], date):
                raise ValueError("period_month должно быть датой")
        
        # Валидация truck_id
        if 'truck_id' in data:
            if not isinstance(data['truck_id'], int) or data['truck_id'] <= 0:
                raise ValueError("truck_id должно быть положительным целым числом")


# Глобальный экземпляр сервиса
monthly_api_service = MonthlyAPIService()
