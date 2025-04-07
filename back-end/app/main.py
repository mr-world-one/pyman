# Third-party imports
from fastapi import FastAPI, HTTPException, Depends
import asyncpg
import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine
import logging
from fastapi.middleware.cors import CORSMiddleware

# Local imports
from app.routers import crud, xpath
from app.routers.authorization import get_current_user
from app.routers import temporary_router, xpath, authorization as auth_router
from app.database import Base
from app.db_test import verify_database_connection

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
app.include_router(authentication.router)
app.include_router(temporary_router.router)

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