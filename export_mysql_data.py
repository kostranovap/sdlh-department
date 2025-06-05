#!/usr/bin/env python3
"""
Скрипт для экспорта данных из MySQL (XAMPP) 
"""
import pymysql
import json
import os
from datetime import datetime

def export_mysql_data():
    """Экспорт данных из MySQL в JSON формат"""
    
    # Подключение к MySQL
    connection = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='',
        database='sdlh_db',
        charset='utf8mb4'
    )
    
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            
            # Создаем папку для экспорта
            export_dir = 'mysql_export'
            os.makedirs(export_dir, exist_ok=True)
            
            # Список таблиц для экспорта
            tables = ['users', 'articles', 'services', 'news', 'programs', 'applications']
            
            for table in tables:
                print(f"Экспортирую таблицу {table}...")
                
                # Получаем все данные из таблицы
                cursor.execute(f"SELECT * FROM {table}")
                data = cursor.fetchall()
                
                # Конвертируем datetime объекты в строки
                for row in data:
                    for key, value in row.items():
                        if isinstance(value, datetime):
                            row[key] = value.isoformat()
                
                # Сохраняем в JSON файл
                with open(f'{export_dir}/{table}.json', 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                
                print(f"✅ Таблица {table}: экспортировано {len(data)} записей")
            
            print(f"\n🎉 Экспорт завершен! Файлы сохранены в папке '{export_dir}'")
            
    except Exception as e:
        print(f"❌ Ошибка при экспорте: {e}")
        
    finally:
        connection.close()

if __name__ == '__main__':
    print("🚀 Начинаю экспорт данных из MySQL...")
    export_mysql_data() 