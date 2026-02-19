# bot/handlers/group.py
from aiogram import Router
from aiogram.types import Message, ChatMemberUpdated
from aiogram.filters import ChatMemberUpdatedFilter, IS_NOT_MEMBER, IS_MEMBER, Command
from bot.utils.logging_setup import get_logger

logger = get_logger(__name__)
router = Router(name="group_handlers")

@router.my_chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def bot_added_to_group(event: ChatMemberUpdated):
    """Приветствие при добавлении бота в группу."""
    logger.info(
        "Bot added to group",
        extra={"group_id": event.chat.id, "user_id": event.from_user.id}
    )
    await event.answer(
        "🤖 Я добавлен в группу!\n"
        "Теперь я могу:\n"
        "- Приветствовать новых участников\n"
        "- Обрабатывать текстовые сообщения"
    )

@router.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def welcome_new_member(event: ChatMemberUpdated):
    """Приветствие новых участников."""
    if event.new_chat_member.user.is_bot:
        return  # Игнорируем ботов

    logger.info(
        "New member joined",
        extra={"group_id": event.chat.id, "user_id": event.new_chat_member.user.id}
    )
    await event.answer(
        f"👋 Добро пожаловать, {event.new_chat_member.user.mention}!\n"
        "Напишите что-нибудь, чтобы начать общение."
    )

@router.message(~F.chat.type.in_({"private"}), ~F.text.startswith("/"), ~F.is_bot)
async def handle_group_message(message: Message):
    """Обработка сообщений в групповых чатах."""
    logger.info(
        "Group message received",
        extra={
            "group_id": message.chat.id,
            "user_id": message.from_user.id,
            "text": message.text
        }
    )
    await message.reply(
        "💬 Я вижу ваше сообщение!\n"
        f"👤 От: {message.from_user.full_name}\n"
        f"📝 Текст: {message.text}"
    )
