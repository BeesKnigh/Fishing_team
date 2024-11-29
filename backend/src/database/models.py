from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime

Base = declarative_base()

class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    client_pas = Column(String)  # Пароль, будем хешировать
    created_at = Column(DateTime, default=datetime.utcnow)

# Создание базы данных
DATABASE_URL = "sqlite:///./test.db"  # Используем SQLite для простоты

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Функция для создания таблиц
def init_db():
    Base.metadata.create_all(bind=engine)
