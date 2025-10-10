"""
Сервисы для работы с данными.
"""
from .truck_service import TruckService
from .costs_service import CostsService
from .report_service import ReportService
from .database_service import DatabaseService

__all__ = [
    'TruckService',
    'CostsService', 
    'ReportService',
    'DatabaseService'
]
