# SQLAlchemy 2.0 style
from __future__ import annotations
from datetime import date
from typing import List, Optional

from sqlalchemy import (
    Date,
    ForeignKey,
    Integer,
    Numeric,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import MetaData

# Конвенция имён для ограничений (удобно для Alembic)
convention = {
    "ix": "ix__%(table_name)s__%(column_0_name)s",
    "uq": "uq__%(table_name)s__%(column_0_name)s",
    "ck": "ck__%(table_name)s__%(constraint_name)s",
    "fk": "fk__%(table_name)s__%(column_0_name)s__%(referred_table_name)s",
    "pk": "pk__%(table_name)s",
}

class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=convention)


# A. Трак (справочник)
class Truck(Base):
    __tablename__ = "truck"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tractor_no: Mapped[str] = mapped_column(Text, nullable=False, unique=True)

    # навигация
    monthly_rows: Mapped[List[MonthlyRow]] = relationship(
        back_populates="truck",
        cascade="all, delete-orphan",
        passive_deletes=False,
    )
    fixed_costs_items: Mapped[List[FixedCostsTruck]] = relationship(
        back_populates="truck",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def __repr__(self) -> str:
        return f"Truck(id={self.id}, tractor_no={self.tractor_no!r})"


# B. Строки из месячного файла
class MonthlyRow(Base):
    __tablename__ = "monthly_row"
    __table_args__ = (
        UniqueConstraint("period_month", "truck_id", name="uq_month_truck"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    period_month: Mapped[date] = mapped_column(Date, nullable=False)

    truck_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("truck.id", ondelete="RESTRICT"),
        nullable=False,
    )

    driver_name: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    total_rev: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    total_miles: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    salary: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    fuel: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    tolls: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    repair: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=0)

    truck: Mapped[Truck] = relationship(back_populates="monthly_rows")

    def __repr__(self) -> str:
        return f"MonthlyRow(id={self.id}, month={self.period_month}, truck_id={self.truck_id})"


# C. Фиксированные значения для каждого трака
class FixedCostsTruck(Base):
    __tablename__ = "fixed_costs_truck"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    truck_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("truck.id", ondelete="SET NULL"),
        nullable=True,
    )

    truck_payment: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    trailer_payment: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    physical_damage_insurance_truck: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    physical_damage_insurance_trailer: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=0)

    truck: Mapped[Optional[Truck]] = relationship(back_populates="fixed_costs_items")

    def __repr__(self) -> str:
        return f"FixedCostsTruck(id={self.id}, truck_id={self.truck_id})"


# D. Общие фиксированные значения
class FixedCostsCommon(Base):
    __tablename__ = "fixed_costs_common"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    ifta: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    insurance: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    eld: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    tablet: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    tolls: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=0)

    def __repr__(self) -> str:
        return f"FixedCostsCommon(id={self.id})"