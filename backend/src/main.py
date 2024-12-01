from fastapi import FastAPI
from api.client import router as client_router
from database.models import init_db
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Разрешаем запросы с фронтенда (из вашего локального хоста)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:63342"],  # Разрешаем только с вашего фронтенда
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все методы (GET, POST и т.д.)
    allow_headers=["*", "Authorization"],  # Разрешаем все заголовки
)

# Инициализация базы данных
init_db()

# Подключение роутера
app.include_router(client_router)

