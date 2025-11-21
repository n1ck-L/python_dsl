from fastapi import FastAPI, Depends, HTTPException, status
from datetime import datetime
import uvicorn
from models import User, UserResponse, Token
from auth import get_current_user, create_access_token, verify_password
from datetime import timedelta

app = FastAPI()

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
async def root():
    """Корневой endpoint с информацией о API"""
    return {
        "message": "Auth API Service",
        "endpoints": {
            "login": "POST /login - авторизация пользователя",
            "me": "GET /me - информация о текущем пользователе",
            "docs": "GET /docs - интерактивная документация API"
        },
        "test_users": [
            {"username": "admin", "password": "admin123", "role": "administrator"},
            {"username": "user", "password": "user123", "role": "user"}
        ]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8443,
        ssl_keyfile="resources/server.key",
        ssl_certfile="resources/server.crt",
        reload=True
    )