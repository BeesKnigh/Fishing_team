from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.models import Client as DBClient, SessionLocal, Card as DBCard
from database.schemas import Client, ClientCreate, Card, CardCreate, Token, TokenData
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import List

router = APIRouter()

# Секретный ключ для создания JWT токенов
SECRET_KEY = "your_secret_key_here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

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

# Функция для создания JWT токена
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Определение схемы OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Функция для получения текущего пользователя из JWT токена
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    return token_data

# Логин (получение JWT токена)
@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(DBClient).filter(DBClient.name == form_data.username).first()
    if user is None or not verify_password(form_data.password, user.client_pas):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": form_data.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

# Получить всех клиентов
@router.get("/clients", response_model=List[Client])
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
    hashed_password = hash_password(client.client_pas)
    db_client = DBClient(name=client.name, client_pas=hashed_password)
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

# Получить все карты для клиента
@router.get("/cards/{client_id}", response_model=List[Card])
def get_cards(client_id: int, db: Session = Depends(get_db)):
    cards = db.query(DBCard).filter(DBCard.client_id == client_id).all()
    if not cards:
        raise HTTPException(status_code=404, detail="Cards not found")
    return cards

# Создать новую карту
@router.post("/cards", response_model=Card)
def create_card(card: CardCreate, db: Session = Depends(get_db)):
    db_card = DBCard(
        card_type=card.card_type,
        card_status=card.card_status,
        expiration_date=card.expiration_date,
        balance=card.balance,
        client_id=card.client_id
    )
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card
