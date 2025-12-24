from pydantic import BaseModel

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    username: str
    role: str
    full_name: str

class UserInDB(BaseModel):
    username: str
    password: str
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
    users: list[UserListItem]
    total: int
    timestamp: str