"""
Роутер для модуля trucks.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ...dependencies import get_db
from .schemas import TruckCreate, TruckUpdate, TruckResponse, TruckListResponse
from .service import truck_service

router = APIRouter(prefix="/trucks", tags=["trucks"])


@router.get("/", response_model=TruckListResponse)
async def get_trucks(db: Session = Depends(get_db)):
    """Получить все траки."""
    trucks = truck_service.get_all_trucks(db)
    return TruckListResponse(trucks=trucks, total=len(trucks))


@router.get("/{truck_id}", response_model=TruckResponse)
async def get_truck(truck_id: int, db: Session = Depends(get_db)):
    """Получить трак по ID."""
    truck = truck_service.get_truck_by_id(db, truck_id)
    if not truck:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Трак с ID {truck_id} не найден"
        )
    return truck


@router.post("/", response_model=TruckResponse, status_code=status.HTTP_201_CREATED)
async def create_truck(truck_data: TruckCreate, db: Session = Depends(get_db)):
    """Создать новый трак."""
    try:
        truck = truck_service.create_truck(db, truck_data.tractor_no)
        return truck
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{truck_id}", response_model=TruckResponse)
async def update_truck(
    truck_id: int, 
    truck_data: TruckUpdate, 
    db: Session = Depends(get_db)
):
    """Обновить трак."""
    try:
        truck = truck_service.update_truck(db, truck_id, truck_data.tractor_no)
        return truck
    except ValueError as e:
        if "не найден" in str(e):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )


@router.delete("/{truck_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_truck(truck_id: int, db: Session = Depends(get_db)):
    """Удалить трак."""
    try:
        deleted = truck_service.delete_truck(db, truck_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Трак с ID {truck_id} не найден"
            )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{truck_id}/can-delete")
async def can_delete_truck(truck_id: int, db: Session = Depends(get_db)):
    """Проверить, можно ли удалить трак."""
    can_delete = truck_service.can_delete_truck(db, truck_id)
    return {"truck_id": truck_id, "can_delete": can_delete}
