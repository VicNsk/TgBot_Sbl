# bot/__main__.py (фрагмент)
from bot.config import Config
from bot.database.base import Database
from bot.database.models import User, Blacklist

from aiogram import Dispatcher
from aiogram.types import ErrorEvent
from bot.utils.logging_setup import get_logger
from bot.utils.exceptions import BlacklistError

logger = get_logger(__name__)

async def main():
    # Инициализация БД
    db = Database()
    await db.init_models()

    # Создание бота и диспетчера
    bot = Bot(token=Config.BOT_TOKEN, parse_mode="HTML")
    dp = Dispatcher()

    # Регистрация обработчиков
    from bot.handlers import user, admin, group
    dp.include_router(user.router)
    dp.include_router(admin.router)
    dp.include_router(group.router)

     # Регистрация middleware
    dp.update.middleware(BlacklistMiddleware())

    # Запуск
    if Config.USE_WEBHOOK:
        # Webhook setup (пока не реализован)
        pass
    else:
        await dp.start_polling(bot)

    # Глобальный обработчик ошибок
    @dp.errors()
    async def error_handler(event: ErrorEvent):
        if isinstance(event.exception, BlacklistError):
            # Не логгируем как ошибку - это штатная ситуация
            logger.info("Blocked request: %s", event.exception)
            return

        logger.exception(
            "Critical error: %s",
            event.exception,
            extra={
                "update": event.update.model_dump_json(),
                "user_id": event.update.effective_user.id if event.update.effective_user else None
            }
        )
