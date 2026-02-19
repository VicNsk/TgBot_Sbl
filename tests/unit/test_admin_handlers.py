# tests/unit/test_admin_handlers.py
async def test_blacklist_add(mock_message, mock_session):
    msg = mock_message(text="/blacklist add 12345")
    await cmd_blacklist_add(msg, mock_session)

    # Проверка добавления в БД
    result = await mock_session.execute("SELECT * FROM blacklist WHERE user_id=12345")
    assert result.fetchone() is not None
    assert "добавлен в ЧС" in msg.answer.call_args[0][0]

async def test_blacklist_add_duplicate(mock_message, mock_session):
    # Сначала добавляем
    await cmd_blacklist_add(mock_message(text="/blacklist add 12345"), mock_session)

    # Пытаемся добавить дубликат
    await cmd_blacklist_add(mock_message(text="/blacklist add 12345"), mock_session)
    assert "уже в черном списке" in mock_message().answer.call_args[0][0]
