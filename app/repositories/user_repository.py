from abc import ABC, abstractmethod
from typing import Optional
from models.user import UserInDB

class AbstractUserRepository(ABC):
    @abstractmethod
    def get_by_username(self, username: str) -> Optional[UserInDB]:
        pass

class InMemoryUserRepository(AbstractUserRepository):
    _db = {
        "admin": UserInDB(
            username="admin",
            password="admin123",
            role="administrator",
            full_name="Администратор Системы"
        ),
        "user": UserInDB(
            username="user",
            password="user123",
            role="user",
            full_name="Обычный Пользователь"
        ),
    }

    def get_by_username(self, username: str) -> Optional[UserInDB]:
        return self._db.get(username)