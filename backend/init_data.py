#!/usr/bin/env python3
"""
Скрипт для инициализации тестовых данных
"""

from app import create_app, db
from app.models import User, Service, News, Article

def init_test_data():
    """Создание тестовых данных"""
    
    app = create_app()
    with app.app_context():
        # Создаем таблицы
        db.create_all()
        
        # Проверяем, есть ли уже данные
        if User.query.first():
            print("Данные уже существуют!")
            return
        
        # Создаем администратора
        admin = User(
            username='admin',
            email='admin@dlh.gov.ru',
            full_name='Администратор Системы',
            role='admin'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        
        # Создаем тестового пользователя
        user = User(
            username='testuser',
            email='user@example.com',
            full_name='Тестовый Пользователь',
            role='user'
        )
        user.set_password('user123')
        db.session.add(user)
        
        # Создаем услуги
        services = [
            Service(
                name='Разрешение на рубку деревьев',
                description='Получение разрешения на рубку зеленых насаждений на территории городских лесов',
                requirements='Паспорт, правоустанавливающие документы на землю, схема участка',
                documents_needed='Заявление, паспорт, документы на участок',
                processing_time='10 рабочих дней',
                cost='Бесплатно',
                responsible_department='Отдел лесопользования',
                is_active=True
            ),
            Service(
                name='Аренда лесного участка',
                description='Предоставление лесного участка в аренду для заготовки древесины',
                requirements='Юридическое лицо или ИП, документы о финансовой состоятельности',
                documents_needed='Заявление, учредительные документы, финансовые гарантии',
                processing_time='30 рабочих дней',
                cost='Согласно тарифам',
                responsible_department='Отдел лесных отношений',
                is_active=True
            ),
            Service(
                name='Лесовосстановительные работы',
                description='Проведение работ по восстановлению лесных насаждений',
                requirements='Проект лесовосстановления, согласованный с департаментом',
                documents_needed='Заявление, проект работ, смета расходов',
                processing_time='15 рабочих дней',
                cost='По смете',
                responsible_department='Отдел лесовосстановления',
                is_active=True
            ),
            Service(
                name='Справка о лесопатологическом состоянии',
                description='Получение справки о санитарном состоянии лесного участка',
                requirements='Указание координат участка, цель получения справки',
                documents_needed='Заявление, схема участка',
                processing_time='5 рабочих дней',
                cost='Бесплатно',
                responsible_department='Отдел лесозащиты',
                is_active=True
            ),
            Service(
                name='Согласование проекта освоения лесов',
                description='Экспертиза и согласование проектов освоения лесных участков',
                requirements='Проект освоения лесов, выполненный специализированной организацией',
                documents_needed='Заявление, проект освоения, документы проектировщика',
                processing_time='20 рабочих дней',
                cost='Согласно тарифам',
                responsible_department='Отдел лесного планирования',
                is_active=True
            )
        ]
        
        for service in services:
            db.session.add(service)
        
        # Создаем новости
        news_items = [
            News(
                title='Запуск новой программы лесовосстановления',
                content='Департамент лесного хозяйства объявляет о запуске масштабной программы по восстановлению лесных насаждений. В рамках программы планируется высадить более 100 тысяч деревьев на территории региона.',
                summary='Новая программа лесовосстановления предусматривает высадку 100 тысяч деревьев',
                category='programs',
                is_published=True,
                is_important=True,
                author_id=1
            ),
            News(
                title='Обновление системы подачи заявлений',
                content='С 1 января вступают в силу новые правила подачи заявлений на получение государственных услуг. Теперь большинство заявлений можно подать в электронном виде через портал государственных услуг.',
                summary='Новые правила электронной подачи заявлений',
                category='announcements',
                is_published=True,
                is_important=False,
                author_id=1
            ),
            News(
                title='Результаты мониторинга лесных пожаров',
                content='По итогам пожароопасного сезона зафиксировано снижение количества лесных пожаров на 15% по сравнению с прошлым годом. Это стало возможным благодаря усилению профилактических мер.',
                summary='Снижение количества лесных пожаров на 15%',
                category='ecology',
                is_published=True,
                is_important=False,
                author_id=1
            ),
            News(
                title='Внедрение цифровых технологий в лесное хозяйство',
                content='Департамент активно внедряет современные цифровые технологии для мониторинга состояния лесов. Использование дронов и спутниковых снимков позволяет оперативно выявлять нарушения.',
                summary='Цифровизация лесного хозяйства',
                category='technology',
                is_published=True,
                is_important=False,
                author_id=1
            ),
            News(
                title='Международная конференция по лесному хозяйству',
                content='В следующем месяце состоится международная конференция, посвященная устойчивому развитию лесного хозяйства. Ожидается участие экспертов из 20 стран.',
                summary='Международная конференция по лесному хозяйству',
                category='events',
                is_published=True,
                is_important=True,
                author_id=1
            )
        ]
        
        for news in news_items:
            db.session.add(news)
        
        # Создаем статьи
        articles = [
            Article(
                title='История департамента лесного хозяйства',
                content='Департамент лесного хозяйства был создан в 1998 году для координации деятельности по охране, защите и воспроизводству лесов. За годы работы департамент...',
                summary='История создания и развития департамента',
                page='about',
                category='history',
                is_published=True,
                author_id=1
            ),
            Article(
                title='Структура департамента',
                content='Департамент включает в себя несколько специализированных отделов: отдел лесопользования, отдел лесовосстановления, отдел лесозащиты и другие...',
                summary='Организационная структура департамента',
                page='about',
                category='structure',
                is_published=True,
                author_id=1
            )
        ]
        
        for article in articles:
            db.session.add(article)
        
        # Сохраняем все изменения
        db.session.commit()
        
        print("✅ Тестовые данные успешно созданы!")
        print("\n📋 Созданные аккаунты:")
        print("Администратор: admin / admin123")
        print("Пользователь: testuser / user123")
        print(f"\n📊 Статистика:")
        print(f"- Пользователей: {User.query.count()}")
        print(f"- Услуг: {Service.query.count()}")
        print(f"- Новостей: {News.query.count()}")
        print(f"- Статей: {Article.query.count()}")

if __name__ == '__main__':
    init_test_data() 