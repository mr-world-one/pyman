"""
AI-powered corruption risk analysis for tenders.

Provides:
- Price deviation analysis (tender price vs market median)
- Discriminatory requirements detection via Gemini LLM
- Overall risk score calculation
"""

import json
import logging
import re
import statistics
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


def calculate_price_deviation(
    tender_items: List[Dict[str, Any]],
    matched_items: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """Compare tender unit prices with median market prices from store data.

    For each tender item that has store matches, compute:
      - median_market_price: median of effective store prices
      - deviation_pct: percentage difference (positive = tender is more expensive)
      - risk_level: "high" if deviation > 20%, "medium" if > 10%, "low" otherwise

    Returns a list of per-item risk assessments.
    """
    results = []

    for group in matched_items:
        tender_item = group.get("tender_item", {})
        matches = group.get("matches", [])
        item_name = tender_item.get("name", "")

        tender_price = None
        raw = tender_item.get("unit_price")
        if raw is not None:
            try:
                tender_price = float(raw)
            except (ValueError, TypeError):
                pass

        if not tender_price or tender_price <= 0:
            results.append({
                "item_name": item_name,
                "tender_price": tender_price,
                "median_market_price": None,
                "deviation_pct": None,
                "risk_level": "unknown",
                "reason": "Тендерна ціна відсутня або нульова",
            })
            continue

        if not matches:
            results.append({
                "item_name": item_name,
                "tender_price": tender_price,
                "median_market_price": None,
                "deviation_pct": None,
                "risk_level": "unknown",
                "reason": "Немає ринкових даних для порівняння",
            })
            continue

        # Collect effective prices from matched store products
        market_prices = []
        for m in matches:
            ep = m.get("price_on_sale") or m.get("price")
            if ep is not None:
                try:
                    market_prices.append(float(ep))
                except (ValueError, TypeError):
                    pass

        if not market_prices:
            results.append({
                "item_name": item_name,
                "tender_price": tender_price,
                "median_market_price": None,
                "deviation_pct": None,
                "risk_level": "unknown",
                "reason": "Жоден ринковий товар не має ціни",
            })
            continue

        median_price = statistics.median(market_prices)
        if median_price <= 0:
            results.append({
                "item_name": item_name,
                "tender_price": tender_price,
                "median_market_price": median_price,
                "deviation_pct": None,
                "risk_level": "unknown",
                "reason": "Медіанна ринкова ціна нульова",
            })
            continue

        deviation_pct = round((tender_price - median_price) / median_price * 100, 1)

        if abs(deviation_pct) > 20:
            risk_level = "high"
        elif abs(deviation_pct) > 10:
            risk_level = "medium"
        else:
            risk_level = "low"

        results.append({
            "item_name": item_name,
            "tender_price": tender_price,
            "median_market_price": round(median_price, 2),
            "deviation_pct": deviation_pct,
            "risk_level": risk_level,
            "reason": (
                f"Тендерна ціна {'вище' if deviation_pct > 0 else 'нижче'} "
                f"ринкової на {abs(deviation_pct)}%"
            ),
        })

    return results


async def analyze_discriminatory_requirements(specification_text: str) -> Optional[Dict[str, Any]]:
    """Use Gemini to detect potentially discriminatory requirements in tender specs.

    Looks for requirements that may point to a specific supplier, such as:
    - Overly specific brand/model requirements
    - Unique technical parameters only one vendor satisfies
    - Unusual packaging, color, or certification requirements

    Returns dict with findings or None if Gemini is unavailable.
    """
    from app.services.llm_validator import _get_model, _parse_response

    model = _get_model()
    if not model:
        logger.warning("Gemini not configured — discriminatory requirement analysis skipped")
        return None

    if not specification_text or len(specification_text.strip()) < 50:
        return {"discriminatory_requirements": [], "summary": "Текст специфікації занадто короткий для аналізу"}

    prompt = f"""Ти — експерт з аналізу тендерної документації в Україні на предмет можливих корупційних ризиків.

ЗАДАЧА: Проаналізуй текст тендерної специфікації та знайди вимоги, які можуть вказувати на конкретного постачальника або обмежувати конкуренцію.

Шукай наступні ознаки:
1. Вказівка конкретного бренду/виробника без формулювання "або еквівалент"
2. Надмірно специфічні технічні параметри (наприклад, точний відтінок кольору, специфічна форма кнопки)
3. Вимоги до сертифікації, якою володіє лише один постачальник
4. Нестандартні вимоги до пакування або маркування
5. Необґрунтовано короткі терміни поставки
6. Вимоги до досвіду, що відсікають більшість учасників
7. Посилання на конкретні ТУ замість ДСТУ/ГОСТ

Поверни JSON об'єкт:
{{
  "discriminatory_requirements": [
    {{
      "text": "цитата з тексту",
      "type": "brand_lock|specific_parameter|certification|packaging|deadline|experience|other",
      "severity": "high|medium|low",
      "explanation": "чому це може бути дискримінаційним"
    }}
  ],
  "summary": "загальний висновок про рівень ризику дискримінації",
  "overall_risk": "high|medium|low"
}}

Якщо дискримінаційних вимог не знайдено — поверни порожній масив discriminatory_requirements з overall_risk = "low".

Текст специфікації:
{specification_text[:25000]}"""

    try:
        response = await model.generate_content_async(prompt)
        logger.info(f"Gemini discriminatory analysis response: {response.text[:300]}")

        # Try to parse JSON
        try:
            data = json.loads(response.text)
            if isinstance(data, dict):
                return data
        except json.JSONDecodeError:
            pass

        # Fallback: extract JSON object from text
        match = re.search(r'\{.*\}', response.text, re.DOTALL)
        if match:
            try:
                data = json.loads(match.group())
                if isinstance(data, dict):
                    return data
            except json.JSONDecodeError:
                pass

        logger.warning(f"Could not parse discriminatory analysis response: {response.text[:200]}")
        return None

    except Exception as e:
        logger.error(f"Gemini discriminatory analysis failed: {e}")
        return None


def calculate_overall_risk_score(
    price_risks: List[Dict[str, Any]],
    discriminatory_analysis: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Calculate an overall risk score (0-100) based on price and discriminatory analyses.

    Scoring:
    - Price deviation contributes up to 50 points
    - Discriminatory requirements contribute up to 50 points

    Returns a summary dict with score, level, and breakdown.
    """
    price_score = 0
    if price_risks:
        high_count = sum(1 for r in price_risks if r.get("risk_level") == "high")
        medium_count = sum(1 for r in price_risks if r.get("risk_level") == "medium")
        total_assessed = sum(1 for r in price_risks if r.get("risk_level") in ("high", "medium", "low"))

        if total_assessed > 0:
            price_score = min(50, round(
                (high_count * 50 + medium_count * 25) / total_assessed
            ))

    discrim_score = 0
    if discriminatory_analysis:
        overall = discriminatory_analysis.get("overall_risk", "low")
        if overall == "high":
            discrim_score = 50
        elif overall == "medium":
            discrim_score = 25

        # Additional per-finding scoring
        findings = discriminatory_analysis.get("discriminatory_requirements", [])
        high_findings = sum(1 for f in findings if f.get("severity") == "high")
        medium_findings = sum(1 for f in findings if f.get("severity") == "medium")
        finding_score = min(50, high_findings * 15 + medium_findings * 8)
        discrim_score = max(discrim_score, finding_score)

    total_score = min(100, price_score + discrim_score)

    if total_score >= 60:
        level = "high"
    elif total_score >= 30:
        level = "medium"
    else:
        level = "low"

    return {
        "risk_score": total_score,
        "risk_level": level,
        "price_risk_score": price_score,
        "discriminatory_risk_score": discrim_score,
        "breakdown": {
            "price_deviations": price_risks,
            "discriminatory_analysis": discriminatory_analysis,
        },
    }
