"""
Pydantic схемы для модуля monthly.
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date


class MonthlyDataResponse(BaseModel):
    """Схема ответа с месячными данными."""
    id: int
    period_month: date
    truck_id: int
    driver_name: Optional[str] = None
    total_rev: float
    total_miles: int
    salary: float
    fuel: float
    tolls: float
    
    class Config:
        from_attributes = True


class MonthlyDataCreate(BaseModel):
    """Схема для создания месячных данных."""
    period_month: date = Field(..., description="Период (месяц/год)")
    truck_id: int = Field(..., description="ID трака")
    driver_name: Optional[str] = Field(None, description="Имя водителя")
    total_rev: float = Field(ge=0, description="Общий доход")
    total_miles: int = Field(ge=0, description="Общий пробег")
    salary: float = Field(ge=0, description="Зарплата")
    fuel: float = Field(ge=0, description="Топливо")
    tolls: float = Field(ge=0, description="Пошлины")


class MonthlyDataUpdate(BaseModel):
    """Схема для обновления месячных данных."""
    driver_name: Optional[str] = Field(None, description="Имя водителя")
    total_rev: Optional[float] = Field(None, ge=0, description="Общий доход")
    total_miles: Optional[int] = Field(None, ge=0, description="Общий пробег")
    salary: Optional[float] = Field(None, ge=0, description="Зарплата")
    fuel: Optional[float] = Field(None, ge=0, description="Топливо")
    tolls: Optional[float] = Field(None, ge=0, description="Пошлины")


class MonthlyDataListResponse(BaseModel):
    """Схема ответа со списком месячных данных."""
    monthly_data: List[MonthlyDataResponse]
    total: int


class PeriodResponse(BaseModel):
    """Схема ответа с периодом."""
    period: str
    year: int
    month: int


class PeriodListResponse(BaseModel):
    """Схема ответа со списком периодов."""
    periods: List[PeriodResponse]
    total: int


class FileUploadResponse(BaseModel):
    """Схема ответа после загрузки файла."""
    message: str
    records_processed: int
    records_created: int
    errors: List[str] = []
