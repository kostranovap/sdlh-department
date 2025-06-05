import os
import sys

# Добавляем backend в путь Python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app import create_app

# Создание экземпляра приложения
app = create_app()

if __name__ == '__main__':
    # Для локальной разработки
    app.run(host='127.0.0.1', port=5000, debug=True) 