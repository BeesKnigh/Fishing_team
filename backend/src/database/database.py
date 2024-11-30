from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Здесь указываем путь к базе данных (в данном случае SQLite)
DATABASE_URL = "sqlite:///./test.db"

# Создаем движок для подключения к базе данных
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Создаем сессию для взаимодействия с базой данных
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Зависимость для получения сессии базы данных
def get_db():
    db = SessionLocal()  # Создаем сессию
    try:
        yield db  # Возвращаем сессию для использования в запросах
    finally:
        db.close()  # Закрываем сессию, когда она больше не нужна
