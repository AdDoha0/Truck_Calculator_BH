#!/bin/bash

# Скрипт для запуска FastAPI сервера
# Использование: ./run_api.sh [port]

set -e

# Настройки
API_PORT=${1:-8000}
API_HOST="0.0.0.0"
API_MODULE="project.api.main:app"

echo "🚀 Запуск FastAPI сервера..."
echo "📍 Хост: $API_HOST"
echo "🔌 Порт: $API_PORT"
echo "📦 Модуль: $API_MODULE"
echo ""

# Проверяем, что виртуальное окружение активировано
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "⚠️  Внимание: Виртуальное окружение не активировано"
    echo "💡 Активируйте его командой: source venv/bin/activate"
    echo ""
fi

# Проверяем наличие uvicorn
if ! command -v uvicorn &> /dev/null; then
    echo "❌ uvicorn не найден. Установите зависимости:"
    echo "   pip install -r requirements.txt"
    exit 1
fi

# Создаем базу данных если её нет
echo "🗄️  Проверка базы данных..."
python -c "
from project.models.database import ensure_db_exists
db_path = ensure_db_exists()
print(f'✅ База данных: {db_path}')
"

echo ""
echo "🌐 API будет доступен по адресам:"
echo "   📖 Swagger UI: http://localhost:$API_PORT/docs"
echo "   📚 ReDoc: http://localhost:$API_PORT/redoc"
echo "   ❤️  Health: http://localhost:$API_PORT/health"
echo ""
echo "🛑 Для остановки нажмите Ctrl+C"
echo ""

# Запускаем сервер
uvicorn $API_MODULE \
    --host $API_HOST \
    --port $API_PORT \
    --reload \
    --log-level info
