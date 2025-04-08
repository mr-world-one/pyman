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

from scraper.parsers.website import Website
from scraper.utils.config import SELENIUM_OPTIONS, EXCPLICIT_TIMEOUT, IMPLICIT_TIMEOUT, SELENIUM_EXPERIMENTAL_OPTIONS, MAX_ATTEMPTS, DELAY

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
                    logger.error(message)
                    if attempt == max_attempts:
                        final_message = f"Failed after {max_attempts} attempts in {func.__name__}"
                        logger.exception(final_message)
                        raise Exception(
                            final_message) from last_exception
                    attempt += 1
                    time.sleep(delay)
            if last_exception:
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
                    logger.error(message)
                    if attempt == max_attempts:
                        final_message = f"Failed after {max_attempts} attempts in {func.__name__}"
                        logger.exception(final_message)
                        raise Exception(
                            final_message) from last_exception
                    attempt += 1
                    time.sleep(delay)
            if last_exception:
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


class UnableToSendKeysException(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class UnableToPressButtonException(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class UnableToOpenSearchResultsException(Exception):
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

    def __init__(self, website_info: 'Website'):
        """
        Initializes the BaseParser with Selenium WebDriver and website information.

        :param website_info: Configuration object containing website-specific details (e.g., XPaths, URL).
        :type website_info: WebsiteInfo
        :raises WebDriverException: If the Chrome WebDriver fails to initialize.
        """
        self.options = Options()
        for option in SELENIUM_OPTIONS:
            self.options.add_argument(option)
        self.options.add_experimental_option(
            'prefs', SELENIUM_EXPERIMENTAL_OPTIONS)
        self.driver = webdriver.Chrome(service=Service(
            ChromeDriverManager().install()), options=self.options)
        self.driver.implicitly_wait(IMPLICIT_TIMEOUT)
        self.wait = WebDriverWait(self.driver, EXCPLICIT_TIMEOUT)
        self.website_info = website_info

    def normalize_price(self, price: str, ignore_price_format: bool) -> Union[float, str]:
        """
        Normalizes a price string into a float based on a predefined regular expression pattern.

        This method takes a price string, removes whitespace, and attempts to extract a numeric value using a regular
        expression pattern defined in `self.website_info.price_format`. If successful, it returns the price as a float.
        If normalization fails, it either returns the original string (if `ignore_price_format` is True) or raises an exception.

        Args:
            price (str): The raw price string to normalize (e.g., "$19.99", "19.99 USD").
            ignore_price_format (bool): If True, returns the original string when normalization fails; if False, raises
                                        an exception. 

        Returns:
            float | str: The normalized price as a float if the pattern matches, or the original price string if normalization
                        fails and `ignore_price_format` is True.

        Raises:
            PriceIsNotNormalizedException: If the price cannot be normalized and `ignore_price_format` is False.
            ValueError: If the matched string cannot be converted to a float (e.g., invalid numeric format).
        """
        formatted_price = price.replace(' ', '').strip()
        match = re.search(self.website_info.price_format, formatted_price)
        if match:
            return float(match.group())

        if ignore_price_format:
            return price
        message = f"{self.website_info}: Could not normalize price: {price} with pattern: {self.website_info.price_format}"
        logger.error(message)
        raise PriceIsNotNormalizedException(message)

    @retry_on_timeout()
    @retry_on_stale_element()
    def _parse_elements(self, xpath: str, multiple: bool = False) -> Union['WebElement', List['WebElement']]:
        """
        Parses elements from the webpage using the provided XPath with retry on timeout.

        This method attempts to locate one or more elements on the current webpage using the specified XPath expression.
        It leverages a WebDriver wait mechanism to ensure elements are present before returning them.

        Args:
            xpath (str): The XPath expression used to locate elements on the webpage.
            multiple (bool, optional): If True, returns a list of all matching elements; if False, returns a single element.
                                    Defaults to False.

        Returns:
            WebElement | List[WebElement]: A single WebElement if `multiple` is False, or a list of WebElements if `multiple` is True.

        Raises:
            TimeoutException: If the elements cannot be located within the timeout period after all retry attempts.
            StaleElementReferenceException: If an element becomes stale during processing (handled by retry decorator in calling methods).
            NoSuchElementException: If the XPath does not match any elements (depending on WebDriver configuration).
            WebDriverException: If an unexpected WebDriver-related error occurs (e.g., browser disconnection).
        """
        if multiple:
            return self.wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
        else:
            return self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))

    def get_price(self, url: str, ignore_price_format: bool, open_page: bool = True) -> float | str:
        """
        Retrieves the regular price of a product from a webpage.

        This method navigates to the specified URL (if `open_page` is True) and extracts the product price using an XPath
        defined in `website_info.product_xpaths.PRICE`. The price is then parsed based on the `ignore_price_format` flag.

        Args:
            url (str): The URL of the webpage containing the product price.
            ignore_price_format (bool): If True, returns the price as a raw string; if False, attempts to parse it as a float.
            open_page (bool, optional): If True, opens the webpage before retrieving the price. Defaults to True.

        Returns:
            float | str: The parsed price as a float if `ignore_price_format` is False and parsing succeeds,
                                the raw price string if `ignore_price_format` is True.

        Raises:
            PriceNotFoundException: 
            WebDriverException: If an error occurs while opening the page or interacting with the browser.
            PriceIsNotNormalizedException: If the price text cannot be converted to a float and `ignore_price_format` is False (from `_parse_price`).
        """
        if open_page:
            self.open_page(url)

        try:
            price = self._parse_price(
                xpath=self.website_info.product_xpaths.PRICE, ignore_price_format=ignore_price_format)
            return price
        except PriceIsNotNormalizedException:
            raise
        except Exception:
            message = f"{self.website_info}: Couldn't get price with {self.website_info.product_xpaths.PRICE}, maybe product is on sale."
            logger.error(message)
            try:
                price_without_sale = self._parse_price(
                    xpath=self.website_info.product_xpaths.PRICE_WITHOUT_SALE, ignore_price_format=ignore_price_format)
                return price_without_sale
            except Exception as e:
                message = f"{self.website_info}: Couldn't get price with {self.website_info.product_xpaths.PRICE_WITHOUT_SALE}, unknown reason"
                logger.exception(message)
                raise PriceNotFoundException from e

    def get_price_on_sale(self, url: str, ignore_price_format: bool, open_page: bool = True) -> float | str:
        """
        Retrieves the sale price of a product from a webpage.

        This method navigates to the specified URL (if `open_page` is True) and extracts the sale price using an XPath
        defined in `website_info.product_xpaths.PRICE_ON_SALE`. The price is then parsed based on the `ignore_price_format` flag.

        Args:
            url (str): The URL of the webpage containing the product sale price.
            ignore_price_format (bool): If True, returns the sale price as a raw string; if False, attempts to parse it as a float.
            open_page (bool, optional): If True, opens the webpage before retrieving the sale price. Defaults to True.

        Returns:
            float | str: The parsed sale price as a float if `ignore_price_format` is False and parsing succeeds,
                                the raw sale price string if `ignore_price_format` is True.

        Raises:
            PriceNotFoundException
            WebDriverException: If an error occurs while opening the page or interacting with the browser.
            PriceIsNotNormalizedException: If the sale price text cannot be converted to a float and `ignore_price_format` is False (from `_parse_price`).
        """
        if open_page:
            self.open_page(url)

        try:
            return self._parse_price(xpath=self.website_info.product_xpaths.PRICE_ON_SALE, ignore_price_format=ignore_price_format)
        except PriceIsNotNormalizedException:
            raise
        except Exception as e:
            message = f'{self.website_info}: Unable to get price on sale with {self.website_info.product_xpaths.PRICE_ON_SALE}, maybe product is not on sale.'
            logger.exception(message)
            raise PriceNotFoundException from e

    def get_availability(self, url: str, open_page: bool = True) -> bool:
        """
        Checks the availability of a product on a webpage.

        This method navigates to the specified URL (if `open_page` is True) and checks the product's availability by locating
        an element with an XPath defined in `website_info.product_xpaths.AVAILABILITY`. It returns True if the predefined
        `AVAILABLE_TEXT` is found in the element's text.

        Args:
            url (str): The URL of the webpage containing the product availability information.
            open_page (bool, optional): If True, opens the webpage before checking availability. Defaults to True.

        Returns:
            bool: True if the product is available (i.e., `AVAILABLE_TEXT` is in the element's text), False otherwise.

        Raises:
            AvailabilityNotFoundException:
            WebDriverException: If an error occurs while opening the page or interacting with the browser.
        """
        if open_page:
            self.open_page(url)
        try:
            availability_element = self._parse_elements(
                xpath=self.website_info.product_xpaths.AVAILABILITY, multiple=False)
            return self.website_info.product_xpaths.AVAILABLE_TEXT in availability_element.text
        except Exception as e:
            message = f'{self.website_info}: Unable to get information about availability with {self.website_info.product_xpaths.AVAILABILITY} and {self.website_info.product_xpaths.AVAILABLE_TEXT}'
            logger.exception(message)
            raise AvailabilityNotFoundException from e

    def get_price_details(self, url: str, ignore_price_format: bool, open_page: bool = True) -> Tuple[float, float, bool]:
        if open_page:
            self.open_page(url=url)

        price = self.get_price(
            url=url, ignore_price_format=ignore_price_format, open_page=False)

        price_on_sale = None
        try:
            price_on_sale = self.get_price_on_sale(
                url=url, ignore_price_format=ignore_price_format, open_page=False)
        except Exception:
            # product can be on regular price
            pass

        is_on_sale = price_on_sale is not None

        return price, price_on_sale, is_on_sale

    def get_title(self, url: str, open_page: bool = True) -> str:
        """
        Retrieves the title of a product from a webpage.

        This method navigates to the specified URL (if `open_page` is True) and extracts the product title using an XPath
        defined in `self.website_info.product_xpaths.TITLE`. It returns the text content of the located title element.

        Args:
            url (str): The URL of the webpage containing the product title.
            open_page (bool, optional): If True, opens the webpage before retrieving the title. Defaults to True.

        Returns:
            str: The text content of the title element.

        Raises:
            TimeoutException: If the title element cannot be located within the timeout period (from `_parse_elements`).
            StaleElementReferenceException: If the title element becomes stale during processing (e.g., page refreshes).
            NoSuchElementException: If the title XPath does not match any elements (depending on WebDriver configuration).
            WebDriverException: If an error occurs while opening the page or interacting with the browser.
        """
        if open_page:
            self.open_page(url)
        try:
            return self._parse_elements(self.website_info.product_xpaths.TITLE).text
        except Exception as e:
            message = f'{self.website_info}: Unable to get title with {self.website_info.product_xpaths.TITLE}'
            logger.exception(message)
            raise TitleNotFoundException from e

    def _parse_price(self, xpath: str, ignore_price_format: bool = True) -> Union[float, str]:
        """
        Parses a price from a webpage using the specified XPath.

        This method locates a price element on the webpage using the provided XPath and attempts to normalize its text
        into a float value. If normalization fails, it either returns the raw text (if `ignore_price_format` is True) or raises
        an exception (if `ignore_price_format` is False).

        Args:
            xpath (str): The XPath expression used to locate the price element on the webpage.
            ignore_price_format (bool, optional): If True, returns the raw text when normalization fails; if False, raises an
                                            exception. Defaults to True.

        Returns:
            float | str: The normalized price as a float if successful, or the raw text string if normalization fails and
                        `ignore_price_format` is True.

        Raises:
            PriceIsNotNormalizedException: If the price text cannot be normalized into a float and `ignore_price_format` is False.
            TimeoutException: If the price element cannot be located within the timeout period (from `_parse_elements`).
            StaleElementReferenceException: If the price element becomes stale during processing (from `_parse_elements`).
            WebDriverException: If an unexpected WebDriver-related error occurs during element retrieval.
            AttributeError: If `self._parse_elements` or `self._normalize_price` is not properly defined or initialized.
            TypeError: If `price_element.text` is None or not a string when passed to `_normalize_price`.
        """
        price_element = None
        price_element = self._parse_elements(xpath, multiple=False)
        return self.normalize_price(price_element.text, ignore_price_format=ignore_price_format)

    @retry_on_timeout()
    def open_page(self, url: str) -> None:
        if not self.website_info.url in url:
            message = f'Unable to open {url}, expected to get url in {self.website_info.url} domain.'
            logger.exception(message)
            raise InvalidPageException(message)

        try:
            if self.driver.current_url != url:
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
        except WebDriverException:
            message = f"Failed to quit WebDriver"
            logger.exception(message)
            raise
        except Exception as e:
            message = f"Failed to quit WebDriver"
            logger.exception(message)
            raise Exception(message) from e

    def __del__(self):
        self._close()

    def info_about_product(self, url: str, fast_parse: bool = True, ignore_price_format: bool = False,
                           raise_exception: bool = False) -> 'ProductInfo':
        self.open_page(url)
        price, is_on_sale, price_on_sale, is_available, title = None, None, None, None, None
        if fast_parse:
            try:
                price = self.get_price(
                    url=url, ignore_price_format=ignore_price_format, open_page=False)
            except PriceNotFoundException:
                if raise_exception:
                    raise
        else:
            try:
                price, price_on_sale, is_on_sale = self.get_price_details(
                    url=url, ignore_price_format=ignore_price_format, open_page=False)
            except PriceNotFoundException:
                if raise_exception:
                    raise

            try:
                is_available = self.get_availability(url=url, open_page=False)
            except AvailabilityNotFoundException:
                if raise_exception:
                    raise

        try:
            title = self.get_title(url=url, open_page=False)
        except TitleNotFoundException:
            if raise_exception:
                raise

        return ProductInfo(url, price, is_on_sale, price_on_sale, is_available, title)

    @retry_on_stale_element()
    @retry_on_timeout()
    def _send_keys(self, xpath: str, keys: str | Keys):
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
            element = self._parse_elements(xpath=xpath, multiple=False)
            element.send_keys(keys)
        except (TimeoutException, StaleElementReferenceException):
            raise
        except Exception as e:
            message = "Failed to send keys"
            logger.exception(message)
            raise UnableToSendKeysException(message) from e

    @retry_on_stale_element()
    @retry_on_timeout()
    def _press_button(self, xpath: str):
        """
        Clicks the specified button.

        This method attempts to click the provided button element. If an error occurs while trying to click
        the button (e.g., if the button is not interactable), an exception is raised.

        :param button: The button element to be clicked.
        :type button: WebElement
        :raises UnableToPressButtonException: If the button cannot be clicked.
        """
        try:
            button = self._parse_elements(xpath, multiple=False)
            button.click()
        except (TimeoutException, StaleElementReferenceException):
            raise
        except Exception as e:
            message = "Failed to click button"
            logger.exception(message)
            raise UnableToPressButtonException(message) from e

    def _open_search_results(self, product: str) -> None:
        try:
            self.open_page(self.website_info.url)
        except (Exception) as e:  # open_page already tried multiple times
            message = f'Unable to open website using {self.website_info.url}'
            logger.exception(message)
            raise UnableToOpenSearchResultsException(message)

        try:
            self._send_keys(
                self.website_info.website_navigation.SEARCH_FIELD, product)
        except Exception as e:  # general exception because _parse_elements has tried multiple times to load element but failed
            message = "Search field not found."
            logger.exception(message)
            raise UnableToOpenSearchResultsException(message) from e

        try:
            self._send_keys(
                self.website_info.website_navigation.SEARCH_FIELD, Keys.ENTER)
        except Exception as e:  # _send_keys tried multiple times
            logger.error(
                "Failed to use ENTER key, attempting to click submit button.")
            try:
                self._press_button(
                    self.website_info.website_navigation.SUBMIT_BUTTON)
            except Exception as e:
                message = f'Unable to press enter and press search_button'
                logger.exception(message)
                raise UnableToOpenSearchResultsException(message) from e

    @retry_on_timeout()
    @retry_on_stale_element()
    def _search_results_get_products_urls(self, n: int) -> List[str]:
        product_urls = []
        try:
            product_url_elements = self._parse_elements(
                xpath=self.website_info.website_navigation.SEARCH_RESULT_PRODUCTS_XPATH_TEMPLATES,
                multiple=True)[:n]
            for url_element in product_url_elements:
                product_url = url_element.get_attribute(
                    self.website_info.website_navigation.SEARCH_RESULT_LINK_ATTRIBUTE)
                product_urls.append(product_url)
        except (StaleElementReferenceException, TimeoutException):
            raise
        except Exception as e:
            message = f'{self.website_info}: Unable to get n product urls using Xpath-template: {self.website_info.website_navigation.SEARCH_RESULT_PRODUCTS_XPATH_TEMPLATES}'
            logger.exception(message)
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

        products = []
        for product_url in product_urls:
            try:
                product_info = self.info_about_product(product_url, fast_parse=fast_parse,
                                                       raise_exception=raise_exception,
                                                       ignore_price_format=ignore_price_format)
                products.append(product_info)
            except Exception as e:
                logger.exception(
                    f"Failed to parse product info for {product_url}")
                if raise_exception:
                    raise e

        if len(products) < n:
            message = f"Warning: Only {len(products)} products found, expected {n}."
            logger.warning(message)
            if raise_exception:
                raise UnableToGetNProductUrls(message)
        return products

    def find_n_products(self, product: str, n: int, fast_parse=True, ignore_price_format=True, raise_exception=False):
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
