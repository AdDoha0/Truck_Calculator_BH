#!/bin/bash

# Скрипт для запуска полного приложения (FastAPI + Streamlit)
# Использование: ./start_app.sh [streamlit_port] [api_port]

set -e

# Настройки
STREAMLIT_PORT=${1:-8501}
API_PORT=${2:-8000}
STREAMLIT_HOST="localhost"
API_HOST="localhost"

echo "🚀 Запуск полного приложения (FastAPI + Streamlit)..."
echo "📊 Streamlit: http://$STREAMLIT_HOST:$STREAMLIT_PORT"
echo "🔌 FastAPI: http://$API_HOST:$API_PORT"
echo ""

# Проверяем, что виртуальное окружение активировано
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "⚠️  Внимание: Виртуальное окружение не активировано"
    echo "💡 Активируйте его командой: source venv/bin/activate"
    echo ""
fi

# Проверяем наличие зависимостей
if ! command -v streamlit &> /dev/null || ! command -v uvicorn &> /dev/null; then
    echo "❌ Зависимости не найдены. Установите их:"
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
echo "🌐 Приложение будет доступно по адресам:"
echo "   📊 Streamlit UI: http://$STREAMLIT_HOST:$STREAMLIT_PORT"
echo "   📖 API Swagger: http://$API_HOST:$API_PORT/docs"
echo "   📚 API ReDoc: http://$API_HOST:$API_PORT/redoc"
echo "   ❤️  API Health: http://$API_HOST:$API_PORT/health"
echo ""
echo "🛑 Для остановки нажмите Ctrl+C"
echo ""

# Функция для остановки всех процессов
cleanup() {
    echo ""
    echo "🛑 Остановка приложения..."
    kill $API_PID $STREAMLIT_PID 2>/dev/null || true
    exit 0
}

# Устанавливаем обработчик сигналов
trap cleanup SIGINT SIGTERM

# Запускаем FastAPI в фоне
echo "🔌 Запуск FastAPI сервера..."
uvicorn project.api.main:app \
    --host 0.0.0.0 \
    --port $API_PORT \
    --reload \
    --log-level info &
API_PID=$!

# Ждем немного, чтобы API запустился
sleep 3

# Запускаем Streamlit в фоне
echo "📊 Запуск Streamlit приложения..."
streamlit run project/ui/app.py \
    --server.port $STREAMLIT_PORT \
    --server.address $STREAMLIT_HOST \
    --server.headless true &
STREAMLIT_PID=$!

# Ждем завершения процессов
wait $API_PID $STREAMLIT_PID
