# tests/unit/test_logging.py
import logging
from io import StringIO
from bot.utils.logging_setup import ContextualFormatter, setup_logging, get_logger
import os
from bot.config import Config

def test_log_format():
    stream = StringIO()
    handler = logging.StreamHandler(stream)
    formatter = ContextualFormatter(
        "[%(levelname)s] [%(asctime)s] [%(name)s] — %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)

    logger = logging.getLogger("test_logger")
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    logger.info("Test message", extra={"user_id": 123, "data": "test"})

    log_output = stream.getvalue().strip()
    assert "[INFO]" in log_output
    assert "test_logger" in log_output
    assert "Test message (user_id=123, data=test)" in log_output


def test_log_rotation(tmp_path):
    # Настраиваем временный путь
    log_file = tmp_path / "bot.log"
    orig_handler = logging.FileHandler
    logging.FileHandler = lambda *args, **kwargs: orig_handler(log_file, *args[1:], **kwargs)

    try:
        setup_logging()

        # Заполняем лог до 11 МБ
        logger = logging.getLogger("rotation_test")
        large_msg = "A" * 1000
        for _ in range(11000):
            logger.info(large_msg)

        # Проверяем ротацию
        assert os.path.exists(log_file)
        assert any(f.startswith("bot.log.") for f in os.listdir(tmp_path))
    finally:
        logging.FileHandler = orig_handler


def test_log_level_from_env(monkeypatch):
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    Config.load()

    logger = get_logger("level_test")
    assert logger.getEffectiveLevel() == logging.DEBUG

    monkeypatch.setenv("LOG_LEVEL", "WARNING")
    Config.load()
    assert logger.getEffectiveLevel() == logging.WARNING

