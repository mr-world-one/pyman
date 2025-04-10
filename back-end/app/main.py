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
from app.routers.prozorro_router import prozorro_router
from statistics import mean
import logging
from io import BytesIO
from openpyxl import load_workbook


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
app.include_router(prozorro_router)


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


# rozetka = RozetkaParser()
# @app.get("/excel-page")
# async def upload_excel():
#     try:
#         product = "iphone"
#         rozetka_data = rozetka.find_n_products(
#             product=product,
#             n=2,
#             fast_parse=False,
#             ignore_price_format=True,
#             raise_exception=False
#         )
#         if not rozetka_data:
#             logger.warning("No products found")
#             return {"status": "warning", "message": "No products found", "data": []}
#         return {"status": "success", "message": "Products found", "data": rozetka_data}
#     except Exception as e:
#         logger.error(f"Error in upload_excel: {str(e)}")
#         return {"status": "error", "message": str(e), "data": []}

def parse_excel_file(file_content: bytes):
    try:
        workbook = load_workbook(filename=BytesIO(file_content))
        sheet = workbook.active
        
        headers = [cell.value for cell in sheet[1]]
        required_columns = ['Назва товару', 'Кількість', 'Ціна', 'Сума']
        
        if not all(col in headers for col in required_columns):
            raise ValueError("Excel file is missing required columns")
        
        col_indices = {header: idx for idx, header in enumerate(headers)}
        
        data = []
        for row_idx, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):
            quantity = row[col_indices['Кількість']]
            price = row[col_indices['Ціна']]
            total = row[col_indices['Сума']]
            
            if quantity is None or price is None or total is None:
                logger.info(f"Skipping row {row_idx} due to empty values")
                continue
                
            try:
                row_data = {
                    'product_name': row[col_indices['Назва товару']],
                    'original_quantity': int(quantity),
                    'original_price_uah': float(price),
                    'original_total_uah': float(total),
                    'rozetka_results': []
                }
                data.append(row_data)
            except (ValueError, TypeError) as e:
                logger.warning(f"Skipping row {row_idx} due to invalid data: {str(e)}")
                continue
        
        if not data:
            raise ValueError("No valid data found in the Excel file")
            
        return data
        
    except Exception as e:
        raise ValueError(f"Error parsing Excel file: {str(e)}")

@app.post("/excel-page")
async def upload_excel(file: UploadFile = File(...)):
    try:
        file_content = await file.read()
        data = parse_excel_file(file_content)
        rozetka = RozetkaParser()
        # Проходимо по кожному рядку і шукаємо продукти
        for row in data:
            product_name = row['product_name']
            if not product_name or not isinstance(product_name, str):
                logger.warning(f"Invalid product name in row: {row}")
                continue
                
            logger.info(f"Searching for: '{product_name}'")
            
            try:
                # Скидаємо будь-який внутрішній стан парсера, якщо це можливо
                if hasattr(rozetka, 'clear_cache'):
                    rozetka.clear_cache()
                
                # Виконуємо пошук для поточного товару
                rozetka_data = rozetka.find_n_products(
                    product=product_name.strip(),  # Видаляємо пробіли
                    n=2,
                    fast_parse=False,
                    ignore_price_format=True,
                    raise_exception=False
                )
                
                if not rozetka_data:
                    logger.warning(f"No products found for '{product_name}'")
                else:
                    for item in rozetka_data:
                        item_dict = item.__dict__ if hasattr(item, '__dict__') else dict(item)
                        # Перевіряємо, чи результат відповідає запиту
                        if product_name.lower() not in item_dict.get('title', '').lower():
                            logger.warning(f"Result '{item_dict.get('title', '')}' does not match '{product_name}'")
                            continue
                        row['rozetka_results'].append(item_dict)
                    logger.info(f"Found {len(row['rozetka_results'])} relevant products for '{product_name}'")
                    
            except Exception as e:
                logger.error(f"Error searching for '{product_name}': {str(e)}")
                continue
        
        has_results = any(row['rozetka_results'] for row in data)
        if not has_results:
            logger.warning("No products found for any item")
            return {"status": "warning", "message": "No products found for any item", "data": data}
            
        return {
            "status": "success",
            "message": "Products found",
            "data": data
        }
        
    except ValueError as ve:
        logger.error(f"ValueError in upload_excel: {str(ve)}")
        return {"status": "error", "message": str(ve), "data": []}
    except Exception as e:
        logger.error(f"Error in upload_excel: {str(e)}")
        return {"status": "error", "message": f"Unexpected error: {str(e)}", "data": []}

# @app.post("/excel-page")
# async def upload_excel(file: UploadFile = File(...)):
#     try:
#         file_content = await file.read()
#         data = parse_excel_file(file_content)

        
#         d = []
        
#         for row in data:
#             product_name = row['product_name']
#             logger.info(f"Searching for: '{product_name}'")

#             try:
#                 rozetka_data = rozetka.find_n_products(
#                     product=product_name,
#                     n=2,
#                     fast_parse=False,
#                     ignore_price_format=True,
#                     raise_exception=False
#                 )
#                 d.append(rozetka_data)
#                 print("success" + str(e))
#             except Exception as e:
#                 print("No result" + str(e))
#                 continue

#     except Exception as e:
#         return str(e)

#     return {
#         "status": "success",
#         "message": "Products found",
#         "data": d
#     }