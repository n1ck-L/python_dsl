## Cистема резервирования объектов на FastAPI

На данный момент проект представляет собой полностью рабочий пример системы резервирования с использованием FastAPI, JWT-токенов и самоподписанного SSL-сертификата. В данной системе реализована возможность резервирования объектов, поиска по тегам с помощь boolia, а также возможность мгновенного резрирования при поиске. Помио этого, реализована панель администратора для пользователя с ролью "administrator" с раширенными возможностями управления.


Два хардкодных пользователя:
- admin / admin123 → роль administrator
- user  / user123  → роль user

Оссобенности:
- Выдача JWT-токена сроком действия 30 минут
- Сервер работает только по HTTPS (порт 8443)
- фронтенд на js, html, css
- использование dsl из библиотеки boolia для поиска объектов по тегам

### Структура проекта
```
app/
├── frontend/
|
├── models/                 # директория c Pydantic-схемами для API
│   ├── room.py
│   └── user.py
├── repositories/           # директория с классами и интерфейсами для работы с БД
│   ├── room_repository.py
│   └── user_repository.py
├── resources/              # директория для размещения SSL-сертификатов 
│   ├── server.key
│   └── server.crt
├── routers/                # директория с реализауией API
│   ├── auth_api.py
│   ├── rooms_api.py
│   └── users_api.py
├── services/               # директория с сервисами приложенич
│   └── auth_service.py
├── dependecies.py          # функции, используемые в качестве зависимостей конечных точек
├── main.py                 # основной файл FastAPI
└── static/                 # мнимая директория, автоматически монтируется из папки frontend
```
### Инструкция по запуску

#### 1. Склонировать или скачать репозиторий
```bash
git clone https://github.com/n1ck-L/python_dsl.git
cd python_dsl
```
#### 2. Убедиться, что установлен Python ≥ 3.9

#### 3. Создать и активировать виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate          # Linux/macOS
# или
venv\Scripts\activate             # Windows
```

#### 4. Установить зависимости:
```Bash
pip install -r requirements.txt
# или
python -m pip install -r requirements.txt
```
#### 5. Создать папку для сертификатов и сгенерировать самоподписанный сертификат:

```Bash
mkdir app/resources
cd app/resources
```

#### 6. Генерация самоподписанного сертификата:

#### 6.1. Генерируем приватный ключ сервера (аналог ca.key)
```bash
openssl genrsa -out server.key 4096
```

#### 6.2. Создаём самоподписанный сертификат сервера (он же будет и корневым CA для клиента)
```bash
openssl req -new -x509 \
    -key server.key \
    -out server.crt \
    -days 3650 \
    -subj "/C=RU/ST=Moscow/O=Test CA/CN=localhost" \
    -addext "subjectAltName = DNS:localhost, DNS:*.localhost, IP:127.0.0.1"
```

#### 6.3. Проверка того, что получилось (опционально) 
```bash
openssl x509 -in server.crt -text -noout | grep -E "Subject:|Issuer:|DNS:|IP Address"
```

После выполнения команды в каталоге resources/ появятся файлы server.key и server.crt.

#### 7. Запустить приложение:

```Bash
cd ../..
python main.py
```

#### 8. Открыть в браузере адрес: https://0.0.0.0:8443
! Браузер покажет предупреждение о самоподписанном сертификате — необходимо принять его (кнопка «Продолжить», «Принять риск» и т.п.).

![alt text](img/image.png)


### Где искать нужный код при дальнейшем развитии

- Изменить/добавить/удалить пользователей — app/repositories/user_repository.py
- Изменить/добавить/удалить комнаты - app/repositories/room_reposotory.py
- Изменить время жизни токена — app/services/auth_service.py константа ACCESS_TOKEN_EXPIRE_MINUTES
- Добавить новые endpoint — директория app/routets/
- Доработать фронтенд — frontend/script-main.js - основная логика, frontend/style.css - стили, frontend/indes.html - описание страницы
