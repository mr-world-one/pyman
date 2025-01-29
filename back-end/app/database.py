from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "postgresql+asyncpg://postgres:573572S@localhost:5432/Softserve_project_db"

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
