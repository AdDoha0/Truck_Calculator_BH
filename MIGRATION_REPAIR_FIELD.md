# Миграция базы данных - добавление поля Ремонт

## ⚠️ ВАЖНО: Обновление структуры базы данных

При обновлении системы до новой версии с продвинутой таблицей управления траками необходимо выполнить миграцию базы данных.

## Что изменилось?

В таблицу `monthly_row` добавлено новое поле `repair` для учёта расходов на ремонт.

## Автоматическая миграция

Если вы используете существующую базу данных, выполните следующую команду:

```bash
cd /home/user/my_projects/BH/truck_calculate
source venv/bin/activate
python -c "
from project.data.database.database import get_db_session
from sqlalchemy import text

with get_db_session() as session:
    try:
        session.execute(text('ALTER TABLE monthly_row ADD COLUMN repair NUMERIC(12, 2) NOT NULL DEFAULT 0'))
        session.commit()
        print('✅ Миграция выполнена успешно!')
    except Exception as e:
        print(f'⚠️ Ошибка миграции: {e}')
        print('Возможно, поле уже существует.')
"
```

## Для новых установок

Если вы устанавливаете систему впервые, миграция не требуется. Поле `repair` будет создано автоматически при инициализации базы данных.

## Проверка успешной миграции

После выполнения миграции можно проверить структуру таблицы:

```bash
source venv/bin/activate
python -c "
from project.data.database.database import get_db_session
from sqlalchemy import inspect

with get_db_session() as session:
    inspector = inspect(session.bind)
    columns = inspector.get_columns('monthly_row')
    col_names = [col['name'] for col in columns]
    
    if 'repair' in col_names:
        print('✅ Поле repair успешно добавлено!')
    else:
        print('❌ Поле repair отсутствует!')
"
```

## Откат изменений (если нужно)

Если по какой-то причине требуется откатить изменения:

```bash
source venv/bin/activate
python -c "
from project.data.database.database import get_db_session
from sqlalchemy import text

with get_db_session() as session:
    try:
        session.execute(text('ALTER TABLE monthly_row DROP COLUMN repair'))
        session.commit()
        print('✅ Поле repair удалено!')
    except Exception as e:
        print(f'⚠️ Ошибка: {e}')
"
```

## Обновление кода

После миграции базы данных убедитесь, что обновлены следующие файлы:

1. ✅ `project/data/database/models.py` - добавлено поле `repair`
2. ✅ `project/ui/adapters/streamlit_adapter.py` - методы работы с новым полем
3. ✅ `project/ui/db_utils.py` - обёртки для UI
4. ✅ `project/ui/pages/4_References.py` - продвинутая таблица с колонкой ремонта

## Поддержка

Если возникли проблемы с миграцией, проверьте:
- Используется ли правильное виртуальное окружение
- Доступна ли база данных для записи
- Нет ли конфликтующих версий SQLAlchemy

