# app/core/config.py

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Настройки приложения, загружаемые из .env или переменных окружения.
    Использует Pydantic v2 BaseSettings (pydantic-settings) для валидации и документирования.
    """

    # 🔐 Секретный ключ для подписи JWT-токенов
    SECRET_KEY: str = Field(
        ..., env="SECRET_KEY", description="Секретный ключ для подписи JWT"
    )

    # 🔒 Алгоритм подписи токенов (по умолчанию HS256)
    ALGORITHM: str = Field(
        "HS256", env="ALGORITHM", description="Алгоритм подписи JWT"
    )

    # ⏱ Время жизни access-токена в минутах
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        30, env="ACCESS_TOKEN_EXPIRE_MINUTES", description="Время жизни access-токена (мин)"
    )

    # 🐘 Синхронный URL для Alembic и/или sync SQLAlchemy движков
    DATABASE_URL: str = Field(
        ..., env="DATABASE_URL", description="Синхронный URL для SQLAlchemy/Alembic"
    )

    # 🐼 Асинхронный URL для FastAPI + async SQLAlchemy
    ASYNC_DATABASE_URL: str = Field(
        ..., env="ASYNC_DATABASE_URL", description="Асинхронный URL для SQLAlchemy"
    )

    # ⚡️ Redis брокер очередей для Celery
    REDIS_BROKER_URL: str = Field(
        ..., env="REDIS_BROKER_URL", description="URL брокера (Redis) для Celery"
    )

    # 📦 Redis backend для хранения результатов Celery
    REDIS_BACKEND_URL: str = Field(
        ..., env="REDIS_BACKEND_URL", description="URL backend (Redis) для результатов Celery"
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        # case_sensitive = True  # при необходимости чувствительность к регистру

# Экземпляр настроек для импорта в любом месте приложения
settings = Settings()
