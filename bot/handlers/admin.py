# bot/handlers/admin.py
from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from bot.config import Config
from bot.database.repositories import BlacklistRepository
from bot.utils.exceptions import BlacklistError

router = Router(name="admin_handlers")

class AdminFilter:
    def __init__(self):
        self.admin_ids = Config.ADMINS

    def __call__(self, message: Message) -> bool:
        return message.from_user.id in self.admin_ids

@router.message(AdminFilter(), Command("settings"))
async def cmd_settings(message: Message):
    await message.answer("⚙️ Админ-панель")

@router.message(AdminFilter(), Command("blacklist"))
async def cmd_blacklist(message: Message, session: AsyncSession):
    """Просмотр черного списка."""
    repo = BlacklistRepository(session)
    blocked_users = await repo.get_all()

    if not blocked_users:
        await message.answer("✅ Черный список пуст")
        return

    response = "📛 Черный список:\n"
    for user in blocked_users[:20]:  # Ограничение для безопасности
        response += f"• {user.user_id} (причина: {user.reason or 'не указана'})\n"

    if len(blocked_users) > 20:
        response += f"\n... и еще {len(blocked_users) - 20} пользователей"

    await message.answer(response)

@router.message(AdminFilter(), F.text.startswith("/blacklist add"))
async def cmd_blacklist_add(message: Message, session: AsyncSession):
    """Добавление в черный список."""
    try:
        user_id = int(message.text.split()[3])
    except (IndexError, ValueError):
        await message.answer("❌ Неверный формат команды. Используйте:\n/blacklist add <user_id>")
        return

    repo = BlacklistRepository(session)
    try:
        await repo.add(user_id, "Добавлен через админ-панель")
        await session.commit()
        await message.answer(f"✅ Пользователь {user_id} добавлен в ЧС")
    except BlacklistError as e:
        await message.answer(f"⚠️ {str(e)}")

@router.message(AdminFilter(), F.text.startswith("/blacklist remove"))
async def cmd_blacklist_remove(message: Message, session: AsyncSession):
    """Удаление из черного списка."""
    try:
        user_id = int(message.text.split()[3])
    except (IndexError, ValueError):
        await message.answer("❌ Неверный формат команды. Используйте:\n/blacklist remove <user_id>")
        return

    repo = BlacklistRepository(session)
    if await repo.remove(user_id):
        await session.commit()
        await message.answer(f"✅ Пользователь {user_id} удален из ЧС")
    else:
        await message.answer(f"⚠️ Пользователь {user_id} не найден в ЧС")
