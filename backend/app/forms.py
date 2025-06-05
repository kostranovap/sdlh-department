from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, BooleanField, EmailField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models import User

class LoginForm(FlaskForm):
    """Форма входа в систему"""
    class Meta:
        csrf = False
    username = StringField('Имя пользователя', validators=[DataRequired()], 
                          render_kw={"placeholder": "Введите имя пользователя"})
    password = PasswordField('Пароль', validators=[DataRequired()],
                           render_kw={"placeholder": "Введите пароль"})
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

class RegistrationForm(FlaskForm):
    """Форма регистрации"""
    class Meta:
        csrf = False
    username = StringField('Имя пользователя', validators=[
        DataRequired(), 
        Length(min=4, max=20, message="Имя пользователя должно быть от 4 до 20 символов")
    ], render_kw={"placeholder": "Придумайте имя пользователя"})
    
    email = EmailField('Email', validators=[DataRequired(), Email()],
                      render_kw={"placeholder": "ваш@email.ru"})
    
    full_name = StringField('Полное имя', validators=[DataRequired()],
                           render_kw={"placeholder": "Фамилия Имя Отчество"})
    
    password = PasswordField('Пароль', validators=[
        DataRequired(),
        Length(min=6, message="Пароль должен быть не менее 6 символов")
    ], render_kw={"placeholder": "Придумайте надежный пароль"})
    
    password2 = PasswordField('Повторите пароль', validators=[
        DataRequired(), 
        EqualTo('password', message="Пароли должны совпадать")
    ], render_kw={"placeholder": "Повторите пароль"})
    
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Это имя пользователя уже занято')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Этот email уже зарегистрирован')

class ServiceApplicationForm(FlaskForm):
    """Форма подачи заявления на услугу"""
    class Meta:
        csrf = False
    service_id = SelectField('Услуга или программа', coerce=str, validators=[DataRequired()])
    
    full_name = StringField('Полное имя', validators=[DataRequired()],
                           render_kw={"placeholder": "Фамилия Имя Отчество"})
    
    email = EmailField('Email', validators=[DataRequired(), Email()],
                      render_kw={"placeholder": "ваш@email.ru"})
    
    phone = StringField('Телефон', validators=[DataRequired()],
                       render_kw={"placeholder": "+7 (___) ___-__-__"})
    
    organization = StringField('Организация (если применимо)',
                              render_kw={"placeholder": "Название организации/ИП"})
    
    description = TextAreaField('Описание заявки', validators=[DataRequired()],
                               render_kw={"placeholder": "Подробно опишите вашу заявку...", "rows": 5})
    
    documents = TextAreaField('Прикрепленные документы',
                             render_kw={"placeholder": "Перечислите документы, которые вы готовы предоставить", "rows": 3})
    
    agree_processing = BooleanField('Согласие на обработку персональных данных')
    
    submit = SubmitField('Подать заявление')

class NewsletterForm(FlaskForm):
    """Форма подписки на новости"""
    class Meta:
        csrf = False
    email = EmailField('Email', validators=[DataRequired(), Email()],
                      render_kw={"placeholder": "ваш@email.ru"})
    
    categories = SelectField('Категории новостей', choices=[
        ('all', 'Все новости'),
        ('programs', 'Программы и инициативы'),
        ('events', 'Мероприятия и события'),
        ('urgent', 'Срочные уведомления')
    ])
    
    agree_processing = BooleanField('Согласие на обработку персональных данных')
    
    submit = SubmitField('Подписаться')

class ChangePasswordForm(FlaskForm):
    """Форма смены пароля"""
    class Meta:
        csrf = False
    old_password = PasswordField('Текущий пароль', validators=[DataRequired()],
                                render_kw={"placeholder": "Введите текущий пароль"})
    
    new_password = PasswordField('Новый пароль', validators=[
        DataRequired(),
        Length(min=6, message="Пароль должен быть не менее 6 символов")
    ], render_kw={"placeholder": "Введите новый пароль"})
    
    new_password2 = PasswordField('Повторите новый пароль', validators=[
        DataRequired(), 
        EqualTo('new_password', message="Пароли должны совпадать")
    ], render_kw={"placeholder": "Повторите новый пароль"})
    
    submit = SubmitField('Изменить пароль') 