import os
import sys

# Добавляем backend в путь Python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app import create_app, db
from backend.app.models import User, Article, Service, News, Program
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

if __name__ == '__main__':
    # Для локальной разработки
    app.run(host='127.0.0.1', port=5000, debug=True) 