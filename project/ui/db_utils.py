"""
Утилиты для работы с базой данных в Streamlit приложении.
Содержит функции для CRUD операций и обработки ошибок.
"""

import sys
from pathlib import Path
from typing import List, Optional, Dict, Any
import streamlit as st

# Добавляем путь к модулям БД
sys.path.append(str(Path(__file__).parent.parent / "data" / "database"))

try:
    from database import get_db_session, ensure_db_exists
    from models import Base, Truck, FixedCostsTruck, FixedCostsCommon
except ImportError as e:
    st.error(f"Ошибка импорта моделей БД: {e}")
    st.stop()


def init_database():
    """Инициализация базы данных при старте приложения"""
    try:
        db_path = ensure_db_exists()
        return db_path
    except Exception as e:
        st.error(f"Ошибка инициализации базы данных: {e}")
        return None


def safe_db_operation(operation_func):
    """Декоратор для безопасного выполнения операций с БД"""
    def wrapper(*args, **kwargs):
        try:
            return operation_func(*args, **kwargs)
        except Exception as e:
            st.error(f"Ошибка при работе с БД: {e}")
            return None
    return wrapper


# =============================================================================
# CRUD для траков
# =============================================================================

@safe_db_operation
def create_truck(tractor_no: str) -> bool:
    """Создать новый трак"""
    if not tractor_no or not tractor_no.strip():
        st.error("Номер трака не может быть пустым")
        return False
        
    tractor_no = tractor_no.strip()
    
    with get_db_session() as session:
        # Проверка на дубликаты
        existing = session.query(Truck).filter(Truck.tractor_no == tractor_no).first()
        if existing:
            st.error(f"Трак {tractor_no} уже существует!")
            return False
            
        # Создание нового трака
        truck = Truck(tractor_no=tractor_no)
        session.add(truck)
        session.commit()
        st.success(f"✅ Трак {tractor_no} успешно добавлен!")
        return True


@safe_db_operation
def get_all_trucks() -> List[Dict[str, Any]]:
    """Получить список всех траков"""
    with get_db_session() as session:
        trucks = session.query(Truck).all()
        return [
            {
                "id": truck.id,
                "tractor_no": truck.tractor_no,
                "monthly_rows_count": len(truck.monthly_rows) if truck.monthly_rows else 0,
                "fixed_costs_count": len(truck.fixed_costs_items) if truck.fixed_costs_items else 0,
            }
            for truck in trucks
        ]


@safe_db_operation
def get_truck_by_id(truck_id: int) -> Optional[Dict[str, Any]]:
    """Получить трак по ID"""
    with get_db_session() as session:
        truck = session.query(Truck).filter(Truck.id == truck_id).first()
        if truck:
            return {
                "id": truck.id,
                "tractor_no": truck.tractor_no,
                "monthly_rows_count": len(truck.monthly_rows) if truck.monthly_rows else 0,
                "fixed_costs_count": len(truck.fixed_costs_items) if truck.fixed_costs_items else 0,
            }
        return None


@safe_db_operation
def get_truck_by_tractor_no(tractor_no: str) -> Optional[Dict[str, Any]]:
    """Получить трак по номеру"""
    with get_db_session() as session:
        truck = session.query(Truck).filter(Truck.tractor_no == tractor_no).first()
        if truck:
            return {
                "id": truck.id,
                "tractor_no": truck.tractor_no,
                "monthly_rows_count": len(truck.monthly_rows) if truck.monthly_rows else 0,
                "fixed_costs_count": len(truck.fixed_costs_items) if truck.fixed_costs_items else 0,
            }
        return None


@safe_db_operation
def update_truck(truck_id: int, new_tractor_no: str) -> bool:
    """Обновить номер трака"""
    if not new_tractor_no or not new_tractor_no.strip():
        st.error("Номер трака не может быть пустым")
        return False
        
    new_tractor_no = new_tractor_no.strip()
    
    with get_db_session() as session:
        truck = session.query(Truck).filter(Truck.id == truck_id).first()
        if not truck:
            st.error("Трак не найден!")
            return False
            
        # Проверка на дубликаты (исключая текущий трак)
        existing = session.query(Truck).filter(
            Truck.tractor_no == new_tractor_no,
            Truck.id != truck_id
        ).first()
        if existing:
            st.error(f"Трак {new_tractor_no} уже существует!")
            return False
            
        old_no = truck.tractor_no
        truck.tractor_no = new_tractor_no
        session.commit()
        st.success(f"✅ Трак {old_no} переименован в {new_tractor_no}!")
        return True


@safe_db_operation
def delete_truck(truck_id: int) -> bool:
    """Удалить трак"""
    with get_db_session() as session:
        truck = session.query(Truck).filter(Truck.id == truck_id).first()
        if not truck:
            st.error("Трак не найден!")
            return False
            
        tractor_no = truck.tractor_no
        
        # Проверка на связанные записи
        if truck.monthly_rows:
            st.error(f"Нельзя удалить трак {tractor_no} - есть связанные месячные записи ({len(truck.monthly_rows)} шт.)")
            return False
            
        session.delete(truck)
        session.commit()
        st.success(f"🗑️ Трак {tractor_no} удалён!")
        return True


# =============================================================================
# CRUD для общих фиксированных расходов
# =============================================================================

@safe_db_operation
def get_common_fixed_costs() -> Optional[Dict[str, Any]]:
    """Получить общие фиксированные расходы"""
    with get_db_session() as session:
        costs = session.query(FixedCostsCommon).first()
        if costs:
            return {
                "id": costs.id,
                "ifta": float(costs.ifta),
                "insurance": float(costs.insurance),
                "eld": float(costs.eld),
                "tablet": float(costs.tablet),
                "tolls": float(costs.tolls),
            }
        return {
            "id": None,
            "ifta": 0.0,
            "insurance": 0.0,
            "eld": 0.0,
            "tablet": 0.0,
            "tolls": 0.0,
        }


@safe_db_operation
def save_common_fixed_costs(ifta: float, insurance: float, eld: float, tablet: float, tolls: float) -> bool:
    """Сохранить общие фиксированные расходы"""
    with get_db_session() as session:
        costs = session.query(FixedCostsCommon).first()
        
        if costs:
            # Обновляем существующую запись
            costs.ifta = ifta
            costs.insurance = insurance
            costs.eld = eld
            costs.tablet = tablet
            costs.tolls = tolls
        else:
            # Создаём новую запись
            costs = FixedCostsCommon(
                ifta=ifta,
                insurance=insurance,
                eld=eld,
                tablet=tablet,
                tolls=tolls
            )
            session.add(costs)
            
        session.commit()
        st.success("✅ Общие фиксированные расходы сохранены!")
        return True


# =============================================================================
# CRUD для индивидуальных фиксированных расходов по тракам
# =============================================================================

@safe_db_operation
def get_truck_fixed_costs(truck_id: int) -> Optional[Dict[str, Any]]:
    """Получить фиксированные расходы для конкретного трака"""
    with get_db_session() as session:
        costs = session.query(FixedCostsTruck).filter(FixedCostsTruck.truck_id == truck_id).first()
        if costs:
            return {
                "id": costs.id,
                "truck_id": costs.truck_id,
                "truck_payment": float(costs.truck_payment),
                "trailer_payment": float(costs.trailer_payment),
                "physical_damage_insurance_truck": float(costs.physical_damage_insurance_truck),
                "physical_damage_insurance_trailer": float(costs.physical_damage_insurance_trailer),
            }
        return {
            "id": None,
            "truck_id": truck_id,
            "truck_payment": 0.0,
            "trailer_payment": 0.0,
            "physical_damage_insurance_truck": 0.0,
            "physical_damage_insurance_trailer": 0.0,
        }


@safe_db_operation
def save_truck_fixed_costs(truck_id: int, truck_payment: float, trailer_payment: float, 
                          pd_truck: float, pd_trailer: float) -> bool:
    """Сохранить фиксированные расходы для трака"""
    with get_db_session() as session:
        # Проверяем что трак существует
        truck = session.query(Truck).filter(Truck.id == truck_id).first()
        if not truck:
            st.error("Трак не найден!")
            return False
            
        costs = session.query(FixedCostsTruck).filter(FixedCostsTruck.truck_id == truck_id).first()
        
        if costs:
            # Обновляем существующую запись
            costs.truck_payment = truck_payment
            costs.trailer_payment = trailer_payment
            costs.physical_damage_insurance_truck = pd_truck
            costs.physical_damage_insurance_trailer = pd_trailer
        else:
            # Создаём новую запись
            costs = FixedCostsTruck(
                truck_id=truck_id,
                truck_payment=truck_payment,
                trailer_payment=trailer_payment,
                physical_damage_insurance_truck=pd_truck,
                physical_damage_insurance_trailer=pd_trailer
            )
            session.add(costs)
            
        session.commit()
        st.success(f"✅ Фиксированные расходы для трака {truck.tractor_no} сохранены!")
        return True


@safe_db_operation
def delete_truck_fixed_costs(truck_id: int) -> bool:
    """Удалить фиксированные расходы для трака"""
    with get_db_session() as session:
        costs = session.query(FixedCostsTruck).filter(FixedCostsTruck.truck_id == truck_id).first()
        if costs:
            session.delete(costs)
            session.commit()
            st.success("🗑️ Фиксированные расходы удалены!")
            return True
        else:
            st.warning("Фиксированные расходы для этого трака не найдены")
            return False


def get_trucks_list_for_selectbox() -> List[Dict[str, Any]]:
    """Получить список траков для selectbox'а"""
    trucks = get_all_trucks()
    if trucks:
        return [{"id": truck["id"], "label": truck["tractor_no"]} for truck in trucks]
    return []