# 🚀 Быстрый старт

## Запуск приложения

```bash
# 1. Активировать виртуальное окружение
source venv/bin/activate

# 2. Запустить Streamlit
streamlit run project/frontend/app.py
```

## Структура

```
project/frontend/
├── app.py              # Главная страница
├── ui_utils.py         # Утилиты
└── pages/
    ├── 1_Upload.py     # Загрузка данных
    ├── 2_Report.py     # Отчёты
    ├── 3_Settings.py   # Настройки
    └── 4_References.py # Справочники
```

Приложение откроется на http://localhost:8501
