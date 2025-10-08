# 🚛 BH Trans - Truck Dashboard

Многостраничное Streamlit приложение для управления отчётностью по тракам.

## 📁 Структура проекта

```
project/ui/
├── app.py                    # Главная страница приложения
├── ui_utils.py               # Общие утилиты и стили
└── pages/
    ├── 1_Upload.py           # Загрузка данных (5 Excel файлов)
    ├── 2_Report.py           # Отчёты и KPI
    ├── 3_Settings.py         # Настройки фиксированных расходов
    └── 4_References.py       # Справочники траков и периодов
```

## 🚀 Запуск приложения

### 1. Активируйте виртуальное окружение

```bash
cd /home/user/my_projects/BH/truck_calculate
source venv/bin/activate
```

### 2. Запустите Streamlit

```bash
cd project/ui
streamlit run app.py --server.port 8502
```

### 3. Откройте браузер

Приложение автоматически откроется по адресу: **http://localhost:8502**

## 📋 Функционал страниц

### 📁 Upload (Загрузка)
- Выбор месяца отчёта и валюты
- Загрузка 5 Excel файлов:
  - ⛽ Fuel - расходы на топливо
  - 🛣️ Tolls - дорожные сборы
  - 🔧 Repair - ремонт
  - 👷 Salary - зарплаты
  - 💵 Gross - выручка и пробег
- Предпросмотр загруженных данных
- Валидация tractor_no

### 📊 Report (Отчёт)
- KPI метрики: Revenue, Variable, Fixed, Gross Profit
- Таблица v_unit_month по тракам
- Графики:
  - GP по тракам (bar chart)
  - RPM/CPM по тракам (line chart)
  - Динамика GP (area chart)

### ⚙️ Settings (Настройки)
- **Общие расходы**: IFTA, Insurance, ELD, Tablet
- **Индивидуальные по траку**: Truck payment, Trailer payment, PD Insurance

### 📚 References (Справочники)
- Справочник траков
- Загруженные периоды
- Логи операций

## 🎨 Особенности

- ✨ Официальная многостраничная структура Streamlit
- 🎯 Стандартное оформление Streamlit
- 📊 Демо-данные для preview
- 🔄 Кеширование данных
- 📱 Адаптивный wide layout

## ⚠️ Примечание

Текущая версия - **UI prototype** без подключения к базе данных. Все данные - демонстрационные.

