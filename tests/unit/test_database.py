# tests/unit/test_database.py
import pytest
from bot.database.base import Database
from bot.database.models import User, Blacklist

@pytest.mark.asyncio
async def test_db_init():
    db = Database("sqlite+aiosqlite:///:memory:")
    await db.init_models()

    # Проверка создания таблиц
    async with db.engine.begin() as conn:
        result = await conn.run_sync(
            lambda sync_conn: sync_conn.dialect.has_table(sync_conn, "users")
        )
        assert result is True

        result = await conn.run_sync(
            lambda sync_conn: sync_conn.dialect.has_table(sync_conn, "blacklist")
        )
        assert result is True
