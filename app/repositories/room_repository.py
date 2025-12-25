from abc import ABC, abstractmethod
from typing import List, Optional
from models.room import RoomInDB, RoomBase
from datetime import datetime

class IRoomRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[RoomInDB]:
        pass

    @abstractmethod
    def get_by_id(self, room_id: int) -> Optional[RoomInDB]:
        pass

    @abstractmethod
    def book_room(self, room_id: int, username: str) -> bool:
        pass

    @abstractmethod
    def unbook_room(self, room_id: int, username: str, role: str) -> bool:
        pass

    @abstractmethod
    def add_room(self, room_data: RoomBase) -> None:
        pass

    @abstractmethod
    def delete_room(self, room_id: int) -> bool:
        pass



class InMemoryRoomRepository(IRoomRepository):
    _db: List[RoomInDB] = [
        RoomInDB(id=1, name="Комната 1", description="Переговорная комната", tags=["wifi", "tv"], booked=False),
        RoomInDB(id=2, name="Комната 12", description="Переговорная комната", tags=["wifi", "coffee", "view"], booked=False),
        RoomInDB(id=3, name="Комната 3", description="Переговорная комната", tags=["wifi", "balcony", "smoking"], booked=True, booked_by="user"),
    ]
    _next_id = 4

    def get_all(self) -> List[RoomInDB]:
        return self._db[:]

    def get_by_id(self, room_id: int) -> Optional[RoomInDB]:
        for room in self._db:
            if room.id == room_id:
                return room
        return None

    def book_room(self, room_id: int, username: str) -> bool:
        for room in self._db:
            if room.id == room_id and not room.booked:
                room.booked = True
                room.booked_by = username
                room.booked_at = datetime.now()
                return True
        return False
    
    def unbook_room(self, room_id: int, username: str, role: str) -> bool:
        for room in self._db:
            if room.id == room_id and room.booked:
                if room.booked_by == username or role == "administrator":
                    room.booked = False
                    room.booked_by = None
                    room.booked_at = None
                    return True
        return False
    
    def add_room(self, room_data: RoomBase):
        new_room = RoomInDB(
            id=self._next_id,
            name=room_data.name,
            description=room_data.description,
            tags=room_data.tags,
            booked=False
        )
        self._db.append(new_room)
        self._next_id += 1

    def delete_room(self, room_id: int) -> bool:
        for i, room in enumerate(self._db):
            if room.id == room_id:
                del self._db[i]
                return True
        return False