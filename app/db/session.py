from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine  # Асинхронный движок и сессия
from sqlalchemy.orm import sessionmaker  # Фабрика сессий

from app.core.config import settings  # 🔗 импортируем конфигурацию


# Создаём асинхронный SQLAlchemy Engine
async_engine = create_async_engine(
    settings.ASYNC_DATABASE_URL,  # строка подключения к PostgreSQL
    echo=True  # логируем SQL-запросы в stdout (удобно для отладки)
)

# Создаём асинхронную фабрику сессий — на базе AsyncSession
AsyncSessionLocal = sessionmaker(
    bind=async_engine,  # используем наш асинхронный engine
    expire_on_commit=False,  # не инвалидировать объекты после commit (реже ошибки)
    class_=AsyncSession  # обязательно: использовать AsyncSession, а не обычный Session
)