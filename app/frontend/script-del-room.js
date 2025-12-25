let token = localStorage.getItem('auth_token');

async function delRoom() {
    if (!token) {
        alert('Доступ запрещён. Войдите в систему.');
        window.location.href = '/static/index.html';
        return;
    }

    const checkResponse = await fetch('/rooms', {
        headers: { 'Authorization': `Bearer ${token}` }
    });

    if (checkResponse.status === 403 || checkResponse.status === 401) {
        alert('Доступ запрещён. Только для администратора.');
        window.location.href = '/static/index.html';
        return;
    }

    const form = document.getElementById('del-room-form');
    const errorEl = document.getElementById('error-message');

    if (!form) {
        console.error('Форма не найдена');
        return;
    }

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        errorEl.textContent = '';

        const room_id = document.getElementById('room_id').value.trim();

        if (!room_id || room_id <= 0) {
            errorEl.textContent = 'Введите корректный ID комнаты';
            return;
        }

        if (!confirm(`Вы уверены, что хотите удалить комнату с ID ${room_id}?\nЭто действие необратимо!`)) {
            return;
        }

        const response = await fetch(`/rooms/del-room?room_id=${room_id}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.ok) {
            alert('Комната успешно удалена!');
            window.location.href = '/static/index.html';
        } else {
            const data = await response.json();
            errorEl.textContent = data.detail || 'Ошибка при удалении комнаты';
        }
    });
}

// Запуск при загрузке страницы
document.addEventListener('DOMContentLoaded', delRoom);