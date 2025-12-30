from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from boolia import evaluate

from models.room import RoomInDB, RoomBase, BookingRequest, SearchRequest
from repositories.room_repository import IRoomRepository
from dependencies import get_room_repo, get_current_user, get_admin_user
from models.user import UserInDB

router = APIRouter(prefix="/rooms", tags=["rooms"])

@router.get("/", response_model=List[RoomInDB])
async def get_all_rooms(repo: IRoomRepository = Depends(get_room_repo)):
    """Список всех объектов бронирования"""
    return repo.get_all()


@router.post("/book")
async def book_room(
    request: BookingRequest,
    repo: IRoomRepository = Depends(get_room_repo),
    current_user: UserInDB = Depends(get_current_user)
):
    """Бронирование объекта (требует аутентификации)"""
    success = repo.book_room(request.room_id, current_user.username)
    if not success:
        raise HTTPException(status_code=400, detail="Объект уже забронирован или не существует")
    

@router.post("/unbook")
async def unbook_room(
    request: BookingRequest,
    repo: IRoomRepository = Depends(get_room_repo),
    current_user: UserInDB = Depends(get_current_user)
):
    """Бронирование объекта (требует аутентификации)"""
    success = repo.unbook_room(request.room_id, current_user.username, current_user.role)
    if not success:
        raise HTTPException(status_code=400, detail="Объект уже освобожден или не существует")
    

@router.post("/add-room")
async def add_room(
    room_data: RoomBase,
    repo: IRoomRepository = Depends(get_room_repo),
    admin: UserInDB = Depends(get_admin_user)
):
    """Добавление новой комнаты - только для админа"""
    repo.add_room(room_data)


@router.delete("/del-room")
async def delete_room(
    room_id: int,
    repo: IRoomRepository = Depends(get_room_repo),
    admin: UserInDB = Depends(get_admin_user)
):
    """Удаление комнаты по ID - только для админа"""
    success = repo.delete_room(room_id)
    if not success:
        raise HTTPException(status_code=404, detail="Комната не найдена")
    return {"detail": "Комната успешно удалена"}


@router.post("/search", response_model=List[RoomInDB])
async def boolia_search(
    query: SearchRequest,
    repo: IRoomRepository = Depends(get_room_repo),
):
    all_rooms = repo.get_all()
    filtered_rooms = []
    for room in all_rooms:
        set_tags = set(room.tags)
        res = evaluate(query.request, context={}, tags=set_tags, on_missing="none")
        if res is not False:
            filtered_rooms.append(room)
    return filtered_rooms


@router.post("/search-and-book")
async def search_and_book(
    query: SearchRequest,
    repo: IRoomRepository = Depends(get_room_repo),
    current_user: UserInDB = Depends(get_current_user)
):
    """
    Атомарно ищет комнаты по тегам (как /search), находит первую свободную
    и сразу бронирует её на текущего пользователя.
    """
    all_rooms = repo.get_all()

    suitable_free_rooms = []
    for room in all_rooms:
        if room.booked:
            continue  # пропускаем уже забронированные

        set_tags = set(room.tags)
        res = evaluate(query.request, context={}, tags=set_tags, on_missing="none")
        if res is not False:
            suitable_free_rooms.append(room)

    if not suitable_free_rooms:
        raise HTTPException(status_code=404, detail="Подходящих свободных комнат не найдено")

    # Берём первую подходящую и пытаемся забронировать
    room_to_book = suitable_free_rooms[0]

    success = repo.book_room(room_to_book.id, current_user.username)
    if not success:
        raise HTTPException(status_code=400, detail="Комната стала недоступна в процессе бронирования")