#!/usr/bin/env sh
# entrypoint.sh

# Ждём БД (опционально через pg_isready)
# until pg_isready -h $POSTGRES_HOST -p $POSTGRES_PORT; do
#   echo "Waiting for postgres..."
#   sleep 2
# done

# Прогоняем миграции
alembic upgrade head

# Стартуем Uvicorn
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
