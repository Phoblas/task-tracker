from app.db.session import AsyncSessionLocal  # Фабрика сессий
from typing import AsyncGenerator  # Специальный генератор для асинхронных зависимостей
from sqlalchemy.ext.asyncio import AsyncSession  # Тип возвращаемой сессии

# Зависимость для FastAPI: получить асинхронную сессию БД
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:  # Создаём сессию через контекстный менеджер
        try:
            yield session
            # можно явно вызвать session.commit() при необходимости
        except Exception:
            await session.rollback()  # Откатим изменения в случае ошибки
            raise
        finally:
            await session.close()  # Всегда закрываем соединение (возвращаем в пул)
