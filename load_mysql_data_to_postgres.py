#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для загрузки экспортированных данных из MySQL в PostgreSQL
"""

import json
import os
import requests
from datetime import datetime

# URL вашего приложения на Render
RENDER_URL = "https://sdlh-department.onrender.com"

def load_json_file(filename):
    """Загружает данные из JSON файла"""
    filepath = os.path.join('mysql_export', filename)
    if not os.path.exists(filepath):
        print(f"❌ Файл {filepath} не найден")
        return []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"✅ Загружено {len(data)} записей из {filename}")
    return data

def upload_data_to_render():
    """Загружает данные на Render через специальный endpoint"""
    
    print("🚀 Начинаю загрузку данных в PostgreSQL на Render...")
    
    # Загружаем все данные
    users_data = load_json_file('users.json')
    services_data = load_json_file('services.json')
    programs_data = load_json_file('programs.json')
    news_data = load_json_file('news.json')
    articles_data = load_json_file('articles.json')
    applications_data = load_json_file('applications.json')
    
    # Подготавливаем пакет данных
    data_package = {
        'users': users_data,
        'services': services_data,
        'programs': programs_data,
        'news': news_data,
        'articles': articles_data,
        'applications': applications_data
    }
    
    try:
        # Отправляем данные на Render
        print("📤 Отправляю данные на сервер...")
        response = requests.post(
            f"{RENDER_URL}/load-mysql-data-secret-route",
            json=data_package,
            timeout=300  # 5 минут таймаут
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Данные успешно загружены!")
            print(f"📊 Статистика:")
            for table, count in result.get('loaded', {}).items():
                print(f"   • {table}: {count} записей")
        else:
            print(f"❌ Ошибка загрузки: {response.status_code}")
            print(f"📋 Ответ сервера: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка соединения: {e}")

if __name__ == "__main__":
    upload_data_to_render() 