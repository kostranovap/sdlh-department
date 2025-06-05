from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
import os

# Инициализация расширений
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    """Создание Flask приложения для учебного проекта"""
    app = Flask(__name__, 
                template_folder='../../frontend/templates',
                static_folder='../../frontend/static')
    
    # Загрузка конфигурации
    app.config.from_object(Config)
    
    # Инициализация расширений
    db.init_app(app)
    login_manager.init_app(app)
    
    # Настройка Flask-Login
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Для доступа к этой странице необходимо войти в систему.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        from .models import User
        return User.query.get(int(user_id))
    
    # Маршрут для обслуживания загруженных файлов
    @app.route('/static/uploads/<path:filename>')
    def uploaded_file(filename):
        upload_path = os.path.join(app.root_path, '..', 'frontend', 'static', 'uploads')
        return send_from_directory(upload_path, filename)
    
    # Добавляем функции в контекст шаблонов
    @app.context_processor
    def utility_processor():
        from .utils import get_image_url
        return dict(get_image_url=get_image_url)
    
    # Добавляем фильтр для переносов строк
    @app.template_filter('nl2br')
    def nl2br_filter(text):
        """Конвертирует переносы строк в HTML"""
        if text is None:
            return ''
        return text.replace('\n', '<br>')
    
    # Создаем папки для изображений при инициализации
    with app.app_context():
        from .utils import ensure_upload_folders
        ensure_upload_folders()
    
    # Регистрация Blueprint'ов
    from .routes.main import main
    from .routes.auth import auth
    from .routes.admin import admin
    
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(admin, url_prefix='/admin')
    
    return app 