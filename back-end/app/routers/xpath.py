#Third-party imports
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
#Local imports
from app.database import get_db
from app.schemas.schema import StoreCreate, StoreResponse, StoreEditRequest
from app.xpath_functionality.xpath import create_store, get_store, get_all_stores, edit_store, delete_store


router = APIRouter()


@router.get("/store/")
async def all_store(db: AsyncSession = Depends(get_db)):
    return await get_all_stores(db)


@router.get("/store/{name}", response_model=StoreResponse)
async def get_spec_store(name:str, db:AsyncSession = Depends(get_db)):
    return await get_store(name, db)


@router.post("/store/", response_model=StoreResponse)
async def add_store(store_data:StoreCreate, db:AsyncSession = Depends(get_db)):
    return await create_store(**store_data.dict(), db=db)


@router.put("/store/{name}", response_model=StoreResponse)
async def modify_store(name:str, store_data:StoreEditRequest, db:AsyncSession = Depends(get_db)):
    return await edit_store(name, **store_data.dict(exclude_unset=True), db=db)

@router.delete("/store/{name}")
async def del_store(name: str, db:AsyncSession = Depends(get_db)) -> dict:
    return await delete_store(name, db)