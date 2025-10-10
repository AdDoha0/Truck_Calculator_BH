"""
Главный файл FastAPI приложения.

Точка входа для REST API с модульной архитектурой по доменам.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from .config import settings
from .modules.trucks.router import router as trucks_router
from .modules.costs.router import router as costs_router
from .modules.monthly.router import router as monthly_router
from .modules.reports.router import router as reports_router


def create_app() -> FastAPI:
    """Создать и настроить FastAPI приложение."""
    
    app = FastAPI(
        title=settings.api_title,
        version=settings.api_version,
        description=settings.api_description,
        docs_url="/docs",
        redoc_url="/redoc",
    )
    
    # CORS middleware для работы с Streamlit
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Подключение роутеров модулей
    app.include_router(trucks_router, prefix="/api/v1")
    app.include_router(costs_router, prefix="/api/v1")
    app.include_router(monthly_router, prefix="/api/v1")
    app.include_router(reports_router, prefix="/api/v1")
    
    # Health check endpoint
    @app.get("/health")
    async def health_check():
        """Проверка состояния API."""
        return {"status": "healthy", "version": settings.api_version}
    
    # Обработка ошибок валидации
    @app.exception_handler(ValueError)
    async def value_error_handler(request, exc):
        return JSONResponse(
            status_code=400,
            content={"detail": str(exc)}
        )
    
    return app


# Создание экземпляра приложения
app = create_app()


if __name__ == "__main__":
    uvicorn.run(
        "project.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
