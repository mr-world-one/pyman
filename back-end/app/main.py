import sys
sys.path.append("C:\\Users\\it-support\\pyman")  
from fastapi import FastAPI, HTTPException, Depends
import asyncpg
import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine
import logging
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from scraper.parsers.rozetka_parser import RozetkaParser
from fastapi import FastAPI, File, UploadFile

# Local imports
from .routers import crud, xpath
from .routers.authorization import router as auth_router, get_current_user
from .database import Base
from .db_test import verify_database_connection
# ... решта коду без змін

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()
app = FastAPI(
    title="CheckIT API",
    description="API for tender checking and analysis",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", "http://localhost:5174", "http://localhost:5175", "http://localhost:5176", "http://localhost:5177",
        "http://localhost:5178", "http://localhost:5179", "http://localhost:5180", "http://localhost:5181", "http://localhost:5182",
        "http://127.0.0.1:5173", "http://127.0.0.1:5174", "http://127.0.0.1:5175", "http://127.0.0.1:5176", "http://127.0.0.1:5177",
        "http://127.0.0.1:5178", "http://127.0.0.1:5179", "http://127.0.0.1:5180", "http://127.0.0.1:5181", "http://127.0.0.1:5182"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database initialization
async def init_db():
    try:
        if not await verify_database_connection():
            raise Exception("Database connection verification failed")

        engine = create_async_engine(
            os.getenv("DATABASE_URL"),
            echo=True,
            pool_pre_ping=True,
            pool_size=5,
            max_overflow=10
        )
        
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            logger.info("Database tables created successfully")
            
        return engine
    except Exception as e:
        logger.error(f"Database initialization failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Database initialization failed: {str(e)}"
        )

@app.on_event("startup")
async def startup():
    try:
        await init_db()
        logger.info("Application startup completed successfully")
    except Exception as e:
        logger.error(f"Application startup failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Application startup failed: {str(e)}"
        )

# Include routers with authentication
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(
    crud.router,
    prefix="/api",
    tags=["CRUD Operations"],
    dependencies=[Depends(get_current_user)]
)
app.include_router(
    xpath.router,
    prefix="/xpath",
    tags=["XPath Operations"],
    dependencies=[Depends(get_current_user)]
)

@app.get("/", tags=["Root"])
async def home() -> dict:
    return {
        "message": "Welcome to CheckIT API",
        "documentation": "/docs"
    }

async def test_db_connection():
    try:
        conn = await asyncpg.connect(
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            database=os.getenv("POSTGRES_DB"),
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT")
        )
        await conn.execute('SELECT 1')
        await conn.close()
        logger.info("Test database connection successful")
        return {
            "status": "success",
            "message": "Database connection successful",
            "details": {
                "host": os.getenv("POSTGRES_HOST"),
                "database": os.getenv("POSTGRES_DB"),
                "port": os.getenv("POSTGRES_PORT")
            }
        }
    except Exception as e:
        logger.error(f"Test database connection failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Database connection failed: {str(e)}"
        )

# @app.post("/excel-page")
# async def upload_excel(string):#(file: UploadFile = File(...)):
#     # # Читання Excel
#     # df = pd.read_excel(file.file, skiprows=1)  # Пропускаємо перший рядок (заголовки без назв)
#     # df.columns = ["Номер", "Назва товару", "Кількість", "Ціна, грн", "Сума, грн"]  # Встановлюємо правильні назви колонок
#     # df = df.dropna(subset=["Назва товару"])  # Видаляємо рядки без назв (наприклад, підсумок)

#     # products = df["Назва товару"].tolist()  # Список назв товарів
#     # excel_prices = df["Ціна, грн"].tolist()  # Список цін із тендеру

#     product = "Iphone 16"

#     # Ініціалізація парсера Rozetka
#     rozetka = RozetkaParser()
#     comp = rozetka.find_n_products(product)

#     # Збір даних і порівняння
#     # comparison = []
#     # for product, excel_price in zip(products, excel_prices):
#     #     # Парсимо 5 товарів із Rozetka
#     #     rozetka_data = rozetka.find_n_products(
#     #         product=product,
#     #         n = 2,  # Шукаємо 2 товарів
#     #         fast_parse=True,  # Тільки price і title
#     #         ignore_price_format=True,  # Повертаємо рядок, якщо не float
#     #         raise_exception=False  # Пропускаємо помилки
#     #     )

#     #     # Вибираємо найнижчу ціну
#     #     prices = [item.price for item in rozetka_data if item.price is not None]
#     #     rozetka_price = min(prices, default=None) if prices else None
#     #     rozetka_title = rozetka_data[0].title if rozetka_data else product  # Беремо першу назву або з Excel

#     #     comparison.append({
#     #         "name": rozetka_title,
#     #         "excelPrice": excel_price,
#     #         "rozetkaPrice": rozetka_price
#     #     })
#     return comp

@app.post("/excel-page")
async def upload_excel():
    try:
        product = "iphone"
        rozetka = RozetkaParser()
        rozetka_data = rozetka.find_n_products(
            product=product,
            n=2,
            fast_parse=True,
            ignore_price_format=True,
            raise_exception=False
        )
    except Exception as e:
        return "Error"
    return "Success"