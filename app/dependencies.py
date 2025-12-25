from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from jose import JWTError, jwt
from repositories.user_repository import IUserRepository, InMemoryUserRepository
from repositories.room_repository import IRoomRepository, InMemoryRoomRepository
from models.user import UserInDB
from services.auth_service import AuthService

security = HTTPBearer()
SECRET_KEY = "d7c7a7eaf565eaee31291b478320e4a2d9126405aa0d6074657e5ce5c8f0fccd"
ALGORITHM = "HS256"

def get_user_repo() -> IUserRepository:
    """Получение базы данных c пользоватлями"""
    return InMemoryUserRepository()

def get_room_repo() -> IRoomRepository:
    """Получение базы данных c комнатами"""
    return InMemoryRoomRepository()

def get_auth_service() -> AuthService:
    """Получение сервиса аутентификации"""
    return AuthService(get_user_repo())

async def get_current_user(credentials=Depends(security)):
    """Получение текущего пользователя из токена"""
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = get_user_repo().get_by_username(username)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


async def get_admin_user(current_user: UserInDB = Depends(get_current_user)):
    "Проверка, что пользователь является адвинистратором"
    if current_user.role != "administrator":
        
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав"
        )
    return current_user