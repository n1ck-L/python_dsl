let token = localStorage.getItem('auth_token');

async function loadUsers() {

    if (!token) {
        alert('Вы не авторизованы');
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

    if (!response.ok) throw new Error('Ошибка загрузки');

    const data = await response.json();

    const list = document.getElementById('users-list');
    list.innerHTML = `<p>Всего пользователей: <strong>${data.total}</strong></p><ul>`;
    data.users.forEach(user => {
        list.innerHTML += `
            <li class="user-list-items">
                <strong>${user.username}</strong> (${user.role}) — ${user.full_name}
            </li>`;
    });
}

// Запускаем при загрузке страницы
document.addEventListener('DOMContentLoaded', loadUsers);