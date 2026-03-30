"""
CRUD router for the tender type system.

Endpoints:
  POST   /tenders/              — create a tender (type-aware)
  GET    /tenders/              — list tenders (filter by type/status, paginate)
  GET    /tenders/{id}          — get full tender with items
  PUT    /tenders/{id}          — update tender metadata
  DELETE /tenders/{id}          — delete tender
  POST   /tenders/import/{pid}  — import from Prozorro API + auto-classify
  POST   /tenders/{id}/analyze  — run price comparison for product tenders
"""

import logging
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.tender import Tender, TenderItem
from app.routers.authorization import get_current_user
from app.schemas.tender import (
    TenderCreate,
    TenderUpdate,
    TenderResponse,
    TenderListItem,
    TenderType,
    ProductTenderCreate,
    ServiceTenderCreate,
    WorkTenderCreate,
)
from app.services.tender_classifier import classify_tender_type, classify_tender_type_async

logger = logging.getLogger(__name__)

tender_router = APIRouter(prefix="/tenders", tags=["Tenders"])


# ── Helpers ───────────────────────────────────────────────────────

def _build_items(tender_type: str, items_data: list) -> list[TenderItem]:
    """Convert Pydantic item list to ORM TenderItem objects."""
    result = []
    for item_schema in items_data:
        data = item_schema.model_dump()
        result.append(TenderItem(**data))
    return result


def _tender_to_list_item(tender: Tender) -> dict:
    """Convert ORM Tender to TenderListItem-compatible dict."""
    return {
        "id": tender.id,
        "tender_type": tender.tender_type,
        "prozorro_id": tender.prozorro_id,
        "title": tender.title,
        "status": tender.status,
        "customer_name": tender.customer_name,
        "total_amount": tender.total_amount,
        "items_count": len(tender.items) if tender.items else 0,
        "created_at": tender.created_at,
    }


# ── CREATE ────────────────────────────────────────────────────────

@tender_router.post("/", response_model=TenderResponse, status_code=201)
async def create_tender(
    data: TenderCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Create a new tender. The schema is validated per tender_type."""
    # Check for duplicate prozorro_id
    existing = await db.execute(
        select(Tender).where(Tender.prozorro_id == data.prozorro_id)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Тендер з таким Prozorro ID вже існує")

    tender = Tender(
        tender_type=data.tender_type,
        prozorro_id=data.prozorro_id,
        title=data.title,
        description=data.description,
        expected_cost=data.expected_cost,
        currency=data.currency,
        status="active",
        customer_name=data.customer_name,
        region=data.region,
        total_amount=data.total_amount,
        user_id=current_user.id if hasattr(current_user, "id") else 1,
    )

    # Set type-specific fields
    if isinstance(data, ProductTenderCreate):
        tender.warranty_required = data.warranty_required
    elif isinstance(data, ServiceTenderCreate):
        tender.requires_license = data.requires_license
    elif isinstance(data, WorkTenderCreate):
        tender.project_documentation = data.project_documentation

    tender.items = _build_items(data.tender_type, data.items)

    db.add(tender)
    await db.commit()
    await db.refresh(tender)

    logger.info(f"Created tender #{tender.id} ({tender.tender_type}): {tender.title}")
    return tender


# ── LIST ──────────────────────────────────────────────────────────

@tender_router.get("/", response_model=List[TenderListItem])
async def list_tenders(
    tender_type: Optional[TenderType] = None,
    status: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """List tenders for current user with optional filters and pagination."""
    user_id = current_user.id if hasattr(current_user, "id") else 1
    q = select(Tender).where(Tender.user_id == user_id)

    if tender_type:
        q = q.where(Tender.tender_type == tender_type.value)
    if status:
        q = q.where(Tender.status == status)

    q = q.order_by(Tender.created_at.desc())
    q = q.offset((page - 1) * limit).limit(limit)

    result = await db.execute(q)
    tenders = result.scalars().all()

    return [_tender_to_list_item(t) for t in tenders]


# ── GET ONE ───────────────────────────────────────────────────────

@tender_router.get("/{tender_id}", response_model=TenderResponse)
async def get_tender(
    tender_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Get full tender details with items."""
    user_id = current_user.id if hasattr(current_user, "id") else 1
    result = await db.execute(
        select(Tender).where(Tender.id == tender_id, Tender.user_id == user_id)
    )
    tender = result.scalar_one_or_none()
    if not tender:
        raise HTTPException(status_code=404, detail="Тендер не знайдено")
    return tender


# ── UPDATE ────────────────────────────────────────────────────────

@tender_router.put("/{tender_id}", response_model=TenderResponse)
async def update_tender(
    tender_id: int,
    data: TenderUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Update tender metadata (not items)."""
    user_id = current_user.id if hasattr(current_user, "id") else 1
    result = await db.execute(
        select(Tender).where(Tender.id == tender_id, Tender.user_id == user_id)
    )
    tender = result.scalar_one_or_none()
    if not tender:
        raise HTTPException(status_code=404, detail="Тендер не знайдено")

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(tender, field, value)

    await db.commit()
    await db.refresh(tender)

    logger.info(f"Updated tender #{tender.id}: {list(update_data.keys())}")
    return tender


# ── DELETE ────────────────────────────────────────────────────────

@tender_router.delete("/{tender_id}")
async def delete_tender(
    tender_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Delete a tender and all its items."""
    user_id = current_user.id if hasattr(current_user, "id") else 1
    result = await db.execute(
        select(Tender).where(Tender.id == tender_id, Tender.user_id == user_id)
    )
    tender = result.scalar_one_or_none()
    if not tender:
        raise HTTPException(status_code=404, detail="Тендер не знайдено")

    await db.delete(tender)
    await db.commit()

    logger.info(f"Deleted tender #{tender_id}")
    return {"message": f"Тендер #{tender_id} видалено"}


# ── IMPORT FROM PROZORRO ──────────────────────────────────────────

@tender_router.post("/import/{prozorro_id}", response_model=TenderResponse, status_code=201)
async def import_from_prozorro(
    prozorro_id: str,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Import a tender from Prozorro API and auto-classify its type."""
    from app.prozorro_functionality.prozorro import get_contract, get_contract_info
    from app.routers.prozorro_router import convert_ua_to_hex_id

    # Check for duplicate
    existing = await db.execute(
        select(Tender).where(Tender.prozorro_id == prozorro_id)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Тендер з таким Prozorro ID вже існує")

    # Convert UA-ID if needed
    hex_id = prozorro_id
    if prozorro_id.upper().startswith("UA-"):
        hex_id = await convert_ua_to_hex_id(prozorro_id.upper())

    # Fetch raw tender data
    contract = get_contract(hex_id)
    if not contract:
        raise HTTPException(status_code=404, detail="Тендер не знайдено в Prozorro")

    # Extract items
    try:
        raw_items = await get_contract_info(hex_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Помилка отримання даних: {str(e)}")

    # Classify type using LLM (async)
    tender_type = await classify_tender_type_async(raw_items)

    # Calculate total
    total_amount = sum(
        float(item.get("unit_price", 0)) * float(item.get("quantity", 1))
        for item in raw_items
        if item.get("unit_price") and item.get("unit_price") != " "
    )
    if not total_amount:
        total_amount = contract.get("value", {}).get("amount", 0)

    user_id = current_user.id if hasattr(current_user, "id") else 1

    tender = Tender(
        tender_type=tender_type.value,
        prozorro_id=prozorro_id,
        title=contract.get("title", contract.get("description", f"Тендер {prozorro_id}")),
        description=contract.get("description"),
        expected_cost=contract.get("value", {}).get("amount"),
        currency=contract.get("value", {}).get("currency", "UAH"),
        status="active",
        customer_name=contract.get("procuringEntity", {}).get("name"),
        total_amount=total_amount,
        user_id=user_id,
    )

    # Build items
    for raw in raw_items:
        unit_price = raw.get("unit_price", 0)
        if unit_price == " ":
            unit_price = 0

        item = TenderItem(
            name=raw.get("name", ""),
            quantity=float(raw.get("quantity", 1)),
            unit_name=raw.get("unit_name", "од."),
            unit_price=float(unit_price),
        )

        # Set type-specific fields based on classification
        if tender_type == TenderType.SERVICE:
            item.service_type = "послуга"
        elif tender_type == TenderType.WORK:
            item.work_type = "роботи"

        tender.items.append(item)

    db.add(tender)
    await db.commit()
    await db.refresh(tender)

    logger.info(
        f"Imported tender #{tender.id} from Prozorro ({prozorro_id}), "
        f"type={tender_type.value}, items={len(tender.items)}"
    )
    return tender


# ── ANALYZE (price comparison) ────────────────────────────────────

@tender_router.post("/{tender_id}/analyze")
async def analyze_tender(
    tender_id: int,
    stores: str = Query(default="rozetka", description="Comma-separated store keys"),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Run price comparison for a tender's items using configured stores."""
    from app.services.parser_service import search_and_validate_items

    user_id = current_user.id if hasattr(current_user, "id") else 1
    result = await db.execute(
        select(Tender).where(Tender.id == tender_id, Tender.user_id == user_id)
    )
    tender = result.scalar_one_or_none()
    if not tender:
        raise HTTPException(status_code=404, detail="Тендер не знайдено")

    if tender.tender_type == TenderType.SERVICE.value:
        return {
            "status": "skipped",
            "message": "Порівняння цін не застосовується для тендерів на послуги",
            "tender_id": tender_id,
        }

    store_list = [s.strip() for s in stores.split(",") if s.strip()]
    if not store_list:
        store_list = ["rozetka"]

    # Convert ORM items to dicts for the existing search service
    items_for_search = [
        {
            "name": item.name,
            "quantity": item.quantity,
            "unit_name": item.unit_name,
            "unit_price": item.unit_price,
        }
        for item in tender.items
    ]

    try:
        matched_items = await search_and_validate_items(
            items=items_for_search,
            stores=store_list,
            n=3,
        )

        # Save price history for tracking
        from app.services.parser_service import save_price_history
        for i, group in enumerate(matched_items):
            if i < len(tender.items) and group.get("matches"):
                await save_price_history(tender.items[i].id, group["matches"])

        return {
            "status": "success",
            "message": "Аналіз завершено",
            "tender_id": tender_id,
            "tender_type": tender.tender_type,
            "prozorro_data": items_for_search,
            "matched_items": matched_items,
            "stores_used": store_list,
        }
    except Exception as e:
        logger.error(f"Analyze tender #{tender_id} error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ── PRICE HISTORY ────────────────────────────────────────────────

@tender_router.get("/{tender_id}/price-history")
async def get_price_history(
    tender_id: int,
    days: int = Query(default=30, ge=1, le=365, description="Number of days to look back"),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Get price history for all items in a tender."""
    from datetime import datetime, timedelta
    from app.models.tender import PriceHistory

    user_id = current_user.id if hasattr(current_user, "id") else 1
    result = await db.execute(
        select(Tender).where(Tender.id == tender_id, Tender.user_id == user_id)
    )
    tender = result.scalar_one_or_none()
    if not tender:
        raise HTTPException(status_code=404, detail="Тендер не знайдено")

    cutoff = datetime.utcnow() - timedelta(days=days)
    item_ids = [item.id for item in tender.items]

    if not item_ids:
        return {"tender_id": tender_id, "items": []}

    history_result = await db.execute(
        select(PriceHistory)
        .where(PriceHistory.item_id.in_(item_ids), PriceHistory.created_at >= cutoff)
        .order_by(PriceHistory.created_at.asc())
    )
    history_entries = history_result.scalars().all()

    # Group by item
    items_history = {}
    for entry in history_entries:
        if entry.item_id not in items_history:
            # Find item name
            item_name = next(
                (item.name for item in tender.items if item.id == entry.item_id), ""
            )
            items_history[entry.item_id] = {
                "item_id": entry.item_id,
                "item_name": item_name,
                "tender_price": next(
                    (item.unit_price for item in tender.items if item.id == entry.item_id), 0
                ),
                "history": [],
            }
        items_history[entry.item_id]["history"].append({
            "price": entry.price,
            "source_store": entry.source_store,
            "product_title": entry.product_title,
            "date": entry.created_at.isoformat() if entry.created_at else None,
        })

    return {
        "tender_id": tender_id,
        "days": days,
        "items": list(items_history.values()),
    }
