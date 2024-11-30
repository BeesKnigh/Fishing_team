from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine
from datetime import datetime
import pytz

# Указываем часовой пояс UTC+3
timezone = pytz.timezone("Europe/Moscow")  # или другой нужный тебе часовой пояс

Base = declarative_base()

class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    client_pas = Column(String)  # Пароль, будем хешировать
    created_at = Column(DateTime, default=lambda: datetime.now(timezone))  # Используем текущий часовой пояс

    # Определение отношения с картами
    cards = relationship("Card", back_populates="owner")

class Transaction(Base):
    __tablename__ = 'transactions'

    transaction_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ip = Column(String, default="0.0.0.0")  # IP адрес по умолчанию
    device_id = Column(Float, nullable=False)
    device_type = Column(String, nullable=False)
    tran_code = Column(Integer, default=30)  # Код операции по умолчанию
    mcc = Column(Integer, default=1000)
    datetime = Column(DateTime, default=lambda: datetime.now(timezone))  # Текущее время по умолчанию
    sum = Column(Float, nullable=False)
    oper_type = Column(String, nullable=False)
    oper_status = Column(String, nullable=False)
    pin_inc_count = Column(Integer, nullable=False)  # Количество неверных попыток ПИН-кода
    client_id = Column(Integer, ForeignKey("clients.id"))  # Связь с клиентом
    client = relationship("Client", back_populates="transactions")

class Card(Base):
    __tablename__ = 'cards'

    id = Column(Integer, primary_key=True, index=True)
    card_type = Column(String, index=True)
    card_status = Column(String, default="active")  # Значение по умолчанию активна
    expiration_date = Column(String, default= "2030-06-10")
    balance = Column(Float, nullable=False)  # По умолчанию баланс 0
    client_id = Column(Integer, ForeignKey('clients.id'))

    # Определение отношения с владельцем (Client)
    owner = relationship("Client", back_populates="cards")


# Создание базы данных
DATABASE_URL = "sqlite:///./test.db"  # Используем SQLite для простоты

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Функция для создания таблиц
def init_db():
    Base.metadata.create_all(bind=engine)
