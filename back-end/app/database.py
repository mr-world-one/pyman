from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

#loading all data from .env file
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

#  асинхронний двигун бази даних
engine = create_async_engine(DATABASE_URL, echo=True)

# Фабрика сесій для роботи з БД
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

# Базовий клас моделей
Base = declarative_base()

# Функція для отримання сесії (залежність FastAPI)
async def get_db():
    async with SessionLocal() as session:
        yield session
