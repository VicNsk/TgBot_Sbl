# bot/config.py
import json
import logging
from typing import List
from dotenv import dotenv_values

class Config:
    """Безопасная загрузка и валидация переменных окружения."""

    BOT_TOKEN: str
    ADMINS: List[int]
    USE_WEBHOOK: bool
    LOG_LEVEL: int

    @classmethod
    def load(cls, env_file: str = ".env") -> None:
        """
        Загрузка конфигурации из указанного файла.

        Args:
            env_file: Путь к .env файлу (по умолчанию ".env")
        """
        env = dotenv_values(env_file)

        # Обязательные параметры
        if not (token := env.get("BOT_TOKEN")):
            raise ValueError("BOT_TOKEN must be set in .env")
        cls.BOT_TOKEN = token

        # Парсинг ADMINS
        try:
            cls.ADMINS = json.loads(env.get("ADMINS", "[]"))
            if not isinstance(cls.ADMINS, list):
                raise ValueError("ADMINS must be a JSON array")
        except json.JSONDecodeError:
            raise ValueError("Invalid ADMINS format in .env")

        # Конвертация USE_WEBHOOK
        cls.USE_WEBHOOK = env.get("USE_WEBHOOK", "False").strip().lower() == "true"

        # Настройка уровня логирования
        log_level = env.get("LOG_LEVEL", "INFO").upper()
        cls.LOG_LEVEL = getattr(logging, log_level, logging.INFO)
