let token = localStorage.getItem('auth_token');

// Проверка состояния системы
async function checkSystemStatus() {
    try {
        const response = await fetch('/health');
        const data = await response.json();
        document.getElementById('system-status').textContent = 
            `Система работает (${new Date(data.timestamp).toLocaleTimeString()})`;
    } catch (error) {
        document.getElementById('system-status').textContent = 'Система недоступна';
    }
}

// Функция входа
async function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const errorElement = document.getElementById('login-error');

    errorElement.textContent = '';

    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password })
        });

        if (!response.ok) {
            throw new Error('Неверные учетные данные');
        }

        const data = await response.json();
        token = data.access_token;
        
        // Сохраняем токен в localStorage
        localStorage.setItem('auth_token', token);
        
        // Показываем информацию о пользователе
        await loadUserInfo();
        
    } catch (error) {
        errorElement.textContent = 'Ошибка: ' + error.message;
    }
}

// Загрузка информации о пользователе
async function loadUserInfo() {
    if (!token) return;

    try {
        const response = await fetch('/me', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (!response.ok) {
            throw new Error('Ошибка авторизации');
        }

        const user = await response.json();
        
        // Заполняем информацию о пользователе
        document.getElementById('user-username').textContent = user.username;
        document.getElementById('user-role').textContent = user.role;
        document.getElementById('user-fullname').textContent = user.full_name;
        
        // Показываем блок с информацией
        document.getElementById('login-form').style.display = 'none';
        document.getElementById('user-info').style.display = 'block';

        if (user.role == "administrator") {
            document.getElementById('admin-panel').style.display = 'block';
        }
        
    } catch (error) {
        console.error('Error loading user info:', error);
        logout();
    }
}

// Выход из системы
function logout() {
    token = null;
    localStorage.removeItem('auth_token');
    document.getElementById('login-form').style.display = 'block';
    document.getElementById('user-info').style.display = 'none';
    document.getElementById('admin-panel').style.display = 'none';
    document.getElementById('username').value = '';
    document.getElementById('password').value = '';
    document.getElementById('login-error').textContent = '';
}

// Проверяем, есть ли сохраненный токен при загрузке страницы
document.addEventListener('DOMContentLoaded', async () => {
    checkSystemStatus();
    
    // Проверяем токен каждые 30 секунд
    setInterval(checkSystemStatus, 30000);
    
    if (token) {
        await loadUserInfo();
    }
});