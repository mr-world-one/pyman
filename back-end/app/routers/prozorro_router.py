import asyncio
import logging
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


