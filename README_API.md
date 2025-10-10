# BH Trans Truck Management API

REST API для системы управления траками и расчета затрат, построенный на FastAPI с модульной архитектурой.

## 🏗️ Архитектура

### Модульная структура по доменам:
- **trucks** - управление траками
- **costs** - управление затратами и расчеты
- **monthly** - месячные данные и загрузка файлов
- **reports** - генерация отчетов

### Технологический стек:
- **FastAPI** - веб-фреймворк
- **SQLAlchemy** - ORM для работы с БД
- **Pydantic** - валидация и сериализация данных
- **SQLite** - база данных
- **Streamlit** - веб-интерфейс (использует API)

## 🚀 Быстрый старт

### 1. Установка зависимостей

```bash
# Активируйте виртуальное окружение
source venv/bin/activate

# Установите зависимости
pip install -r requirements.txt
```

### 2. Запуск приложения

#### Вариант 1: Полное приложение (API + UI)
```bash
./start_app.sh
```

#### Вариант 2: Только API
```bash
./run_api.sh
```

#### Вариант 3: Ручной запуск
```bash
# Терминал 1 - FastAPI
uvicorn project.api.main:app --reload --port 8000

# Терминал 2 - Streamlit
streamlit run project/ui/app.py --server.port 8501
```

### 3. Доступ к приложению

- **Streamlit UI**: http://localhost:8501
- **API Swagger**: http://localhost:8000/docs
- **API ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 📚 API Документация

### Основные эндпоинты:

#### Trucks (Управление траками)
- `GET /api/v1/trucks` - получить все траки
- `GET /api/v1/trucks/{truck_id}` - получить трак по ID
- `POST /api/v1/trucks` - создать новый трак
- `PUT /api/v1/trucks/{truck_id}` - обновить трак
- `DELETE /api/v1/trucks/{truck_id}` - удалить трак

#### Costs (Управление затратами)
- `GET /api/v1/costs/trucks/{truck_id}` - затраты трака
- `PUT /api/v1/costs/trucks/{truck_id}` - обновить затраты трака
- `GET /api/v1/costs/common` - общие затраты
- `PUT /api/v1/costs/common` - обновить общие затраты
- `POST /api/v1/costs/calculate` - расчет затрат и прибыли

#### Monthly (Месячные данные)
- `GET /api/v1/monthly/trucks/{truck_id}` - месячные данные трака
- `POST /api/v1/monthly/upload` - загрузка файла с данными
- `GET /api/v1/monthly/periods/available` - доступные периоды

#### Reports (Отчеты)
- `GET /api/v1/reports/truck/{truck_id}` - отчет по траку
- `GET /api/v1/reports/fleet` - флотовый отчет
- `GET /api/v1/reports/period/{period}` - отчет за период

## 🔧 Конфигурация

Настройки приложения находятся в `project/api/config.py`:

```python
class Settings(BaseSettings):
    api_title: str = "BH Trans Truck Management API"
    api_version: str = "v1"
    cors_origins: list[str] = ["http://localhost:8501"]
    database_url: str = "sqlite:///./truck_data.db"
```

## 🗄️ База данных

- **Тип**: SQLite
- **Файл**: `truck_data.db` (создается автоматически)
- **Миграции**: Автоматическое создание таблиц при первом запуске

### Основные таблицы:
- `truck` - справочник траков
- `monthly_row` - месячные данные
- `fixed_costs_truck` - фиксированные затраты траков
- `fixed_costs_common` - общие фиксированные затраты

## 🧪 Тестирование API

### Через Swagger UI:
1. Откройте http://localhost:8000/docs
2. Выберите эндпоинт
3. Нажмите "Try it out"
4. Заполните параметры и нажмите "Execute"

### Через curl:
```bash
# Получить все траки
curl http://localhost:8000/api/v1/trucks

# Создать трак
curl -X POST http://localhost:8000/api/v1/trucks \
  -H "Content-Type: application/json" \
  -d '{"tractor_no": "ABC-123"}'

# Health check
curl http://localhost:8000/health
```

## 🔄 Интеграция с Streamlit

Streamlit UI использует HTTP клиент (`project/ui/api_client.py`) для взаимодействия с API:

```python
from project.ui.api_client import api

# Получить все траки
trucks = api.trucks.get_trucks()

# Создать трак
new_truck = api.trucks.create_truck("ABC-123")

# Рассчитать затраты
calculation = api.costs.calculate_costs(
    truck_id=1,
    revenue=10000,
    variable_costs={"salary": 2000, "fuel": 1500, "tolls": 200, "repair": 300}
)
```

## 🐛 Отладка

### Логи FastAPI:
```bash
uvicorn project.api.main:app --reload --log-level debug
```

### Проверка базы данных:
```bash
python -c "
from project.models.database import get_engine
engine = get_engine(echo=True)
with engine.connect() as conn:
    result = conn.execute('SELECT name FROM sqlite_master WHERE type=\"table\"')
    print('Таблицы:', [row[0] for row in result])
"
```

## 📝 Разработка

### Структура модуля:
```
api/modules/trucks/
├── __init__.py
├── router.py      # FastAPI роутер
├── schemas.py     # Pydantic схемы
├── service.py     # Бизнес-логика
└── crud.py        # Операции с БД
```

### Добавление нового эндпоинта:
1. Добавьте схему в `schemas.py`
2. Добавьте логику в `service.py`
3. Добавьте CRUD операции в `crud.py`
4. Добавьте роут в `router.py`

## 🚀 Развертывание

### Production настройки:
```bash
uvicorn project.api.main:app \
  --host 0.0.0.0 \
  --port 8000 \
  --workers 4 \
  --log-level warning
```

### Docker (опционально):
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "project.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 📞 Поддержка

При возникновении проблем:
1. Проверьте логи приложения
2. Убедитесь, что все зависимости установлены
3. Проверьте доступность базы данных
4. Обратитесь к документации FastAPI: https://fastapi.tiangolo.com/
