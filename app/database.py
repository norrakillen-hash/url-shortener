from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from app.config import settings
from typing import AsyncGenerator

# Движок (Engine) — сердце подключения к БД
engine = create_async_engine(settings.DATABASE_URL, echo=True)

# Фабрика сессий. Сессия — это "разговор" с БД (запрос -> ответ -> коммит)
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Базовый класс для всех наших моделей (таблиц)
Base = declarative_base()

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
