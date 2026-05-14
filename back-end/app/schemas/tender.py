"""
Pydantic schemas for the tender type system.

Provides:
- TenderType enum
- Per-type item schemas (ProductItem, ServiceItem, WorkItem)
- Per-type tender schemas (ProductTender, ServiceTender, WorkTender)
- Discriminated union TenderCreate for automatic routing by tender_type
- Response schemas for list/detail views
"""

from datetime import datetime
from enum import Enum
from typing import Annotated, List, Literal, Optional, Union

from pydantic import BaseModel, Field


# ── Enum ──────────────────────────────────────────────────────────

class TenderType(str, Enum):
    PRODUCT = "product"
    SERVICE = "service"
    WORK = "work"
    CONSULTING = "consulting"
    MIXED = "mixed"


# ── Item schemas ──────────────────────────────────────────────────

class ProductItem(BaseModel):
    name: str
    quantity: float
    unit_name: str
    unit_price: float
    dk_code: Optional[str] = None
    specifications: Optional[str] = None
    delivery_address: Optional[str] = None
    delivery_deadline: Optional[str] = None
    brand: Optional[str] = None
    dstu_gost: Optional[str] = None
    weight_per_unit_g: Optional[float] = None
    shelf_life_days: Optional[int] = None


class ServiceItem(BaseModel):
    name: str
    service_type: str
    quantity: float
    unit_name: str
    unit_price: float
    period_start: Optional[str] = None
    period_end: Optional[str] = None
    qualification_requirements: Optional[str] = None
    location: Optional[str] = None
    sla_description: Optional[str] = None
    license_required: Optional[bool] = None


class WorkItem(BaseModel):
    name: str
    work_type: str
    quantity: float
    unit_name: str
    unit_price: float
    object_address: str
    estimated_duration_days: int
    technical_specs: Optional[str] = None
    permit_required: Optional[bool] = None
    subcontracting_allowed: Optional[bool] = None
    materials_included: Optional[bool] = None
    warranty_months: Optional[int] = None


# ── Tender create schemas (discriminated by tender_type) ──────────

class _TenderCreateBase(BaseModel):
    prozorro_id: str = Field(..., min_length=1, max_length=100)
    title: str = Field(..., min_length=1, max_length=500)
    description: Optional[str] = None
    expected_cost: Optional[float] = None
    currency: str = "UAH"
    customer_name: Optional[str] = None
    region: Optional[str] = None


class ProductTenderCreate(_TenderCreateBase):
    tender_type: Literal["product"]
    items: List[ProductItem] = Field(..., min_length=1)
    total_amount: float
    warranty_required: bool = False


class ServiceTenderCreate(_TenderCreateBase):
    tender_type: Literal["service"]
    items: List[ServiceItem] = Field(..., min_length=1)
    total_amount: float
    requires_license: bool = False


class WorkTenderCreate(_TenderCreateBase):
    tender_type: Literal["work"]
    items: List[WorkItem] = Field(..., min_length=1)
    total_amount: float
    project_documentation: Optional[str] = None


TenderCreate = Annotated[
    Union[ProductTenderCreate, ServiceTenderCreate, WorkTenderCreate],
    Field(discriminator="tender_type"),
]


# ── Tender update schema ─────────────────────────────────────────

class TenderUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    expected_cost: Optional[float] = None
    status: Optional[str] = None
    customer_name: Optional[str] = None
    region: Optional[str] = None
    total_amount: Optional[float] = None


# ── Response schemas ──────────────────────────────────────────────

class TenderItemResponse(BaseModel):
    id: int
    name: str
    quantity: float
    unit_name: str
    unit_price: Optional[float] = None
    price_source: str = "tender"
    # Product
    dk_code: Optional[str] = None
    brand: Optional[str] = None
    dstu_gost: Optional[str] = None
    weight_per_unit_g: Optional[float] = None
    shelf_life_days: Optional[int] = None
    specifications: Optional[str] = None
    delivery_address: Optional[str] = None
    delivery_deadline: Optional[str] = None
    # Service
    service_type: Optional[str] = None
    period_start: Optional[str] = None
    period_end: Optional[str] = None
    qualification_requirements: Optional[str] = None
    sla_description: Optional[str] = None
    license_required: Optional[bool] = None
    location: Optional[str] = None
    # Work
    work_type: Optional[str] = None
    object_address: Optional[str] = None
    estimated_duration_days: Optional[int] = None
    technical_specs: Optional[str] = None
    permit_required: Optional[bool] = None
    subcontracting_allowed: Optional[bool] = None
    materials_included: Optional[bool] = None
    warranty_months: Optional[int] = None

    extra_data: Optional[dict] = None

    class Config:
        from_attributes = True


class TenderResponse(BaseModel):
    id: int
    tender_type: TenderType
    prozorro_id: str
    title: str
    description: Optional[str] = None
    expected_cost: Optional[float] = None
    currency: str
    status: str
    customer_name: Optional[str] = None
    region: Optional[str] = None
    total_amount: Optional[float] = None
    warranty_required: bool = False
    requires_license: bool = False
    project_documentation: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    items: List[TenderItemResponse] = []

    class Config:
        from_attributes = True


class TenderListItem(BaseModel):
    """Lightweight schema for list views (no items)."""
    id: int
    tender_type: TenderType
    prozorro_id: str
    title: str
    status: str
    customer_name: Optional[str] = None
    total_amount: Optional[float] = None
    items_count: int = 0
    created_at: datetime

    class Config:
        from_attributes = True
