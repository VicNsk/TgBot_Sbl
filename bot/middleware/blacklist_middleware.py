# bot/middleware/blacklist_middleware.py
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery
from bot.database.repositories import BlacklistRepository
from bot.utils.exceptions import BlacklistError

class BlacklistMiddleware(BaseMiddleware):
    """Проверяет пользователя на наличие в черном списке."""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        # Определяем user_id из события
        user_id = None
        if isinstance(event, Message):
            user_id = event.from_user.id
        elif isinstance(event, CallbackQuery):
            user_id = event.from_user.id

        if user_id is None:
            return await handler(event, data)

        # Проверка в черном списке
        blacklist_repo = BlacklistRepository(data["session"])
        if await blacklist_repo.is_blocked(user_id):
            logger = data.get("logger")
            if logger:
                logger.warning(
                    "Blocked request from blacklisted user",
                    extra={"user_id": user_id}
                )
            raise BlacklistError(f"User {user_id} is blacklisted")

        return await handler(event, data)
