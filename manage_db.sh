#!/bin/bash

# Скрипт для управления базой данных

# Активировать виртуальное окружение
source venv/bin/activate

# Функция для отображения помощи
show_help() {
    echo "Управление базой данных Truck Calculate"
    echo ""
    echo "Использование: ./manage_db.sh [команда]"
    echo ""
    echo "Команды:"
    echo "  create      - Создать базу данных и все таблицы"
    echo "  drop        - Удалить все таблицы (требует подтверждения)"
    echo "  recreate    - Пересоздать базу данных (требует подтверждения)"
    echo "  example     - Запустить примеры использования"
    echo "  info        - Показать информацию о базе данных"
    echo "  help        - Показать эту справку"
    echo ""
}

# Функция для отображения информации о БД
show_info() {
    python project/data/database/db_info.py $@
}

# Обработка команд
case "$1" in
    create)
        echo "Создание базы данных..."
        python project/data/database/migrate.py create
        ;;
    drop)
        read -p "Вы уверены, что хотите удалить все таблицы? Это удалит все данные! (yes/no): " confirm
        if [ "$confirm" = "yes" ]; then
            python project/data/database/migrate.py drop
        else
            echo "Операция отменена."
        fi
        ;;
    recreate)
        read -p "Вы уверены, что хотите пересоздать базу данных? Это удалит все данные! (yes/no): " confirm
        if [ "$confirm" = "yes" ]; then
            rm -f project/data/truck_data.db
            python project/data/database/migrate.py create
        else
            echo "Операция отменена."
        fi
        ;;
    example)
        echo "Запуск примеров использования..."
        python project/data/database/example_usage.py
        ;;
    info)
        show_info
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        if [ -z "$1" ]; then
            show_help
        else
            echo "Неизвестная команда: $1"
            echo ""
            show_help
            exit 1
        fi
        ;;
esac

