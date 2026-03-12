import json
import logging
import re

import requests

from scraper.parsers import ProductInfo

logger = logging.getLogger(__name__)

EPICENTR_SEARCH_URL = "https://epicentrk.ua/ua/search/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Accept": "text/html",
}


class EpicentrParser:

    def _close(self):
        pass

    def _search_products(self, product: str, n: int) -> list:
        """Fetch Epicentr search page and parse schema.org JSON-LD product data."""
        resp = requests.get(
            EPICENTR_SEARCH_URL,
            params={"q": product},
            headers=HEADERS,
            timeout=20,
        )
        resp.raise_for_status()

        # JSON-LD is embedded in regular <script> tags (not type="application/ld+json")
        products = []
        for block in re.findall(r'<script[^>]*>(.*?)</script>', resp.text, re.DOTALL):
            block = block.strip()
            if not (block.startswith('{') and '"ItemList"' in block):
                continue
            try:
                data = json.loads(block)
                if data.get("@type") == "ItemList":
                    for item in data.get("itemListElement", [])[:n]:
                        product_data = item.get("item", {})
                        if product_data.get("@type") == "Product":
                            products.append(product_data)
            except (json.JSONDecodeError, KeyError):
                continue

        return products[:n]

    def find_n_products(self, product: str, n: int, fast_parse=True, ignore_price_format=True, raise_exception=False):
        results = []
        try:
            items = self._search_products(product, n)
            logger.info(f"[epicentr] Found {len(items)} products for '{product}'")

            for item in items:
                try:
                    offers = item.get("offers", {})
                    price = None
                    if isinstance(offers, dict):
                        price_str = offers.get("price")
                        if price_str is not None:
                            try:
                                price = float(price_str)
                            except (ValueError, TypeError):
                                price = price_str

                    url = item.get("url", "")
                    if url and not url.startswith("http"):
                        url = f"https://epicentrk.ua{url}"

                    info = ProductInfo(
                        url=url,
                        price=price,
                        is_on_sale=False,
                        price_on_sale=None,
                        is_available=offers.get("availability", "") == "https://schema.org/InStock" if isinstance(offers, dict) else None,
                        title=item.get("name", ""),
                    )
                    results.append(info)
                except Exception as e:
                    logger.warning(f"[epicentr] Failed to parse product: {e}")
                    if raise_exception:
                        raise

        except Exception as e:
            logger.warning(f"[epicentr] Search failed for '{product}': {e}")
            if raise_exception:
                raise

        logger.info(f"[epicentr] Returning {len(results)} products for '{product}'")
        return results
