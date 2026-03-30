"""
Automatic tender type classifier.

Determines the tender type (product / service / work) based on
item names using regex patterns and the existing is_service_item() helper.
"""

import re
from typing import List, Dict, Any

from app.schemas.tender import TenderType
from app.services.llm_validator import is_service_item

_WORK_PATTERNS = re.compile(
    r'(?i)\bбудівництво\b|'
    r'\bреконструкція\b|'
    r'\bкапітальний\s+ремонт\b|'
    r'\bпроектн[іи]\b|'
    r'\bпроектування\b|'
    r'\bмонтажн[іи]\b|'
    r'\bбудівельн[іи]\b|'
    r'\bземляні роботи\b|'
    r'\bпрокладання\b'
)


def classify_tender_type(items: List[Dict[str, Any]]) -> TenderType:
    """Classify tender type based on item names.

    Returns the most likely TenderType based on majority of items.
    """
    if not items:
        return TenderType.PRODUCT

    service_count = 0
    work_count = 0
    product_count = 0

    for item in items:
        name = item.get("name", "") or item.get("description", "") or ""
        if _WORK_PATTERNS.search(name):
            work_count += 1
        elif is_service_item(name):
            service_count += 1
        else:
            product_count += 1

    if work_count > product_count and work_count >= service_count:
        return TenderType.WORK
    if service_count > product_count:
        return TenderType.SERVICE
    if service_count > 0 and product_count > 0:
        return TenderType.MIXED
    return TenderType.PRODUCT
