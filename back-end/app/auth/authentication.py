# Third-party imports  
from datetime import datetime, timedelta  
from fastapi import Depends, HTTPException, status  
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm  
from jose import JWTError, jwt  
from passlib.context import CryptContext  
from sqlalchemy.ext.asyncio import AsyncSession  
from sqlalchemy.future import select
from dotenv import load_dotenv
import os

# Local imports  
from app.database import get_db  
from app.models.model import User  
from app.schemas.schema import Token

#loading all data from .env file
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "token")


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(name: str, db: AsyncSession = Depends(get_db)):
    result = db.execute(select(User).filter(name == (User.name)))
    user = result.scalar_one_or_none()
    if user:
        return user
    else:
        return None

def authenticate_user(name: str, password: str, db: AsyncSession = Depends(get_db)):
    user = get_user(name, db)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False

    return user



def create_access_token(data: dict, expires_delta: timedelta or None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes = 20)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    credential_exception = HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials!", headers= {"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms= [ALGORITHM])
        name: str = payload.get("sub")
        if name is None:
            raise credential_exception

    except JWTError:
        raise credential_exception

    user = get_user(name, db)
    if user is None:
        raise credential_exception

    return user