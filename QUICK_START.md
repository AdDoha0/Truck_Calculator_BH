

/home/user/my_projects/BH/truck_calculate/
├── project/
│   ├── main.py                          # Описание проекта (можно оставить)
│   │
│   ├── ui/                              # UI слой (уже есть)
│   │   ├── app.py                       # Главная страница Streamlit
│   │   ├── ui_utils.py                  # UI утилиты
│   │   └── pages/                       # Страницы приложения
│   │       ├── 1_Upload.py
│   │       ├── 2_Report.py
│   │       ├── 3_Settings.py
│   │       └── 4_References.py
│   │
│   ├── business/                        # 🎯 Бизнес-логика (НОВОЕ)
│   │   ├── __init__.py
│   │   ├── services/                    # Сервисы с бизнес-логикой
│   │   │   ├── __init__.py
│   │   │   ├── upload_service.py        # Логика загрузки и валидации
│   │   │   ├── calculation_service.py   # Расчёты (RPM, CPM, GP и т.д.)
│   │   │   ├── report_service.py        # Генерация отчётов
│   │   │   └── settings_service.py      # Управление настройками
│   │   │
│   │   ├── models/                      # Доменные модели (Pydantic/dataclasses)
│   │   │   ├── __init__.py
│   │   │   ├── truck.py                 # Модель трака
│   │   │   ├── period.py                # Модель периода
│   │   │   ├── expenses.py              # Модели расходов
│   │   │   └── report.py                # Модели отчётов
│   │   │
│   │   └── validators/                  # Валидаторы данных
│   │       ├── __init__.py
│   │       ├── file_validator.py        # Валидация файлов
│   │       └── data_validator.py        # Валидация данных
│   │
│   ├── data/                            # 💾 Слой данных (НОВОЕ)
│   │   ├── __init__.py
│   │   ├── repositories/                # Паттерн Repository
│   │   │   ├── __init__.py
│   │   │   ├── base_repository.py       # Базовый репозиторий
│   │   │   ├── truck_repository.py      # Работа с траками
│   │   │   ├── expense_repository.py    # Работа с расходами
│   │   │   └── report_repository.py     # Работа с отчётами
│   │   │
│   │   ├── database/                    # Работа с БД
│   │   │   ├── __init__.py
│   │   │   ├── connection.py            # Подключение к БД
│   │   │   ├── models.py                # SQLAlchemy/ORM модели
│   │   │   └── migrations/              # Миграции (Alembic)
│   │   │
│   │   └── schemas/                     # SQL схемы/DDL
│   │       └── init.sql
│   │
│   ├── utils/                           # 🛠️ Утилиты (НОВОЕ)
│   │   ├── __init__.py
│   │   ├── excel_parser.py              # Парсинг Excel
│   │   ├── logger.py                    # Логирование
│   │   └── config.py                    # Конфигурация
│   │
│   └── tests/                           # 🧪 Тесты (НОВОЕ)
│       ├── __init__.py
│       ├── test_services/
│       ├── test_repositories/
│       └── test_validators/
│
├── config/                              # ⚙️ Конфигурация (НОВОЕ)
│   ├── settings.yaml
│   └── database.yaml
│
├── requirements.txt
├── run_app.sh
└── QUICK_START.md
