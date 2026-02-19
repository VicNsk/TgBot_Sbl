# tests/unit/test_user_handlers.py
from aiogram.types import Message
from bot.handlers.user import cmd_start, cmd_help, handle_user_message

async def test_cmd_start(mock_message, caplog):
    await cmd_start(mock_message())
    assert "Добро пожаловать в бот!" in mock_message().answer.call_args[0][0]
    assert "User started bot" in caplog.text

async def test_handle_message(mock_message, caplog):
    msg = mock_message(text="Test message")
    await handle_user_message(msg)
    assert "Получено сообщение:" in msg.answer.call_args[0][0]
    assert "Test message" in caplog.text
