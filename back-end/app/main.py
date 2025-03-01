#Third-party imports
from fastapi import FastAPI, HTTPException
import asyncpg
import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine
import logging

#Local imports
from app.routers import temporary_router, authentication, xpath
from app.database import Base
from app.db_test import verify_database_connection

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
app = FastAPI()

# Database initialization
async def init_db():
    try:
        # First verify the connection
        if not await verify_database_connection():
            raise Exception("Database connection verification failed")

        # Create SQLAlchemy engine
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

app.include_router(temporary_router.router)
app.include_router(authentication.router)
app.include_router(xpath.router)

@app.get("/")
def home() -> dict:
    return {"msg": "HomePage"}

@app.get("/test-db")
async def test_database():
    return await test_db_connection()

async def test_db_connection():
    try:
        # Test raw connection
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