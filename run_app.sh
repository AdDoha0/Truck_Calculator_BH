#!/bin/bash

# Скрипт для запуска BH Trans Dashboard

echo "🚛 Запуск BH Trans Dashboard..."
echo ""

# Активация виртуального окружения
if [ -d "venv" ]; then
    echo "✓ Активация виртуального окружения..."
    source venv/bin/activate
else
    echo "❌ Виртуальное окружение не найдено!"
    echo "   Создайте его командой: python3 -m venv venv"
    exit 1
fi

# Проверка наличия Streamlit
if ! command -v streamlit &> /dev/null; then
    echo "❌ Streamlit не установлен!"
    echo "   Установите его: pip install streamlit pandas openpyxl"
    exit 1
fi

# Запуск приложения
echo "✓ Запуск Streamlit приложения..."
echo ""
export PYTHONPATH=/home/user/my_projects/BH/truck_calculate/project
cd project
streamlit run ui/app.py
