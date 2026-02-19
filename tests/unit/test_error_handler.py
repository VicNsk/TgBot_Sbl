# tests/unit/test_error_handler.py
import pytest
from aiogram.types import Update
from bot.__main__ import error_handler
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_error_handler_logs_exception(caplog):
    # Создаем фейковую ошибку
    update = Update(update_id=1, message=AsyncMock())
    event = AsyncMock(exception=ValueError("Test error"), update=update)

    # Вызываем обработчик
    await error_handler(event)

    # Проверяем лог
    assert "Critical error: Test error" in caplog.text
    assert "user_id" in caplog.records[0].args["extra"]
