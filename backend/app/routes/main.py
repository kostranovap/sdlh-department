from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from sqlalchemy import or_
from app import db
from app.models import User, Article, Service, Application, News, Program
from app.forms import ServiceApplicationForm, NewsletterForm

# Создание blueprint для основных страниц
main = Blueprint('main', __name__)

@main.route('/')
def index():
    """Главная страница"""
    # Получаем 3 случайные новости
    from sqlalchemy import func
    latest_news = News.query.filter_by(is_published=True).order_by(
        func.random()
    ).limit(3).all()
    
    # Получаем важные новости
    important_news = News.query.filter_by(
        is_published=True, 
        is_important=True
    ).order_by(News.created_at.desc()).limit(3).all()
    
    # Получаем популярные услуги
    popular_services = Service.query.filter_by(is_active=True).limit(6).all()
    
    # Статистика лесов
    forest_stats = {
        'total_area': '2.3 млн',
        'protected_areas': '156',
        'reforested': '45.2 тыс',
        'fires_prevented': '98.5%'
    }
    
    return render_template('pages/index.html',
                         latest_news=latest_news,
                         important_news=important_news,
                         popular_services=popular_services,
                         forest_stats=forest_stats)

@main.route('/about')
def about():
    """О департаменте"""
    # Получаем статьи для страницы "О департаменте"
    articles = Article.query.filter_by(page='about', is_published=True).all()
    
    # Получаем исторические новости для timeline (важные новости, отсортированные по дате создания)
    history_news = News.query.filter_by(
        is_published=True, 
        is_important=True
    ).order_by(News.created_at.asc()).limit(10).all()
    
    return render_template('pages/about.html', articles=articles, history_news=history_news)

@main.route('/info', methods=['GET', 'POST'])
def info():
    """Информация - услуги и программы"""
    form = ServiceApplicationForm()
    
    # Получаем все услуги и программы
    services_list = Service.query.filter_by(is_active=True).all()
    programs_list = Program.query.filter_by(is_active=True).all()
    
    # Преобразуем в словари для JSON
    services_dict = [service.to_dict() for service in services_list]
    programs_dict = [program.to_dict() for program in programs_list]
    
    # Заполняем выбор в форме (услуги + программы)
    choices = []
    for service in services_list:
        choices.append((f"service_{service.id}", f"Услуга: {service.name}"))
    for program in programs_list:
        choices.append((f"program_{program.id}", f"Программа: {program.name}"))
    
    form.service_id.choices = choices
    
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash('Для подачи заявления необходимо войти в систему', 'warning')
            # Возвращаем на ту же страницу с сообщением и JS откроет модальное окно
            return render_template('pages/info.html', 
                                 services=services_dict,
                                 programs=programs_dict,
                                 form=form,
                                 show_login_modal=True)
        
        # Определяем тип заявки
        selection = form.service_id.data
        if selection.startswith('service_'):
            application_type = 'service'
            service_id = int(selection.replace('service_', ''))
            program_id = None
        else:
            application_type = 'program'
            program_id = int(selection.replace('program_', ''))
            service_id = None
        
        # Создание заявления
        application = Application(
            application_type=application_type,
            service_id=service_id,
            program_id=program_id,
            user_id=current_user.id,
            full_name=form.full_name.data,
            email=form.email.data,
            phone=form.phone.data,
            organization=form.organization.data,
            description=form.description.data,
            documents=form.documents.data,
            status='new'
        )
        
        try:
            db.session.add(application)
            db.session.commit()
            flash('Заявление успешно подано! Вы можете отследить его статус в личном кабинете.', 'success')
            return redirect(url_for('auth.profile'))
        except Exception as e:
            db.session.rollback()
            flash('Произошла ошибка при подаче заявления. Попробуйте еще раз.', 'error')
    
    return render_template('pages/info.html', 
                         services=services_dict,
                         programs=programs_dict,
                         form=form)

@main.route('/monitoring')
def monitoring():
    """Мониторинг лесов"""
    # Здесь можно добавить реальные данные мониторинга
    monitoring_data = {
        'fire_danger_class': 'II',
        'temperature': '+18°C',
        'humidity': '65%',
        'wind_speed': '12 м/с',
        'last_update': '03.01.2025 14:30',
        'active_fires': '2',
        'controlled_area': '1.2 тыс. га',
        'extinguished_fires': '1',
        'healthy_forests': '89.3%',
        'damaged_areas': '7.2%',
        'recovering_areas': '3.5%'
    }
    
    articles = Article.query.filter_by(page='monitoring', is_published=True).all()
    
    # Получаем последние важные новости для предупреждений (последние 5)
    alert_news = News.query.filter_by(
        is_published=True, 
        is_important=True
    ).order_by(News.created_at.desc()).limit(5).all()
    
    return render_template('pages/monitoring.html', 
                         articles=articles,
                         alert_news=alert_news,
                         **monitoring_data)

@main.route('/news')
def news():
    """Список новостей"""
    page = request.args.get('page', 1, type=int)
    sort = request.args.get('sort', 'new')  # 'new' - сначала новые, 'old' - сначала старые
    
    # Определяем порядок сортировки
    if sort == 'old':
        order = News.created_at.asc()
    else:  # sort == 'new' по умолчанию
        order = News.created_at.desc()
    
    news_items = News.query.filter_by(is_published=True).order_by(
        News.is_important.desc(), order
    ).paginate(page=page, per_page=6, error_out=False)
    
    return render_template('news.html', news_items=news_items, current_sort=sort)

@main.route('/news/<int:id>')
def news_detail(id):
    """Просмотр отдельной новости"""
    news_item = News.query.filter_by(id=id, is_published=True).first_or_404()
    
    # Увеличиваем счетчик просмотров
    news_item.view_count += 1
    db.session.commit()
    
    # Получаем похожие новости (последние 3)
    related_news = News.query.filter(
        News.id != id,
        News.is_published == True
    ).order_by(News.created_at.desc()).limit(3).all()
    
    return render_template('news_detail.html', 
                         news_item=news_item, 
                         related_news=related_news)

@main.route('/sitemap')
def sitemap():
    """Карта сайта"""
    # Статистика сайта
    stats = {
        'total_pages': '5',
        'total_news': News.query.filter_by(is_published=True).count(),
        'last_update': '03.01.2025',
        'total_services': Service.query.filter_by(is_active=True).count()
    }
    
    return render_template('pages/sitemap.html', **stats)

@main.route('/newsletter', methods=['POST'])
def newsletter():
    """Подписка на новости"""
    form = NewsletterForm()
    
    if form.validate_on_submit():
        # Здесь можно добавить логику подписки
        flash('Вы успешно подписались на новости!', 'success')
    else:
        flash('Ошибка при подписке. Проверьте введенные данные.', 'error')
    
    return redirect(request.referrer or url_for('main.index'))

# API маршруты для AJAX запросов
@main.route('/api/search')
def api_search():
    """API поиска для выпадающего меню"""
    query = request.args.get('q', '').strip()
    if len(query) < 2:
        return jsonify([])
    
    results = []
    
    # Поиск в новостях
    news_results = News.query.filter(
        News.title.contains(query),
        News.is_published == True
    ).limit(5).all()
    
    for news in news_results:
        results.append({
            'title': news.title,
            'type': 'Новость',
            'url': url_for('main.news_detail', id=news.id),
            'icon': '📰'
        })
    
    # Поиск в услугах  
    service_results = Service.query.filter(
        Service.name.contains(query),
        Service.is_active == True
    ).limit(5).all()
    
    for service in service_results:
        results.append({
            'title': service.name,
            'type': 'Услуга',
            'url': url_for('main.info'),
            'icon': '📋'
        })
    
    # Добавляем страницы сайта
    pages = [
        {'title': 'О департаменте', 'url': url_for('main.about'), 'icon': '🏢'},
        {'title': 'Подача заявлений', 'url': url_for('main.info'), 'icon': '📝'},
        {'title': 'Мониторинг лесов', 'url': url_for('main.monitoring'), 'icon': '🌲'},
        {'title': 'Новости', 'url': url_for('main.news'), 'icon': '📰'},
        {'title': 'Карта сайта', 'url': url_for('main.sitemap'), 'icon': '🗺️'},
    ]
    
    for page in pages:
        if query.lower() in page['title'].lower():
            results.append({
                'title': page['title'],
                'type': 'Страница',
                'url': page['url'],
                'icon': page['icon']
            })
    
    return jsonify(results[:8])

@main.route('/api/stats')
def api_stats():
    """API для получения статистики"""
    stats = {
        'total_users': User.query.count(),
        'total_applications': Application.query.count(),
        'total_news': News.query.filter_by(is_published=True).count(),
        'total_services': Service.query.filter_by(is_active=True).count()
    }
    return jsonify(stats)

# Обработчик ошибки 404
@main.app_errorhandler(404)
def not_found_error(error):
    """Страница ошибки 404"""
    return render_template('pages/404.html'), 404