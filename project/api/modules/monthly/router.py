"""
Роутер для модуля monthly.
"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List

from ...dependencies import get_db
from .schemas import (
    MonthlyDataResponse, MonthlyDataCreate, MonthlyDataUpdate,
    MonthlyDataListResponse, PeriodResponse, PeriodListResponse,
    FileUploadResponse
)
from .service import monthly_api_service

router = APIRouter(prefix="/monthly", tags=["monthly"])


@router.get("/trucks/{truck_id}", response_model=MonthlyDataListResponse)
async def get_monthly_data_for_truck(truck_id: int, db: Session = Depends(get_db)):
    """Получить месячные данные для трака."""
    monthly_data = monthly_api_service.get_monthly_data_for_truck(db, truck_id)
    return MonthlyDataListResponse(monthly_data=monthly_data, total=len(monthly_data))


@router.get("/{monthly_id}", response_model=MonthlyDataResponse)
async def get_monthly_data(monthly_id: int, db: Session = Depends(get_db)):
    """Получить месячные данные по ID."""
    monthly_data = monthly_api_service.get_monthly_data_by_id(db, monthly_id)
    if not monthly_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Месячные данные с ID {monthly_id} не найдены"
        )
    return monthly_data


@router.post("/", response_model=MonthlyDataResponse, status_code=status.HTTP_201_CREATED)
async def create_monthly_data(
    monthly_data: MonthlyDataCreate, 
    db: Session = Depends(get_db)
):
    """Создать месячные данные."""
    try:
        data_dict = monthly_data.model_dump()
        result = monthly_api_service.create_monthly_data(db, data_dict)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{monthly_id}", response_model=MonthlyDataResponse)
async def update_monthly_data(
    monthly_id: int,
    monthly_data: MonthlyDataUpdate,
    db: Session = Depends(get_db)
):
    """Обновить месячные данные."""
    try:
        updates_dict = monthly_data.model_dump(exclude_none=True)
        
        if not updates_dict:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Необходимо указать хотя бы одно поле для обновления"
            )
        
        result = monthly_api_service.update_monthly_data(db, monthly_id, updates_dict)
        return result
    except ValueError as e:
        if "не найдены" in str(e):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )


@router.delete("/{monthly_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_monthly_data(monthly_id: int, db: Session = Depends(get_db)):
    """Удалить месячные данные."""
    deleted = monthly_api_service.delete_monthly_data(db, monthly_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Месячные данные с ID {monthly_id} не найдены"
        )


@router.get("/periods/available", response_model=PeriodListResponse)
async def get_available_periods(db: Session = Depends(get_db)):
    """Получить доступные периоды."""
    periods_str = monthly_api_service.get_available_periods(db)
    
    periods = []
    for period_str in periods_str:
        # Парсим дату из строки
        from datetime import datetime
        try:
            period_date = datetime.fromisoformat(period_str).date()
            periods.append(PeriodResponse(
                period=period_str,
                year=period_date.year,
                month=period_date.month
            ))
        except ValueError:
            # Если не удается распарсить, добавляем как есть
            periods.append(PeriodResponse(
                period=period_str,
                year=0,
                month=0
            ))
    
    return PeriodListResponse(periods=periods, total=len(periods))


@router.post("/upload", response_model=FileUploadResponse)
async def upload_monthly_data(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Загрузить месячные данные из файла."""
    try:
        # Проверка типа файла
        if not file.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Имя файла не указано"
            )
        
        # Читаем содержимое файла
        file_content = await file.read()
        
        # Обрабатываем файл
        result = monthly_api_service.process_uploaded_file(db, file_content, file.filename)
        
        return FileUploadResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка обработки файла: {str(e)}"
        )


@router.get("/", response_model=MonthlyDataListResponse)
async def get_all_monthly_data(db: Session = Depends(get_db)):
    """Получить все месячные данные."""
    monthly_data = monthly_api_service.get_all_monthly_data(db)
    return MonthlyDataListResponse(monthly_data=monthly_data, total=len(monthly_data))
