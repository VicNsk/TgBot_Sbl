# tests/test_imports.py
import pytest

def test_imports():
    """Проверка базовых импортов"""
    import bot.config
    import bot.database.repositories
    import bot.utils.exceptions
    import bot.handlers.admin
    import bot.middleware.blacklist_middleware

    assert True  # Если импорты прошли, тест пройден
