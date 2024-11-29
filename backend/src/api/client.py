from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.models import Client as DBClient, SessionLocal
from database.schemas import Client, ClientCreate
from passlib.context import CryptContext

router = APIRouter()

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# Зависимость для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Функция для хеширования пароля
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Функция для проверки пароля
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Получить всех клиентов
@router.get("/clients", response_model=list[Client])
def get_clients(db: Session = Depends(get_db)):
    clients = db.query(DBClient).all()
    return clients

# Получить клиента по ID
@router.get("/clients/{client_id}", response_model=Client)
def get_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(DBClient).filter(DBClient.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

# Создать нового клиента
@router.post("/clients", response_model=Client)
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    # Хешируем пароль перед сохранением
    hashed_password = hash_password(client.client_pas)
    db_client = DBClient(name=client.name, client_pas=hashed_password)
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client
