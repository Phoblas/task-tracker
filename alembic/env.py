from logging.config import fileConfig
from sqlalchemy.ext.asyncio import AsyncEngine

from alembic import context
import asyncio
import os

from dotenv import load_dotenv
load_dotenv()

from app.db.base import Base
from app.db.session import async_engine
from app.core.config import settings  # добавь импорт

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

target_metadata = Base.metadata


def run_migrations_offline():
    """Запуск миграций в offline-режиме."""
    url = os.environ["DATABASE_URL"]
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """Асинхронный запуск миграций."""
    connectable: AsyncEngine = async_engine

    async with connectable.begin() as connection:
        await connection.run_sync(
            lambda sync_conn: context.configure(
                connection=sync_conn,
                target_metadata=target_metadata,
                compare_type=True,  # сравнивать типы столбцов (например, String(50) vs String(100))
            )
        )

        # run_migrations без аргументов
        await connection.run_sync(lambda conn: context.run_migrations())


def run():
    if context.is_offline_mode():
        run_migrations_offline()
    else:
        asyncio.run(run_migrations_online())


run()
