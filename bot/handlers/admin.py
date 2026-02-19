# bot/handlers/admin.py
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from bot.config import Config

router = Router(name="admin_handlers")

class AdminFilter:
    """Проверяет, является ли пользователь администратором."""
    def __init__(self):
        self.admin_ids = Config.ADMINS

    def __call__(self, message: Message) -> bool:
        return message.from_user.id in self.admin_ids

@router.message(AdminFilter(), Command("settings"))
async def cmd_settings(message: Message):
    """Админ-панель (только для администраторов)."""
    await message.answer("⚙️ Админ-панель:\n"
                        "/blacklist - просмотреть ЧС\n"
                        "/blacklist add <id> - добавить в ЧС\n"
                        "/blacklist remove <id> - удалить из ЧС")
