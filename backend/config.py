import os
from datetime import timedelta

class Config:
    """Конфигурация для учебного проекта СДЛХ"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-for-sdlh-project'
    
    # Определяем тип базы данных на основе окружения
    if os.environ.get('DATABASE_URL'):
        # Production на Render с PostgreSQL
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
        if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
            SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)
    else:
        # Локальная разработка с MySQL
        MYSQL_HOST = '127.0.0.1'
        MYSQL_PORT = 3306
        MYSQL_USER = 'root'
        MYSQL_PASSWORD = ''  # По умолчанию в XAMPP пароль пустой
        MYSQL_DATABASE = 'sdlh_db'
        SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Отладка выключена для production
    DEBUG = os.environ.get('FLASK_ENV') != 'production'
    
    # Настройки пагинации
    POSTS_PER_PAGE = 5
    
    # Настройки Flask-Login
    REMEMBER_COOKIE_DURATION = timedelta(days=7)
    
    # Настройки загрузки файлов
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB максимальный размер файла
    UPLOAD_FOLDER = 'frontend/static/images/uploads'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    
    # Пути к изображениям
    IMAGES_ARTICLES = 'frontend/static/images/articles'
    IMAGES_NEWS = 'frontend/static/images/news'
    IMAGES_SERVICES = 'frontend/static/images/services'
    IMAGES_GALLERY = 'frontend/static/images/gallery' 