from pydantic import BaseModel
from datetime import datetime

class ClientBase(BaseModel):
    name: str
    client_pas: str  # Пароль, который будет хешироваться

class ClientCreate(ClientBase):
    pass

class Client(ClientBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True  # Включаем поддержку SQLAlchemy моделей
