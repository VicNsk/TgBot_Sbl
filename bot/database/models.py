# bot/database/models.py
from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    UniqueConstraint
)
from .base import Base

class User(Base):
    """Модель пользователя."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, index=True)
    username = Column(String(255), nullable=True)
    is_blocked = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint('telegram_id', name='_user_uc'),
    )

class Blacklist(Base):
    """Модель черного списка."""
    __tablename__ = "blacklist"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True, index=True)
    reason = Column(String(255), nullable=True)
    added_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint('user_id', name='_blacklist_uc'),
    )
