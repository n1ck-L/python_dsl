from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import Response
<<<<<<< Updated upstream
from routers import auth_api, admin_api
from datetime import datetime
=======
from datetime import datetime
from routers import auth_api, users_api, rooms_api
>>>>>>> Stashed changes
import uvicorn

app = FastAPI()

# Создаем URL-префикс, по которому будут доступны файлы
app.mount("/static", StaticFiles(directory="app/frontend"), name="static")

app.include_router(auth_api.router)
<<<<<<< Updated upstream
app.include_router(admin_api.router)
=======
app.include_router(users_api.router)
app.include_router(rooms_api.router)
>>>>>>> Stashed changes


@app.get("/")
async def serve_frontend():
    with open("app/frontend/index.html", "r", encoding="utf-8") as f:
        return Response(content=f.read(), media_type="text/html")
    
@app.get("/health")
async def health_check():
    """Health check endpoint"""
<<<<<<< Updated upstream
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}
=======
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}
>>>>>>> Stashed changes


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8443,
        ssl_keyfile="app/resources/server.key",
        ssl_certfile="app/resources/server.crt",
        reload=True
    )