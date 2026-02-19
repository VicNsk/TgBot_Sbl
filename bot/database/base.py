# bot/database/base.py
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Database:
    """Управление асинхронным подключением к БД."""

    def __init__(self, db_url: str = "sqlite+aiosqlite:///./bot.db"):
        self.engine = create_async_engine(
            db_url,
            echo=False,
            connect_args={"check_same_thread": False}
        )
        self.async_session = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    async def init_models(self) -> None:
        """Создание таблиц при старте."""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
