import os
import uuid
import time
from werkzeug.utils import secure_filename
from PIL import Image
from flask import current_app

def allowed_file(filename):
    """Проверка разрешенного расширения файла"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def generate_filename(original_filename):
    """Генерация уникального имени файла с timestamp"""
    extension = original_filename.rsplit('.', 1)[1].lower()
    timestamp = str(int(time.time()))
    secure_name = secure_filename(original_filename.rsplit('.', 1)[0])
    return f"{timestamp}_{secure_name}.{extension}"

def save_image(image_file, category='uploads', resize_width=None):
    """
    Универсальное сохранение изображения
    
    Args:
        image_file: Файл изображения
        category: Категория (news, articles, services, uploads, gallery)
        resize_width: Ширина для изменения размера (optional)
    
    Returns:
        str: URL путь к сохраненному файлу для использования в HTML
    """
    if not image_file or image_file.filename == '':
        print("Ошибка: Файл изображения пустой")
        return None
    
    if not allowed_file(image_file.filename):
        print(f"Ошибка: Неподдерживаемый формат файла: {image_file.filename}")
        return None
    
    # Генерируем уникальное имя файла
    filename = generate_filename(image_file.filename)
    print(f"Сгенерированное имя файла: {filename}")
    
    # Определяем папку для сохранения относительно frontend/static
    upload_folder = os.path.join(
        current_app.root_path, '..', 'frontend', 'static', 'uploads', category
    )
    
    # Преобразуем в абсолютный путь
    upload_folder = os.path.abspath(upload_folder)
    print(f"Папка для сохранения: {upload_folder}")
    
    # Создаем папку если её нет
    os.makedirs(upload_folder, exist_ok=True)
    
    # Полный путь к файлу
    file_path = os.path.join(upload_folder, filename)
    print(f"Полный путь к файлу: {file_path}")
    
    try:
        # Если нужно изменить размер
        if resize_width:
            # Сбрасываем указатель файла в начало
            image_file.seek(0)
            img = Image.open(image_file)
            print(f"Оригинальный размер изображения: {img.size}")
            
            # Сохраняем пропорции
            ratio = min(resize_width / img.width, resize_width / img.height)
            new_width = int(img.width * ratio)
            new_height = int(img.height * ratio)
            
            print(f"Новый размер: {new_width}x{new_height}")
            
            # Изменяем размер
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Сохраняем с оптимизацией
            img.save(file_path, optimize=True, quality=85)
        else:
            # Сбрасываем указатель файла в начало
            image_file.seek(0)
            # Сохраняем как есть
            image_file.save(file_path)
        
        # Проверяем что файл реально создан
        if os.path.exists(file_path):
            print(f"Файл успешно сохранен: {file_path}")
            file_size = os.path.getsize(file_path)
            print(f"Размер файла: {file_size} байт")
        else:
            print("ОШИБКА: Файл не был создан!")
            return None
        
        # Возвращаем URL для использования в HTML
        result_url = f"/static/uploads/{category}/{filename}"
        print(f"Возвращаемый URL: {result_url}")
        return result_url
        
    except Exception as e:
        print(f"Ошибка при сохранении изображения: {e}")
        import traceback
        traceback.print_exc()
        return None

def delete_image(image_url):
    """
    Удаление изображения по URL
    
    Args:
        image_url: URL изображения (например: /static/uploads/news/image.jpg)
    """
    if not image_url or not image_url.startswith('/static/'):
        return True
    
    try:
        # Убираем /static/ из начала пути
        relative_path = image_url.replace('/static/', '')
        full_path = os.path.join(current_app.root_path, '..', 'frontend', 'static', relative_path)
        
        if os.path.exists(full_path):
            os.remove(full_path)
            print(f"Удалено изображение: {full_path}")
        return True
    except Exception as e:
        print(f"Ошибка при удалении изображения: {e}")
        return False

def get_image_url(image_path):
    """
    Получение полного URL изображения для использования в шаблонах
    
    Args:
        image_path: Путь к изображению 
    
    Returns:
        str: URL для использования в src
    """
    if not image_path:
        return '/static/images/placeholder-leader.svg'  # Изображение-заглушка
    
    # Если путь уже начинается с /static/, возвращаем как есть
    if image_path.startswith('/static/'):
        return image_path
    
    # Иначе добавляем /static/
    return f'/static/{image_path}'

def create_thumbnail(image_url, width=200):
    """
    Создание миниатюры изображения
    
    Args:
        image_url: URL оригинального изображения
        width: Ширина миниатюры
    
    Returns:
        str: URL миниатюры
    """
    if not image_url or not image_url.startswith('/static/'):
        return None
    
    try:
        # Убираем /static/ из начала пути
        relative_path = image_url.replace('/static/', '')
        full_path = os.path.join(current_app.root_path, '..', 'frontend', 'static', relative_path)
        
        if not os.path.exists(full_path):
            return None
        
        # Создаем имя для миниатюры
        path_parts = relative_path.split('/')
        filename = path_parts[-1]
        name, ext = filename.rsplit('.', 1)
        thumb_filename = f"{name}_thumb.{ext}"
        
        # Путь к миниатюре
        thumb_relative = '/'.join(path_parts[:-1]) + '/' + thumb_filename
        thumb_full_path = os.path.join(current_app.root_path, '..', 'frontend', 'static', thumb_relative)
        
        # Если миниатюра уже существует, возвращаем её
        if os.path.exists(thumb_full_path):
            return f"/static/{thumb_relative}"
        
        # Создаем миниатюру
        img = Image.open(full_path)
        
        # Сохраняем пропорции
        ratio = width / img.width
        new_height = int(img.height * ratio)
        
        # Изменяем размер
        img = img.resize((width, new_height), Image.Resampling.LANCZOS)
        
        # Сохраняем миниатюру
        img.save(thumb_full_path, optimize=True, quality=80)
        
        return f"/static/{thumb_relative}"
        
    except Exception as e:
        print(f"Ошибка при создании миниатюры: {e}")
        return None

def ensure_upload_folders():
    """Создание всех необходимых папок для загрузки изображений"""
    base_path = os.path.join(current_app.root_path, '..', 'frontend', 'static', 'uploads')
    categories = ['news', 'articles', 'services', 'gallery', 'users']
    
    for category in categories:
        folder_path = os.path.join(base_path, category)
        os.makedirs(folder_path, exist_ok=True)
        
        # Создаем .gitkeep файл для сохранения папки в git
        gitkeep_path = os.path.join(folder_path, '.gitkeep')
        if not os.path.exists(gitkeep_path):
            with open(gitkeep_path, 'w') as f:
                f.write('')
    
    print("Созданы папки для изображений:", categories) 