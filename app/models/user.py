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
    password: str        # пока храним открыто, потом будет хеш
    role: str
    full_name: str

class Token(BaseModel):
    access_token: str
    token_type: str