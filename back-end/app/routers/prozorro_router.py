import asyncio
import logging
import httpx
from typing import Optional, List

from fastapi import APIRouter, HTTPException, Depends, Query

from app.prozorro_functionality.prozorro import get_contract_info
from app.routers.authorization import get_current_user
from app.services.parser_service import (
    search_products_async,
    search_products_for_items,
    search_and_validate_items,
    get_available_stores,
)

prozorro_router = APIRouter()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

PROZORRO_SEARCH_URL = "https://prozorro.gov.ua/api/search/tenders"

async def convert_ua_to_hex_id(ua_id: str) -> str:
    """Конвертує публічний UA-ID у внутрішній 32-символьний hex ID через clarity-project."""
    import re
    async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
        try:
            # Використовуємо clarity-project як надійний індекс-агрегатор
            response = await client.get(f"https://clarity-project.info/tender/{ua_id.lower()}")
            response.raise_for_status()

            # Парсимо hex id з тегу canonical link сторінки
            match = re.search(r'clarity-project\.info/tender/([0-9a-f]{32})', response.text)
            
            if not match:
                logger.error(f"Не вдалося знайти hex ID для {ua_id}. HTML розмір: {len(response.text)}")
                raise HTTPException(status_code=404, detail=f"Тендер з ID {ua_id} (hex) не знайдено.")

            hex_id = match.group(1)
            return hex_id

        except httpx.HTTPStatusError as e:
            logger.error(f"Помилка пошуку ID (проксі-сервер агрегатора): {e}")
            if e.response.status_code == 404:
                raise HTTPException(status_code=404, detail="Тендер з таким UA-ID не існує")
            raise HTTPException(status_code=502, detail="Помилка при спробі знайти тендер")
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Внутрішня помилка конвертації ID: {e}")
            raise HTTPException(status_code=500, detail=f"Внутрішня помилка пошуку тендера: {str(e)}")


@prozorro_router.get("/stores/available")
async def list_available_stores():
    """Return list of stores available for price comparison."""
    return get_available_stores()


@prozorro_router.get("/search-tender/{contract_id}")
async def prozorro_data(
    contract_id: str,
    stores: str = Query(default="rozetka", description="Comma-separated store keys: rozetka,silpo,epicentr,citadel"),
    current_user: str = Depends(get_current_user),
):
    """
    Search Prozorro tender by contract ID and compare prices from selected stores.
    Selenium runs in background threads via asyncio.to_thread().
    """
    store_list = [s.strip() for s in stores.split(",") if s.strip()]
    if not store_list:
        store_list = ["rozetka"]

    try:
        # Автоматична конвертація, якщо ID починається на "UA-"
        if contract_id.upper().startswith("UA-"):
            logger.info(f"Конвертація публічного ID: {contract_id}")
            contract_id = await convert_ua_to_hex_id(contract_id.upper())
            logger.info(f"Отримано внутрішній HEX ID: {contract_id}")

        pr_data = get_contract_info(contract_id)
        matched_items = await search_and_validate_items(
            items=pr_data,
            stores=store_list,
            n=3,
        )

        return {
            "status": "success",
            "message": "Products found",
            "prozorro_data": pr_data,
            "matched_items": matched_items,
            "stores_used": store_list,
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in prozorro_data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


