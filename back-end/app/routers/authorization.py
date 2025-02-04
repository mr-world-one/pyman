from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession  # Імпортуємо AsyncSession
from sqlalchemy.future import select  # Для асинхронних запитів
from app.schemas.schema import UserCreate, Token
from app.models.model import User
from app.database import get_db
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional  # Імпортуємо для використання Optional

# Конфігурація JWT
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Хешування паролів
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()

# Функція хешування пароля
def get_password_hash(password: str):
    return pwd_context.hash(password)

# Функція перевірки пароля
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Генерація JWT-токена
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Реєстрація нового користувача
@router.post("/register", response_model=Token)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):  # Використовуємо AsyncSession
    # Виконуємо асинхронний запит для перевірки, чи існує користувач
    result = await db.execute(select(User).filter(User.email == user.email))
    db_user = result.scalar_one_or_none()
    
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    new_user = User(name=user.name, email=user.email, hashed_password=hashed_password)  # Виправлено тут
    
    db.add(new_user)
    await db.commit()  # Використовуємо асинхронний commit
    await db.refresh(new_user)  # Оновлюємо користувача після коміту
    
    access_token = create_access_token(data={"sub": new_user.name})
    return {"access_token": access_token, "token_type": "bearer"}


# Авторизація користувача
@router.post("/login", response_model=Token)
async def login(user: UserCreate, db: AsyncSession = Depends(get_db)):  # Використовуємо AsyncSession
    result = await db.execute(select(User).filter(User.email == user.email))
    db_user = result.scalar_one_or_none()

    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": db_user.name})
    return {"access_token": access_token, "token_type": "bearer"}
