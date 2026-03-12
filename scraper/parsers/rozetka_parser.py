import logging
import requests

from scraper.parsers import ProductInfo

logger = logging.getLogger(__name__)

ROZETKA_SEARCH_URL = "https://search.rozetka.com.ua/ua/search/api/v6/"
ROZETKA_PRODUCT_URL = "https://rozetka.com.ua/api/product-api/v4/goods/get-main"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Accept": "application/json",
}


class RozetkaParser:

    def _close(self):
        pass

    def _search_ids(self, product: str, n: int) -> list:
        """Search Rozetka and return up to n product IDs."""
        resp = requests.get(
            ROZETKA_SEARCH_URL,
            params={"text": product, "lang": "ua"},
            headers=HEADERS,
            timeout=15,
        )
        resp.raise_for_status()
        goods = resp.json().get("data", {}).get("goods", [])
        return [g["id"] for g in goods[:n]]

    def _get_product_details(self, product_id: int) -> dict:
        """Fetch product details by ID."""
        resp = requests.get(
            ROZETKA_PRODUCT_URL,
            params={"goodsId": product_id, "lang": "ua"},
            headers=HEADERS,
            timeout=15,
        )
        resp.raise_for_status()
        return resp.json().get("data", {})

    def find_n_products(self, product, n, fast_parse=True, raise_exception=False, ignore_price_format=True):
        results = []
        try:
            ids = self._search_ids(product, n)
            logger.info(f"[rozetka] Found {len(ids)} product IDs for '{product}'")

            for pid in ids:
                try:
                    details = self._get_product_details(pid)
                    price = details.get("price")
                    old_price = details.get("old_price")
                    is_on_sale = old_price is not None and old_price != price and old_price > 0
                    price_on_sale = price if is_on_sale else None
                    actual_price = old_price if is_on_sale else price

                    info = ProductInfo(
                        url=details.get("href", f"https://rozetka.com.ua/ua/p{pid}/"),
                        price=actual_price,
                        is_on_sale=is_on_sale,
                        price_on_sale=price_on_sale,
                        is_available=details.get("sell_status") == "available",
                        title=details.get("title", ""),
                    )
                    results.append(info)
                except Exception as e:
                    logger.warning(f"[rozetka] Failed to get details for product {pid}: {e}")
                    if raise_exception:
                        raise

        except Exception as e:
            logger.warning(f"[rozetka] Search failed for '{product}': {e}")
            if raise_exception:
                raise

        logger.info(f"[rozetka] Returning {len(results)} products for '{product}'")
        return results
