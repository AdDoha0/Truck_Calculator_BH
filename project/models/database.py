"""
SQLAlchemy models and database management.
Combines database models and connection management.
"""
from __future__ import annotations
from datetime import date
from typing import List, Optional
from pathlib import Path
from contextlib import contextmanager

from sqlalchemy import (
    Date,
    ForeignKey,
    Integer,
    Numeric,
    Text,
    UniqueConstraint,
    create_engine,
    text,
    MetaData,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker, Session

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


# ========== SQLAlchemy Models ==========

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


# ========== Database Management ==========

# Default database path - pointing to project root
DB_PATH = Path(__file__).parent.parent.parent / "truck_data.db"


def get_engine(db_path: Path = None, echo: bool = False):
    """
    Get SQLAlchemy engine.
    
    Args:
        db_path: Path to SQLite database file. If None, uses default path.
        echo: If True, SQLAlchemy will log all SQL statements.
        
    Returns:
        SQLAlchemy Engine object
    """
    if db_path is None:
        db_path = DB_PATH
    
    database_url = f"sqlite:///{db_path}"
    return create_engine(database_url, echo=echo)


def get_session_factory(db_path: Path = None):
    """
    Get a session factory (sessionmaker).
    
    Args:
        db_path: Path to SQLite database file. If None, uses default path.
        
    Returns:
        SQLAlchemy sessionmaker
    """
    engine = get_engine(db_path)
    return sessionmaker(bind=engine)


@contextmanager
def get_db_session(db_path: Path = None) -> Session:
    """
    Context manager for database sessions.
    Automatically commits on success, rolls back on error.
    
    Usage:
        with get_db_session() as session:
            truck = Truck(tractor_no="ABC123")
            session.add(truck)
            # Automatically commits when exiting context
    
    Args:
        db_path: Path to SQLite database file. If None, uses default path.
        
    Yields:
        SQLAlchemy Session object
    """
    SessionFactory = get_session_factory(db_path)
    session = SessionFactory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def init_db(db_path: Path = None, echo: bool = False):
    """
    Initialize database - create tables if they don't exist.
    
    Args:
        db_path: Path to SQLite database file. If None, uses default path.
        echo: If True, SQLAlchemy will log all SQL statements.
        
    Returns:
        SQLAlchemy Engine object
    """
    engine = get_engine(db_path, echo=echo)
    Base.metadata.create_all(engine)
    
    if echo:
        with engine.connect() as conn:
            result = conn.execute(text(
                "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
            ))
            tables = [row[0] for row in result]
            print(f"Tables: {', '.join(tables)}")
    
    return engine


def ensure_db_exists(db_path: Path = None):
    """
    Ensure database exists and is initialized.
    Creates tables if database file doesn't exist.
    
    Args:
        db_path: Path to SQLite database file. If None, uses default path.
        
    Returns:
        Path to the database file
    """
    if db_path is None:
        db_path = DB_PATH
    
    if not db_path.exists():
        print(f"Database not found. Creating new database at: {db_path}")
        init_db(db_path)
        print("✓ Database created successfully!")
    
    return db_path


def drop_all_tables(db_path: Path = None):
    """
    Drop all tables from the database.
    
    WARNING: This will delete all data!
    
    Args:
        db_path: Path to SQLite database file. If None, uses default path.
    """
    if db_path is None:
        db_path = DB_PATH
    
    engine = get_engine(db_path)
    print(f"Dropping all tables from: {db_path}")
    Base.metadata.drop_all(engine)
    print("✓ All tables dropped!")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "create":
            init_db(echo=True)
            print("✓ Database created successfully!")
        elif command == "drop":
            confirm = input("Are you sure you want to drop all tables? This will delete all data! (yes/no): ")
            if confirm.lower() == "yes":
                drop_all_tables()
            else:
                print("Operation cancelled.")
        elif command == "recreate":
            confirm = input("Are you sure you want to recreate all tables? This will delete all data! (yes/no): ")
            if confirm.lower() == "yes":
                drop_all_tables()
                init_db(echo=True)
                print("✓ Database recreated successfully!")
            else:
                print("Operation cancelled.")
        elif command == "info":
            # Basic database info
            db_path = DB_PATH
            if db_path.exists():
                size_bytes = db_path.stat().st_size
                size_kb = size_bytes / 1024
                print(f"📊 Database: {db_path}")
                print(f"   Size: {size_kb:.2f} KB")
                
                engine = get_engine()
                with engine.connect() as conn:
                    result = conn.execute(text(
                        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
                    ))
                    tables = [row[0] for row in result]
                    print(f"   Tables: {', '.join(tables)}")
                    
                    for table in tables:
                        result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                        count = result.scalar()
                        print(f"     - {table}: {count} rows")
            else:
                print(f"❌ Database not found: {db_path}")
        else:
            print(f"Unknown command: {command}")
            print("Available commands: create, drop, recreate, info")
    else:
        # Default: ensure database exists
        ensure_db_exists()
