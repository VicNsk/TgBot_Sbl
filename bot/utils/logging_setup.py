# bot/utils/logging_setup.py
import logging
import sys
from logging.handlers import RotatingFileHandler
from bot.config import Config

# Стандартные атрибуты LogRecord (исключаем из extra)
STANDARD_ATTRS = {
    'args', 'asctime', 'created', 'exc_info', 'exc_text', 'filename',
    'funcName', 'levelname', 'levelno', 'lineno', 'module', 'msecs',
    'msg', 'message', 'name', 'pathname', 'process', 'processName',
    'relativeCreated', 'stack_info', 'thread', 'threadName'
}

class ContextualFormatter(logging.Formatter):
    """Кастомный форматтер с поддержкой extra-параметров."""

    def format(self, record: logging.LogRecord) -> str:
        # Форматируем стандартное сообщение
        log_message = super().format(record)

        # Собираем extra-поля
        extra_fields = []
        for key, value in record.__dict__.items():
            if key not in STANDARD_ATTRS and value is not None:
                extra_fields.append(f"{key}={value}")

        # Добавляем extra в конец сообщения
        if extra_fields:
            return f"{log_message} ({', '.join(extra_fields)})"
        return log_message

def setup_logging() -> None:
    """Настройка глобального логгера."""
    logger = logging.getLogger()
    logger.setLevel(Config.LOG_LEVEL)

    # Формат: [УРОВЕНЬ] [ВРЕМЯ] [МОДУЛЬ] — Сообщение
    log_format = "[%(levelname)s] [%(asctime)s] [%(name)s] — %(message)s"
    formatter = ContextualFormatter(
        fmt=log_format,
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Консольный обработчик
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Файловый обработчик с ротацией
    file_handler = RotatingFileHandler(
        "bot.log",
        maxBytes=10 * 1024 * 1024,  # 10 МБ
        backupCount=5,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Убираем дублирование логов
    logger.propagate = False

def get_logger(name: str) -> logging.Logger:
    """Возвращает настроенный логгер с указанным именем."""
    return logging.getLogger(name)
