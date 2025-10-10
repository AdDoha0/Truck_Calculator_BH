"""
Конфигурация FastAPI приложения.
"""
from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    """Настройки приложения."""
    
    # API настройки
    api_title: str = "BH Trans Truck Management API"
    api_version: str = "v1"
    api_description: str = "REST API для управления траками и расчета затрат"
    
    # CORS настройки (для Streamlit)
    cors_origins: list[str] = [
        "http://localhost:8501",  # Streamlit по умолчанию
        "http://127.0.0.1:8501",
    ]
    
    # База данных
    database_url: str = "sqlite:///./truck_data.db"
    database_echo: bool = False
    
    # Путь к базе данных (для совместимости с существующим кодом)
    database_path: Path = Path(__file__).parent.parent.parent / "truck_data.db"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Глобальный экземпляр настроек
settings = Settings()
