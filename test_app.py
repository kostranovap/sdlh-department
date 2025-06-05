#!/usr/bin/env python3
"""
Тестовый скрипт для проверки работоспособности приложения
"""
import os
import sys

# Добавляем backend в путь
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def test_app_creation():
    """Тест создания Flask приложения"""
    try:
        from backend.app import create_app
        app = create_app()
        print("✅ Flask приложение успешно создано")
        return True
    except Exception as e:
        print(f"❌ Ошибка создания приложения: {e}")
        return False

def test_imports():
    """Тест импорта зависимостей"""
    try:
        import flask
        import flask_sqlalchemy
        import flask_login
        import flask_wtf
        print("✅ Все зависимости успешно импортированы")
        return True
    except ImportError as e:
        print(f"❌ Ошибка импорта: {e}")
        return False

def main():
    """Основная функция тестирования"""
    print("🧪 Тестирование проекта СДЛХ...")
    print("-" * 50)
    
    tests = [
        ("Импорт зависимостей", test_imports),
        ("Создание приложения", test_app_creation),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 {test_name}:")
        if test_func():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Результат: {passed}/{total} тестов пройдено")
    
    if passed == total:
        print("🎉 Проект готов к деплою!")
        return True
    else:
        print("⚠️  Есть проблемы, требующие исправления")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1) 