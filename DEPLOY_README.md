# 🚀 Деплой проекта СДЛХ на Render.com

## 📋 Подготовка проекта

### 1. Экспорт данных из MySQL (XAMPP)

Если у вас есть данные в MySQL, сначала экспортируйте их:

```bash
# Запустите XAMPP и убедитесь что MySQL работает
python export_mysql_data.py
```

Это создаст папку `mysql_export` с JSON файлами ваших данных.

### 2. Проверка структуры проекта

Убедитесь, что у вас есть следующие файлы в корне:
- ✅ `app.py` - точка входа для Render
- ✅ `requirements.txt` - зависимости Python
- ✅ `create_initial_data.py` - создание начальных данных
- ✅ `.gitignore` - исключения для Git

## 🌐 Деплой на Render.com

### Шаг 1: Подготовка GitHub репозитория

1. **Создайте репозиторий на GitHub:**
   - Зайдите на [github.com](https://github.com)
   - Нажмите "New repository"
   - Название: `sdlh-department`
   - Сделайте публичным
   - Не добавляйте README (у нас уже есть файлы)

2. **Загрузите проект:**
```bash
# В корне вашего проекта выполните:
git init
git add .
git commit -m "Initial commit: СДЛХ Department website"
git branch -M main
git remote add origin https://github.com/ВАШ-ЛОГИН/sdlh-department.git
git push -u origin main
```

### Шаг 2: Создание аккаунта на Render.com

1. Зайдите на [render.com](https://render.com)
2. Нажмите **"Get Started For Free"**
3. Зарегистрируйтесь через GitHub аккаунт

### Шаг 3: Создание PostgreSQL базы данных

1. В Render Dashboard нажмите **"New +"**
2. Выберите **"PostgreSQL"**
3. Настройки:
   - **Name**: `sdlh-database`
   - **Database**: `sdlh_db`  
   - **User**: `sdlh_user`
   - **Region**: `Oregon (US West)`
   - **Plan**: **Free** (1GB, 30 дней)
4. Нажмите **"Create Database"**
5. **Сохраните External Database URL** - он понадобится!

### Шаг 4: Создание Web Service

1. Нажмите **"New +" → "Web Service"**
2. Подключите GitHub и выберите репозиторий `sdlh-department`
3. Настройки:

| Параметр | Значение |
|----------|----------|
| **Name** | `sdlh-department` |
| **Environment** | `Python 3` |
| **Region** | `Oregon (US West)` |
| **Branch** | `main` |
| **Root Directory** | оставьте пустым |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn app:app` |

### Шаг 5: Настройка переменных окружения

В разделе **Environment Variables** добавьте:

| Key | Value |
|-----|-------|
| `FLASK_ENV` | `production` |
| `SECRET_KEY` | `your-super-secret-key-here` |
| `DATABASE_URL` | *URL вашей PostgreSQL базы* |

### Шаг 6: Деплой

1. Нажмите **"Create Web Service"**
2. Дождитесь завершения билда (5-10 минут)
3. После успешного деплоя получите URL вида: `https://sdlh-department.onrender.com`

### Шаг 7: Инициализация базы данных

1. В Render Dashboard откройте ваш Web Service
2. Перейдите в **Shell** 
3. Выполните команду:
```bash
python create_initial_data.py
```

## 🔑 Данные для входа

После инициализации базы данных:

- **Администратор**: 
  - Логин: `admin`
  - Пароль: `admin123`

- **Пользователь**:
  - Логин: `user`  
  - Пароль: `user123`

## ⚠️ Важные замечания

### Ограничения бесплатного плана:

1. **Web Service:**
   - Засыпает через 15 минут неактивности
   - Время пробуждения: 30-60 секунд
   - 750 часов работы в месяц

2. **PostgreSQL:**
   - 1GB хранилища
   - Действует 30 дней
   - После истечения можно апгрейдить

### Обновление сайта:

Для обновления кода:
```bash
git add .
git commit -m "Описание изменений"
git push origin main
```

Render автоматически пересоберет и задеплоит изменения.

## 🏆 Для защиты диплома

**Укажите в отчете:**
- **Ссылка на сайт**: `https://sdlh-department.onrender.com`
- **Ссылка на GitHub**: `https://github.com/ВАШ-ЛОГИН/sdlh-department`
- **Технологии**: Flask, PostgreSQL, Render.com
- **Тип хостинга**: Бесплатный с ограничениями

## 🆘 Troubleshooting

**Проблема**: Сайт не загружается
- **Решение**: Подождите 1-2 минуты (приложение просыпается)

**Проблема**: Ошибка базы данных
- **Решение**: Проверьте правильность DATABASE_URL в Environment Variables

**Проблема**: Статические файлы не загружаются
- **Решение**: Убедитесь что папка `frontend/static` существует в репозитории

## 📞 Поддержка

При возникновении проблем проверьте логи в Render Dashboard → ваш сервис → **Logs** 