from fastapi import APIRouter, Depends, HTTPException, status
from models.user import UserLogin, Token, UserResponse
from services.auth_service import AuthService
from dependencies import get_auth_service, get_current_user

router = APIRouter()

@router.post("/login", response_model=Token)
async def login(form: UserLogin, service: AuthService = Depends(get_auth_service)):
    """Авторизация пользователя"""
    user = service.authenticate(form.username, form.password)
    if not user:
        raise HTTPException(status_code=401, detail="Неверное имя пользователя или пароль")
    return {"access_token": service.create_token(user.username), "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
async def me(current_user = Depends(get_current_user)):
    """Получение информации о текущем пользователе"""
    return UserResponse(
        username=current_user.username,
        role=current_user.role,
        full_name=current_user.full_name
    )