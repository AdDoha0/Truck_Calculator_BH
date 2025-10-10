"""
Роутер для модуля reports.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from ...dependencies import get_db
from .schemas import (
    TruckReportResponse, FleetReportResponse, PeriodReportResponse,
    ProfitabilityAnalysis, ReportSummary
)
from .service import reports_api_service

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/truck/{truck_id}", response_model=TruckReportResponse)
async def get_truck_report(
    truck_id: int, 
    period: str = None,
    db: Session = Depends(get_db)
):
    """Получить детальный отчет по траку."""
    try:
        result = reports_api_service.get_truck_report(db, truck_id, period)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get("/fleet", response_model=FleetReportResponse)
async def get_fleet_report(db: Session = Depends(get_db)):
    """Получить флотовый отчет."""
    result = reports_api_service.get_fleet_report(db)
    return result


@router.get("/period/{period}", response_model=PeriodReportResponse)
async def get_period_report(period: str, db: Session = Depends(get_db)):
    """Получить отчет за период."""
    try:
        result = reports_api_service.get_period_report(db, period)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/profitability", response_model=List[ProfitabilityAnalysis])
async def get_profitability_analysis(db: Session = Depends(get_db)):
    """Получить анализ прибыльности всех траков."""
    result = reports_api_service.get_profitability_analysis(db)
    return result


@router.get("/summary", response_model=ReportSummary)
async def get_report_summary(db: Session = Depends(get_db)):
    """Получить сводку по отчетам."""
    # Получаем базовую статистику
    fleet_report = reports_api_service.get_fleet_report(db)
    
    return ReportSummary(
        report_type="fleet_summary",
        generated_at=datetime.now().isoformat(),
        period=None,
        total_records=fleet_report["total_trucks"],
        summary_stats={
            "total_revenue": fleet_report["total_revenue"],
            "total_profit": fleet_report["total_profit"],
            "average_margin": fleet_report["average_margin_percent"],
            "profitable_trucks": len([t for t in fleet_report["truck_reports"] if t["profit"] > 0])
        }
    )
