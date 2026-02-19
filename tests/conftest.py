# tests/conftest.py
import sys
from pathlib import Path

# Добавляем корень проекта в путь поиска модулей
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
