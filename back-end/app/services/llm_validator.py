"""
LLM-based product validation and weight normalization using Google Gemini.
Validates that store products actually match the tender item,
and extracts weight/volume info for price-per-unit normalization.
"""

import json
import logging
import os
import re
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

_gemini_model = None

# Tender items matching these patterns are services, not physical products
_SERVICE_PATTERNS = re.compile(
    r'(?i)^послуг[иіа]\b|'
    r'\bпослуг[иіа]\s+з\b|'
    r'\bобслуговування\b|'
    r'\bремонт\b.*\bобладнання\b|'
    r'\bоренд[аи]\b|'
    r'\bперевезення\b|'
    r'\bтранспортування\b|'
    r'\bстрахування\b|'
    r'\bнавчання\b|'
    r'\bпроектування\b|'
    r'\bмонтаж\b|'
    r'\bдемонтаж\b'
)


def is_service_item(name: str) -> bool:
    """Check if a tender item is a service rather than a physical product."""
    return bool(_SERVICE_PATTERNS.search(name))


def _get_model():
    """Lazy-init Gemini model. Returns None if API key is not configured."""
    global _gemini_model
    if _gemini_model is not None:
        return _gemini_model

    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        logger.info("GEMINI_API_KEY not set — LLM validation disabled")
        return None

    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        _gemini_model = genai.GenerativeModel(
            "gemini-2.0-flash-lite",
            generation_config={"temperature": 0.0, "response_mime_type": "application/json"},
        )
        logger.info("Gemini model initialized successfully")
        return _gemini_model
    except Exception as e:
        logger.warning(f"Failed to initialize Gemini model: {e}")
        return None


def _build_prompt(
    tender_name: str,
    tender_price: float,
    tender_quantity: Optional[float],
    tender_unit: Optional[str],
    store_items: List[Dict[str, Any]],
) -> str:
    items_text = ""
    for i, item in enumerate(store_items, 1):
        price = item.get("price_on_sale") or item.get("price") or "?"
        items_text += f'{i}. [{item.get("store_name", "?")}] "{item.get("title", "?")}" — {price} грн\n'

    qty_info = ""
    if tender_quantity and tender_unit:
        qty_info = f"\nКількість: {tender_quantity} {tender_unit}"

    return f"""Ти — суворий експерт з порівняння товарів для тендерних закупівель в Україні.

ЗАДАЧА: Визначити, чи кожен знайдений товар є ТИМ САМИМ конкретним продуктом що й тендерний товар.

Тендерний товар: "{tender_name}"
Ціна за одиницю: {tender_price} грн{qty_info}

Знайдені товари в магазинах:
{items_text}

ПРАВИЛА ОЦІНКИ is_relevant — будь ДУЖЕ СУВОРИМ:

RELEVANT (true) — ТІЛЬКИ якщо товар є тим самим конкретним продуктом або його прямим аналогом:
- "Масло вершкове 72%" ↔ "Масло вершкове Селянське 72.5%" → true (той самий тип, схожі характеристики)
- "Папір А4 500 аркушів" ↔ "Папір офісний А4 80г/м2" → true (той самий тип товару)
- "Цукор білий 1кг" ↔ "Цукор білий кристалічний" → true

NOT RELEVANT (false) — якщо:
- Товари мають спільні слова але це РІЗНІ категорії: "Бензин А-95" ↔ "Ареометр для бензину" → false
- Послуга vs товар: "Послуги з харчування" ↔ "Засіб для миття посуду" → false
- Різний тип послуги: "Послуги з харчування" ↔ "Послуга з параметризації лічильників" → false
- Загальне слово збігається але продукт інший: "Набір пінцетів" ↔ "Послуги харчування" → false
- Аксесуар/інструмент для товару а не сам товар: "Кава мелена" ↔ "Кавомолка" → false
- Цемент ↔ Бетон → false (різні матеріали)

При сумніві — став false. Краще пропустити підходящий товар, ніж включити непідходящий.

Для кожного товару також визнач:
- "store_weight_g" (number|null): вага/об'єм товару з НАЗВИ МАГАЗИНУ в грамах/мл. "500г"→500, "1кг"→1000, "1.5л"→1500, "250мл"→250. null якщо не вказано.
- "tender_weight_g" (number|null): вага/об'єм з НАЗВИ ТЕНДЕРУ в грамах/мл. null якщо не вказано.

Відповідай ТІЛЬКИ JSON масивом:
[{{"index": 1, "is_relevant": false, "store_weight_g": null, "tender_weight_g": null}}, ...]"""


def _parse_response(response_text: str, n_items: int) -> Optional[List[Dict]]:
    """Parse Gemini JSON response, with fallback regex extraction."""
    try:
        data = json.loads(response_text)
        if isinstance(data, list):
            return data
    except json.JSONDecodeError:
        pass

    # Fallback: try to extract JSON array from text
    match = re.search(r'\[.*\]', response_text, re.DOTALL)
    if match:
        try:
            data = json.loads(match.group())
            if isinstance(data, list):
                return data
        except json.JSONDecodeError:
            pass

    logger.warning(f"Failed to parse Gemini response: {response_text[:200]}")
    return None


def _set_default_fields(store_items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Set default LLM fields when validation is skipped."""
    for item in store_items:
        item["is_relevant"] = True
        item["store_weight_g"] = None
        item["tender_weight_g"] = None
        item["price_per_unit"] = None
        item["tender_price_per_unit"] = None
    return store_items


async def validate_matches(
    tender_name: str,
    tender_price: float,
    tender_quantity: Optional[float],
    tender_unit: Optional[str],
    store_items: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Use Gemini to validate which store items are true matches for the tender item,
    and extract weight/volume for price normalization.

    Returns store_items enriched with:
      - is_relevant (bool)
      - store_weight_g (float|None)
      - tender_weight_g (float|None)
      - price_per_unit (float|None)  — normalized price (per kg/l)
      - tender_price_per_unit (float|None)

    If Gemini is unavailable, returns all items as-is (no filtering).
    """
    model = _get_model()

    if model is None or not store_items:
        return _set_default_fields(store_items)

    prompt = _build_prompt(tender_name, tender_price, tender_quantity, tender_unit, store_items)

    try:
        response = await model.generate_content_async(prompt)
        logger.info(f"Gemini response for '{tender_name[:60]}': {response.text[:300]}")
        llm_results = _parse_response(response.text, len(store_items))
    except Exception as e:
        logger.warning(f"Gemini API call failed for '{tender_name[:60]}': {e}")
        return _set_default_fields(store_items)

    if llm_results is None:
        return _set_default_fields(store_items)

    # Build index map from LLM response
    llm_map = {}
    for entry in llm_results:
        idx = entry.get("index")
        if idx is not None:
            llm_map[idx] = entry

    # Enrich store items with LLM data
    enriched = []
    for i, item in enumerate(store_items, 1):
        llm_entry = llm_map.get(i, {})
        is_relevant = llm_entry.get("is_relevant", False)  # Default to False if missing
        store_weight_g = llm_entry.get("store_weight_g")
        tender_weight_g = llm_entry.get("tender_weight_g")

        # Compute normalized price per kg/l if both weights are known
        effective_price = (
            float(item.get("price_on_sale"))
            if item.get("price_on_sale")
            else float(item.get("price")) if item.get("price") else None
        )

        price_per_unit = None
        tender_price_per_unit = None
        if store_weight_g and store_weight_g > 0 and effective_price is not None:
            price_per_unit = round(effective_price / store_weight_g * 1000, 2)  # per kg/l
        if tender_weight_g and tender_weight_g > 0 and tender_price:
            tender_price_per_unit = round(tender_price / tender_weight_g * 1000, 2)

        item["is_relevant"] = is_relevant
        item["store_weight_g"] = store_weight_g
        item["tender_weight_g"] = tender_weight_g
        item["price_per_unit"] = price_per_unit
        item["tender_price_per_unit"] = tender_price_per_unit
        enriched.append(item)

    relevant_count = sum(1 for e in enriched if e["is_relevant"])
    logger.info(f"LLM validation for '{tender_name[:60]}': {relevant_count}/{len(enriched)} relevant")

    return enriched

async def extract_items_from_text(text: str) -> Optional[List[Dict[str, Any]]]:
    """Extract structured tender items (name, quantity, unit, prices) from PDF text via Gemini."""
    model = _get_model()
    if not model:
        logger.warning("Gemini model not configured — cannot extract items from text")
        return None

    prompt = f"""Ти — експерт з аналізу тендерної документації в Україні.

ЗАДАЧА: Знайди у тексті специфікації перелік товарів/послуг із цінами та кількостями.

Поверни JSON масив об'єктів із полями:
- "name" (string) — назва товару/послуги
- "quantity" (number) — кількість
- "unit_name" (string) — одиниця виміру (шт, кг, л, упак, тощо)
- "unit_price" (number) — ціна за одиницю
- "total_price" (number) — загальна вартість позиції

ПРАВИЛА:
- Використовуй ціну БЕЗ ПДВ, якщо вказано обидві
- Повертай числа, а не рядки
- Пропускай рядки з підсумками, заголовками, нумерацією
- Якщо товарів не знайдено — поверни порожній масив []
- Не вигадуй дані — витягуй тільки те, що є в тексті

Текст документації:
{text[:30000]}"""

    try:
        response = await model.generate_content_async(prompt)
        logger.info(f"Gemini item extraction response: {response.text[:300]}")
        data = _parse_response(response.text, 0)
        if data is not None:
            logger.info(f"Extracted {len(data)} items from text")
        return data
    except Exception as e:
        logger.error(f"Failed to extract items from text via Gemini: {e}")
        return None


async def analyze_document_text(text: str) -> Optional[List[Dict[str, Any]]]:
    """Аналізує витягнутий текст тендерної документації за допомогою LLM."""
    model = _get_model()
    if not model:
        logger.warning("Модель Gemini не налаштована для аналізу документів.")
        return None

    prompt = f"""Проаналізуй текст тендерної документації. Знайди технічні специфікації товарів.
Витягни: назву товару, ДСТУ/ГОСТ, кількість, одиниці виміру та детальні технічні характеристики.
Поверни результат у форматі JSON масиву.

Текст документації:
{text[:30000]}"""

    try:
        response = await model.generate_content_async(prompt)
        logger.info(f"LLM response for doc analysis: {response.text[:200]}")
        data = _parse_response(response.text, 0)
        return data
    except Exception as e:
        logger.error(f"Помилка аналізу тексту документа: {e}")
        return None

