from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class RoomBase(BaseModel):
    name: str
    description: Optional[str] = None
    tags: List[str] = []  # теги для логического выражения

class RoomInDB(RoomBase):
    id: int
    booked: bool = False
    booked_by: Optional[str] = None
    booked_at: Optional[datetime] = None

class BookingRequest(BaseModel):
    room_id: int

class SearchRequest(BaseModel):
    request: str