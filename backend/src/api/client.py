from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.models import Client as DBClient, Transaction as DBTransaction, Card as DBCard, BlacklistedToken
from database.schemas import Client, ClientCreate, Transaction, TransactionCreate, Card, CardCreate, TokenData, Token
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import List
from database.database import get_db
import os

router = APIRouter()

# Секретный ключ для создания JWT токенов
SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# Функция для хеширования пароля
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Функция для проверки пароля
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# Функция для добавления карт в таблицу транзакций
def add_cards_to_transactions(db: Session):
    # Получаем все карты из базы данных
    cards = db.query(DBCard).all()

    # Для каждой карты создаем транзакцию
    for card in cards:
        # Пример создания транзакции, данные для транзакции могут быть изменены в зависимости от логики
        db_transaction = DBTransaction(
            device_id=12345,  # Примерное значение
            device_type="ATM",  # Примерное значение
            tran_code=30,  # Примерное значение
            mcc=1000,  # Примерное значение
            datetime=datetime.now(),  # Время создания транзакции
            sum=card.balance,  # Баланс карты как сумма транзакции (можно заменить другой логикой)
            oper_type="purchase",  # Примерный тип операции
            oper_status="success",  # Примерный статус операции
            pin_inc_count=0,  # Примерное значение
            client_id=card.client_id  # Привязываем к клиенту
        )

        # Добавляем транзакцию в сессию и сохраняем
        db.add(db_transaction)

    # Сохраняем все транзакции в базе данных
    db.commit()


# Функция для создания JWT токена
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})

    # Добавляем client_id в токен
    client_id = data.get("client_id")
    if client_id:
        to_encode.update({"client_id": client_id})

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
        # Декодируем токен
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        client_id: int = payload.get("client_id")  # Добавляем извлечение client_id из токена

        if username is None or client_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Проверка, есть ли токен в черном списке
    blacklisted_token = db.query(BlacklistedToken).filter(BlacklistedToken.token == token).first()
    if blacklisted_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been blacklisted",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Если токен валидный и не в черном списке, возвращаем данные пользователя
    token_data = TokenData(username=username, client_id=client_id)  # Добавляем client_id в объект TokenData
    return token_data

# Логин (получение JWT токена)
@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(DBClient).filter(DBClient.name == form_data.username).first()
    if user is None or not verify_password(form_data.password, user.client_pas):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # Здесь мы добавляем client_id в данные для токена
    access_token = create_access_token(data={"sub": form_data.username, "client_id": user.id},
                                       expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout")
def logout(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # Добавляем токен в черный список
    blacklisted_token = BlacklistedToken(token=token)
    db.add(blacklisted_token)
    db.commit()

    # Теперь можно вернуться с сообщением об успешном выходе
    return {"message": "Logout successful"}

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

# Получить все транзакции
@router.get("/transactions", response_model=List[Transaction])
def get_transactions(db: Session = Depends(get_db)):
    transactions = db.query(DBTransaction).all()
    return transactions

# Получить транзакцию по ID
@router.get("/transactions/{transaction_id}", response_model=Transaction)
def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = db.query(DBTransaction).filter(DBTransaction.transaction_id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction

# Создать новую транзакцию
@router.post("/transactions", response_model=Transaction)
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    # Получаем карту по client_id
    db_card = db.query(DBCard).filter(DBCard.client_id == transaction.client_id).first()

    if db_card:
        # Если карта найдена, создаем транзакцию с данными карты
        db_transaction = DBTransaction(
            device_id=transaction.device_id,
            device_type=transaction.device_type,
            mcc=transaction.mcc,
            sum=transaction.sum,
            oper_type=transaction.oper_type,
            oper_status=transaction.oper_status,
            pin_inc_count=transaction.pin_inc_count,
            client_id=transaction.client_id,
            card_type=db_card.card_type,  # Добавляем тип карты
            card_status=db_card.card_status,  # Добавляем статус карты
            expiration_date=db_card.expiration_date,  # Добавляем дату истечения
            balance=db_card.balance  # Добавляем баланс
        )
    else:
        # Если карта не найдена, создаем транзакцию без данных карты
        db_transaction = DBTransaction(
            device_id=transaction.device_id,
            device_type=transaction.device_type,
            mcc=transaction.mcc,
            sum=transaction.sum,
            oper_type=transaction.oper_type,
            oper_status=transaction.oper_status,
            pin_inc_count=transaction.pin_inc_count,
            client_id=transaction.client_id
        )

    # Добавляем транзакцию в базу данных
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

# Получить все карты для клиента
@router.get("/cards/{client_id}", response_model=List[Card])
def get_cards(client_id: int, db: Session = Depends(get_db)):
    cards = db.query(DBCard).filter(DBCard.client_id == client_id).all()
    if not cards:
        raise HTTPException(status_code=404, detail="Cards not found")
    return cards

# Создать новую карту
@router.post("/cards", response_model=Card)
def create_card(card: CardCreate, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    # Используем client_id из текущего пользователя (извлечено из токена)
    client_id = current_user.client_id

    # Проверяем, существует ли клиент в базе данных
    client = db.query(DBClient).filter(DBClient.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    # Создаем карту с клиентом
    db_card = DBCard(
        card_type=card.card_type,
        card_status=card.card_status,
        expiration_date=card.expiration_date,
        balance=card.balance,
        client_id=client_id  # Привязываем карту к client_id из токена
    )

    db.add(db_card)
    db.commit()
    db.refresh(db_card)

    # Добавляем транзакции для привязанной карты
    add_cards_to_transactions(db)

    return db_card
