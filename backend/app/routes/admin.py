from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from flask_login import login_required, current_user
from functools import wraps
from app import db
from app.models import User, Article, Service, Application, News, Program
from ..utils import save_image, delete_image, get_image_url, ensure_upload_folders
from datetime import datetime

admin = Blueprint('admin', __name__)

def admin_required(f):
    """Декоратор для проверки прав администратора"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('Доступ запрещен. Требуются права администратора.', 'error')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@admin.route('/')
@login_required
@admin_required
def dashboard():
    """Главная страница админки"""
    # Создаем папки для изображений при первом запуске
    ensure_upload_folders()
    
    users_count = User.query.count()
    articles_count = Article.query.count()
    services_count = Service.query.count()
    applications_count = Application.query.count()
    news_count = News.query.count()
    
    # Последние заявки
    recent_applications = Application.query.order_by(Application.created_at.desc()).limit(5).all()
    
    stats = {
        'users': users_count,
        'articles': articles_count,
        'services': services_count,
        'applications': applications_count,
        'news': news_count
    }
    
    return render_template('admin/dashboard.html', stats=stats, recent_applications=recent_applications)

@admin.route('/users', methods=['GET', 'POST'])
@login_required
@admin_required
def users():
    """Управление пользователями"""
    if request.method == 'POST':
        # Создание нового пользователя
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        full_name = request.form.get('full_name', '').strip()
        password = request.form.get('password', '').strip()
        role = request.form.get('role', 'user')
        
        # Базовая валидация
        if not username or not email or not password:
            flash('Все поля обязательны для заполнения', 'error')
        elif User.query.filter_by(username=username).first():
            flash('Пользователь с таким логином уже существует', 'error')
        elif User.query.filter_by(email=email).first():
            flash('Пользователь с таким email уже существует', 'error')
        else:
            try:
                new_user = User(
                    username=username,
                    email=email,
                    full_name=full_name,
                    role=role
                )
                new_user.set_password(password)
                
                db.session.add(new_user)
                db.session.commit()
                
                flash(f'Пользователь {username} успешно создан', 'success')
            except Exception as e:
                db.session.rollback()
                flash('Ошибка при создании пользователя', 'error')
        
        return redirect(url_for('admin.users'))
    
    page = request.args.get('page', 1, type=int)
    users = User.query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    return render_template('admin/users.html', users=users)

@admin.route('/articles')
@login_required
@admin_required
def articles():
    """Управление статьями"""
    page = request.args.get('page', 1, type=int)
    articles = Article.query.order_by(Article.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    return render_template('admin/articles.html', articles=articles)

@admin.route('/articles/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_article():
    """Добавление новой статьи"""
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        summary = request.form.get('summary', '')
        page = request.form['page']
        category = request.form.get('category', '')
        is_featured = 'is_featured' in request.form
        
        # Обработка загруженного изображения
        image_url = None
        if 'image' in request.files:
            image_file = request.files['image']
            if image_file.filename != '':
                image_url = save_image(image_file, 'articles', resize_width=800)
                if not image_url:
                    flash('Ошибка при загрузке изображения', 'error')
                    return render_template('admin/add_article.html')
        
        article = Article(
            title=title,
            content=content,
            summary=summary,
            page=page,
            category=category,
            is_featured=is_featured,
            image_url=image_url,
            author_id=current_user.id
        )
        
        db.session.add(article)
        db.session.commit()
        
        flash('Статья успешно добавлена', 'success')
        return redirect(url_for('admin.articles'))
    
    return render_template('admin/add_article.html')

@admin.route('/articles/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_article(id):
    """Редактирование статьи"""
    article = Article.query.get_or_404(id)
    
    if request.method == 'POST':
        article.title = request.form['title']
        article.content = request.form['content']
        article.summary = request.form.get('summary', '')
        article.page = request.form['page']
        article.category = request.form.get('category', '')
        article.is_featured = 'is_featured' in request.form
        
        # Обработка нового изображения
        if 'image' in request.files:
            image_file = request.files['image']
            if image_file.filename != '':
                # Удаляем старое изображение
                if article.image_url:
                    delete_image(article.image_url)
                
                # Сохраняем новое
                new_image_url = save_image(image_file, 'articles', resize_width=800)
                if new_image_url:
                    article.image_url = new_image_url
                else:
                    flash('Ошибка при загрузке изображения', 'error')
        
        db.session.commit()
        flash('Статья успешно обновлена', 'success')
        return redirect(url_for('admin.articles'))
    
    return render_template('admin/edit_article.html', article=article)

@admin.route('/articles/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_article(id):
    """Удаление статьи"""
    article = Article.query.get_or_404(id)
    
    # Удаляем изображение
    if article.image_url:
        delete_image(article.image_url)
    
    db.session.delete(article)
    db.session.commit()
    
    flash('Статья успешно удалена', 'success')
    return redirect(url_for('admin.articles'))

@admin.route('/news')
@login_required
@admin_required
def news():
    """Управление новостями"""
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', 'all')
    
    # Фильтрация новостей
    query = News.query
    if status == 'published':
        query = query.filter_by(is_published=True)
    elif status == 'draft':
        query = query.filter_by(is_published=False)
    elif status == 'important':
        query = query.filter_by(is_important=True)
    
    news_items = query.order_by(News.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
    return render_template('admin/news.html', 
                         news_items=news_items,
                         current_status=status)

@admin.route('/news/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_news():
    """Создание новости"""
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        is_published = request.form.get('is_published') == 'on'
        is_important = request.form.get('is_important') == 'on'
        
        # Обработка загрузки изображения с помощью универсальной функции
        image_url = None
        if 'image' in request.files and request.files['image'].filename:
            image_file = request.files['image']
            image_url = save_image(image_file, 'news', resize_width=800)
            
            if not image_url:
                flash('Ошибка при загрузке изображения. Проверьте формат файла.', 'error')
                return render_template('admin/create_news.html')
        
        news_item = News(
            title=title,
            content=content,
            summary=None,
            image_url=image_url,
            is_published=is_published,
            is_important=is_important,
            author_id=current_user.id
        )
        
        try:
            db.session.add(news_item)
            db.session.commit()
            flash('Новость успешно создана!', 'success')
            return redirect(url_for('admin.news'))
        except Exception as e:
            db.session.rollback()
            flash('Ошибка при создании новости', 'error')
            print(f"Ошибка создания новости: {e}")
    
    return render_template('admin/create_news.html')

@admin.route('/news/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_news(id):
    """Редактирование новости"""
    news_item = News.query.get_or_404(id)
    
    if request.method == 'POST':
        news_item.title = request.form.get('title')
        news_item.content = request.form.get('content')
        news_item.is_published = request.form.get('is_published') == 'on'
        news_item.is_important = request.form.get('is_important') == 'on'
        
        # Обработка загрузки нового изображения
        if 'image' in request.files and request.files['image'].filename:
            image_file = request.files['image']
            new_image_url = save_image(image_file, 'news', resize_width=800)
            
            if new_image_url:
                # Удаляем старое изображение
                if news_item.image_url:
                    delete_image(news_item.image_url)
                
                news_item.image_url = new_image_url
            else:
                flash('Ошибка при загрузке нового изображения', 'warning')
        
        news_item.updated_at = datetime.utcnow()
        
        try:
            db.session.commit()
            flash('Новость успешно обновлена!', 'success')
            return redirect(url_for('admin.news'))
        except Exception as e:
            db.session.rollback()
            flash('Ошибка при обновлении новости', 'error')
            print(f"Ошибка обновления новости: {e}")
    
    return render_template('admin/edit_news.html', news_item=news_item)

@admin.route('/news/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_news(id):
    """Удаление новости"""
    news_item = News.query.get_or_404(id)
    
    # Удаляем изображение если есть
    if news_item.image_url:
        delete_image(news_item.image_url)
    
    try:
        db.session.delete(news_item)
        db.session.commit()
        flash('Новость успешно удалена!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Ошибка при удалении новости', 'error')
        print(f"Ошибка удаления новости: {e}")
    
    return redirect(url_for('admin.news'))

@admin.route('/upload_image', methods=['POST'])
@login_required
@admin_required
def upload_image():
    """AJAX загрузка изображения"""
    if 'image' not in request.files:
        return jsonify({'success': False, 'error': 'Файл не выбран'})
    
    image_file = request.files['image']
    category = request.form.get('category', 'uploads')
    resize_width = request.form.get('resize_width', type=int)
    
    if image_file.filename == '':
        return jsonify({'success': False, 'error': 'Файл не выбран'})
    
    image_url = save_image(image_file, category, resize_width=resize_width)
    
    if image_url:
        return jsonify({
            'success': True, 
            'image_url': image_url,
            'full_url': get_image_url(image_url)
        })
    else:
        return jsonify({'success': False, 'error': 'Ошибка при загрузке изображения'})

@admin.route('/services')
@login_required
@admin_required
def services():
    """Управление услугами"""
    page = request.args.get('page', 1, type=int)
    services = Service.query.order_by(Service.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    # Добавляем пустую пагинацию для программ, чтобы шаблон не падал
    programs = Program.query.order_by(Program.created_at.desc()).paginate(
        page=1, per_page=10, error_out=False
    )
    return render_template('admin/services.html', services=services, programs=programs)

@admin.route('/services_programs')
@login_required
@admin_required
def services_programs():
    """Объединенная страница услуг и программ"""
    page = request.args.get('page', 1, type=int)
    services = Service.query.order_by(Service.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    programs = Program.query.order_by(Program.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    return render_template('admin/services.html', services=services, programs=programs)

@admin.route('/services/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_service():
    """Добавление новой услуги"""
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        requirements = request.form.get('requirements', '')
        documents_needed = request.form.get('documents_needed', '')
        processing_time = request.form.get('processing_time', '')
        cost = request.form.get('cost', '')
        responsible_department = request.form.get('responsible_department', '')
        contact_info = request.form.get('contact_info', '')
        is_active = 'is_active' in request.form
        
        service = Service(
            name=name,
            description=description,
            requirements=requirements,
            documents_needed=documents_needed,
            processing_time=processing_time,
            cost=cost,
            responsible_department=responsible_department,
            contact_info=contact_info,
            is_active=is_active
        )
        
        try:
            db.session.add(service)
            db.session.commit()
            flash('Услуга успешно добавлена', 'success')
            return redirect(url_for('admin.services_programs'))
        except Exception as e:
            db.session.rollback()
            flash('Ошибка при добавлении услуги', 'error')
    
    return render_template('admin/add_service.html')

@admin.route('/services/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_service(id):
    """Редактирование услуги"""
    service = Service.query.get_or_404(id)
    
    if request.method == 'POST':
        service.name = request.form['name']
        service.description = request.form['description']
        service.requirements = request.form.get('requirements', '')
        service.documents_needed = request.form.get('documents_needed', '')
        service.processing_time = request.form.get('processing_time', '')
        service.cost = request.form.get('cost', '')
        service.responsible_department = request.form.get('responsible_department', '')
        service.contact_info = request.form.get('contact_info', '')
        service.is_active = 'is_active' in request.form
        
        try:
            db.session.commit()
            flash('Услуга успешно обновлена', 'success')
            return redirect(url_for('admin.services_programs'))
        except Exception as e:
            db.session.rollback()
            flash('Ошибка при обновлении услуги', 'error')
    
    return render_template('admin/edit_service.html', service=service)

@admin.route('/services/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_service(id):
    """Удаление услуги"""
    service = Service.query.get_or_404(id)
    
    try:
        db.session.delete(service)
        db.session.commit()
        flash('Услуга успешно удалена', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Ошибка при удалении услуги', 'error')
    
    return redirect(url_for('admin.services_programs'))

@admin.route('/programs/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_program():
    """Добавление новой программы"""
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        objectives = request.form.get('objectives', '')
        requirements = request.form.get('requirements', '')
        benefits = request.form.get('benefits', '')
        duration = request.form.get('duration', '')
        funding = request.form.get('funding', '')
        responsible_department = request.form.get('responsible_department', '')
        contact_info = request.form.get('contact_info', '')
        is_active = 'is_active' in request.form
        
        program = Program(
            name=name,
            description=description,
            objectives=objectives,
            requirements=requirements,
            benefits=benefits,
            duration=duration,
            funding=funding,
            responsible_department=responsible_department,
            contact_info=contact_info,
            is_active=is_active
        )
        
        try:
            db.session.add(program)
            db.session.commit()
            flash('Программа успешно добавлена', 'success')
            return redirect(url_for('admin.services_programs'))
        except Exception as e:
            db.session.rollback()
            flash('Ошибка при добавлении программы', 'error')
    
    return render_template('admin/add_program.html')

@admin.route('/programs/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_program(id):
    """Редактирование программы"""
    program = Program.query.get_or_404(id)
    
    if request.method == 'POST':
        program.name = request.form['name']
        program.description = request.form['description']
        program.objectives = request.form.get('objectives', '')
        program.requirements = request.form.get('requirements', '')
        program.benefits = request.form.get('benefits', '')
        program.duration = request.form.get('duration', '')
        program.funding = request.form.get('funding', '')
        program.responsible_department = request.form.get('responsible_department', '')
        program.contact_info = request.form.get('contact_info', '')
        program.is_active = 'is_active' in request.form
        
        try:
            db.session.commit()
            flash('Программа успешно обновлена', 'success')
            return redirect(url_for('admin.services_programs'))
        except Exception as e:
            db.session.rollback()
            flash('Ошибка при обновлении программы', 'error')
    
    return render_template('admin/edit_program.html', program=program)

@admin.route('/programs/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_program(id):
    """Удаление программы"""
    program = Program.query.get_or_404(id)
    
    try:
        db.session.delete(program)
        db.session.commit()
        flash('Программа успешно удалена', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Ошибка при удалении программы', 'error')
    
    return redirect(url_for('admin.services_programs'))

@admin.route('/applications')
@login_required
@admin_required
def applications():
    """Управление заявлениями"""
    page = request.args.get('page', 1, type=int)
    
    # Получаем все заявления без фильтрации
    applications = Application.query.order_by(Application.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('admin/applications.html', applications=applications)

@admin.route('/applications/<int:id>/approve', methods=['POST'])
@login_required
@admin_required
def approve_application(id):
    """Одобрение заявления"""
    application = Application.query.get_or_404(id)
    
    if application.status in ['new', 'in_progress']:
        application.status = 'approved'
        application.processed_at = datetime.utcnow()
        application.admin_comment = f"Заявление одобрено администратором {current_user.full_name}"
        
        try:
            db.session.commit()
            flash(f'Заявление #{application.id} успешно одобрено', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Ошибка при одобрении заявления', 'error')
    else:
        flash('Заявление уже обработано', 'warning')
    
    return redirect(url_for('admin.applications'))

@admin.route('/applications/<int:id>/reject', methods=['POST'])
@login_required
@admin_required
def reject_application(id):
    """Отклонение заявления"""
    application = Application.query.get_or_404(id)
    
    if application.status in ['new', 'in_progress']:
        application.status = 'rejected'
        application.processed_at = datetime.utcnow()
        application.admin_comment = f"Заявление отклонено администратором {current_user.full_name}"
        
        try:
            db.session.commit()
            flash(f'Заявление #{application.id} отклонено', 'info')
        except Exception as e:
            db.session.rollback()
            flash('Ошибка при отклонении заявления', 'error')
    else:
        flash('Заявление уже обработано', 'warning')
    
    return redirect(url_for('admin.applications')) 