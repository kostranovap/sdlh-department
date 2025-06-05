/**
 * Основной JavaScript модуль для сайта СДЛХ
 * Содержит общую логику сайта
 */

class SDLHSite {
    constructor() {
        this.init();
    }

    init() {
        // Инициализируем компоненты при загрузке DOM
        this.initMobileMenu();
        this.initFlashMessages();
        this.initSearch();
        this.initForms();
        this.initTables();
        this.initSmoothScroll();
        
        console.log('СДЛХ: Основной модуль загружен');
    }

    /**
     * Мобильное меню
     */
    initMobileMenu() {
        const toggle = document.querySelector('#nav-toggle');
        const nav = document.querySelector('#nav-list');
        
        if (toggle && nav) {
            toggle.addEventListener('click', () => {
                const isOpen = nav.classList.contains('active');
                
                if (isOpen) {
                    nav.classList.remove('active');
                    toggle.setAttribute('aria-expanded', 'false');
                    toggle.classList.remove('active');
                } else {
                    nav.classList.add('active');
                    toggle.setAttribute('aria-expanded', 'true');
                    toggle.classList.add('active');
                }
            });

            // Закрываем меню при нажатии Escape
            document.addEventListener('keydown', (e) => {
                if (e.key === 'Escape' && nav.classList.contains('active')) {
                    nav.classList.remove('active');
                    toggle.setAttribute('aria-expanded', 'false');
                    toggle.classList.remove('active');
                    toggle.focus();
                }
            });

            // Закрываем меню при клике вне его
            document.addEventListener('click', (e) => {
                if (!toggle.contains(e.target) && !nav.contains(e.target)) {
                    nav.classList.remove('active');
                    toggle.setAttribute('aria-expanded', 'false');
                    toggle.classList.remove('active');
                }
            });

            // Адаптируем меню под размер экрана
            this.handleResize();
            window.addEventListener('resize', () => this.handleResize());
        }
    }

    handleResize() {
        const nav = document.querySelector('#nav-list');
        const toggle = document.querySelector('#nav-toggle');
        
        if (window.innerWidth > 768) {
            // На больших экранах показываем меню и скрываем кнопку
            if (nav) {
                nav.classList.remove('active');
                nav.style.display = ''; // Убираем инлайн стиль, пусть CSS управляет
            }
            if (toggle) {
                toggle.setAttribute('aria-expanded', 'false');
                toggle.classList.remove('active');
            }
        } else {
            // На маленьких экранах контролируем меню через кнопку
            if (nav && !nav.classList.contains('active')) {
                nav.style.display = ''; // Убираем инлайн стиль, пусть CSS управляет
            }
        }
    }

    /**
     * Флеш сообщения
     */
    initFlashMessages() {
        const closeButtons = document.querySelectorAll('.close-flash');
        
        closeButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                const message = e.target.closest('.flash-message');
                if (message) {
                    message.style.opacity = '0';
                    message.style.transform = 'translateY(-10px)';
                    
                    setTimeout(() => {
                        message.remove();
                    }, 300);
                }
            });
        });

        // Автоматическое скрытие сообщений через 5 секунд
        const messages = document.querySelectorAll('.flash-message');
        messages.forEach(message => {
            setTimeout(() => {
                if (message.parentNode) {
                    const closeBtn = message.querySelector('.close-flash');
                    if (closeBtn) {
                        closeBtn.click();
                    }
                }
            }, 5000);
        });
    }

    /**
     * Поиск
     */
    initSearch() {
        const searchForm = document.querySelector('.search-form');
        const searchInput = document.getElementById('search-input');
        
        if (searchForm && searchInput) {
            // Добавляем индикатор загрузки
            searchForm.addEventListener('submit', (e) => {
                const submitBtn = searchForm.querySelector('.search-btn');
                if (submitBtn) {
                    submitBtn.innerHTML = '<span>⏳</span>';
                    submitBtn.disabled = true;
                }
            });

            // Очистка поиска
            if (searchInput.value) {
                this.addClearButton(searchInput);
            }

            searchInput.addEventListener('input', (e) => {
                if (e.target.value) {
                    this.addClearButton(e.target);
                } else {
                    this.removeClearButton(e.target);
                }
            });
        }
    }

    addClearButton(input) {
        if (input.parentNode.querySelector('.clear-search')) return;
        
        const clearBtn = document.createElement('button');
        clearBtn.type = 'button';
        clearBtn.className = 'clear-search';
        clearBtn.innerHTML = '✕';
        clearBtn.setAttribute('aria-label', 'Очистить поиск');
        clearBtn.style.cssText = `
            position: absolute;
            right: 45px;
            top: 50%;
            transform: translateY(-50%);
            background: none;
            border: none;
            color: rgba(255,255,255,0.7);
            cursor: pointer;
            padding: 5px;
            font-size: 14px;
        `;
        
        clearBtn.addEventListener('click', () => {
            input.value = '';
            input.focus();
            this.removeClearButton(input);
        });
        
        input.parentNode.style.position = 'relative';
        input.parentNode.appendChild(clearBtn);
    }

    removeClearButton(input) {
        const clearBtn = input.parentNode.querySelector('.clear-search');
        if (clearBtn) {
            clearBtn.remove();
        }
    }

    /**
     * Формы
     */
    initForms() {
        const forms = document.querySelectorAll('form');
        
        forms.forEach(form => {
            // Валидация в реальном времени
            const inputs = form.querySelectorAll('input, textarea, select');
            inputs.forEach(input => {
                input.addEventListener('blur', () => this.validateField(input));
                input.addEventListener('input', () => this.clearFieldError(input));
            });

            // Обработка отправки формы
            form.addEventListener('submit', (e) => {
                if (!this.validateForm(form)) {
                    e.preventDefault();
                }
            });
        });
    }

    validateField(field) {
        const value = field.value.trim();
        let isValid = true;
        let errorMessage = '';

        // Проверка обязательных полей
        if (field.hasAttribute('required') && !value) {
            isValid = false;
            errorMessage = 'Это поле обязательно для заполнения';
        }

        // Проверка email
        if (field.type === 'email' && value) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(value)) {
                isValid = false;
                errorMessage = 'Введите корректный email адрес';
            }
        }

        // Проверка телефона
        if (field.type === 'tel' && value) {
            const phoneRegex = /^[\+]?[7|8]?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$/;
            if (!phoneRegex.test(value)) {
                isValid = false;
                errorMessage = 'Введите корректный номер телефона';
            }
        }

        // Проверка минимальной длины
        const minLength = field.getAttribute('minlength');
        if (minLength && value.length < parseInt(minLength)) {
            isValid = false;
            errorMessage = `Минимальная длина: ${minLength} символов`;
        }

        this.showFieldError(field, isValid ? '' : errorMessage);
        return isValid;
    }

    validateForm(form) {
        const fields = form.querySelectorAll('input, textarea, select');
        let isValid = true;

        fields.forEach(field => {
            if (!this.validateField(field)) {
                isValid = false;
            }
        });

        return isValid;
    }

    showFieldError(field, message) {
        this.clearFieldError(field);
        
        if (message) {
            field.classList.add('error');
            
            const errorDiv = document.createElement('div');
            errorDiv.className = 'error-message';
            errorDiv.textContent = message;
            errorDiv.setAttribute('role', 'alert');
            
            field.parentNode.appendChild(errorDiv);
        } else {
            field.classList.remove('error');
        }
    }

    clearFieldError(field) {
        field.classList.remove('error');
        const errorMessage = field.parentNode.querySelector('.error-message');
        if (errorMessage) {
            errorMessage.remove();
        }
    }

    /**
     * Таблицы
     */
    initTables() {
        const tables = document.querySelectorAll('.table');
        
        tables.forEach(table => {
            // Делаем таблицы доступными для скринридеров
            if (!table.getAttribute('role')) {
                table.setAttribute('role', 'table');
            }

            // Добавляем сортировку, если есть соответствующие классы
            const sortableHeaders = table.querySelectorAll('th[data-sort]');
            sortableHeaders.forEach(header => {
                header.style.cursor = 'pointer';
                header.setAttribute('role', 'button');
                header.setAttribute('tabindex', '0');
                
                header.addEventListener('click', () => this.sortTable(table, header));
                header.addEventListener('keydown', (e) => {
                    if (e.key === 'Enter' || e.key === ' ') {
                        e.preventDefault();
                        this.sortTable(table, header);
                    }
                });
            });
        });
    }

    sortTable(table, header) {
        const column = header.getAttribute('data-sort');
        const tbody = table.querySelector('tbody');
        const rows = Array.from(tbody.querySelectorAll('tr'));
        
        const isAscending = header.classList.contains('sort-asc');
        const isDescending = header.classList.contains('sort-desc');
        
        // Очищаем предыдущую сортировку
        table.querySelectorAll('th').forEach(th => {
            th.classList.remove('sort-asc', 'sort-desc');
            th.removeAttribute('aria-sort');
        });
        
        // Определяем направление сортировки
        let sortDirection = 'asc';
        if (isAscending) {
            sortDirection = 'desc';
        }
        
        // Сортируем строки
        rows.sort((a, b) => {
            const aValue = a.children[parseInt(column)].textContent.trim();
            const bValue = b.children[parseInt(column)].textContent.trim();
            
            let comparison = 0;
            if (aValue > bValue) comparison = 1;
            if (aValue < bValue) comparison = -1;
            
            return sortDirection === 'asc' ? comparison : -comparison;
        });
        
        // Обновляем таблицу
        rows.forEach(row => tbody.appendChild(row));
        
        // Обновляем индикаторы сортировки
        header.classList.add(`sort-${sortDirection}`);
        header.setAttribute('aria-sort', sortDirection === 'asc' ? 'ascending' : 'descending');
    }

    /**
     * Плавная прокрутка
     */
    initSmoothScroll() {
        const links = document.querySelectorAll('a[href^="#"]');
        
        links.forEach(link => {
            link.addEventListener('click', (e) => {
                const href = link.getAttribute('href');
                
                if (href === '#') return;
                
                const target = document.querySelector(href);
                if (target) {
                    e.preventDefault();
                    
                    const offsetTop = target.offsetTop - 100; // Отступ для фиксированной шапки
                    
                    window.scrollTo({
                        top: offsetTop,
                        behavior: 'smooth'
                    });
                    
                    // Устанавливаем фокус на целевой элемент
                    setTimeout(() => {
                        target.setAttribute('tabindex', '-1');
                        target.focus();
                    }, 500);
                }
            });
        });
    }

    /**
     * Утилитарные методы
     */
    
    // Показать индикатор загрузки
    showLoader(element) {
        const loader = document.createElement('div');
        loader.className = 'loader';
        loader.innerHTML = '<div class="spinner"></div>';
        loader.style.cssText = `
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(255,255,255,0.8);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 1000;
        `;
        
        element.style.position = 'relative';
        element.appendChild(loader);
    }

    // Скрыть индикатор загрузки
    hideLoader(element) {
        const loader = element.querySelector('.loader');
        if (loader) {
            loader.remove();
        }
    }

    // Показать уведомление
    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 20px;
            background: #4a7c59;
            color: white;
            border-radius: 5px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            z-index: 10000;
            transform: translateX(100%);
            transition: transform 0.3s ease;
        `;
        
        if (type === 'error') {
            notification.style.background = '#dc3545';
        } else if (type === 'warning') {
            notification.style.background = '#ffc107';
            notification.style.color = '#000';
        } else if (type === 'success') {
            notification.style.background = '#28a745';
        }
        
        document.body.appendChild(notification);
        
        // Анимация появления
        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
        }, 10);
        
        // Автоматическое скрытие
        setTimeout(() => {
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.remove();
                }
            }, 300);
        }, 3000);
    }
}

// Инициализация при загрузке DOM
document.addEventListener('DOMContentLoaded', () => {
    window.sdlhSite = new SDLHSite();
});

// Обработка ошибок JavaScript
window.addEventListener('error', (e) => {
    console.error('JavaScript ошибка:', e.error);
    
    // В режиме разработки показываем уведомление
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
        if (window.sdlhSite) {
            window.sdlhSite.showNotification('Произошла ошибка JavaScript. Проверьте консоль.', 'error');
        }
    }
});

// Функции для модальных окон авторизации
function openAuthModal(type) {
    const modal = document.getElementById('authModal');
    const modalTitle = document.getElementById('modalTitle');
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    const switchToRegister = document.getElementById('switchToRegister');
    const switchToLogin = document.getElementById('switchToLogin');
    const authMessage = document.getElementById('authMessage');
    
    // Очищаем сообщения и формы
    authMessage.className = 'auth-message';
    authMessage.style.display = 'none';
    clearAuthForms();
    
    if (type === 'login') {
        modalTitle.textContent = 'Вход в систему';
        loginForm.style.display = 'block';
        registerForm.style.display = 'none';
        switchToRegister.style.display = 'block';
        switchToLogin.style.display = 'none';
    } else {
        modalTitle.textContent = 'Регистрация';
        loginForm.style.display = 'none';
        registerForm.style.display = 'block';
        switchToRegister.style.display = 'none';
        switchToLogin.style.display = 'block';
    }
    
    modal.classList.add('active');
}

function closeAuthModal() {
    const modal = document.getElementById('authModal');
    modal.classList.remove('active');
    clearAuthForms();
}

function switchAuthForm(type) {
    openAuthModal(type);
}

function clearAuthForms() {
    document.getElementById('loginForm').reset();
    document.getElementById('registerForm').reset();
    
    const authMessage = document.getElementById('authMessage');
    authMessage.className = 'auth-message';
    authMessage.style.display = 'none';
    
    // Включаем кнопки отправки
    const submitButtons = document.querySelectorAll('.btn-modal-submit');
    submitButtons.forEach(btn => {
        btn.disabled = false;
        btn.textContent = btn.textContent.replace('...', '');
    });
}

function showAuthMessage(message, type = 'error') {
    const authMessage = document.getElementById('authMessage');
    authMessage.textContent = message;
    authMessage.className = `auth-message ${type}`;
    authMessage.style.display = 'block';
}

// Дополнительная инициализация для модальных окон
document.addEventListener('DOMContentLoaded', function() {
    // Закрытие модального окна при клике на overlay
    const authModal = document.getElementById('authModal');
    if (authModal) {
        authModal.addEventListener('click', function(e) {
            if (e.target === this) {
                closeAuthModal();
            }
        });
    }
    
    // Обработчик формы входа
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const submitBtn = this.querySelector('.btn-modal-submit');
            const originalText = submitBtn.textContent;
            submitBtn.disabled = true;
            submitBtn.textContent = 'Входим...';
            
            const formData = new FormData(this);
            
            fetch('/auth/ajax/login', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showAuthMessage(data.message, 'success');
                    setTimeout(() => {
                        window.location.reload();
                    }, 1000);
                } else {
                    showAuthMessage(data.message, 'error');
                    submitBtn.disabled = false;
                    submitBtn.textContent = originalText;
                }
            })
            .catch(error => {
                showAuthMessage('Произошла ошибка. Попробуйте еще раз.', 'error');
                submitBtn.disabled = false;
                submitBtn.textContent = originalText;
            });
        });
    }
    
    // Обработчик формы регистрации
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const submitBtn = this.querySelector('.btn-modal-submit');
            const originalText = submitBtn.textContent;
            submitBtn.disabled = true;
            submitBtn.textContent = 'Регистрируем...';
            
            const formData = new FormData(this);
            
            fetch('/auth/ajax/register', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showAuthMessage(data.message, 'success');
                    if (data.show_login) {
                        setTimeout(() => {
                            switchAuthForm('login');
                        }, 2000);
                    }
                } else {
                    showAuthMessage(data.message, 'error');
                    submitBtn.disabled = false;
                    submitBtn.textContent = originalText;
                }
            })
            .catch(error => {
                showAuthMessage('Произошла ошибка. Попробуйте еще раз.', 'error');
                submitBtn.disabled = false;
                submitBtn.textContent = originalText;
            });
        });
    }
});

// Глобальная функция для бургер-меню (полная перезапись)
function toggleMobileNav() {
    console.log('toggleMobileNav вызвана');
    
    const toggle = document.querySelector('#nav-toggle');
    let existingMenu = document.querySelector('#mobile-dropdown-menu');
    
    if (existingMenu) {
        // Закрываем существующее меню
        existingMenu.remove();
        toggle.classList.remove('active');
        toggle.setAttribute('aria-expanded', 'false');
        console.log('Меню закрыто');
        return;
    }
    
    // Создаем новое меню
    const mobileMenu = document.createElement('div');
    mobileMenu.id = 'mobile-dropdown-menu';
    mobileMenu.style.cssText = `
        position: absolute;
        top: 100%;
        left: 0;
        right: 0;
        background: #2d5a27;
        z-index: 9999;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        padding: 20px;
        font-family: Inter, sans-serif;
    `;
    
    // Добавляем пункты меню (основные страницы + авторизация)
    const menuItems = [
        { text: 'Главная', href: '/', current: window.location.pathname === '/' },
        { text: 'О департаменте', href: '/about', current: window.location.pathname === '/about' },
        { text: 'Подача заявлений', href: '/info', current: window.location.pathname === '/info' },
        { text: 'Мониторинг', href: '/monitoring', current: window.location.pathname === '/monitoring' },
        { text: 'Новости', href: '/news', current: window.location.pathname === '/news' }
    ];
    
    // Добавляем разделитель и авторизацию
    const isAuth = document.querySelector('.btn-auth[href*="profile"]');
    if (isAuth) {
        menuItems.push(
            { text: '— — — — —', href: '#', divider: true },
            { text: 'Профиль', href: '/auth/profile' },
            { text: 'Выход', href: '/auth/logout' }
        );
    } else {
        menuItems.push(
            { text: '— — — — —', href: '#', divider: true },
            { text: 'Вход', href: '#', modal: 'login' },
            { text: 'Регистрация', href: '#', modal: 'register' }
        );
    }
    
    // Создаем HTML для меню
    menuItems.forEach(item => {
        const link = document.createElement('a');
        link.href = item.href;
        link.textContent = item.text;
        
        if (item.divider) {
            // Стили для разделителя
            link.style.cssText = `
                display: block;
                color: rgba(255,255,255,0.3);
                text-decoration: none;
                padding: 10px 0;
                text-align: center;
                font-size: 14px;
                cursor: default;
                pointer-events: none;
            `;
        } else {
            link.style.cssText = `
                display: block;
                color: white;
                text-decoration: none;
                padding: 15px 0;
                border-bottom: 1px solid rgba(255,255,255,0.1);
                font-size: 16px;
                font-weight: 400;
                transition: background-color 0.2s ease;
                ${item.current ? 'background: rgba(255,255,255,0.1); font-weight: 500;' : ''}
            `;
            link.onmouseover = () => link.style.background = 'rgba(255,255,255,0.1)';
            link.onmouseout = () => link.style.background = item.current ? 'rgba(255,255,255,0.1)' : 'transparent';
            
            // Добавляем обработчик для модальных окон
            if (item.modal) {
                link.onclick = (e) => {
                    e.preventDefault();
                    openAuthModal(item.modal);
                    toggleMobileNav(); // Закрываем мобильное меню
                    return false;
                };
            }
        }
        
        mobileMenu.appendChild(link);
    });
    
    // Добавляем меню к навигации
    const nav = document.querySelector('.header-nav .container');
    nav.style.position = 'relative'; // Делаем навигацию позиционируемой
    nav.appendChild(mobileMenu);
    toggle.classList.add('active');
    toggle.setAttribute('aria-expanded', 'true');
    
    // Закрытие при клике вне меню
    setTimeout(() => {
        document.addEventListener('click', function closeMenu(e) {
            if (!mobileMenu.contains(e.target) && !toggle.contains(e.target)) {
                toggleMobileNav();
                document.removeEventListener('click', closeMenu);
            }
        });
    }, 100);
    
    console.log('Меню создано и показано');
}



// Экспорт для модульных систем
if (typeof module !== 'undefined' && module.exports) {
    module.exports = SDLHSite;
} 