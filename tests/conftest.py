# tests/conftest.py
import sys
from pathlib import Path

# Добавляем корень проекта в путь поиска модулей
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Создаем пустой __init__.py в tests, если его нет
init_file = project_root / "tests" / "__init__.py"
if not init_file.exists():
    init_file.touch()
