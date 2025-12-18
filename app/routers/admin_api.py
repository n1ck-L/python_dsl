# app/routers/user.py   (или admin.py — как захочешь)
from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime
from typing import List

from models.user import UserListItem, UserListResponse, UserInDB
from repositories.user_repository import AbstractUserRepository
from dependencies import get_user_repo, get_current_user  

router = APIRouter()


async def get_admin_user(current_user: UserInDB = Depends(get_current_user)):
    if current_user.role != "administrator":
        
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав"
        )
    return current_user


@router.get("/users", response_model=UserListResponse)
async def get_all_users(
    repo: AbstractUserRepository = Depends(get_user_repo),
    admin: UserInDB = Depends(get_admin_user)  # данная зависимость, будет гарантировать, что только админ модет получить доступ к /users
):
    """
    Получение списка всех пользователей. Доступно только администратору
    """
    raw_users = repo.get_all()

    users_list: List[UserListItem] = [
        UserListItem(
            username=user.username,
            full_name=user.full_name,
            role=user.role
        )
        for user in raw_users
    ]

    return UserListResponse(
        users=users_list,
        total=len(users_list),
        timestamp=datetime.utcnow().isoformat()
    )


@router.post("/users")
async def add_new_user(
        form: UserInDB,
        repo: AbstractUserRepository = Depends(get_user_repo),
        admin: UserInDB = Depends(get_admin_user)
    ):
    """
    Добалвление нового пользователя. Доступно только администратору
    """
    repo.add_new_user(form)


@router.delete("/users/{username}")
async def delete_user(
        username: str,
        repo: AbstractUserRepository = Depends(get_user_repo),
        admin: UserInDB = Depends(get_admin_user)
    ):
    """
    Добалвление нового пользователя. Доступно только администратору
    """
    repo.delete_user(username)