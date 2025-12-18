from abc import ABC, abstractmethod
from typing import Optional, List
from models.user import UserInDB

class AbstractUserRepository(ABC):
    @abstractmethod
    def get_by_username(self, username: str) -> Optional[UserInDB]:
        pass

    @abstractmethod
    def get_all(self) -> List[UserInDB]:
        pass

    @abstractmethod
    def add_new_user(self, new_data: UserInDB) -> None:
        pass

    @abstractmethod
    def delete_user(self, username: str) -> None:
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
    
    def get_all(self) -> List[UserInDB]:
        return list(self._db.values())
    
    def add_new_user(self, new_data):
        self._db[new_data.username] = new_data

    def delete_user(self, username):
        self._db.pop(username)