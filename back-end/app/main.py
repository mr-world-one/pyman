#Third-party imports
from fastapi import FastAPI

#Local imports
from .routers import temporary_router, authorization as auth_router, xpath
from app.database import engine, Base
from app.routers.prozorro_router import prozorro_router

app = FastAPI()

# Кріейтимо таблиці при запуску програми
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("startup")
async def startup():
    await init_db()

app.include_router(temporary_router.router)
app.include_router(xpath.router)
app.include_router(prozorro_router)
app.include_router(auth_router.router)  # Додаємо авторизацію

@app.get("/")
def home() -> dict:
    return {"msg" : "HomePage"}