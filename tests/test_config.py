# tests/test_config.py
import json
import logging
import pytest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from bot.config import Config

@pytest.fixture
def temp_env_file(tmp_path):
    """Создает временный .env файл с минимальной конфигурацией"""
    env_file = tmp_path / ".env"
    # ВСЕГДА добавляем BOT_TOKEN, кроме тестов, проверяющих его отсутствие
    env_file.write_text("BOT_TOKEN=test_token\n")
    yield env_file
    if env_file.exists():
        env_file.unlink()

def test_valid_config(temp_env_file):
    """Проверка валидной конфигурации"""
    temp_env_file.write_text(
        "BOT_TOKEN=test_token\n"
        'ADMINS=[123456789, 987654321]\n'
        "USE_WEBHOOK=True\n"
        "LOG_LEVEL=DEBUG"
    )

    Config.load(str(temp_env_file))

    assert Config.BOT_TOKEN == "test_token"
    assert Config.ADMINS == [123456789, 987654321]
    assert Config.USE_WEBHOOK is True
    assert Config.LOG_LEVEL == logging.DEBUG

def test_invalid_admins_format(temp_env_file):
    """Проверка обработки невалидного JSON в ADMINS"""
    # Добавляем только проблемный параметр, BOT_TOKEN уже есть из фикстуры
    temp_env_file.write_text(
        "BOT_TOKEN=test_token\n"
        'ADMINS="not a json"'  # Невалидный JSON
    )

    with pytest.raises(ValueError, match="Invalid ADMINS format"):
        Config.load(str(temp_env_file))

def test_missing_bot_token(tmp_path):
    """Проверка отсутствия BOT_TOKEN"""
    env_file = tmp_path / ".env"
    env_file.write_text('ADMINS=[]')

    with pytest.raises(ValueError, match="BOT_TOKEN must be set"):
        Config.load(str(env_file))

def test_type_conversions(temp_env_file):
    """Проверка конвертации типов"""
    temp_env_file.write_text(
        "BOT_TOKEN=test_token\n"  # Обязательный параметр
        "USE_WEBHOOK=  true \n"
        "LOG_LEVEL=WARNING"
    )
    Config.load(str(temp_env_file))

    assert Config.USE_WEBHOOK is True
    assert Config.LOG_LEVEL == logging.WARNING
