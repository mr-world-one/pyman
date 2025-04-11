import logging
import time

from functools import wraps
from scraper.utils import MAX_ATTEMPTS, DELAY
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

LOG_FILE_PATH = "scraper.log"
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        # logging.FileHandler(LOG_FILE_PATH),
        logging.StreamHandler()
    ],
    encoding='utf-8'
)

logger = logging.getLogger(__name__)


def retry_on_timeout(max_attempts=MAX_ATTEMPTS, delay=DELAY):
    """
    A decorator to retry a function on TimeoutException up to a specified number of attempts.

    Args:
        max_attempts (int, optional): Maximum number of retry attempts. Defaults to 3.
        delay (float, optional): Delay in seconds between retry attempts. Defaults to 1.0.

    Returns:
        callable: The decorated function that returns the original function's result.

    Raises:
        Exception: If all attempts are exhausted, raises an exception with details of the last error.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 1
            last_exception = None

            while attempt <= max_attempts:
                try:
                    logger.debug(
                        f"Attempt {attempt} of {max_attempts} for function {func.__name__}")
                    result = func(*args, **kwargs)
                    logger.debug(
                        f"Successfully executed {func.__name__} on attempt {attempt}")
                    return result

                except TimeoutException as e:
                    last_exception = e
                    logger.warning(
                        f"Attempt {attempt}/{max_attempts} failed for {func.__name__}: "
                        f"TimeoutException - {str(e)}"
                    )
                    if attempt == max_attempts:
                        error_msg = (
                            f"Exhausted all {max_attempts} attempts for {func.__name__}. "
                            f"Last arguments: args={args}, kwargs={kwargs}"
                        )
                        logger.error(error_msg, exc_info=True)
                        raise Exception(error_msg) from last_exception

                    attempt += 1
                    logger.info(f"Waiting {delay} seconds before next attempt")
                    time.sleep(delay)

            if last_exception:
                logger.critical(
                    f"Unexpected loop termination for {func.__name__}")
                raise last_exception
        return wrapper
    return decorator


def retry_on_stale_element(max_attempts=MAX_ATTEMPTS, delay=DELAY):
    """
    A decorator to retry a function on StaleElementReferenceException up to a specified number of attempts.

    Args:
        max_attempts (int, optional): Maximum number of retry attempts. Defaults to 3.
        delay (float, optional): Delay in seconds between retry attempts. Defaults to 1.0.

    Returns:
        callable: The decorated function that returns the original function's result.

    Raises:
        Exception: If all attempts are exhausted, raises an exception with details of the last error.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 1
            last_exception = None

            while attempt <= max_attempts:
                try:
                    logger.debug(
                        f"Attempt {attempt} of {max_attempts} for function {func.__name__}")
                    result = func(*args, **kwargs)
                    logger.debug(
                        f"Successfully executed {func.__name__} on attempt {attempt}")
                    return result

                except StaleElementReferenceException as e:
                    last_exception = e
                    logger.warning(
                        f"Attempt {attempt}/{max_attempts} failed for {func.__name__}: "
                        f"StaleElementReferenceException - {str(e)}"
                    )
                    if attempt == max_attempts:
                        error_msg = (
                            f"Exhausted all {max_attempts} attempts for {func.__name__}. "
                            f"Last arguments: args={args}, kwargs={kwargs}"
                        )
                        logger.error(error_msg, exc_info=True)
                        raise Exception(error_msg) from last_exception

                    attempt += 1
                    logger.info(f"Waiting {delay} seconds before next attempt")
                    time.sleep(delay)

            if last_exception:
                logger.critical(
                    f"Unexpected loop termination for {func.__name__}")
                raise last_exception
        return wrapper
    return decorator


class ProductInfo:
    def __init__(self, url, price, is_on_sale, price_on_sale, is_available, title):
        self.url = url
        self.price = price
        self.is_on_sale = is_on_sale
        self.price_on_sale = price_on_sale
        self.is_available = is_available
        self.title = title

    def to_dict(self):
        return {
            "url": self.url,
            "price": self.price,
            "is_on_sale": self.is_on_sale,
            "price_on_sale": self.price_on_sale,
            "is_available": self.is_available,
            "title": self.title
        }

    def __str__(self):
        return str(self.to_dict())


class Website:
    def __init__(self, url: str, price_format: str, product_xpaths: 'ProductXpaths', website_navigation: 'NavigationXPaths'):
        self.url = url
        self.price_format = price_format
        self.product_xpaths = product_xpaths
        self.website_navigation = website_navigation

    def __str__(self):
        return f'{self.url}'


class ProductXpaths:
    def __init__(self, price_on_sale, price_without_sale, price, availability, title, available_text):
        self.PRICE_ON_SALE = price_on_sale
        self.PRICE_WITHOUT_SALE = price_without_sale
        self.PRICE = price
        self.AVAILABILITY = availability
        self.TITLE = title
        self.AVAILABLE_TEXT = available_text


class NavigationXPaths:
    def __init__(self, search_field: str, submit_button: str, search_result_products_xpath_templates: str, search_result_link_attribute: str):
        self.SEARCH_FIELD = search_field
        self.SUBMIT_BUTTON = submit_button
        self.SEARCH_RESULT_PRODUCTS_XPATH_TEMPLATES = search_result_products_xpath_templates
        self.SEARCH_RESULT_LINK_ATTRIBUTE = search_result_link_attribute
