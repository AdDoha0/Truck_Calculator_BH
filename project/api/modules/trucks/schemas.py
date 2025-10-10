"""
Pydantic схемы для модуля trucks.
"""
from pydantic import BaseModel, Field
from typing import Optional


class TruckCreate(BaseModel):
    """Схема для создания трака."""
    tractor_no: str = Field(
        ..., 
        min_length=2, 
        max_length=20,
        description="Номер трактора"
    )


class TruckUpdate(BaseModel):
    """Схема для обновления трака."""
    tractor_no: str = Field(
        ..., 
        min_length=2, 
        max_length=20,
        description="Новый номер трактора"
    )


class TruckResponse(BaseModel):
    """Схема ответа с данными трака."""
    id: int
    tractor_no: str
    monthly_count: int = 0
    has_fixed_costs: bool = False
    
    class Config:
        from_attributes = True


class TruckListResponse(BaseModel):
    """Схема ответа со списком траков."""
    trucks: list[TruckResponse]
    total: int
