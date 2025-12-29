let token = localStorage.getItem('auth_token');

async function delUser() {
    if (!token) {
        alert('Доступ запрещён. Войдите в систему.');
        window.location.href = '/static/index.html';
        return;
    }

    const response = await fetch('/users/', {
        headers: { 'Authorization': `Bearer ${token}` }
    });

    if (response.status === 403) {
        alert('Доступ запрещён. Только для администратора.');
        window.location.href = '/static/index.html';
        return;
    }

    const form = document.getElementById('del-user-form');
    const errorEl = document.getElementById('error-message');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        errorEl.textContent = '';

        const username = document.getElementById('username').value.trim();

        const response = await fetch(`/users/del-user?username=${username}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.ok) {
            window.location.href = '/static/index.html';
        }
        else {
            const data = await response.json();
            errorEl.textContent = data.detail || 'Ошибка при удалении пользователя';
        }
    });
};

document.addEventListener('DOMContentLoaded', delUser);