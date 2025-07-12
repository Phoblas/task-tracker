import asyncio
import os

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from dotenv import load_dotenv

load_dotenv()  # Загружаем переменные окружения из .env

DATABASE_URL = os.getenv("ASYNC_DATABASE_URL")

# Создаем асинхронный движок
engine = create_async_engine(DATABASE_URL, echo=True)


async def main():
    try:
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))  # <-- оборачиваем SQL в text()
            print("✅ Connected to the database. Result:", result.scalar())
    except Exception as e:
        print("❌ Failed to connect to database:", e)


if __name__ == "__main__":
    asyncio.run(main())
