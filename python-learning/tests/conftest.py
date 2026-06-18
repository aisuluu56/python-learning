"""
Настройка путей для тестов
"""

import sys
import os

# Добавляем путь к папке python_syntax_practice
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
python_syntax_path = os.path.join(project_root, "python_syntax_practice")

if python_syntax_path not in sys.path:
    sys.path.insert(0, python_syntax_path)

if project_root not in sys.path:
    sys.path.insert(0, project_root)