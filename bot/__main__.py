# bot/__main__.py (фрагмент)
from bot.config import Config
from bot.database.base import Database
from bot.database.models import User, Blacklist

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

    # Запуск
    if Config.USE_WEBHOOK:
        # Webhook setup (пока не реализован)
        pass
    else:
        await dp.start_polling(bot)
