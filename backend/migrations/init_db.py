"""
Скрипт инициализации базы данных для проекта СДЛХ
Создает таблицы и заполняет их тестовыми данными
"""
import sys
import os

# Добавляем путь к родительской папке для импорта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.models import db, User, Article, Service, News, Application
from datetime import datetime

def create_database():
    """Создание всех таблиц"""
    print("Создание таблиц базы данных...")
    db.create_all()
    print("✅ Таблицы созданы успешно!")

def create_admin_user():
    """Создание администратора"""
    print("Создание администратора...")
    
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@sdlh.ru',
            full_name='Администратор СДЛХ',
            role='admin',
            phone='+7-999-123-45-67'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        print("✅ Администратор создан: admin / admin123")
    else:
        print("⚠️ Администратор уже существует")

def create_test_users():
    """Создание тестовых пользователей"""
    print("Создание тестовых пользователей...")
    
    users_data = [
        {
            'username': 'user1',
            'email': 'user1@test.ru',
            'full_name': 'Иван Петров',
            'role': 'user',
            'phone': '+7-999-111-11-11'
        },
        {
            'username': 'user2', 
            'email': 'user2@test.ru',
            'full_name': 'Мария Сидорова',
            'role': 'user',
            'phone': '+7-999-222-22-22'
        }
    ]
    
    for user_data in users_data:
        if not User.query.filter_by(username=user_data['username']).first():
            user = User(**user_data)
            user.set_password('123456')
            db.session.add(user)
            print(f"✅ Пользователь создан: {user_data['username']} / 123456")

def create_services():
    """Создание услуг департамента"""
    print("Создание услуг департамента...")
    
    services_data = [
        {
            'name': 'Разрешение на вырубку деревьев',
            'description': 'Получение разрешения на санитарную или плановую вырубку деревьев',
            'requirements': 'Заявление, план участка, обоснование необходимости',
            'documents_needed': 'Паспорт, документы на участок, план территории',
            'processing_time': '10 рабочих дней',
            'cost': 'Бесплатно',
            'responsible_department': 'Отдел лесопользования',
            'contact_info': 'Тел: +7-999-100-10-01, email: trees@sdlh.ru'
        },
        {
            'name': 'Аренда лесного участка',
            'description': 'Оформление договора аренды лесного участка для заготовки древесины',
            'requirements': 'Юридическое лицо, лицензия на лесозаготовку',
            'documents_needed': 'Устав организации, лицензии, финансовые гарантии',
            'processing_time': '30 рабочих дней',
            'cost': 'Согласно тарифам',
            'responsible_department': 'Отдел лесных договоров',
            'contact_info': 'Тел: +7-999-100-10-02, email: rent@sdlh.ru'
        },
        {
            'name': 'Лесопатологическое обследование',
            'description': 'Проведение обследования лесных насаждений на предмет болезней и вредителей',
            'requirements': 'Заявление от землевладельца или арендатора',
            'documents_needed': 'Заявление, план участка',
            'processing_time': '14 рабочих дней',
            'cost': 'Бесплатно для физ. лиц',
            'responsible_department': 'Отдел лесозащиты',
            'contact_info': 'Тел: +7-999-100-10-03, email: protection@sdlh.ru'
        },
        {
            'name': 'Согласование строительства в лесных зонах',
            'description': 'Получение согласования на строительство объектов в лесной зоне',
            'requirements': 'Проект строительства, экологическая экспертиза',
            'documents_needed': 'Проект, разрешения, экспертизы',
            'processing_time': '45 рабочих дней',
            'cost': 'Согласно тарифам',
            'responsible_department': 'Отдел строительства',
            'contact_info': 'Тел: +7-999-100-10-04, email: build@sdlh.ru'
        },
        {
            'name': 'Восстановление лесов',
            'description': 'Консультации и поддержка по восстановлению лесных массивов',
            'requirements': 'Заявление, план восстановления',
            'documents_needed': 'Заявление, план участка, проект восстановления',
            'processing_time': '20 рабочих дней',
            'cost': 'Частичное финансирование',
            'responsible_department': 'Отдел лесовосстановления',
            'contact_info': 'Тел: +7-999-100-10-05, email: restore@sdlh.ru'
        }
    ]
    
    for service_data in services_data:
        if not Service.query.filter_by(name=service_data['name']).first():
            service = Service(**service_data)
            db.session.add(service)
            print(f"✅ Услуга создана: {service_data['name']}")

def create_articles():
    """Создание статей для страниц"""
    print("Создание статей...")
    
    admin = User.query.filter_by(username='admin').first()
    
    # Пути к тестовым изображениям (можно добавить реальные позже)
    sample_images = {
        'index': [
            'images/articles/welcome.jpg',
            'images/articles/mission.jpg',
            'images/articles/services.jpg',
            'images/articles/ecology.jpg',
            'images/articles/contacts.jpg'
        ],
        'about': [
            'images/articles/history.jpg',
            'images/articles/structure.jpg',
            'images/articles/management.jpg',
            'images/articles/achievements.jpg',
            'images/articles/plans.jpg'
        ],
        'services': [
            'images/articles/digital_services.jpg',
            'images/articles/consulting.jpg',
            'images/articles/licensing.jpg',
            'images/articles/monitoring.jpg',
            'images/articles/reference.jpg'
        ],
        'monitoring': [
            'images/articles/satellite.jpg',
            'images/articles/fires.jpg',
            'images/articles/logging.jpg',
            'images/articles/ecological.jpg',
            'images/articles/restoration.jpg'
        ],
        'ecology': [
            'images/articles/biodiversity.jpg',
            'images/articles/pollution.jpg',
            'images/articles/education.jpg',
            'images/articles/research.jpg',
            'images/articles/cooperation.jpg'
        ]
    }
    
    articles_data = [
        # Статьи для главной страницы
        {
            'title': 'Добро пожаловать на сайт СДЛХ',
            'content': 'Департамент лесного хозяйства обеспечивает охрану, защиту и рациональное использование лесных ресурсов региона. Наша основная задача - сохранение природного богатства для будущих поколений.',
            'summary': 'Приветствие на официальном сайте департамента',
            'page': 'index',
            'category': 'info',
            'is_featured': True,
            'image_url': sample_images['index'][0]
        },
        {
            'title': 'Наша миссия',
            'content': 'Сохранение лесных богатств для будущих поколений через устойчивое лесопользование и экологическое просвещение. Мы стремимся к гармонии между потребностями человека и природы.',
            'summary': 'Основные цели и задачи департамента',
            'page': 'index',
            'category': 'mission',
            'image_url': sample_images['index'][1]
        },
        {
            'title': 'Услуги департамента',
            'content': 'Мы предоставляем широкий спектр услуг от выдачи разрешений до консультаций по лесовосстановлению. Все услуги доступны в электронном виде.',
            'summary': 'Обзор предоставляемых услуг',
            'page': 'index',
            'category': 'services',
            'image_url': sample_images['index'][2]
        },
        {
            'title': 'Экологическая безопасность',
            'content': 'Департамент активно работает над сохранением экологического баланса и борьбой с нарушениями. Мониторинг состояния лесов ведется круглосуточно.',
            'summary': 'Вопросы экологической безопасности',
            'page': 'index',
            'category': 'ecology',
            'image_url': sample_images['index'][3]
        },
        {
            'title': 'Контактная информация',
            'content': 'Наши специалисты готовы ответить на ваши вопросы и предоставить необходимые консультации. Работаем с понедельника по пятницу с 9:00 до 18:00.',
            'summary': 'Как связаться с департаментом',
            'page': 'index',
            'category': 'contacts',
            'image_url': sample_images['index'][4]
        },
        
        # Статьи для страницы "О департаменте"
        {
            'title': 'История создания департамента',
            'content': 'Департамент лесного хозяйства был создан в 1985 году для координации лесохозяйственной деятельности в регионе. За годы работы накоплен богатый опыт в области лесного хозяйства.',
            'summary': 'Краткая история создания и развития',
            'page': 'about',
            'category': 'history',
            'image_url': sample_images['about'][0]
        },
        {
            'title': 'Структура департамента',
            'content': 'В состав департамента входят 5 отделов: лесопользования, лесозащиты, лесовосстановления, строительства и контроля. Каждый отдел отвечает за свое направление деятельности.',
            'summary': 'Организационная структура',
            'page': 'about',
            'category': 'structure',
            'image_url': sample_images['about'][1]
        },
        {
            'title': 'Руководство',
            'content': 'Департамент возглавляет Иванов И.И., кандидат сельскохозяйственных наук с 20-летним опытом работы в области лесного хозяйства.',
            'summary': 'Информация о руководящем составе',
            'page': 'about',
            'category': 'management',
            'image_url': sample_images['about'][2]
        },
        {
            'title': 'Достижения и награды',
            'content': 'За годы работы департамент неоднократно отмечался на федеральном уровне за эффективную работу по сохранению и восстановлению лесных ресурсов.',
            'summary': 'Основные достижения департамента',
            'page': 'about',
            'category': 'achievements',
            'image_url': sample_images['about'][3]
        },
        {
            'title': 'Планы развития',
            'content': 'На ближайшие 5 лет запланировано внедрение цифровых технологий и расширение программ лесовосстановления. Планируется увеличить площадь восстановленных лесов на 25%.',
            'summary': 'Стратегические планы развития',
            'page': 'about',
            'category': 'plans',
            'image_url': sample_images['about'][4]
        }
    ]
    
    # Добавляем статьи для остальных страниц (services, monitoring, ecology)
    pages_content = {
        'services': [
            ('Электронные услуги', 'Переход на цифровые технологии в предоставлении государственных услуг'),
            ('Консультационные услуги', 'Бесплатные консультации специалистов по вопросам лесного хозяйства'),
            ('Лицензирование', 'Порядок получения лицензий на различные виды лесохозяйственной деятельности'),
            ('Мониторинг заявок', 'Система отслеживания статуса поданных заявок в режиме реального времени'),
            ('Справочная информация', 'База знаний с ответами на часто задаваемые вопросы')
        ],
        'monitoring': [
            ('Спутниковый мониторинг лесов', 'Система наблюдения за состоянием лесных массивов с использованием спутниковых данных'),
            ('Мониторинг лесных пожаров', 'Система раннего обнаружения и контроля лесных пожаров'),
            ('Контроль вырубок', 'Мониторинг законности проводимых лесозаготовительных работ'),
            ('Экологический мониторинг', 'Наблюдение за экологическим состоянием лесных экосистем'),
            ('Мониторинг восстановления', 'Контроль эффективности мероприятий по лесовосстановлению')
        ],
        'ecology': [
            ('Программы сохранения биоразнообразия', 'Инициативы по защите редких видов флоры и фауны'),
            ('Борьба с загрязнением лесов', 'Мероприятия по очистке лесных территорий от мусора и загрязнений'),
            ('Экологическое просвещение', 'Образовательные программы для населения о важности лесных экосистем'),
            ('Научные исследования', 'Поддержка исследований в области лесной экологии'),
            ('Международное сотрудничество', 'Участие в международных экологических проектах и программах')
        ]
    }
    
    idx = 0
    for page, content_list in pages_content.items():
        for title, summary in content_list:
            articles_data.append({
                'title': title,
                'content': f'{summary}. Подробная информация о {title.lower()} и практические рекомендации по данной теме.',
                'summary': summary,
                'page': page,
                'category': 'info',
                'image_url': sample_images[page][idx % 5]
            })
            idx += 1
    
    for article_data in articles_data:
        if not Article.query.filter_by(title=article_data['title']).first():
            article = Article(**article_data)
            article.author_id = admin.id
            db.session.add(article)
            print(f"✅ Статья создана: {article_data['title']}")

def create_news():
    """Создание новостей"""
    print("Создание новостей...")
    
    admin = User.query.filter_by(username='admin').first()
    
    # Пути к изображениям новостей
    news_images = [
        'images/news/reforestation.jpg',
        'images/news/digital.jpg',
        'images/news/monitoring.jpg',
        'images/news/ecology.jpg',
        'images/news/regulations.jpg'
    ]
    
    news_data = [
        {
            'title': 'Запуск новой программы лесовосстановления',
            'content': 'Департамент объявляет о запуске масштабной программы восстановления лесов, пострадавших от пожаров. Программа рассчитана на 3 года и предусматривает восстановление 1000 га лесных массивов.',
            'summary': 'Новая программа поможет восстановить 1000 га лесных массивов',
            'is_important': True,
            'image_url': news_images[0]
        },
        {
            'title': 'Внедрение цифровых технологий',
            'content': 'С 1 июня все услуги департамента будут доступны в электронном виде через портал госуслуг. Это значительно упростит процедуру получения разрешений и справок.',
            'summary': 'Цифровизация услуг для удобства граждан',
            'is_important': True,
            'image_url': news_images[1]
        },
        {
            'title': 'Результаты мониторинга за весенний период',
            'content': 'По итогам весеннего мониторинга выявлено снижение количества нарушений лесного законодательства на 15%. Улучшение показателей связано с усилением контроля и просветительской работой.',
            'summary': 'Положительная динамика в сфере лесопользования',
            'image_url': news_images[2]
        },
        {
            'title': 'Проведение экологических акций',
            'content': 'В мае-июне запланированы экологические акции по посадке деревьев с участием волонтеров. Ожидается участие более 1000 человек в восстановлении лесного покрова.',
            'summary': 'Приглашаем к участию в экологических мероприятиях',
            'image_url': news_images[3]
        },
        {
            'title': 'Обновление нормативной базы',
            'content': 'Вступили в силу новые правила получения разрешений на использование лесных ресурсов. Изменения направлены на упрощение процедур и повышение прозрачности.',
            'summary': 'Изменения в процедурах получения разрешений',
            'image_url': news_images[4]
        }
    ]
    
    for i, news_item in enumerate(news_data):
        if not News.query.filter_by(title=news_item['title']).first():
            news = News(**news_item)
            news.author_id = admin.id
            db.session.add(news)
            print(f"✅ Новость создана: {news_item['title']}")

def create_placeholder_image():
    """Создание изображения-заглушки"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        # Создаем простое изображение-заглушку
        img = Image.new('RGB', (400, 300), color='#f0f0f0')
        draw = ImageDraw.Draw(img)
        
        # Добавляем текст
        try:
            # Пытаемся использовать стандартный шрифт
            font = ImageFont.load_default()
        except:
            font = None
        
        text = "СДЛХ\nИзображение"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        position = ((400 - text_width) // 2, (300 - text_height) // 2)
        draw.text(position, text, fill='#666666', font=font)
        
        # Сохраняем в папку images
        placeholder_path = 'frontend/static/images/placeholder.jpg'
        os.makedirs(os.path.dirname(placeholder_path), exist_ok=True)
        img.save(placeholder_path, 'JPEG', quality=80)
        
        print("✅ Изображение-заглушка создано")
        
    except ImportError:
        print("⚠️ Pillow не установлен, изображение-заглушка не создано")
    except Exception as e:
        print(f"⚠️ Ошибка при создании заглушки: {e}")

def init_database():
    """Основная функция инициализации"""
    app = create_app()
    
    with app.app_context():
        print("🚀 Начинаем инициализацию базы данных СДЛХ...")
        
        create_database()
        create_admin_user()
        create_test_users()
        create_services()
        create_articles()
        create_news()
        create_placeholder_image()
        
        # Сохраняем все изменения
        db.session.commit()
        print("💾 Все данные сохранены в базе данных")
        
        print("\n✅ Инициализация завершена успешно!")
        print("\n📋 Данные для входа:")
        print("👨‍💼 Администратор: admin / admin123")
        print("👤 Пользователь 1: user1 / 123456")
        print("👤 Пользователь 2: user2 / 123456")
        print("\n📁 Структура изображений:")
        print("📁 frontend/static/images/")
        print("  ├── articles/ (изображения для статей)")
        print("  ├── news/ (изображения для новостей)")  
        print("  ├── services/ (изображения для услуг)")
        print("  ├── gallery/ (галерея)")
        print("  ├── uploads/ (загрузки пользователей)")
        print("  └── placeholder.jpg (заглушка)")

if __name__ == '__main__':
    init_database() 