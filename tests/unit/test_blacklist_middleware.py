# tests/unit/test_blacklist_middleware.py
import pytest
from aiogram.types import Message
from bot.middleware.blacklist_middleware import BlacklistMiddleware
from bot.database.repositories import BlacklistRepository
from bot.utils.exceptions import BlacklistError

@pytest.mark.asyncio
async def test_blacklist_middleware_blocked(mock_session, mock_message):
    # Добавляем пользователя в ЧС
    repo = BlacklistRepository(mock_session)
    await repo.add(12345, "test")
    await mock_session.commit()

    # Создаем middleware
    middleware = BlacklistMiddleware()
    data = {"session": mock_session}

    # Пытаемся обработать сообщение от заблокированного пользователя
    with pytest.raises(BlacklistError):
        await middleware(
            lambda m, d: None,  # handler
            mock_message(user_id=12345),
            data
        )
