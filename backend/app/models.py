from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

class User(UserMixin, db.Model):
    """Модель пользователя"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='user')  # guest, user, admin
    full_name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Связи с указанием foreign_keys для разрешения конфликта
    applications = db.relationship('Application', foreign_keys='Application.user_id', backref='user', lazy='dynamic')
    processed_applications = db.relationship('Application', foreign_keys='Application.processed_by', backref='processor', lazy='dynamic')
    articles = db.relationship('Article', backref='author', lazy='dynamic')
    news = db.relationship('News', backref='author', lazy='dynamic')
    
    def set_password(self, password):
        """Установка хэша пароля"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Проверка пароля"""
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        """Проверка на администратора"""
        return self.role == 'admin'
    
    def __repr__(self):
        return f'<User {self.username}>'

class Article(db.Model):
    """Модель статьи/контента"""
    __tablename__ = 'articles'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    summary = db.Column(db.Text)  # Краткое описание
    page = db.Column(db.String(50), nullable=False, index=True)  # index, about, services...
    category = db.Column(db.String(50))
    image_url = db.Column(db.String(200))
    is_published = db.Column(db.Boolean, default=True)
    is_featured = db.Column(db.Boolean, default=False)  # Важная статья
    view_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def __repr__(self):
        return f'<Article {self.title}>'

class Service(db.Model):
    """Модель услуги департамента"""
    __tablename__ = 'services'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    requirements = db.Column(db.Text)  # Требования для получения
    documents_needed = db.Column(db.Text)  # Необходимые документы
    processing_time = db.Column(db.String(50))  # Срок обработки
    cost = db.Column(db.String(50))  # Стоимость
    responsible_department = db.Column(db.String(100))
    contact_info = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Связи
    applications = db.relationship('Application', backref='service', lazy='dynamic')
    
    def to_dict(self):
        """Конвертация в словарь для JSON"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'requirements': self.requirements,
            'documents_needed': self.documents_needed,
            'processing_time': self.processing_time,
            'cost': self.cost,
            'responsible_department': self.responsible_department,
            'contact_info': self.contact_info,
            'is_active': self.is_active
        }
    
    def __repr__(self):
        return f'<Service {self.name}>'

class Application(db.Model):
    """Модель заявки пользователя"""
    __tablename__ = 'applications'
    
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=True)
    program_id = db.Column(db.Integer, db.ForeignKey('programs.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Тип заявки
    application_type = db.Column(db.String(20), nullable=False)  # 'service' или 'program'
    
    # Данные заявителя
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    organization = db.Column(db.String(200))  # Организация (если есть)
    
    # Содержание заявки - используем JSON для гибкости
    description = db.Column(db.Text)  # Описание заявки
    documents = db.Column(db.Text)  # Прикрепленные документы
    
    # Статус и обработка
    status = db.Column(db.String(20), default='new')  # new, in_progress, approved, rejected
    admin_comment = db.Column(db.Text)
    processed_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Временные метки
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    processed_at = db.Column(db.DateTime)
    
    # Связи
    program = db.relationship('Program', backref='applications')
    
    def __repr__(self):
        return f'<Application {self.id} - {self.full_name}>'

class News(db.Model):
    """Модель новости"""
    __tablename__ = 'news'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    summary = db.Column(db.Text)
    image_url = db.Column(db.String(200))
    is_published = db.Column(db.Boolean, default=True)
    is_important = db.Column(db.Boolean, default=False)  # Важная новость
    view_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def __repr__(self):
        return f'<News {self.title}>'

class Program(db.Model):
    """Модель экологической программы"""
    __tablename__ = 'programs'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    objectives = db.Column(db.Text)  # Цели программы
    requirements = db.Column(db.Text)  # Требования для участия
    benefits = db.Column(db.Text)  # Льготы/преимущества
    duration = db.Column(db.String(50))  # Срок действия
    funding = db.Column(db.String(100))  # Финансирование
    responsible_department = db.Column(db.String(100))
    contact_info = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Конвертация в словарь для JSON"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'objectives': self.objectives,
            'requirements': self.requirements,
            'benefits': self.benefits,
            'duration': self.duration,
            'funding': self.funding,
            'responsible_department': self.responsible_department,
            'contact_info': self.contact_info,
            'is_active': self.is_active
        }
    
    def __repr__(self):
        return f'<Program {self.name}>' 