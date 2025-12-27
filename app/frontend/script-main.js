let token = localStorage.getItem('auth_token');
let currentUsername = null;
let currentUserrole = null;

// Переключение вкладок
function openTab(tabName) {
    document.querySelectorAll('.tab-content').forEach(tab => tab.style.display = 'none');
    document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('active'));

    document.getElementById(tabName + '-tab').style.display = 'block';
    document.querySelector(`button[onclick="openTab('${tabName}')"]`).classList.add('active');
}

// Вход
async function login() {
    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value;
    const errorElement = document.getElementById('login-error');

    errorElement.textContent = '';

    if (!username || !password) {
        errorElement.textContent = 'Заполните все поля';
        return;
    }

    const response = await fetch('/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    });

    if (!response.ok) {
        const err = await response.json();
        throw new Error(err.detail || 'Неверные данные');
    }

    const data = await response.json();
    token = data.access_token;
    localStorage.setItem('auth_token', token);

    await loadUserInfoAndShowInterface();
}

// Загрузка данных и показ интерфейса
async function loadUserInfoAndShowInterface() {
    const response = await fetch('/me', {
        headers: { 'Authorization': `Bearer ${token}` }
    });

    if (!response.ok) throw new Error('Токен недействителен');

    const user = await response.json();

    document.getElementById('user-username').textContent = user.username;
    document.getElementById('user-fullname').textContent = user.full_name;
    document.getElementById('user-role').textContent = user.role;
    currentUsername = user.username;
    currentUserrole = user.role

    // Скрываем логин, показываем основной интерфейс
    document.getElementById('login-form').style.display = 'none';
    document.getElementById('main-interface').style.display = 'block';
    
    if (user.role === "administrator") {
        document.getElementById('admin-panel-tab').style.display = 'block';
        openTab('admin');
        loadUsers()
        loadRoomsAdmin()
    }
    else{
        openTab('rooms');
    }

    loadRooms();
}

// Загрузка всех комнат в таблицу
async function loadRooms() {
    document.getElementById('search-query').value = '';

    const response = await fetch('/rooms/', {
        headers: { 'Authorization': `Bearer ${token}` }
    });

    if (!response.ok) throw new Error('Ошибка загрузки');

    const rooms = await response.json();

    printRooms(rooms);
}

// Поиск комнат по тегам
async function searchRooms() {
    const rooms = await booliaSearch();
    printRooms(rooms);
}

// Поиск комнат и бронирование
async function searchAndBook() {
    const rooms = await booliaSearch();
    if (rooms.length !== 0) {
        // Ищем первую незабронированную комнату
        const firstBooked = rooms.find(room => room.booked === false);
        
        if (firstBooked !== undefined) {
            bookRoom(firstBooked.id);
        }
        else {
            loadRooms();
        }
    }
}

// Функция обращения к API /search
async function booliaSearch() {
    const query_str = document.getElementById('search-query').value;

    const response = await fetch('/rooms/search', {
        method: 'POST',
        headers: { 
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}` 
        },
        body: JSON.stringify({ request: query_str })
    });

    if (!response.ok) throw new Error('Ошибка загрузки');

    const rooms = await response.json();

    return rooms;
}

// Выводит комнаты в виде таблицы
function printRooms(rooms) {
    const tbody = document.getElementById('rooms-list');

    if (rooms.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6">Нет доступных комнат</td></tr>';
        return;
    }

    tbody.innerHTML = '';
    rooms.forEach(room => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${room.id}</td>
            <td><strong>${room.name}</strong></td>
            <td>${room.description || '-'}</td>
            <td>${room.tags.length ? room.tags.join(', ') : '-'}</td>
            <td class="${room.booked ? 'status-booked' : 'status-free'}">
                ${room.booked ? `Забронирована (${room.booked_by || '—'})` : 'Свободна'}
            </td>
            <td>
                ${!room.booked 
                    ? `<button onclick="bookRoom(${room.id})">Забронировать</button>`
                    : ((currentUserrole === "administrator" || room.booked_by === currentUsername)
                        ? `<button onclick="unbookRoom(${room.id})">Освободить</button>`
                        : '')
                }
            </td>
        `;
        tbody.appendChild(row);
    });
}

// Бронирование
async function bookRoom(roomId) {
    const response = await fetch('/rooms/book', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ room_id: roomId })
    });

    if (!response.ok) {
        const err = await response.json();
        throw new Error(err.detail || 'Не удалось забронировать');
    }
    loadRooms();
    loadRoomsAdmin();
}

// Освобождение комнаты
async function unbookRoom(roomId) {
    const response = await fetch('/rooms/unbook', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ room_id: roomId })
    });

    if (!response.ok) {
        const err = await response.json();
        throw new Error(err.detail || 'Не удалось освободить');
    }

    loadRooms();
    loadRoomsAdmin();
}

// Выход
function logout() {
    token = null;
    localStorage.removeItem('auth_token');
    document.getElementById('login-form').style.display = 'block';
    document.getElementById('main-interface').style.display = 'none';
    document.getElementById('admin-panel-tab').style.display = 'none';
}

// Получение списка пользователей
async function loadUsers() {

    if (!token) {
        alert('Вы не авторизованы');
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

// Получение списка комнат
async function loadRoomsAdmin() {

    const response = await fetch('/rooms/', {
        headers: { 'Authorization': `Bearer ${token}` }
    });

    if (!response.ok) throw new Error('Ошибка загрузки');

    const rooms = await response.json();
    const roomsBody = document.getElementById('room-list-admin');
    roomsBody.innerHTML = `<p>Всего комнат: <strong>${rooms.length}</strong></p><ul>`;

    rooms.forEach(room => {
        roomsBody.innerHTML += `
            <li class="user-list-items">
                <strong>${room.name}</strong> (ID: ${room.id}) — <strong>Статус:</strong> ${room.booked 
            ? `Забронирована (${room.booked_by || 'неизвестно'})` 
            : 'Свободна'}
            </li>`;
    });
}

// При загрузке
document.addEventListener('DOMContentLoaded', async () => {
    if (token) {
        await loadUserInfoAndShowInterface();
    }
});