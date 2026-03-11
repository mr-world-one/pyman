"""
Parser service — wraps synchronous Selenium parsers in asyncio.to_thread()
and provides a unified interface for multiple stores.
"""

import asyncio
import logging
from typing import List, Dict, Any, Optional

from scraper.parsers.rozetka_parser import RozetkaParser
from scraper.parsers.silpo_parser import SilpoParser
from scraper.parsers.epicentr_parser import EpicentrParser
from scraper.parsers.citadel_parser import CitadelParser

logger = logging.getLogger(__name__)

# Registry of available parsers
AVAILABLE_PARSERS = {
    "rozetka": {
        "class": RozetkaParser,
        "name": "Rozetka",
        "url": "https://rozetka.com.ua",
    },
    "silpo": {
        "class": SilpoParser,
        "name": "Сільпо",
        "url": "https://silpo.ua",
    },
    "epicentr": {
        "class": EpicentrParser,
        "name": "Епіцентр",
        "url": "https://epicentrk.ua",
    },
    "citadel": {
        "class": CitadelParser,
        "name": "Citadel",
        "url": "https://citadelbuddekor.com.ua",
    },
}


def _sync_search_products(
    parser_key: str,
    product_name: str,
    n: int = 1,
    fast_parse: bool = False,
    ignore_price_format: bool = True,
) -> List[Dict[str, Any]]:
    """
    Synchronous function that creates a parser, searches for products, and returns results.
    This runs inside asyncio.to_thread() to avoid blocking the event loop.
    """
    parser_info = AVAILABLE_PARSERS.get(parser_key)
    if not parser_info:
        raise ValueError(f"Unknown parser: {parser_key}")

    parser = None
    try:
        logger.info(f"[{parser_key}] Creating parser for product: '{product_name}'")
        parser = parser_info["class"]()
        results = parser.find_n_products(
            product=product_name,
            n=n,
            fast_parse=fast_parse,
            ignore_price_format=ignore_price_format,
            raise_exception=False,
        )
        logger.info(f"[{parser_key}] Found {len(results)} products for '{product_name}'")

        # Convert ProductInfo objects to dicts and add store info
        return [
            {
                **product.to_dict(),
                "store": parser_key,
                "store_name": parser_info["name"],
            }
            for product in results
        ]
    except Exception as e:
        logger.warning(f"[{parser_key}] Failed to search for '{product_name}': {e}")
        return []
    finally:
        if parser is not None:
            try:
                parser._close()
            except Exception:
                pass


async def search_products_async(
    product_name: str,
    stores: List[str],
    n: int = 1,
    fast_parse: bool = False,
    ignore_price_format: bool = True,
) -> List[Dict[str, Any]]:
    """
    Search for a product across multiple stores asynchronously.
    Each store parser runs in a separate thread via asyncio.to_thread().

    Args:
        product_name: Name of the product to search for
        stores: List of store keys (e.g., ["rozetka", "epicentr"])
        n: Number of products to find per store
        fast_parse: If True, only get price; if False, get full details
        ignore_price_format: If True, return raw price strings

    Returns:
        List of product dicts with store info attached
    """
    # Validate stores
    valid_stores = [s for s in stores if s in AVAILABLE_PARSERS]
    if not valid_stores:
        logger.warning(f"No valid stores provided: {stores}")
        return []

    # Run all parsers in parallel threads
    tasks = [
        asyncio.to_thread(
            _sync_search_products,
            store,
            product_name,
            n,
            fast_parse,
            ignore_price_format,
        )
        for store in valid_stores
    ]

    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Flatten results
    all_products = []
    for store, result in zip(valid_stores, results):
        if isinstance(result, Exception):
            logger.warning(f"[{store}] Exception during search: {result}")
            continue
        all_products.extend(result)

    return all_products


async def search_products_for_items(
    items: List[Dict[str, Any]],
    stores: List[str],
    n: int = 1,
) -> List[Dict[str, Any]]:
    """
    Search for each item from a list across specified stores.

    Args:
        items: List of dicts with 'name' key (e.g., from Prozorro or Excel)
        stores: List of store keys
        n: Number of products per item per store

    Returns:
        Flat list of all found products
    """
    all_results = []
    for item in items:
        product_name = item.get("name") or item.get("product_name", "")
        if not product_name:
            continue

        results = await search_products_async(
            product_name=product_name,
            stores=stores,
            n=n,
            fast_parse=False,
            ignore_price_format=True,
        )
        all_results.extend(results)

    return all_results


def get_available_stores() -> List[Dict[str, str]]:
    """Return list of available stores for the frontend."""
    return [
        {"key": key, "name": info["name"], "url": info["url"]}
        for key, info in AVAILABLE_PARSERS.items()
    ]
