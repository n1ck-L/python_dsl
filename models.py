from pydantic import BaseModel
from typing import List

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


class UserListItem(BaseModel):
    """Модель для элемента списка пользователей"""
    username: str
    full_name: str
    role: str

class UserListResponse(BaseModel):
    """Модель ответа со списком пользователей"""
    users: List[UserListItem]
    total: int
    timestamp: str

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