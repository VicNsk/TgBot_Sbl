# tests/unit/test_group_handlers.py
async def test_bot_added_to_group(mock_chat_member_updated):
    event = mock_chat_member_updated(
        old_status="left",
        new_status="member"
    )
    await bot_added_to_group(event)
    assert "добавлен в группу" in event.answer.call_args[0][0]

async def test_new_member_welcome(mock_chat_member_updated):
    event = mock_chat_member_updated(
        old_status="left",
        new_status="member",
        user_is_bot=False
    )
    await welcome_new_member(event)
    assert "Добро пожаловать" in event.answer.call_args[0][0]

async def test_ignore_bot_in_group(mock_message):
    msg = mock_message(chat_type="group", is_bot=True)
    await handle_group_message(msg)
    assert msg.reply.called is False  # Боты игнорируются
