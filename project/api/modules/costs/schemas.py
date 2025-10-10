"""
Pydantic схемы для модуля costs.
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict


class TruckCostsResponse(BaseModel):
    """Схема ответа с затратами трака."""
    truck_id: int
    truck_payment: float
    trailer_payment: float
    physical_damage_insurance_truck: float
    physical_damage_insurance_trailer: float


class TruckCostsUpdate(BaseModel):
    """Схема для обновления затрат трака."""
    truck_payment: Optional[float] = Field(None, ge=0, description="Платеж за трак")
    trailer_payment: Optional[float] = Field(None, ge=0, description="Платеж за прицеп")
    physical_damage_insurance_truck: Optional[float] = Field(
        None, ge=0, description="Страховка трака"
    )
    physical_damage_insurance_trailer: Optional[float] = Field(
        None, ge=0, description="Страховка прицепа"
    )


class CommonCostsResponse(BaseModel):
    """Схема ответа с общими затратами."""
    ifta: float
    insurance: float
    eld: float
    tablet: float
    tolls: float


class CommonCostsUpdate(BaseModel):
    """Схема для обновления общих затрат."""
    ifta: Optional[float] = Field(None, ge=0, description="IFTA")
    insurance: Optional[float] = Field(None, ge=0, description="Общая страховка")
    eld: Optional[float] = Field(None, ge=0, description="ELD устройство")
    tablet: Optional[float] = Field(None, ge=0, description="Планшет")
    tolls: Optional[float] = Field(None, ge=0, description="Базовые пошлины")


class VariableCostsData(BaseModel):
    """Переменные затраты для расчета."""
    salary: float = Field(ge=0, description="Зарплата")
    fuel: float = Field(ge=0, description="Топливо")
    tolls: float = Field(ge=0, description="Пошлины")
    repair: float = Field(ge=0, description="Ремонт")


class CostCalculationRequest(BaseModel):
    """Запрос на расчет затрат и прибыли."""
    truck_id: int = Field(..., description="ID трака")
    revenue: float = Field(ge=0, description="Доход")
    variable_costs: VariableCostsData = Field(..., description="Переменные затраты")


class CostCalculationResponse(BaseModel):
    """Результат расчета затрат и прибыли."""
    truck_id: int
    revenue: float
    total_variable_costs: float
    total_fixed_costs: float
    total_all_costs: float
    profit: float
    margin_percent: float
    cost_breakdown: Dict[str, float]


class FleetSummaryRequest(BaseModel):
    """Запрос на расчет флотового отчета."""
    truck_data: list[tuple[int, float, Dict[str, float]]] = Field(
        ..., description="Данные по тракам (truck_id, revenue, variable_costs)"
    )


class FleetSummaryResponse(BaseModel):
    """Результат флотового расчета."""
    total_revenue: float
    total_variable_costs: float
    total_fixed_costs: float
    total_profit: float
    truck_count: int
