# bot/handlers/user.py
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from bot.utils.logging_setup import get_logger

logger = get_logger(__name__)
router = Router(name="user_handlers")

@router.message(Command("start"))
async def cmd_start(message: Message):
    """Приветственное сообщение при старте."""
    logger.info("User started bot", extra={"user_id": message.from_user.id})
    await message.answer(
        "👋 Добро пожаловать в бот!\n\n"
        "Этот шаблон поддерживает:\n"
        "- Админ-панель (/settings)\n"
        "- Управление черным списком\n"
        "- Обработку групповых чатов"
    )

@router.message(Command("help"))
async def cmd_help(message: Message):
    """Справка по командам."""
    logger.info("User requested help", extra={"user_id": message.from_user.id})
    await message.answer(
        "📚 Доступные команды:\n"
        "/start - начать работу\n"
        "/help - показать эту справку\n\n"
        "🔒 Для администраторов:\n"
        "/settings - админ-панель\n"
        "/blacklist - просмотреть черный список"
    )

@router.message(StateFilter(None), ~F.text.startswith("/"))
async def handle_user_message(message: Message):
    """Обработка текстовых сообщений от пользователей."""
    logger.info(
        "Received message",
        extra={
            "user_id": message.from_user.id,
            "username": message.from_user.username,
            "text": message.text
        }
    )
    await message.answer(
        "📝 Получено сообщение:\n"
        f"👤 <b>Имя:</b> {message.from_user.full_name}\n"
        f"🆔 <b>ID:</b> {message.from_user.id}\n"
        f"💬 <b>Текст:</b> {message.text}"
    )

@router.message(Command("start"))
async def cmd_start(message: Message):
    logger.info(
        "User started bot",
        extra={
            "user_id": message.from_user.id,
            "username": message.from_user.username
        }
    )
    await message.answer("👋 Добро пожаловать в бот!")
