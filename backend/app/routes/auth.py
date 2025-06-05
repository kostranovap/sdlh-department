from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User, Application
from app.forms import LoginForm, RegistrationForm
from urllib.parse import urlparse

# Создание blueprint для авторизации
auth = Blueprint('auth', __name__, url_prefix='/auth')

# Страницы входа и регистрации удалены - используются модальные окна

@auth.route('/logout')
@login_required
def logout():
    """Выход из системы"""
    logout_user()
    flash('Вы успешно вышли из системы', 'info')
    return redirect(url_for('main.index'))

@auth.route('/profile')
@login_required
def profile():
    """Профиль пользователя"""
    # Получаем заявления пользователя
    user_applications = Application.query.filter_by(user_id=current_user.id).order_by(
        Application.created_at.desc()
    ).limit(10).all()
    
    return render_template('auth/profile.html', 
                         user_applications=user_applications, 
                         applications=user_applications)

@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Смена пароля"""
    from app.forms import ChangePasswordForm
    form = ChangePasswordForm()
    
    if form.validate_on_submit():
        if current_user.check_password(form.old_password.data):
            current_user.set_password(form.new_password.data)
            try:
                db.session.commit()
                flash('Пароль успешно изменен', 'success')
                return redirect(url_for('auth.profile'))
            except Exception as e:
                db.session.rollback()
                flash('Ошибка при изменении пароля', 'error')
        else:
            flash('Неверный текущий пароль', 'error')
    
    return render_template('auth/change_password.html', title='Смена пароля', form=form)

# AJAX маршруты для модальных окон
@auth.route('/ajax/login', methods=['POST'])
def ajax_login():
    """AJAX вход в систему"""
    if current_user.is_authenticated:
        return jsonify({'success': False, 'message': 'Вы уже авторизованы'})
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            
            # Определяем страницу для перенаправления
            next_page = request.form.get('next') or url_for('main.index')
            if urlparse(next_page).netloc != '':
                next_page = url_for('main.index')
            
            return jsonify({
                'success': True, 
                'message': f'Добро пожаловать, {user.full_name or user.username}!',
                'redirect': next_page
            })
        else:
            return jsonify({'success': False, 'message': 'Неверное имя пользователя или пароль'})
    
    # Собираем ошибки валидации
    errors = []
    for field, field_errors in form.errors.items():
        for error in field_errors:
            errors.append(f"{form[field].label.text}: {error}")
    
    return jsonify({'success': False, 'message': '; '.join(errors) if errors else 'Неверные данные'})

@auth.route('/ajax/register', methods=['POST'])
def ajax_register():
    """AJAX регистрация"""
    if current_user.is_authenticated:
        return jsonify({'success': False, 'message': 'Вы уже авторизованы'})
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            full_name=form.full_name.data,
            role='user'
        )
        user.set_password(form.password.data)
        
        try:
            db.session.add(user)
            db.session.commit()
            return jsonify({
                'success': True, 
                'message': 'Регистрация прошла успешно! Теперь вы можете войти в систему.',
                'show_login': True  # Флаг для показа формы входа
            })
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': 'Произошла ошибка при регистрации. Попробуйте еще раз.'})
    
    # Собираем ошибки валидации
    errors = []
    for field, field_errors in form.errors.items():
        for error in field_errors:
            errors.append(f"{form[field].label.text}: {error}")
    
    return jsonify({'success': False, 'message': '; '.join(errors) if errors else 'Неверные данные'}) 