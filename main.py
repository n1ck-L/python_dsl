from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import Response
from datetime import datetime
import uvicorn
from models import User, UserResponse, Token, UserListItem, UserListResponse, USERS
from auth import get_current_user, create_access_token, verify_password

from datetime import timedelta

app = FastAPI()

# Создаем URL-префикс, по которому будут доступны файлы
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.post("/login", response_model=Token)
async def login(user_data: User):
    """Авторизация пользователя"""
    if not verify_password(user_data.username, user_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль",
        )
    
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user_data.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/me", response_model=UserResponse)
async def read_users_me(current_user: dict = Depends(get_current_user)):
    """Получение информации о текущем пользователе"""
    return {
        "username": current_user["username"],
        "role": current_user["role"],
        "full_name": current_user["full_name"]
    }

@app.get("/")
async def serve_frontend():
    with open("frontend/index.html", "r", encoding="utf-8") as f:
        return Response(content=f.read(), media_type="text/html")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}


@app.get("/users", response_model=UserListResponse)
async def get_all_users():
    """Получение списка всех зарегистрированных пользователей"""
    try:
        # Преобразуем хардкодированных пользователей в нужный формат
        users_list = []
        
        for username, user_data in USERS.items():
            user_item = UserListItem(
                username=user_data["username"],
                full_name=user_data["full_name"],
                role=user_data["role"]
            )
            users_list.append(user_item)
        
        # Формируем ответ
        response = UserListResponse(
            users=users_list,
            total=len(users_list),
            timestamp=datetime.utcnow().isoformat()
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении списка пользователей: {str(e)}"
        )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8443,
        ssl_keyfile="resources/server.key",
        ssl_certfile="resources/server.crt",
        reload=True
    )