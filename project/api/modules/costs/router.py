"""
Роутер для модуля costs.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict

from ...dependencies import get_db
from .schemas import (
    TruckCostsResponse, TruckCostsUpdate,
    CommonCostsResponse, CommonCostsUpdate,
    CostCalculationRequest, CostCalculationResponse,
    FleetSummaryRequest, FleetSummaryResponse
)
from .service import costs_api_service

router = APIRouter(prefix="/costs", tags=["costs"])


# ========== Truck Fixed Costs ==========

@router.get("/trucks/{truck_id}", response_model=TruckCostsResponse)
async def get_truck_costs(truck_id: int, db: Session = Depends(get_db)):
    """Получить фиксированные затраты трака."""
    costs = costs_api_service.get_truck_costs(db, truck_id)
    return TruckCostsResponse(truck_id=truck_id, **costs)


@router.put("/trucks/{truck_id}", response_model=TruckCostsResponse)
async def update_truck_costs(
    truck_id: int, 
    cost_updates: TruckCostsUpdate, 
    db: Session = Depends(get_db)
):
    """Обновить фиксированные затраты трака."""
    try:
        # Преобразуем Pydantic модель в словарь, исключая None значения
        updates_dict = cost_updates.model_dump(exclude_none=True)
        
        if not updates_dict:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Необходимо указать хотя бы одно поле для обновления"
            )
        
        costs = costs_api_service.update_truck_costs(db, truck_id, updates_dict)
        return TruckCostsResponse(truck_id=truck_id, **costs)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


# ========== Common Fixed Costs ==========

@router.get("/common", response_model=CommonCostsResponse)
async def get_common_costs(db: Session = Depends(get_db)):
    """Получить общие фиксированные затраты."""
    costs = costs_api_service.get_common_costs(db)
    return CommonCostsResponse(**costs)


@router.put("/common", response_model=CommonCostsResponse)
async def update_common_costs(
    cost_updates: CommonCostsUpdate, 
    db: Session = Depends(get_db)
):
    """Обновить общие фиксированные затраты."""
    try:
        # Преобразуем Pydantic модель в словарь, исключая None значения
        updates_dict = cost_updates.model_dump(exclude_none=True)
        
        if not updates_dict:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Необходимо указать хотя бы одно поле для обновления"
            )
        
        costs = costs_api_service.update_common_costs(db, updates_dict)
        return CommonCostsResponse(**costs)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


# ========== Cost Calculations ==========

@router.post("/calculate", response_model=CostCalculationResponse)
async def calculate_costs(
    calculation_request: CostCalculationRequest,
    db: Session = Depends(get_db)
):
    """Рассчитать затраты и прибыль для трака."""
    try:
        # Преобразуем переменные затраты в словарь
        variable_costs_dict = calculation_request.variable_costs.model_dump()
        
        result = costs_api_service.calculate_costs(
            db, 
            calculation_request.truck_id,
            calculation_request.revenue,
            variable_costs_dict
        )
        
        return CostCalculationResponse(**result)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/fleet-summary", response_model=FleetSummaryResponse)
async def calculate_fleet_summary(
    fleet_request: FleetSummaryRequest,
    db: Session = Depends(get_db)
):
    """Рассчитать флотовый отчет."""
    try:
        result = costs_api_service.calculate_fleet_summary(db, fleet_request.truck_data)
        return FleetSummaryResponse(**result)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


# ========== Utility Endpoints ==========

@router.get("/common/impact-per-truck")
async def get_common_costs_impact_per_truck(db: Session = Depends(get_db)):
    """Получить влияние общих затрат на каждый трак."""
    impact = costs_api_service.get_common_costs_impact_per_truck(db)
    return {"common_costs_impact_per_truck": impact}
