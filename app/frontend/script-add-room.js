let token = localStorage.getItem('auth_token');

async function addRoom() {
    if (!token) {
        alert('Доступ запрещён. Войдите в систему.');
        window.location.href = '/static/index.html';
        return;
    }

    // Проверка прав администратора
    const checkResponse = await fetch('/rooms', {
        headers: { 'Authorization': `Bearer ${token}` }
    });

    if (checkResponse.status === 403 || checkResponse.status === 401) {
        alert('Доступ запрещён. Только для администратора.');
        window.location.href = '/static/index.html';
        return;
    }

    const form = document.getElementById('add-room-form');
    const errorEl = document.getElementById('error-message');

    if (!form) {
        console.error('Форма не найдена');
        return;
    }

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        errorEl.textContent = '';

        const name = document.getElementById('name').value.trim();
        const description = document.getElementById('description').value.trim();
        const tagsInput = document.getElementById('tags').value.trim();
        const tags = tagsInput 
            ? tagsInput.split(',').map(tag => tag.trim()).filter(tag => tag.length > 0)
            : [];

        if (!name) {
            errorEl.textContent = 'Введите название комнаты';
            return;
        }

        const response = await fetch('/rooms/add-room', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                name: name,
                description: description || null,
                tags: tags
            })
        });

        if (response.ok) {
            alert('Комната успешно добавлена!');
            window.location.href = '/static/index.html';
        } else {
            const data = await response.json();
            errorEl.textContent = data.detail || 'Ошибка при добавлении комнаты';
        }
    });
}

// Запуск при загрузке страницы
document.addEventListener('DOMContentLoaded', addRoom);