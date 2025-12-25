from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime
from typing import List

from models.user import UserListItem, UserListResponse, UserInDB
from repositories.user_repository import IUserRepository
from dependencies import get_user_repo, get_admin_user  

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=UserListResponse)
async def get_all_users(
    repo: IUserRepository = Depends(get_user_repo),
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
        timestamp=datetime.now().isoformat()
    )


@router.post("/add-user")
async def add_new_user(
        form: UserInDB,
        repo: IUserRepository = Depends(get_user_repo),
        admin: UserInDB = Depends(get_admin_user)
    ):
    """
    Добалвление нового пользователя. Доступно только администратору
    """
    repo.add_new_user(form)


@router.delete("/del-user")
async def delete_user(
        username: str,
        repo: IUserRepository = Depends(get_user_repo),
        admin: UserInDB = Depends(get_admin_user)
    ):
    """
    Добалвление нового пользователя. Доступно только администратору
    """
    repo.delete_user(username)