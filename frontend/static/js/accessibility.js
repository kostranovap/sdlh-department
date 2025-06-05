/**
 * Модуль доступности для сайта СДЛХ
 * Реализует требования ГОСТ Р 52872-2012 и WCAG 2.1 AA
 */

class AccessibilityManager {
    constructor() {
        this.isAccessibilityMode = false;
        this.fontSize = 'normal';
        this.colorScheme = 'yellow-black';
        this.showImages = true;
        this.increasedLineHeight = false;
        this.isPanelVisible = false;
        this.init();
    }

    init() {
        // Загружаем сохраненные настройки
        this.loadSettings();
        
        // Инициализируем элементы управления
        this.setupControls();
        
        // Применяем настройки
        this.applySettings();
        
        // Обновляем статус для скринридеров
        this.updateStatus('Система доступности инициализирована');
        
        // Добавляем глобальные обработчики событий
        this.setupGlobalHandlers();
        
        console.log('AccessibilityManager инициализирован');
    }

    setupControls() {
        // Кнопка переключения режима доступности
        const toggleBtn = document.getElementById('toggle-accessibility');
        if (toggleBtn) {
            toggleBtn.addEventListener('click', () => this.toggleAccessibilityMode());
            toggleBtn.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    this.toggleAccessibilityMode();
                }
            });
        }

        // Кнопки управления размером шрифта
        const fontControls = document.querySelectorAll('.font-control');
        fontControls.forEach(button => {
            button.addEventListener('click', (e) => {
                const size = e.target.dataset.size;
                this.setFontSize(size);
            });
            
            button.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    const size = e.target.dataset.size;
                    this.setFontSize(size);
                }
            });
        });

        // Кнопки управления цветовой схемой
        const colorControls = document.querySelectorAll('.color-control');
        colorControls.forEach(button => {
            button.addEventListener('click', (e) => {
                const scheme = e.target.dataset.scheme;
                this.setColorScheme(scheme);
            });
        });

        // Дополнительные опции
        const optionControls = document.querySelectorAll('.option-control');
        optionControls.forEach(button => {
            button.addEventListener('click', (e) => {
                const option = e.target.dataset.option;
                this.toggleOption(option);
            });
        });

        // Горячие клавиши
        document.addEventListener('keydown', (e) => this.handleHotkeys(e));
    }

    setupGlobalHandlers() {
        // Обработчик для кнопки в шапке
        const headerBtn = document.getElementById('open-accessibility-panel');
        if (headerBtn) {
            headerBtn.addEventListener('click', (e) => {
                e.preventDefault();
                this.togglePanel();
            });
        }
        
        // Обработчик закрытия панели
        const closeBtn = document.getElementById('close-accessibility-panel');
        if (closeBtn) {
            closeBtn.addEventListener('click', (e) => {
                e.preventDefault();
                this.hidePanel();
            });
        }
        
        console.log('Обработчики событий настроены:', { headerBtn: !!headerBtn, closeBtn: !!closeBtn });
    }

    togglePanel() {
        const panel = document.getElementById('accessibility-panel');
        if (!panel) return;
        
        this.isPanelVisible = !this.isPanelVisible;
        
        if (this.isPanelVisible) {
            this.showPanel();
        } else {
            this.hidePanel();
        }
    }

    showPanel() {
        const panel = document.getElementById('accessibility-panel');
        if (panel) {
            panel.style.display = 'block';
            document.body.classList.add('accessibility-panel-open');
            this.isPanelVisible = true;
            
            // Фокус на первый элемент управления
            setTimeout(() => {
                const firstControl = panel.querySelector('button');
                if (firstControl) {
                    firstControl.focus();
                }
            }, 100);
            
            this.updateStatus('Панель доступности открыта');
            console.log('Панель доступности показана');
        } else {
            console.warn('Панель доступности не найдена');
        }
    }

    hidePanel() {
        const panel = document.getElementById('accessibility-panel');
        if (panel) {
            panel.style.display = 'none';
            document.body.classList.remove('accessibility-panel-open');
            this.isPanelVisible = false;
            this.updateStatus('Панель доступности закрыта');
            console.log('Панель доступности скрыта');
        }
    }

    toggleAccessibilityMode() {
        this.isAccessibilityMode = !this.isAccessibilityMode;
        this.applySettings();
        this.saveSettings();
        
        const message = this.isAccessibilityMode 
            ? 'Включена версия для слабовидящих' 
            : 'Включена обычная версия';
        
        this.updateStatus(message);
        this.announceChange(message);
        
        // Обновляем ARIA атрибуты
        const toggleBtn = document.getElementById('toggle-accessibility');
        if (toggleBtn) {
            toggleBtn.setAttribute('aria-pressed', this.isAccessibilityMode);
        }
        
        // Показываем/скрываем настройки размера шрифта
        const settings = document.getElementById('accessibility-settings');
        if (settings) {
            settings.style.display = this.isAccessibilityMode ? 'block' : 'none';
        }
        
        console.log('Режим доступности:', this.isAccessibilityMode ? 'включен' : 'выключен');
    }

    setFontSize(size) {
        this.fontSize = size;
        this.applySettings();
        this.saveSettings();
        
        const sizeNames = {
            'normal': 'обычный',
            'large': 'большой',
            'extra-large': 'очень большой'
        };
        
        const message = `Установлен ${sizeNames[size]} размер шрифта`;
        this.updateStatus(message);
        this.announceChange(message);
        
        // Обновляем активную кнопку
        this.updateFontControls();
        
        console.log('Размер шрифта:', size);
    }

    setColorScheme(scheme) {
        this.colorScheme = scheme;
        this.applySettings();
        this.saveSettings();
        
        const schemeNames = {
            'yellow-black': 'желтый фон, черный текст',
            'white-black': 'белый фон, черный текст',
            'black-white': 'черный фон, белый текст'
        };
        
        const message = `Установлена цветовая схема: ${schemeNames[scheme]}`;
        this.updateStatus(message);
        this.announceChange(message);
        
        // Обновляем активную кнопку
        this.updateColorControls();
        
        console.log('Цветовая схема:', scheme);
    }

    toggleOption(option) {
        switch (option) {
            case 'images':
                this.showImages = !this.showImages;
                break;
            case 'line-height':
                this.increasedLineHeight = !this.increasedLineHeight;
                break;
        }
        
        this.applySettings();
        this.saveSettings();
        
        const optionNames = {
            'images': this.showImages ? 'включен показ изображений' : 'отключен показ изображений',
            'line-height': this.increasedLineHeight ? 'увеличен межстрочный интервал' : 'обычный межстрочный интервал'
        };
        
        const message = optionNames[option];
        this.updateStatus(message);
        this.announceChange(message);
        
        // Обновляем кнопки
        this.updateOptionControls();
        
        console.log('Опция изменена:', option, '=', this[option === 'images' ? 'showImages' : 'increasedLineHeight']);
    }

    applySettings() {
        const body = document.body;
        
        // Применяем режим доступности
        if (this.isAccessibilityMode) {
            body.classList.add('accessibility-mode');
            
            // Применяем цветовую схему
            body.classList.remove('color-yellow-black', 'color-white-black', 'color-black-white');
            body.classList.add(`color-${this.colorScheme}`);
            
            // Применяем дополнительные опции
            body.classList.toggle('hide-images', !this.showImages);
            body.classList.toggle('increased-line-height', this.increasedLineHeight);
            
            // Включаем stylesheet
            const accessibilityStyle = document.getElementById('accessibility-style');
            if (accessibilityStyle) {
                accessibilityStyle.disabled = false;
            }
        } else {
            // Убираем все классы доступности
            body.classList.remove('accessibility-mode', 'color-yellow-black', 'color-white-black', 'color-black-white', 'hide-images', 'increased-line-height');
            
            // Отключаем stylesheet
            const accessibilityStyle = document.getElementById('accessibility-style');
            if (accessibilityStyle) {
                accessibilityStyle.disabled = true;
            }
        }
        
        // Применяем размер шрифта
        body.classList.remove('font-normal', 'font-large', 'font-extra-large');
        body.classList.add(`font-${this.fontSize}`);
        
        // Обновляем видимость настроек
        const settings = document.getElementById('accessibility-settings');
        if (settings) {
            settings.style.display = this.isAccessibilityMode ? 'block' : 'none';
        }
        
        // Обновляем кнопки управления
        this.updateButtonText();
        this.updateFontControls();
        this.updateColorControls();
        this.updateOptionControls();
    }

    updateButtonText() {
        // Обновляем текст в кнопке переключения
        const normalText = document.querySelector('.normal-text');
        const accessibleText = document.querySelector('.accessibility-text');
        
        if (this.isAccessibilityMode) {
            if (normalText) normalText.style.display = 'none';
            if (accessibleText) accessibleText.style.display = 'inline';
        } else {
            if (normalText) normalText.style.display = 'inline';
            if (accessibleText) accessibleText.style.display = 'none';
        }
    }

    updateFontControls() {
        const fontControls = document.querySelectorAll('.font-control');
        fontControls.forEach(button => {
            const size = button.dataset.size;
            if (size === this.fontSize) {
                button.classList.add('active');
                button.setAttribute('aria-pressed', 'true');
            } else {
                button.classList.remove('active');
                button.setAttribute('aria-pressed', 'false');
            }
        });
    }

    updateColorControls() {
        const colorControls = document.querySelectorAll('.color-control');
        colorControls.forEach(button => {
            const isActive = button.dataset.scheme === this.colorScheme;
            button.classList.toggle('active', isActive);
            button.setAttribute('aria-pressed', isActive);
        });
    }

    updateOptionControls() {
        const optionControls = document.querySelectorAll('.option-control');
        optionControls.forEach(button => {
            let isActive = false;
            const option = button.dataset.option;
            
            switch (option) {
                case 'images':
                    isActive = this.showImages;
                    break;
                case 'line-height':
                    isActive = this.increasedLineHeight;
                    break;
            }
            
            button.classList.toggle('active', isActive);
            button.setAttribute('aria-pressed', isActive);
        });
    }

    handleHotkeys(e) {
        // Alt + A - переключение режима доступности / показ панели
        if (e.altKey && e.key.toLowerCase() === 'a') {
            e.preventDefault();
            if (!this.isPanelVisible) {
                this.showPanel();
            } else {
                this.toggleAccessibilityMode();
            }
        }
        
        // Alt + 1, 2, 3 - изменение размера шрифта (только в режиме доступности)
        if (e.altKey && ['1', '2', '3'].includes(e.key) && this.isAccessibilityMode) {
            e.preventDefault();
            const sizes = ['normal', 'large', 'extra-large'];
            const size = sizes[parseInt(e.key) - 1];
            this.setFontSize(size);
        }
        
        // Escape - закрыть панель настроек
        if (e.key === 'Escape') {
            if (this.isPanelVisible) {
                this.hidePanel();
            }
        }
    }

    saveSettings() {
        try {
            const settings = {
                accessibilityMode: this.isAccessibilityMode,
                fontSize: this.fontSize,
                colorScheme: this.colorScheme,
                showImages: this.showImages,
                increasedLineHeight: this.increasedLineHeight,
                timestamp: Date.now()
            };
            localStorage.setItem('sdlh_accessibility_settings', JSON.stringify(settings));
            console.log('Настройки доступности сохранены:', settings);
        } catch (error) {
            console.warn('Не удалось сохранить настройки доступности:', error);
        }
    }

    loadSettings() {
        try {
            const saved = localStorage.getItem('sdlh_accessibility_settings');
            if (saved) {
                const settings = JSON.parse(saved);
                
                // Проверяем, что настройки не старше 30 дней
                const maxAge = 30 * 24 * 60 * 60 * 1000; // 30 дней в миллисекундах
                if (settings.timestamp && (Date.now() - settings.timestamp < maxAge)) {
                    this.isAccessibilityMode = settings.accessibilityMode || false;
                    this.fontSize = settings.fontSize || 'normal';
                    this.colorScheme = settings.colorScheme || 'yellow-black';
                    this.showImages = settings.showImages !== undefined ? settings.showImages : true;
                    this.increasedLineHeight = settings.increasedLineHeight || false;
                    console.log('Настройки доступности загружены:', settings);
                } else {
                    console.log('Настройки доступности устарели, используем значения по умолчанию');
                }
            }
        } catch (error) {
            console.warn('Не удалось загрузить настройки доступности:', error);
            // Используем значения по умолчанию
            this.isAccessibilityMode = false;
            this.fontSize = 'normal';
            this.colorScheme = 'yellow-black';
            this.showImages = true;
            this.increasedLineHeight = false;
        }
    }

    updateStatus(message) {
        const status = document.getElementById('accessibility-status');
        if (status) {
            status.textContent = message;
            console.log('Статус доступности:', message);
        }
    }

    announceChange(message) {
        // Создаем временное объявление для скринридеров
        const announcement = document.createElement('div');
        announcement.setAttribute('aria-live', 'assertive');
        announcement.setAttribute('aria-atomic', 'true');
        announcement.className = 'sr-only';
        announcement.textContent = message;
        
        document.body.appendChild(announcement);
        
        // Удаляем объявление через 3 секунды
        setTimeout(() => {
            if (announcement && announcement.parentNode) {
                announcement.parentNode.removeChild(announcement);
            }
        }, 3000);
    }

    // Публичные методы для внешнего использования
    getSettings() {
        return {
            accessibilityMode: this.isAccessibilityMode,
            fontSize: this.fontSize,
            panelVisible: this.isPanelVisible
        };
    }

    setSettings(settings) {
        if (typeof settings.accessibilityMode === 'boolean') {
            this.isAccessibilityMode = settings.accessibilityMode;
        }
        
        if (['normal', 'large', 'extra-large'].includes(settings.fontSize)) {
            this.fontSize = settings.fontSize;
        }
        
        this.applySettings();
        this.saveSettings();
    }

    // Проверка поддержки доступности
    checkAccessibilitySupport() {
        const features = {
            localStorage: typeof(Storage) !== "undefined",
            ariaSupport: 'setAttribute' in document.createElement('div'),
            focusSupport: 'focus' in document.createElement('button')
        };
        
        console.log('Поддержка функций доступности:', features);
        return features;
    }
}

// Глобальные функции для обратной совместимости
window.toggleAccessibilityPanel = function() {
    console.log('toggleAccessibilityPanel вызвана');
    if (window.accessibilityManager) {
        window.accessibilityManager.togglePanel();
    } else {
        console.warn('accessibilityManager не найден');
    }
};

// Простая функция для отладки
window.testAccessibility = function() {
    console.log('Тест доступности:', {
        manager: !!window.accessibilityManager,
        panel: !!document.getElementById('accessibility-panel'),
        button: !!document.getElementById('open-accessibility-panel')
    });
};

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    // Инициализируем менеджер доступности
    window.accessibilityManager = new AccessibilityManager();
    
    // Делаем менеджер доступным глобально для отладки
    window.accessibility = window.accessibilityManager;
    
    console.log('Система доступности СДЛХ готова к работе');
});

// Дополнительная проверка при загрузке страницы
window.addEventListener('load', function() {
    if (window.accessibilityManager) {
        // Проверяем поддержку функций доступности
        window.accessibilityManager.checkAccessibilitySupport();
        
        // Восстанавливаем состояние из URL параметров, если есть
        const urlParams = new URLSearchParams(window.location.search);
        if (urlParams.get('accessibility') === 'true') {
            window.accessibilityManager.setSettings({ accessibilityMode: true });
            window.accessibilityManager.showPanel();
        }
    }
}); 