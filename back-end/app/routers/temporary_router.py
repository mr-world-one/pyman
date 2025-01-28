from fastapi import APIRouter


router = APIRouter()

@router.get("/temp")
def temp() -> dict:
    return {"msg" : "Hello World"}