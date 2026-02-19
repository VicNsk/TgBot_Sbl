# tests/unit/test_models.py
from bot.database.models import User, Blacklist

def test_model_structure():
    """Проверка корректности структуры ORM-моделей"""
    # Проверка модели User
    assert User.__tablename__ == "users"
    assert hasattr(User, "telegram_id")
    assert User.__table__.columns["telegram_id"].unique is True
    assert User.__table__.columns["is_blocked"].default.arg is False

    # Проверка модели Blacklist
    assert Blacklist.__tablename__ == "blacklist"
    assert Blacklist.__table__.columns["user_id"].unique is True
    assert "reason" in Blacklist.__table__.columns
    assert "added_at" in Blacklist.__table__.columns
