from pydantic import BaseModel

class User(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    username: str
    role: str
    full_name: str

class Token(BaseModel):
    access_token: str
    token_type: str

# Хардкод пользователей
USERS = {
    "admin": {
        "username": "admin",
        "password": "admin123",
        "role": "administrator",
        "full_name": "Администратор Системы"
    },
    "user": {
        "username": "user",
        "password": "user123",
        "role": "user",
        "full_name": "Обычный Пользователь"
    }
}