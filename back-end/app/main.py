from fastapi import FastAPI
from routers import temporary_router


app = FastAPI()


app.include_router(temporary_router.router)


@app.get("/")
def home() -> dict:
    return {"msg" : "HomePage"}
