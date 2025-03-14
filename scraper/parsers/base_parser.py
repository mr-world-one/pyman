import logging
import re
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, WebDriverException, StaleElementReferenceException
from typing import Union, List, Tuple
from functools import wraps

from scraper.parsers.website_info import WebsiteInfo
from scraper.utils.config import SELENIUM_OPTIONS, EXCPLICIT_TIMEOUT, IMPLICIT_TIMEOUT, SELENIUM_EXPERIMENTAL_OPTIONS,MAX_ATTEMPTS, DELAY

logger = logging.getLogger(__name__)

def retry_on_timeout(max_attempts=MAX_ATTEMPTS, delay=DELAY):
    """
    Decorator to retry a function on TimeoutException up to max_attempts times.

    :param max_attempts: Maximum number of retry attempts.
    :type max_attempts: int
    :param delay: Delay in seconds between retry attempts.
    :type delay: float
    :return: The decorated function's result.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 1
            last_exception = None
            
            while attempt <= max_attempts:
                try:
                    return func(*args, **kwargs)
                
                except TimeoutException as e:
                    last_exception = e
                    message = f"Attempt {attempt}/{max_attempts} - TimeoutException in {func.__name__}"
                    logger.warning(message)
                    if attempt == max_attempts:
                        final_message = f"Failed after {max_attempts} attempts in {func.__name__}"
                        logger.exception(final_message)
                        raise TimeoutException(final_message) from last_exception
                    attempt += 1
                    time.sleep(delay)
                    
            raise last_exception
        return wrapper
    return decorator

def retry_on_stale_element(max_attempts=MAX_ATTEMPTS, delay=DELAY):
    """
    Decorator to retry a function on StaleElementReferenceException up to max_attempts times.

    :param max_attempts: Maximum number of retry attempts.
    :type max_attempts: int
    :param delay: Delay in seconds between retry attempts.
    :type delay: float
    :return: The decorated function's result.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 1
            last_exception = None
            
            while attempt <= max_attempts:
                try:
                    return func(*args, **kwargs)
                
                except StaleElementReferenceException as e:
                    last_exception = e
                    message = f"Attempt {attempt}/{max_attempts} - StaleElementReferenceException in {func.__name__}"
                    logger.warning(message)
                    if attempt == max_attempts:
                        final_message = f"Failed after {max_attempts} attempts in {func.__name__}"
                        logger.exception(final_message)
                        raise StaleElementReferenceException(final_message) from last_exception
                    attempt += 1
                    time.sleep(delay)
                    
            raise last_exception
        return wrapper
    return decorator

class ElementNotFoundException(Exception):
    def __init__(self, *args):
        super().__init__(*args)
class PriceNotFoundException(ElementNotFoundException):
    def __init__(self, *args):
        super().__init__(*args)
class AvailabilityNotFoundException(ElementNotFoundException):
    def __init__(self, *args):
        super().__init__(*args)
class TitleNotFoundException(ElementNotFoundException):
    def __init__(self, *args):
        super().__init__(*args)

class PriceIsNotNormalizedException(Exception):
    def __init__(self, *args):
        super().__init__(*args)      
        
class PageNotLoadedException(Exception):
        def __init__(self, *args):
            super().__init__(*args)
class UnableToSendKeysException(Exception):
    def __init__(self, *args):
        super().__init__(*args)
class UnableToPressButtonException(Exception):
    def __init__(self, *args):
        super().__init__(*args)
class UnableToOpenSearchResultsException(Exception):
    def __init__(self, *args):
        super().__init__(*args)
class UnableToGetProductInfoException(Exception):
    def __init__(self, *args):
        super().__init__(*args)
class UnableToGetNProductUrls(Exception):
    def __init__(self, *args):
        super().__init__(*args)
class InvalidPageException(Exception):
    def __init__(self, *args):
        super().__init__(*args)

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

class BaseParser:
    """A base class for parsing web pages using Selenium WebDriver."""

    def __init__(self, website_info: 'WebsiteInfo'):
        """
        Initializes the BaseParser with Selenium WebDriver and website information.

        :param website_info: Configuration object containing website-specific details (e.g., XPaths, URL).
        :type website_info: WebsiteInfo
        :raises WebDriverException: If the Chrome WebDriver fails to initialize.
        """
        self.options = Options()
        for option in SELENIUM_OPTIONS:
            self.options.add_argument(option)
        self.options.add_experimental_option('prefs', SELENIUM_EXPERIMENTAL_OPTIONS)
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)
        self.driver.implicitly_wait(IMPLICIT_TIMEOUT)
        self.wait = WebDriverWait(self.driver, EXCPLICIT_TIMEOUT)
        self.website_info = website_info

    def _normalize_price(self, price: str) -> float:
        """
        Normalizes a price string into a float value.

        :param price: The raw price string to normalize.
        :type price: str
        :raises PriceIsNotNormalizedException: If the price cannot be normalized using the specified pattern.
        :return: The normalized price as a float.
        :rtype: float
        """
        formatted_price = price.replace(' ', '').strip()
        match = re.search(self.website_info.price_format, formatted_price)
        if match:
            return float(match.group())
        
        message = f"Could not normalize price: {price} with pattern: {self.website_info.price_format}"
        logger.error(message)
        raise PriceIsNotNormalizedException(message)

    @retry_on_timeout(max_attempts=2)
    def _parse_elements(self, xpath: str, multiple: bool = False) -> Union['WebElement', List['WebElement']]:
        """
        Parses elements from the webpage using the provided XPath with retry on timeout.

        :param xpath: The XPath expression to locate elements.
        :type xpath: str
        :param multiple: If True, returns a list of elements; if False, returns a single element.
        :type multiple: bool
        :raises TimeoutException: If elements cannot be located after all retry attempts.
        :raises ElementNotFoundException: If an unexpected error occurs during parsing.
        :return: A single WebElement or a list of WebElements based on the `multiple` parameter.
        :rtype: WebElement | list[WebElement]
        """
        try:
            if multiple:
                return self.wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
            else:
                return self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        except TimeoutException as e:
            message = f"TimeoutException. Failed to parse elements using XPath: {xpath}"
            logger.exception(message)
            raise

    @retry_on_stale_element()
    def get_price(self, url : str, ignore_price_format : bool, raise_exception : bool, open_page : bool = True) -> float | str | None:
        try:
            if open_page:
                self._open_page(url)
            return self._parse_price(xpath=self.website_info.product_xpaths.PRICE, ignore_format=ignore_price_format)
        except ElementNotFoundException as e:
            if raise_exception:
                raise
        return None
    
    @retry_on_stale_element()
    def get_price_on_sale(self, url : str, ignore_price_format : bool, raise_exception : bool, open_page : bool = True) -> float | str | None:
        try:
            if open_page:
                self._open_page(url)
            return self._parse_price(xpath=self.website_info.product_xpaths.PRICE_ON_SALE, ignore_format=ignore_price_format)
        except ElementNotFoundException as e:
            if raise_exception:
                raise
        return None

    @retry_on_stale_element()
    def get_availability(self, url : str, raise_exception : bool, open_page : bool = True) -> bool:
        try:
            if open_page:
                self._open_page(url)
            availability_element = self._parse_elements(xpath=self.website_info.product_xpaths.AVAILABILITY, multiple=False)
            return self.website_info.product_xpaths.AVAILABLE_TEXT in availability_element.text
        except (ElementNotFoundException) as e:
            message = f"Availability element not found with XPath: { self.website_info.product_xpaths.AVAILABILITY }"
            logger.exception(message)
            if raise_exception:
                raise 
        return False

    @retry_on_stale_element()      
    def get_price_details(self, url : str, ignore_price_format : bool, raise_exception : bool, open_page : bool = True) -> Tuple[float, float, bool]:
        if open_page:
            self._open_page(url=url)

        price = self.get_price(url=url, ignore_price_format=ignore_price_format, raise_exception=raise_exception, open_page=False)

        price_on_sale = self.get_price_on_sale(url=url, ignore_price_format=ignore_price_format, raise_exception=raise_exception, open_page=False)

        is_on_sale = price_on_sale is not None

        return price, price_on_sale, is_on_sale

    @retry_on_stale_element()
    def get_title(self, url : str, raise_exception : bool, open_page : bool = True) -> str | None:
        if open_page:
            self._open_page(url)
        try:
            return self._parse_elements(self.website_info.product_xpaths.TITLE).text
        except Exception as e:
            logger.error(f"Unable to parse title with XPath: {self.website_info.product_xpaths.TITLE}")
            if raise_exception:
                raise TitleNotFoundException from e
        return None

    def _parse_price(self, xpath: str, ignore_format: bool = True) -> Union[float, str]:
        """
        Parses a price from a webpage using the specified XPath.

        :param xpath: The XPath to locate the price element.
        :type xpath: str
        :param ignore_format: If True, returns raw text if normalization fails; if False, raises an exception.
        :type ignore_format: bool
        :raises PriceIsNotNormalizedException: If normalization fails and `ignore_format` is False.
        :raises PriceNotFoundException: If the price element cannot be found or parsed.
        :return: Normalized price as a float, or raw text if `ignore_format` is True and normalization fails.
        :rtype: float | str
        """
        price_element = None
        try:
            price_element = self._parse_elements(xpath, multiple=False)
            return self._normalize_price(price_element.text)
        except PriceIsNotNormalizedException as e:
            if ignore_format:
                return price_element.text
            message = f"Price is not normalized for XPath: {xpath}"
            logger.exception(message)
            raise PriceIsNotNormalizedException(message) from e
        except (ElementNotFoundException, TimeoutException) as e:
            message = f"Price element not found with XPath: {xpath}"
            logger.error(message)
            logger.exception(message)
            raise PriceNotFoundException(message) from e

    def _open_page(self, url: str) -> None:
        """
        Opens a webpage using the provided URL in the WebDriver with retry on timeout.

        :param url: The URL of the page to open.
        :type url: str
        :raises TimeoutException: If the page cannot be loaded after all retry attempts.
        :raises WebDriverException: If a WebDriver-specific error occurs.
        :raises Exception: If an unexpected error occurs during page loading.
        """
        if not self.website_info.url in url:
            message = f'Unable to open {url}, expected to get url in {self.website_info.url} domain.'
            logger.exception(message)
            raise InvalidPageException(message)
        
        try:
            self.driver.get(url)
            
        except TimeoutException as e:
            message = f"Timeout while loading page: {url}"
            logger.exception(message)
            raise  # Handled by retry decorator
        
        except WebDriverException as e:
            message = f"WebDriverException while loading page: {url}"
            logger.exception(message)
            raise WebDriverException(message) from e
        
        except Exception as e:
            message = f"Unexpected error while loading page: {url}"
            logger.exception(message)
            raise Exception(message) from e

    def _close(self) -> None:
        """
        Closes the WebDriver session.

        :raises WebDriverException: If quitting the WebDriver fails due to a WebDriver-specific issue.
        :raises Exception: If an unexpected error occurs while closing the WebDriver.
        """
        try:
            self.driver.quit()
        except WebDriverException as e:
            message = f"Failed to quit WebDriver: {e}"
            logger.exception(message)
            raise WebDriverException(message) from e
        except Exception as e:
            message = f"Failed to quit WebDriver: {e}"
            logger.exception(message)
            raise Exception(message) from e

    def __del__(self):
        self._close()

    def info_about_product(self, url: str, fast_parse: bool = True, ignore_price_format: bool = False, 
                          raise_exception: bool = False) -> 'ProductInfo':
        """
        Retrieves product information from a URL.

        :param url: The product page URL.
        :type url: str
        :param fast_parse: If True, retrieves only basic details (price); if False, includes sale and availability.
        :type fast_parse: bool
        :param ignore_price_format: If True, skips price normalization on failure.
        :type ignore_price_format: bool
        :param raise_exception: If True, raises exceptions on failure; if False, returns None for missing data.
        :type raise_exception: bool
        :raises TimeoutException: If the page cannot be loaded.
        :raises ElementNotFoundException: If elements (e.g., title) cannot be parsed and `raise_exception` is True.
        :raises PriceNotFoundException: If price cannot be found and `raise_exception` is True.
        :return: A ProductInfo object with parsed details.
        :rtype: ProductInfo
        """
        self._open_page(url)
        price, is_on_sale, price_on_sale, is_available = None, None, None, None
        if fast_parse:
            price = self.get_price(url=url, ignore_price_format=ignore_price_format, raise_exception=False, open_page=False)
            if price is None:
                price = self.get_price_on_sale(url=url, ignore_price_format=ignore_price_format, raise_exception=raise_exception, open_page=False)
        else:
            price, price_on_sale, is_on_sale = self.get_price_details(url=url, ignore_price_format=ignore_price_format, raise_exception=raise_exception, open_page=False)

            is_available = self.get_availability(url=url, raise_exception=raise_exception, open_page=False)
        
        title = self.get_title(url=url,raise_exception=raise_exception, open_page=False)
        return ProductInfo(url, price, is_on_sale, price_on_sale, is_available, title)
    
    def _send_keys(self, element : WebElement, keys : str | Keys):
        """
        Sends keys to the specified element.

        This method attempts to send a sequence of keys to the given element. If an error occurs while
        trying to send the keys (e.g., if the element is not interactable), an exception is raised.

        :param element: The web element to which the keys will be sent.
        :type element: WebElement
        :param keys: The keys to send to the element.
        :type keys: str or Keys
        :raises UnableToSendKeysException: If unable to send keys to the element.
        """
        try:
            element.send_keys(keys)
        except (TimeoutException, StaleElementReferenceException):
            raise
        except Exception as e:
            message = "Failed to send keys"
            logger.exception(message)
            raise UnableToSendKeysException(message) from e

    def _press_button(self, button : WebElement):
        """
        Clicks the specified button.

        This method attempts to click the provided button element. If an error occurs while trying to click
        the button (e.g., if the button is not interactable), an exception is raised.

        :param button: The button element to be clicked.
        :type button: WebElement
        :raises UnableToPressButtonException: If the button cannot be clicked.
        """
        try:
            button.click()
        except (TimeoutException, StaleElementReferenceException):
            raise
        except Exception as e:
            message = "Failed to click button"
            logger.exception(message)
            raise UnableToPressButtonException(message) from e
    
    @retry_on_stale_element()
    @retry_on_timeout()
    def _open_search_results(self, product: str) -> None:
        """
        Opens the search results page for a product.

        :param product: The product name to search for.
        :type product: str
        :raises UnableToOpenSearchResultsException: If opening the page, finding the search field, or submitting fails.
        """
        try:
            self._open_page(self.website_info.url)
        except (TimeoutException, StaleElementReferenceException):
            raise 
        except (WebDriverException, Exception) as e:
            message = f'Unable to open website using {self.website_info.url}'
            logger.exception(message)
            raise UnableToOpenSearchResultsException(message)
        
        try:
            search_field = self._parse_elements(self.website_info.website_navigation.SEARCH_FIELD)
            self._send_keys(search_field, product)
        except (TimeoutException, StaleElementReferenceException):
            raise 
        except (ElementNotFoundException, UnableToSendKeysException) as e:
            message = "Search field not found."
            logger.exception(message)
            raise UnableToOpenSearchResultsException(message) from e
        
        try:
            self._send_keys(search_field, Keys.ENTER)
        except (TimeoutException, StaleElementReferenceException):
            raise
        except Exception as e:
            logger.error("Failed to use ENTER key, attempting to click submit button.")
            try:
                submit_button = self._parse_elements(self.website_info.website_navigation.SUBMIT_BUTTON)
                self._press_button(submit_button)
            except (TimeoutException, ElementNotFoundException, UnableToPressButtonException) as e:
                message = f'Unable to press enter and press search_button'
                logger.exception(message)
                raise UnableToOpenSearchResultsException(message) from e

    @retry_on_stale_element()
    @retry_on_timeout()
    def _search_results_get_products_urls(self, n: int) -> List[str]:
        """
        Retrieves URLs of the first `n` products from search results.

        :param n: Number of product URLs to retrieve.
        :type n: int
        :raises UnableToGetNProductUrls: If product URLs cannot be retrieved.
        :return: List of product URLs.
        :rtype: list[str]
        """
        product_urls = []
        try:
            product_url_elements = self._parse_elements(
                xpath=self.website_info.website_navigation.SEARCH_RESULT_PRODUCTS_XPATH_TEMPLATES, 
                multiple=True)[:n]
            for url_element in product_url_elements:
                product_url = url_element.get_attribute(self.website_info.website_navigation.SEARCH_RESULT_LINK_ATTRIBUTE)
                product_urls.append(product_url)
        except (StaleElementReferenceException, TimeoutException):
            raise
        except Exception as e:
            message = f'Unable to get n product urls using Xpath {self.website_info.website_navigation.SEARCH_RESULT_PRODUCTS_XPATH_TEMPLATES} Original error: {e}'
            logger.error(message)
            raise UnableToGetNProductUrls(message) from e
        return product_urls

    def _find_n_products(self, product: str, n: int, fast_parse: bool = True, ignore_price_format: bool = True, 
                        raise_exception: bool = False) -> List['ProductInfo']:
        """
        Searches for and retrieves information on exactly `n` products.

        :param product: The product name to search for.
        :type product: str
        :param n: Number of products to retrieve.
        :type n: int
        :param fast_parse: If True, performs faster parsing (price only).
        :type fast_parse: bool
        :param ignore_price_format: If True, skips price normalization on failure.
        :type ignore_price_format: bool
        :param raise_exception: If True, raises exceptions on failure.
        :type raise_exception: bool
        :raises UnableToGetNProductUrls: If fewer than `n` products are found and `raise_exception` is True.
        :raises Exception: If product info parsing fails and `raise_exception` is True.
        :return: List of ProductInfo objects.
        :rtype: list[ProductInfo]
        """
        self._open_search_results(product)
        product_urls = self._search_results_get_products_urls(n)
        if len(product_urls) < n:
            message = f"Warning: Only {len(product_urls)} products found, expected {n}."
            logger.warning(message)
            if raise_exception:
                raise UnableToGetNProductUrls(message)
        products = []
        for product_url in product_urls:
            try:
                product_info = self.info_about_product(product_url, fast_parse=fast_parse, 
                                                      raise_exception=raise_exception, 
                                                      ignore_price_format=ignore_price_format)
                products.append(product_info)
            except Exception as e:
                logger.exception(f"Failed to parse product info for {product_url}")
                if raise_exception:
                    raise e
        return products

    def find_n_products(self, product : str, n : int, fast_parse=True, ignore_price_format=True, raise_exception=False):
        """
        Abstract method to find `n` products (to be implemented by subclasses).

        :param product: The product name to search for.
        :type product: str
        :param n: Number of products to retrieve.
        :type n: int
        :param fast_parse: If True, performs faster parsing.
        :type fast_parse: bool
        :param ignore_price_format: If True, skips price normalization on failure.
        :type ignore_price_format: bool
        :param raise_exception: If True, raises exceptions on failure.
        :type raise_exception: bool
        :raises NotImplementedError: Always, as this method must be overridden.
        :return: List of ProductInfo objects (in subclasses).
        :rtype: list[ProductInfo]
        """
        raise NotImplementedError()
