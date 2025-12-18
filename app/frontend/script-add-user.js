let token = localStorage.getItem('auth_token');

async function addUser() {
    if (!token) {
        alert('Доступ запрещён. Войдите в систему.');
        window.location.href = '/static/index.html';
        return;
    }

    const response = await fetch('/users', {
        headers: { 'Authorization': `Bearer ${token}` }
    });

    if (response.status === 403) {
        alert('Доступ запрещён. Только для администратора.');
        window.location.href = '/static/index.html';
        return;
    }

    const form = document.getElementById('add-user-form');
    const errorEl = document.getElementById('error-message');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        errorEl.textContent = '';

        const username = document.getElementById('username').value.trim();
        const full_name = document.getElementById('full_name').value.trim();
        const password = document.getElementById('password').value;
        const role = document.getElementById('role').value;

        if (password.length < 8) {
            errorEl.textContent = 'Пароль должен содержать минимум 6 символов';
            return;
        }

        const response = await fetch('/users', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                username,
                full_name,
                password,
                role
            })
        });

        if (response.ok) {
            alert('Пользователь успешно добавлен!');
            window.location.href = '/static/admin-users.html';
        }
        else {
            const data = await response.json();
            errorEl.textContent = data.detail || 'Ошибка при добавлении пользователя';
        }
    });
};

// Запускаем при загрузке страницы
document.addEventListener('DOMContentLoaded', addUser);