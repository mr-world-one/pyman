#Third-party imports
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import Depends, HTTPException
from pydantic import AnyUrl

#Local imports
from app.database import get_db
from app.models.model import Store


async def create_store(name:str, url:AnyUrl, title_xpath:str, available_xpath:str, price_xpath:str, price_without_sale_xpath:str, price_on_sale_xpath:str, db:AsyncSession = Depends(get_db)):
    store = Store(name = name, url = str(url), title_xpath=title_xpath, available_xpath=available_xpath, price_xpath=price_xpath, price_without_sale_xpath=price_without_sale_xpath, price_on_sale_xpath=price_on_sale_xpath)
    db.add(store)
    await db.commit()
    await db.refresh(store)
    return store


async def get_store(name:str, db:AsyncSession = Depends(get_db)):
    result = await db.execute(select(Store).filter(Store.name == name))
    store = result.scalar_one_or_none()
    if not store:
        raise HTTPException(status_code=404, detail="Store not found!")

    return store

async def get_all_stores(db:AsyncSession = Depends(get_db)):
    result = await db.execute(select(Store))
    return result.scalars().all()


async def edit_store(name:str, url:AnyUrl = None, title_xpath:str = None, available_xpath:str = None, price_xpath:str = None, price_without_sale_xpath:str = None, price_on_sale_xpath:str = None, db:AsyncSession = Depends(get_db)):
    result = await db.execute(select(Store).filter(Store.name == name))
    store = result.scalar_one_or_none()
    if not store:
        raise HTTPException(status_code=404, detail="Store not found!")

    if url is not None:
        store.url = str(url)
    if title_xpath is not None:
        store.title_xpath = title_xpath
    if available_xpath is not None:
        store.available_xpath = available_xpath
    if price_xpath is not None:
        store.price_xpath = price_xpath
    if price_without_sale_xpath is not None:
        store.price_without_sale_xpath = price_without_sale_xpath
    if price_on_sale_xpath is not None:
        store.price_on_sale_xpath = price_on_sale_xpath

    await db.commit()
    await db.refresh(store)

    return store


async def delete_store(name:str, db:AsyncSession = Depends(get_db)):
    result = await db.execute(select(Store).filter(Store.name == name))
    store = result.scalar_one_or_none()

    if not store:
        raise HTTPException(status_code=404, detail="Store not found!")

    await db.delete(store)
    await db.commit()
    return {"msg": "Store deleted successfully!"}