from fastapi import FastAPI
from .routers import temporary_router, xpath, authorization as auth_router
from app.database import engine, Base



import logging
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI()

# Увімкнути всі логи
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("uvicorn.error")

class LogExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            logger.error(f"HTTP 500: {str(e)}", exc_info=True)  #  Лог помилки
            raise e  # Перепіднімаємо помилку, щоб FastAPI її коректно обробив

# Додаємо middleware у FastAPI
app.add_middleware(LogExceptionMiddleware)

from fastapi.middleware.trustedhost import TrustedHostMiddleware

app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])
app.debug = True  #  Включає детальне логування

from fastapi.responses import JSONResponse
from fastapi.exception_handlers import HTTPException
from starlette.requests import Request

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f" Внутрішня помилка сервера: {exc}", exc_info=True)
    return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})




app = FastAPI()

# Кріейтимо таблиці при запуску програми
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("startup")
async def startup():
    await init_db()

app.include_router(temporary_router.router)
app.include_router(auth_router.router)  # Додаємо авторизацію
app.include_router(authentication.router)
app.include_router(xpath.router)

@app.get("/")
def home() -> dict:
    return {"msg" : "HomePage"}
