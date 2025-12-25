from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from repositories.user_repository import IUserRepository
from models.user import UserResponse

SECRET_KEY = "d7c7a7eaf565eaee31291b478320e4a2d9126405aa0d6074657e5ce5c8f0fccd"
ALGORITHM = "HS256"

class AuthService:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def authenticate(self, username: str, password: str) -> Optional[UserResponse]:
        user = self.repo.get_by_username(username)
        if not user or user.password != password:
            return None
        return UserResponse(
            username=user.username,
            role=user.role,
            full_name=user.full_name
        )

    def create_token(self, username: str, expires_minutes: int = 30) -> str:
        expire = datetime.now() + timedelta(minutes=expires_minutes)
        to_encode = {"sub": username, "exp": expire}
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)