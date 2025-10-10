"""
Общие зависимости для FastAPI приложения.
"""
from typing import Generator
from sqlalchemy.orm import Session

from project.models.database import get_db_session


def get_db() -> Generator[Session, None, None]:
    """
    Dependency для получения сессии базы данных.
    
    Используется в роутерах для автоматического управления сессиями БД.
    """
    with get_db_session() as session:
        yield session
