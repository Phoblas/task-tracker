import asyncio
import pytest
from testcontainers.postgres import PostgresContainer
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.db.deps import get_db as real_get_db
from app.main import app

# 1) Поднимаем контейнер PostgreSQL
@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer("postgres:16") as pg:
        pg.start()
        yield pg


# 2) Создаём AsyncEngine и AsyncSessionLocal на базе контейнера
@pytest.fixture(scope="session")
async def async_engine(postgres_container: PostgresContainer):
    url = postgres_container.get_connection_url().replace("postgresql://", "postgresql+asyncpg://")
    engine = create_async_engine(url, echo=False)

    # создаём все таблицы
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    await engine.dispose()


@pytest.fixture(scope="function")
async def db_session(async_engine):
    """Каждый тест получает чистую транзакцию и откатывает её по окончании."""
    AsyncSessionLocal = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)
    async with AsyncSessionLocal() as session:
        yield session
        await session.rollback()


# 3) Override get_db для FastAPI
@pytest.fixture(scope="function")
def client(db_session, monkeypatch):
    async def _get_test_db():
        yield db_session
    
    monkeypatch.setattr(real_get_db.__module__, "get_db", _get_test_db)

    from httpx import AsyncClient
    return AsyncClient(app=app, base_url="http://testserver")