"""
Pydantic схемы для модуля reports.
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import date


class TruckReportResponse(BaseModel):
    """Детальный отчет по траку."""
    truck_id: int
    tractor_no: str
    period: str
    revenue: float
    total_variable_costs: float
    total_fixed_costs: float
    total_all_costs: float
    profit: float
    margin_percent: float
    cost_breakdown: Dict[str, float]
    monthly_data_count: int


class FleetReportResponse(BaseModel):
    """Флотовый отчет."""
    total_trucks: int
    total_revenue: float
    total_variable_costs: float
    total_fixed_costs: float
    total_profit: float
    average_profit_per_truck: float
    average_margin_percent: float
    truck_reports: List[TruckReportResponse]


class PeriodReportResponse(BaseModel):
    """Отчет за период."""
    period: str
    year: int
    month: int
    total_trucks: int
    total_revenue: float
    total_variable_costs: float
    total_fixed_costs: float
    total_profit: float
    truck_reports: List[TruckReportResponse]


class ProfitabilityAnalysis(BaseModel):
    """Анализ прибыльности."""
    truck_id: int
    tractor_no: str
    total_revenue: float
    total_costs: float
    profit: float
    margin_percent: float
    is_profitable: bool
    profitability_grade: str  # A, B, C, D, F


class CostBreakdownItem(BaseModel):
    """Элемент разбивки затрат."""
    category: str
    amount: float
    percentage: float


class DetailedCostBreakdown(BaseModel):
    """Детальная разбивка затрат."""
    truck_id: int
    tractor_no: str
    total_amount: float
    variable_costs: List[CostBreakdownItem]
    fixed_costs: List[CostBreakdownItem]
    common_costs: List[CostBreakdownItem]


class ReportSummary(BaseModel):
    """Сводка отчета."""
    report_type: str
    generated_at: str
    period: Optional[str] = None
    total_records: int
    summary_stats: Dict[str, float]
