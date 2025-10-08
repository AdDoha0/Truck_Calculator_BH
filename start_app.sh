#!/bin/bash

# Скрипт запуска Streamlit приложения BH Trans
# 
# Убедитесь, что виртуальное окружение активировано и все зависимости установлены:
# pip install -r requirements.txt

cd "$(dirname "$0")/project/ui"
source ../../venv/bin/activate

echo "🚛 Запуск BH Trans Dashboard..."
echo "📍 Рабочая директория: $(pwd)"
echo "🌐 Приложение будет доступно по адресу: http://localhost:8502"
echo ""

# Останавливаем предыдущий процесс если есть
pkill -f "streamlit run app.py" 2>/dev/null || true

# Запускаем приложение
streamlit run app.py --server.port 8502 --server.address 0.0.0.0
