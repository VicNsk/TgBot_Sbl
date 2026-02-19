# tests/unit/test_admin_filter.py
from bot.handlers.admin import AdminFilter
from aiogram.types import Message, User

def test_admin_filter():
    # Создаем фейковое сообщение
    message = Message(
        message_id=1,
        date=0,
        from_user=User(id=12345, is_bot=False, first_name="Test"),
        chat=AsyncMock()
    )

    # Тест 1: Не админ
    filter = AdminFilter()
    message.from_user.id = 99999
    assert filter(message) is False

    # Тест 2: Админ
    message.from_user.id = Config.ADMINS[0]
    assert filter(message) is True
