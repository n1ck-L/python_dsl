from abc import ABC, abstractmethod
from typing import List, Optional
from models.room import RoomInDB, RoomBase
from datetime import datetime

ADMIN_ROLE = "administrator"
ROOM_TAG = "room"
FREE_ROOM_TAG = "free"
BOOKED_ROOM_TAG = "booked"
BOOKED_BY_TAG = "booked_by_"


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
        RoomInDB(id=1, name="Комната 1", description="Переговорная комната", tags=["room", "wifi", "free"], booked=False),
        RoomInDB(id=2, name="Комната 2", description="Переговорная комната", tags=["room", "coffee", "view", "free"], booked=False),
        RoomInDB(id=3, name="Комната 3", description="Переговорная комната", tags=["room", "wifi", "balcony", "smoking", "booked", "booked_by_user"], booked=True, booked_by="user"),
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
                room.tags.pop(room.tags.index(FREE_ROOM_TAG))
                room.tags.append(BOOKED_ROOM_TAG)
                room.tags.append(BOOKED_BY_TAG+username)
                return True
        return False
    
    def unbook_room(self, room_id: int, username: str, role: str) -> bool:
        for room in self._db:
            if room.id == room_id and room.booked:
                if room.booked_by == username or role == ADMIN_ROLE:
                    room.booked = False
                    room.booked_by = None
                    room.booked_at = None
                    room.tags.append(FREE_ROOM_TAG)
                    room.tags.pop(room.tags.index(BOOKED_ROOM_TAG))
                    room.tags.pop(room.tags.index(BOOKED_BY_TAG+username))
                    return True
        return False
    
    def add_room(self, room_data: RoomBase):
        room_data.tags.insert(0, ROOM_TAG)
        room_data.tags.append(FREE_ROOM_TAG)
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