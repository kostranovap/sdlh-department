import os
import sys

# Добавляем backend в путь Python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app import create_app, db
from backend.app.models import User, Article, Service, News, Program, Application
from flask import Blueprint
from datetime import datetime

# Создание экземпляра приложения для Render
app = create_app()

# Временный маршрут для инициализации базы данных
@app.route('/init-database-secret-route-delete-after-use')
def init_database():
    """Инициализация базы данных через браузер"""
    try:
        with app.app_context():
            # Создаем таблицы
            db.create_all()
            
            # Проверяем, есть ли уже данные
            if User.query.first():
                return "База данных уже инициализирована!"
            
            # Создание администратора
            admin = User(
                username='admin',
                email='admin@dlh.gov.ru',
                full_name='Администратор СДЛХ',
                role='admin',
                is_active=True,
                created_at=datetime.utcnow()
            )
            admin.set_password('admin123')
            
            # Создание тестового пользователя
            user = User(
                username='user',
                email='user@example.com',
                full_name='Тестовый пользователь',
                role='user',
                is_active=True,
                created_at=datetime.utcnow()
            )
            user.set_password('user123')
            
            db.session.add(admin)
            db.session.add(user)
            db.session.commit()
            
            # Создание услуг
            services = [
                Service(
                    name='Разрешение на заготовку древесины',
                    description='Получение разрешения на заготовку древесины для физических и юридических лиц',
                    requirements='Документы на право пользования лесным участком',
                    documents_needed='Паспорт, документы на участок, план лесозаготовок',
                    processing_time='30 рабочих дней',
                    cost='Государственная пошлина',
                    responsible_department='Отдел лесопользования',
                    contact_info='Тел: +7 (495) 123-45-67',
                    is_active=True
                ),
                Service(
                    name='Лесопатологическое обследование',
                    description='Проведение обследования лесных участков на предмет болезней и вредителей',
                    requirements='Заявление от собственника участка',
                    documents_needed='Заявление, документы на участок',
                    processing_time='14 рабочих дней',
                    cost='Бесплатно',
                    responsible_department='Отдел защиты леса',
                    contact_info='Тел: +7 (495) 123-45-68',
                    is_active=True
                ),
                Service(
                    name='Согласование проектов строительства',
                    description='Согласование проектов строительства в лесных массивах',
                    requirements='Проектная документация',
                    documents_needed='Проект, экологическая экспертиза',
                    processing_time='45 рабочих дней',
                    cost='По тарифам',
                    responsible_department='Отдел контроля',
                    contact_info='Тел: +7 (495) 123-45-69',
                    is_active=True
                )
            ]
            
            for service in services:
                db.session.add(service)
            
            # Создание программ
            programs = [
                Program(
                    name='Зеленая планета',
                    description='Программа по лесовосстановлению и охране окружающей среды',
                    objectives='Восстановление лесных массивов, экологическое просвещение',
                    requirements='Возраст от 18 лет, экологическое образование приветствуется',
                    benefits='Сертификат участника, льготы при трудоустройстве',
                    duration='Круглогодично',
                    funding='Федеральный бюджет',
                    responsible_department='Отдел экологии',
                    contact_info='ecology@dlh.gov.ru',
                    is_active=True
                ),
                Program(
                    name='Лесные стражи',
                    description='Волонтерская программа по охране лесов от пожаров',
                    objectives='Предотвращение лесных пожаров, патрулирование',
                    requirements='Возраст от 21 года, физическая подготовка',
                    benefits='Обучение, экипировка, страховка',
                    duration='Апрель-октябрь',
                    funding='Региональный бюджет',
                    responsible_department='Служба пожарной безопасности',
                    contact_info='fire@dlh.gov.ru',
                    is_active=True
                )
            ]
            
            for program in programs:
                db.session.add(program)
            
            # Создание новостей
            news_items = [
                News(
                    title='Запуск новой программы лесовосстановления',
                    content='Департамент лесного хозяйства объявляет о запуске масштабной программы лесовосстановления. В рамках программы планируется высадить более 100 тысяч деревьев.',
                    summary='Новая программа направлена на восстановление лесных массивов',
                    is_published=True,
                    is_important=True,
                    author_id=1,
                    created_at=datetime.utcnow()
                ),
                News(
                    title='Итоги работы за первое полугодие',
                    content='Подведены итоги работы департамента за первое полугодие. Выполнены все плановые показатели по лесовосстановлению и охране лесов.',
                    summary='Отчет о работе департамента',
                    is_published=True,
                    is_important=False,
                    author_id=1,
                    created_at=datetime.utcnow()
                ),
                News(
                    title='Профилактика лесных пожаров',
                    content='В связи с наступлением пожароопасного периода департамент напоминает о правилах поведения в лесу и мерах предосторожности.',
                    summary='Важная информация о пожарной безопасности',
                    is_published=True,
                    is_important=True,
                    author_id=1,
                    created_at=datetime.utcnow()
                )
            ]
            
            for news_item in news_items:
                db.session.add(news_item)
            
            # Создание статей
            articles = [
                Article(
                    title='Добро пожаловать на сайт СДЛХ',
                    content='Департамент лесного хозяйства приветствует вас на официальном сайте. Здесь вы найдете всю необходимую информацию о наших услугах.',
                    summary='Приветствие на главной странице',
                    page='index',
                    category='main',
                    is_published=True,
                    author_id=1
                ),
                Article(
                    title='История департамента',
                    content='Департамент лесного хозяйства был создан в 1990 году для управления лесными ресурсами региона.',
                    summary='История создания департамента',
                    page='about',
                    category='history',
                    is_published=True,
                    author_id=1
                ),
                Article(
                    title='Мониторинг лесных пожаров',
                    content='Департамент ведет круглосуточный мониторинг состояния лесов с использованием современных технологий.',
                    summary='Система мониторинга',
                    page='monitoring',
                    category='fire_monitoring',
                    is_published=True,
                    author_id=1
                ),
                Article(
                    title='Экологические инициативы',
                    content='Наш департамент активно участвует в экологических программах по сохранению биоразнообразия.',
                    summary='Экологическая деятельность',
                    page='ecology',
                    category='initiatives',
                    is_published=True,
                    author_id=1
                )
            ]
            
            for article in articles:
                db.session.add(article)
            
            db.session.commit()
            
            return "✅ База данных успешно инициализирована! Теперь можете перейти на главную страницу."
        
    except Exception as e:
        return f"❌ Ошибка инициализации: {str(e)}"

@app.route('/load-mysql-data-secret-route', methods=['POST'])
def load_mysql_data():
    """Загрузка данных из MySQL экспорта"""
    try:
        from flask import request, jsonify
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Нет данных для загрузки'}), 400
        
        with app.app_context():
            # Очищаем существующие данные
            db.session.query(Application).delete()
            db.session.query(News).delete()
            db.session.query(Article).delete()
            db.session.query(Program).delete()
            db.session.query(Service).delete()
            db.session.query(User).delete()
            db.session.commit()
            
            loaded_counts = {}
            
            # Загружаем пользователей
            if 'users' in data:
                for user_data in data['users']:
                    user = User(
                        username=user_data['username'],
                        email=user_data['email'],
                        full_name=user_data.get('full_name', ''),
                        role=user_data.get('role', 'user'),
                        is_active=user_data.get('is_active', True),
                        created_at=datetime.fromisoformat(user_data['created_at'].replace('Z', '+00:00')) if user_data.get('created_at') else datetime.utcnow()
                    )
                    # Устанавливаем пароль (он уже хэширован в базе)
                    user.password_hash = user_data.get('password_hash', '')
                    db.session.add(user)
                loaded_counts['users'] = len(data['users'])
            
            # Загружаем услуги
            if 'services' in data:
                for service_data in data['services']:
                    service = Service(
                        name=service_data['name'],
                        description=service_data.get('description', ''),
                        requirements=service_data.get('requirements', ''),
                        documents_needed=service_data.get('documents_needed', ''),
                        processing_time=service_data.get('processing_time', ''),
                        cost=service_data.get('cost', ''),
                        responsible_department=service_data.get('responsible_department', ''),
                        contact_info=service_data.get('contact_info', ''),
                        is_active=service_data.get('is_active', True),
                        created_at=datetime.fromisoformat(service_data['created_at'].replace('Z', '+00:00')) if service_data.get('created_at') else datetime.utcnow()
                    )
                    db.session.add(service)
                loaded_counts['services'] = len(data['services'])
            
            # Загружаем программы
            if 'programs' in data:
                for program_data in data['programs']:
                    program = Program(
                        name=program_data['name'],
                        description=program_data.get('description', ''),
                        objectives=program_data.get('objectives', ''),
                        requirements=program_data.get('requirements', ''),
                        benefits=program_data.get('benefits', ''),
                        duration=program_data.get('duration', ''),
                        funding=program_data.get('funding', ''),
                        responsible_department=program_data.get('responsible_department', ''),
                        contact_info=program_data.get('contact_info', ''),
                        is_active=program_data.get('is_active', True),
                        created_at=datetime.fromisoformat(program_data['created_at'].replace('Z', '+00:00')) if program_data.get('created_at') else datetime.utcnow()
                    )
                    db.session.add(program)
                loaded_counts['programs'] = len(data['programs'])
            
            # Загружаем новости
            if 'news' in data:
                for news_data in data['news']:
                    news = News(
                        title=news_data['title'],
                        content=news_data.get('content', ''),
                        summary=news_data.get('summary', ''),
                        image_url=news_data.get('image_url', ''),
                        is_published=news_data.get('is_published', True),
                        is_important=news_data.get('is_important', False),
                        view_count=news_data.get('view_count', 0),
                        author_id=news_data.get('author_id', 1),
                        created_at=datetime.fromisoformat(news_data['created_at'].replace('Z', '+00:00')) if news_data.get('created_at') else datetime.utcnow(),
                        updated_at=datetime.fromisoformat(news_data['updated_at'].replace('Z', '+00:00')) if news_data.get('updated_at') else datetime.utcnow()
                    )
                    db.session.add(news)
                loaded_counts['news'] = len(data['news'])
            
            # Загружаем статьи
            if 'articles' in data:
                for article_data in data['articles']:
                    article = Article(
                        title=article_data['title'],
                        content=article_data.get('content', ''),
                        summary=article_data.get('summary', ''),
                        page=article_data.get('page', ''),
                        category=article_data.get('category', ''),
                        is_published=article_data.get('is_published', True),
                        author_id=article_data.get('author_id', 1),
                        created_at=datetime.fromisoformat(article_data['created_at'].replace('Z', '+00:00')) if article_data.get('created_at') else datetime.utcnow(),
                        updated_at=datetime.fromisoformat(article_data['updated_at'].replace('Z', '+00:00')) if article_data.get('updated_at') else datetime.utcnow()
                    )
                    db.session.add(article)
                loaded_counts['articles'] = len(data['articles'])
            
            # Загружаем заявления
            if 'applications' in data:
                for app_data in data['applications']:
                    application = Application(
                        full_name=app_data['full_name'],
                        email=app_data.get('email', ''),
                        phone=app_data.get('phone', ''),
                        service_id=app_data.get('service_id'),
                        program_id=app_data.get('program_id'),
                        message=app_data.get('message', ''),
                        status=app_data.get('status', 'pending'),
                        created_at=datetime.fromisoformat(app_data['created_at'].replace('Z', '+00:00')) if app_data.get('created_at') else datetime.utcnow()
                    )
                    db.session.add(application)
                loaded_counts['applications'] = len(data['applications'])
            
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Данные успешно загружены!',
                'loaded': loaded_counts
            })
        
    except Exception as e:
        return jsonify({'error': f'Ошибка загрузки данных: {str(e)}'}), 500

if __name__ == '__main__':
    # Для локальной разработки
    app.run(host='127.0.0.1', port=5000, debug=True) 