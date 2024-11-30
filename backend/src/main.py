from fastapi import FastAPI
from api.client import router as client_router
from database.models import init_db

app = FastAPI()

# Инициализация базы данных
init_db()

# Подключение роутера
app.include_router(client_router)
