from fastapi import FastAPI
from .routers import temporary_router
from app.database import engine, Base
from logger import logger

app = FastAPI()

# Кріейтимо таблиці при запуску програми
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("startup")
async def startup():
    await init_db()

app.include_router(temporary_router.router)


@app.get("/")
def home() -> dict:
    logger.info("Home page")
    return {"msg" : "HomePage"}
