from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Схема для авторизации
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str

# Базовая модель для клиента
class ClientBase(BaseModel):
    name: str
    client_pas: str  # Пароль, который будет хешироваться

class ClientCreate(ClientBase):
    pass

class Client(ClientBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True  # Для работы с SQLAlchemy моделями

# Модели для карты
class CardBase(BaseModel):
    card_type: str
    card_status: Optional[str] = "active"  # Значение по умолчанию
    expiration_date: datetime
    balance: float

class CardCreate(CardBase):
    client_id: int  # Мы передаем client_id для связи с клиентом

class Card(CardBase):
    id: int

    class Config:
        orm_mode = True  # Для работы с SQLAlchemy моделями
