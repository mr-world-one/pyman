import re

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
from typing import Union, List, Tuple, Optional
from urllib.parse import urlparse

from scraper.parsers import *
from scraper.parsers.exceptions import *
from scraper.utils import SELENIUM_OPTIONS, EXPLICIT_TIMEOUT, IMPLICIT_TIMEOUT, SELENIUM_EXPERIMENTAL_OPTIONS


class BaseParser:
    """A base class for parsing web pages using Selenium WebDriver."""

    def __init__(self, website_info: Website) -> 'BaseParser':
        """
        Initialize the BaseParser with Selenium WebDriver and website configuration.

        Args:
            website_info (Website): Configuration object containing website-specific details
                                  such as XPaths and URL.

        Attributes:
            options (Options): Selenium WebDriver options configuration
            driver (webdriver.Chrome): Configured Chrome WebDriver instance
            wait (WebDriverWait): WebDriverWait instance for explicit waits
            website_info (Website): Stored website configuration

        Raises:
            WebDriverException: If Chrome WebDriver initialization fails
            TypeError: If website_info is not of type Website
        """
        logger.debug("Starting BaseParser initialization")

        if not isinstance(website_info, Website):
            logger.error(
                f"Invalid website_info type: {type(website_info)}. Expected Website")
            raise TypeError("website_info must be of type Website")

        self.website_info = website_info
        logger.debug(f"Stored website_info: {website_info}")

        self.options = Options()
        self.driver = None

        try:
            for option in SELENIUM_OPTIONS:
                self.options.add_argument(option)
                logger.debug(f"Added Selenium option: {option}")

            self.options.add_experimental_option(
                'prefs', SELENIUM_EXPERIMENTAL_OPTIONS)
            logger.debug(f"Added experimental options: {SELENIUM_EXPERIMENTAL_OPTIONS}")

            logger.info("Initializing Chrome WebDriver")
            self.driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=self.options
            )
            self.driver.implicitly_wait(IMPLICIT_TIMEOUT)
            logger.debug(f"Set implicit wait to {IMPLICIT_TIMEOUT} seconds")

            self.wait = WebDriverWait(self.driver, EXPLICIT_TIMEOUT)
            logger.debug(f"Initialized WebDriverWait with timeout {EXPLICIT_TIMEOUT} seconds")

            logger.info("BaseParser initialization completed successfully")

        except Exception as e:
            logger.error("Failed to initialize WebDriver", exc_info=True)
            if self.driver:
                try:
                    self.driver.quit()
                    logger.debug("Cleaned up WebDriver instance")
                except Exception:
                    logger.warning(
                        "Failed to clean up WebDriver during error handling")
            raise

    def normalize_price(self, price: str, ignore_price_format: bool) -> Union[float, str]:
        """
        Normalize a price string into a float using a predefined regex pattern.

        This method processes a price string by removing whitespace and attempting to extract
        a numeric value based on the regex pattern in `self.website_info.price_format`.
        Returns a float on successful match, or handles failure based on `ignore_price_format`.

        Args:
            price (str): Raw price string to normalize (e.g., "$19.99", "19.99 USD")
            ignore_price_format (bool): If True, returns original string on failure;
                                    if False, raises an exception

        Returns:
            Union[float, str]: Normalized price as float if successful, or original string
                            if normalization fails and `ignore_price_format` is True

        Raises:
            PriceIsNotNormalizedException: If normalization fails and `ignore_price_format` is False
            ValueError: If matched string cannot be converted to float
            AttributeError: If `self.website_info.price_format` is not defined or not a valid regex pattern
        """
        logger.debug(f"Attempting to normalize price")

        formatted_price = price.replace(' ', '').strip()

        try:
            match = re.search(self.website_info.price_format, formatted_price)
            if match:
                matched_price = match.group()
                try:
                    normalized_price = float(matched_price)
                    logger.debug(f"Successfully normalized price to")
                    return normalized_price
                except ValueError as e:
                    logger.error(f"Failed to convert matched price to float", exc_info=True)
                    raise ValueError(f"Cannot convert price to float") from e

            if ignore_price_format:
                logger.warning(f"Price not matched, returning original due to ignore_price_format=True")
                return price

            error_msg = (
                f"Failed to normalize price with pattern"
                f"'{self.website_info.price_format}' for {self.website_info}"
            )
            logger.error(error_msg)
            raise PriceIsNotNormalizedException(error_msg)

        except AttributeError as e:
            logger.error(
                f"Invalid or missing price_format in website_info: {self.website_info}",
                exc_info=True
            )
            raise AttributeError("website_info.price_format is not properly defined") from e
        except re.error as e:
            logger.error(
                f"Invalid regex pattern in website_info.price_format: {self.website_info.price_format}",
                exc_info=True
            )
            raise AttributeError("website_info.price_format contains an invalid regex pattern") from e

    @retry_on_timeout()
    @retry_on_stale_element()
    def _parse_elements(self, xpath: str, multiple: bool = False) -> Union[WebElement, List[WebElement]]:
        """
        Locate elements on a webpage using XPath with retry mechanisms for timeouts and stale elements.

        This method uses WebDriverWait to find elements matching the given XPath expression.
        It supports both single and multiple element retrieval, with automatic retries on
        TimeoutException and StaleElementReferenceException handled by decorators.

        Args:
            xpath (str): XPath expression to locate elements
            multiple (bool): If True, returns all matching elements as a list; if False, returns a single element.
                            Defaults to False

        Returns:
            Union[WebElement, List[WebElement]]: Single WebElement if multiple=False, or list of WebElements if multiple=True

        Raises:
            TimeoutException: If elements aren't found within the timeout period (after retries)
            StaleElementReferenceException: If elements become stale (after retries)
            NoSuchElementException: If no elements match the XPath
            WebDriverException: For unexpected WebDriver errors (e.g., browser crash)
            TypeError: If xpath is not a string
        """
        try:
            if multiple:
                logger.debug("Waiting for presence of all elements")
                elements = self.wait.until(
                    EC.presence_of_all_elements_located((By.XPATH, xpath)))
                logger.debug(f"Found {len(elements)} elements matching XPath")
                return elements
            else:
                logger.debug("Waiting for presence of single element")
                element = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, xpath)))
                logger.debug("Found single element matching XPath")
                return element

        except TimeoutException as e:
            logger.error(
                f"Timeout waiting for elements with XPath: '{xpath}', multiple={multiple}", exc_info=True)
            raise
        except Exception as e:
            logger.error(
                f"Unexpected error parsing elements with XPath: '{xpath}'", exc_info=True)
            raise

    def get_price(self, url: str, ignore_price_format: bool, open_page: bool = True) -> Union[float, str]:
        """
        Retrieve a product's price from a webpage.

        Navigates to the given URL (if open_page is True) and extracts the price using the XPath
        from `website_info.product_xpaths.PRICE`. Falls back to `PRICE_WITHOUT_SALE` if the
        initial attempt fails, with parsing behavior determined by `ignore_price_format`.

        Args:
            url (str): URL of the product webpage
            ignore_price_format (bool): If True, returns raw price string; if False, parses to float
            open_page (bool): If True, loads the webpage before extraction. Defaults to True

        Returns:
            Union[float, str]: Parsed price as float if ignore_price_format=False and parsing succeeds,
                            raw price string if ignore_price_format=True

        Raises:
            PriceNotFoundException: If price cannot be retrieved from either XPath
            WebDriverException: If browser interaction fails
            PriceIsNotNormalizedException: If price parsing fails and ignore_price_format=False
            TimeoutException: (via _parse_elements)
            StaleElementReferenceException: (via _parse_elements)
        """
        logger.debug(f"Getting price from URL: '{url}', open_page={open_page}, ignore_price_format={ignore_price_format}")

        if open_page:
            self.open_page(url)

        try:
            logger.debug(f"Attempting to parse price with XPath: {self.website_info.product_xpaths.PRICE}")
            price = self._parse_price(
                xpath=self.website_info.product_xpaths.PRICE,
                ignore_price_format=ignore_price_format
            )
            logger.debug(f"Successfully retrieved price")
            return price

        except PriceIsNotNormalizedException as e:
            logger.warning(
                f"Price normalization failed with primary XPath: {e}")
            raise

        except Exception as e:
            logger.warning(
                f"Failed to get price with {self.website_info.product_xpaths.PRICE}: {str(e)}. "
                f"Attempting fallback XPath for {self.website_info}",
                exc_info=True
            )

            try:
                logger.debug(f"Attempting fallback price with XPath: {self.website_info.product_xpaths.PRICE_WITHOUT_SALE}")
                price_without_sale = self._parse_price(
                    xpath=self.website_info.product_xpaths.PRICE_WITHOUT_SALE,
                    ignore_price_format=ignore_price_format
                )
                logger.debug(f"Successfully retrieved fallback price")
                return price_without_sale

            except Exception as e:
                error_msg = (
                    f"Failed to get price for {self.website_info} using "
                    f"PRICE_WITHOUT_SALE XPath: {self.website_info.product_xpaths.PRICE_WITHOUT_SALE}"
                )
                logger.error(error_msg, exc_info=True)
                raise PriceNotFoundException(error_msg) from e

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
            TimeoutException: (via _parse_elements)
            StaleElementReferenceException: (via _parse_elements)
        """
        if open_page:
            self.open_page(url)

        try:
            logger.debug(f"Parsing sale price with XPath: {self.website_info.product_xpaths.PRICE_ON_SALE}")
            price = self._parse_price(
                xpath=self.website_info.product_xpaths.PRICE_ON_SALE,
                ignore_price_format=ignore_price_format
            )
            logger.debug(f"Successfully retrieved sale price")
            return price

        except PriceIsNotNormalizedException as e:
            logger.warning(f"Sale price normalization failed")
            raise

        except (TimeoutException) as e:
            error_msg = (
                f"Failed to get sale price for {self.website_info} with "
                f"XPath: {self.website_info.product_xpaths.PRICE_ON_SALE}. "
                "Product may not be on sale"
            )
            logger.error(error_msg, exc_info=True)
            raise PriceNotFoundException(error_msg) from e

        except Exception as e:
            error_msg = (
                f"Unexpected failure getting sale price for {self.website_info} with "
                f"XPath: {self.website_info.product_xpaths.PRICE_ON_SALE}"
            )
            logger.error(error_msg, exc_info=True)
            raise PriceNotFoundException(error_msg) from e

    def get_availability(self, url: str, open_page: bool = True) -> bool:
        """
        Check product availability on a webpage.

        Navigates to the specified URL (if open_page is True) and checks availability using the XPath
        from `website_info.product_xpaths.AVAILABILITY`. Returns True if `AVAILABLE_TEXT` is found
        in the element's text, False otherwise.

        Args:
            url (str): URL of the webpage containing product availability info
            open_page (bool): If True, loads the webpage before checking. Defaults to True

        Returns:
            bool: True if product is available (AVAILABLE_TEXT in element text), False otherwise

        Raises:
            AvailabilityNotFoundException: If availability cannot be determined
            WebDriverException: If browser interaction fails
            TimeoutException: (via _parse_elements)
            StaleElementReferenceException: (via _parse_elements)
        """
        if open_page:
            self.open_page(url)
        try:
            logger.debug(
                f"Parsing availability with XPath: {self.website_info.product_xpaths.AVAILABILITY}")
            availability_element = self._parse_elements(
                xpath=self.website_info.product_xpaths.AVAILABILITY,
                multiple=False
            )
            availability_text = availability_element.text
            is_available = self.website_info.product_xpaths.AVAILABLE_TEXT in availability_text
            logger.debug(
                f"Availability text: '{availability_text}', available: {is_available}")
            return is_available

        except Exception as e:
            error_msg = (
                f"Failed to get availability for {self.website_info} with "
                f"XPath: {self.website_info.product_xpaths.AVAILABILITY} and "
                f"expected text: {self.website_info.product_xpaths.AVAILABLE_TEXT}"
            )
            logger.error(error_msg, exc_info=True)
            raise AvailabilityNotFoundException(error_msg) from e

    def get_price_details(self, url: str, ignore_price_format: bool, open_page: bool = True) -> Tuple[Optional[float], Optional[float], bool]:
        """
        Retrieve detailed pricing information for a product from a webpage.

        Fetches both regular and sale prices (if available) from the given URL, along with an availability flag.
        Opens the page once if open_page is True, then uses cached page state for price queries.

        Args:
            url (str): URL of the product webpage
            ignore_price_format (bool): If True, returns raw price strings; if False, parses to floats
            open_page (bool): If True, loads the webpage before extraction. Defaults to True

        Returns:
            Tuple[Optional[float], Optional[float], bool]: 
                - Regular price (float or str if ignore_price_format=True)
                - Sale price (float, str if ignore_price_format=True, or None if not on sale)
                - Boolean indicating if product is on sale (True if sale price exists)

        Raises:
            WebDriverException: If browser interaction fails during page opening
            PriceNotFoundException: If regular price cannot be retrieved
            TimeoutException: (via _parse_elements)
            StaleElementReferenceException: (via _parse_elements)

        """
        logger.debug(f"Getting price details for URL: '{url}', open_page={open_page}, ignore_price_format={ignore_price_format}")

        if open_page:
            self.open_page(url)

        # Get regular price
        try:
            logger.debug("Fetching regular price")
            price = self.get_price(
                url=url,
                ignore_price_format=ignore_price_format,
                open_page=False
            )
            logger.debug(f"Regular price retrieved")
        except Exception as e:
            logger.error(f"Failed to retrieve regular price for {url}", exc_info=True)
            raise

        # Get sale price (if available)
        price_on_sale = None
        try:
            logger.debug("Fetching sale price")
            price_on_sale = self.get_price_on_sale(
                url=url,
                ignore_price_format=ignore_price_format,
                open_page=False
            )
            logger.debug(f"Sale price retrieved")
        except Exception as e:
            logger.debug(f"No sale price found for {url}, assuming regular price applies")

        # Determine if product is on sale
        is_on_sale = price_on_sale is not None

        return price, price_on_sale, is_on_sale

    def get_title(self, url: str, open_page: bool = True) -> str:
        """
        Retrieve the product title from a webpage.

        Navigates to the specified URL (if open_page is True) and extracts the title using the XPath
        from `self.website_info.product_xpaths.TITLE`. Returns the text content of the title element.

        Args:
            url (str): URL of the webpage containing the product title
            open_page (bool): If True, loads the webpage before extraction. Defaults to True

        Returns:
            str: Text content of the title element

        Raises:
            TitleNotFoundException: If title cannot be retrieved
            WebDriverException: If browser interaction fails
            TimeoutException: (via _parse_elements)
            StaleElementReferenceException: (via _parse_elements)
        """
        if open_page:
            self.open_page(url)
        try:
            logger.debug(
                f"Parsing title with XPath: {self.website_info.product_xpaths.TITLE}")
            title_element = self._parse_elements(
                self.website_info.product_xpaths.TITLE)
            title_text = title_element.text or ""
            if not title_text:
                logger.warning("Title element found but contains no text")
            logger.debug(f"Title retrieved: '{title_text}'")
            return title_text

        except Exception as e:
            error_msg = (
                f"Failed to get title for {self.website_info} with "
                f"XPath: {self.website_info.product_xpaths.TITLE}"
            )
            logger.error(error_msg, exc_info=True)
            raise TitleNotFoundException(error_msg) from e

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
        """
        Navigate to a specified URL using the WebDriver, with timeout retry support.

        Ensures the URL belongs to the expected domain defined in `self.website_info.url` before
        attempting to load it. Only navigates if the current URL differs from the target.

        Args:
            url (str): URL to open in the WebDriver

        Returns:
            None

        Raises:
            InvalidPageException: If URL doesn't belong to the expected domain
            WebDriverException: If browser interaction fails (e.g., invalid URL, browser crash)
            TimeoutException: If page fails to load within timeout (handled by retry decorator)
        """
        logger.debug(f"Attempting to open page: '{url}'")
        expected_domain = urlparse(self.website_info.url).netloc
        actual_domain = urlparse(url).netloc
        if not expected_domain or expected_domain not in actual_domain:
            error_msg = f"URL '{url}' domain '{actual_domain}' doesn't match expected '{expected_domain}'"
            logger.error(error_msg)
            raise InvalidPageException(error_msg)

        # Navigate to URL if different from current
        try:
            current_url = self.driver.current_url
            if current_url != url:
                logger.debug(f"Navigating from '{current_url}' to '{url}'")
                self.driver.get(url)
                # Wait for page to be fully loaded
                self.wait.until(
                    lambda driver: driver.execute_script(
                        "return document.readyState") == "complete"
                )
                logger.debug(f"Successfully loaded page: '{url}'")
            else:
                logger.debug(f"Already on page: '{url}'")

        except TimeoutException as e:
            error_msg = f"Timeout while loading page: '{url}'"
            logger.error(error_msg, exc_info=True)
            raise  # Handled by retry decorator

        except WebDriverException as e:
            error_msg = f"WebDriver error while loading page: '{url}'"
            logger.error(error_msg, exc_info=True)
            raise WebDriverException(error_msg) from e

        except Exception as e:
            error_msg = f"Unexpected error while loading page: '{url}'"
            logger.error(error_msg, exc_info=True)
            raise type(e)(error_msg) from e

    def _close(self) -> None:
        """
        Close the WebDriver session and release associated resources.

        Attempts to terminate the WebDriver instance gracefully. Logs the process and any errors encountered.
        Handles cases where the driver is already closed or not initialized.

        Returns:
            None

        Raises:
            WebDriverException: If quitting the WebDriver fails due to a browser-specific issue
            Exception: For unexpected errors during closure
        """
        logger.debug("Attempting to close WebDriver session")

        try:
            self.driver.quit()
            logger.debug("WebDriver session closed successfully")

        except WebDriverException as e:
            error_msg = "Failed to quit WebDriver due to WebDriver-specific issue"
            logger.error(error_msg, exc_info=True)
            try:
                self.driver.close()
                logger.debug("Fallback: Closed browser window")
            except Exception:
                logger.warning("Fallback close also failed")
            raise WebDriverException(error_msg) from e

        except Exception as e:
            error_msg = "Unexpected error while closing WebDriver"
            logger.error(error_msg, exc_info=True)
            raise e

    def __del__(self):
        self._close()

    def info_about_product(self, url: str, fast_parse: bool = True, ignore_price_format: bool = False,
                           raise_exception: bool = False) -> ProductInfo:
        """
        Gather comprehensive product information from a webpage.

        Opens the specified URL and collects product details (price, sale status, availability, title)
        based on the parsing mode. Fast mode retrieves only the regular price, while full mode
        includes sale price and availability.

        Args:
            url (str): URL of the product webpage
            fast_parse (bool): If True, retrieves only regular price; if False, gets full details. Defaults to True
            ignore_price_format (bool): If True, returns raw price strings; if False, parses to floats. Defaults to False
            raise_exception (bool): If True, raises exceptions on failure; if False, returns partial data. Defaults to False

        Returns:
            ProductInfo: Object containing product details (url, price, is_on_sale, price_on_sale, is_available, title)

        Raises:
            WebDriverException: If page opening fails
            PriceNotFoundException: If price retrieval fails and raise_exception=True
            AvailabilityNotFoundException: If availability check fails and raise_exception=True
            TitleNotFoundException: If title retrieval fails and raise_exception=True
        """
        logger.debug(f"Gathering product info for URL: '{url}', fast_parse={fast_parse}, "
                     f"ignore_price_format={ignore_price_format}, raise_exception={raise_exception}")

        self.open_page(url)

        price = None
        is_on_sale = None
        price_on_sale = None
        is_available = None
        title = None

        if fast_parse:
            try:
                logger.debug("Fetching regular price (fast mode)")
                price = self.get_price(
                    url=url, ignore_price_format=ignore_price_format, open_page=False
                )
                logger.debug(f"Regular price retrieved")
            except PriceNotFoundException as e:
                logger.warning(f"Price not found in fast mode")
                if raise_exception:
                    raise
        else:
            try:
                logger.debug("Fetching full price details")
                price, price_on_sale, is_on_sale = self.get_price_details(
                    url=url, ignore_price_format=ignore_price_format, open_page=False
                )
            except PriceNotFoundException as e:
                logger.warning(f"Price details not found")
                if raise_exception:
                    raise

            try:
                logger.debug("Fetching availability")
                is_available = self.get_availability(url=url, open_page=False)
                logger.debug(f"Availability retrieved: {is_available}")
            except AvailabilityNotFoundException as e:
                logger.warning(f"Availability not found: {e}")
                if raise_exception:
                    raise

        try:
            logger.debug("Fetching title")
            title = self.get_title(url=url, open_page=False)
            logger.debug(f"Title retrieved: '{title}'")
        except TitleNotFoundException as e:
            logger.warning(f"Title not found: {e}")
            if raise_exception:
                raise

        product_info = ProductInfo(url, price, is_on_sale, price_on_sale, is_available, title)
        return product_info

    @retry_on_stale_element()
    @retry_on_timeout()
    def _send_keys(self, xpath: str, keys: Union[str, Keys]) -> None:
        """
        Send keys to an element identified by XPath with retry support.

        Locates an element using the provided XPath and sends the specified keys to it.
        Retries on TimeoutException and StaleElementReferenceException are handled by decorators.

        Args:
            xpath (str): XPath expression to locate the target element
            keys (Union[str, Keys]): Keys to send to the element (string or Selenium Keys object)

        Returns:
            None

        Raises:
            UnableToSendKeysException: If keys cannot be sent to the element (e.g., not interactable)
            TimeoutException: If element isn't found within timeout (after retries)
            StaleElementReferenceException: If element becomes stale (after retries)
        """
        logger.debug(
            # f"Sending keys to element with XPath: '{xpath}', keys: '{str(keys)}'")
            f"Sending keys to element with XPath: '{xpath}''")

        try:
            logger.debug(f"Locating element with XPath: '{xpath}'")
            element = self._parse_elements(xpath=xpath, multiple=False)
            logger.debug("Element located, sending keys")
            element.send_keys(keys)
            # logger.debug(f"Keys '{str(keys)}' sent successfully to element")

        except (TimeoutException, StaleElementReferenceException) as e:
            error_msg = f"Failed to send keys to element with XPath '{xpath}' due to timeout or staleness"
            logger.error(error_msg, exc_info=True)
            raise

        except Exception as e:
            # error_msg = f"Failed to send keys '{str(keys)}' to element with XPath '{xpath}'"
            error_msg = f"Failed to send keys to element with XPath '{xpath}'"
            logger.error(error_msg, exc_info=True)
            raise UnableToSendKeysException(error_msg) from e

    @retry_on_stale_element()
    @retry_on_timeout()
    def _press_button(self, xpath: str) -> None:
        """
        Click a button identified by XPath with retry support.

        Locates a button element using the provided XPath and attempts to click it.
        Retries on TimeoutException and StaleElementReferenceException are handled by decorators.

        Args:
            xpath (str): XPath expression to locate the button element

        Returns:
            None

        Raises:
            UnableToPressButtonException: If the button cannot be clicked (e.g., not interactable)
            TimeoutException: If button isn't found within timeout (after retries)
            StaleElementReferenceException: If button becomes stale (after retries)
        """
        logger.debug(f"Attempting to press button with XPath: '{xpath}'")

        try:
            logger.debug(f"Locating button with XPath: '{xpath}'")
            button = self._parse_elements(xpath=xpath, multiple=False)
            logger.debug("Button located, attempting to click")
            button.click()
            logger.debug(f"Button with XPath '{xpath}' clicked successfully")

        except (TimeoutException, StaleElementReferenceException) as e:
            error_msg = f"Failed to click button with XPath '{xpath}' due to timeout or staleness"
            logger.error(error_msg, exc_info=True)
            raise  # Handled by retry decorators

        except Exception as e:
            error_msg = f"Failed to click button with XPath '{xpath}'"
            logger.error(error_msg, exc_info=True)
            raise UnableToPressButtonException(error_msg) from e

    @retry_on_stale_element()
    @retry_on_timeout()
    def _open_search_results(self, product: str) -> None:
        """
        Open search results page for a given product on the website.

        Navigates to the base website URL, enters the product name in the search field,
        and submits the search either by pressing Enter or clicking the submit button.

        Args:
            product (str): Product name to search for

        Returns:
            None

        Raises:
            UnableToOpenSearchResultsException: If any step (page load, search field input, or submission) fails
        """
        logger.debug(f"Opening search results for product: '{product}'")

        try:
            logger.debug(f"Navigating to base URL: '{self.website_info.url}'")
            self.open_page(self.website_info.url)
            logger.debug("Base page opened successfully")
        except Exception as e:
            error_msg = f"Unable to open website using '{self.website_info.url}'"
            logger.error(error_msg, exc_info=True)
            raise UnableToOpenSearchResultsException(error_msg) from e

        try:
            logger.debug(
                f"Entering product name into search field with XPath: '{self.website_info.website_navigation.SEARCH_FIELD}'")
            self._send_keys(
                self.website_info.website_navigation.SEARCH_FIELD, product)
            logger.debug(f"Product name '{product}' entered successfully")
        except Exception as e:
            error_msg = f"Search field not found with XPath '{self.website_info.website_navigation.SEARCH_FIELD}'"
            logger.error(error_msg, exc_info=True)
            raise UnableToOpenSearchResultsException(error_msg) from e

        try:
            logger.debug("Submitting search with Enter key")
            self._send_keys(
                self.website_info.website_navigation.SEARCH_FIELD, Keys.ENTER)
            logger.debug("Search submitted successfully with Enter key")
        except Exception as e:
            logger.warning(
                f"Failed to submit search with Enter key: {str(e)}. Attempting submit button.")
            try:
                logger.debug(
                    f"Clicking submit button with XPath: '{self.website_info.website_navigation.SUBMIT_BUTTON}'")
                self._press_button(
                    self.website_info.website_navigation.SUBMIT_BUTTON)
                logger.debug("Search submitted successfully with button")
            except Exception as e:
                error_msg = (
                    f"Unable to submit search using Enter key or button with "
                    f"XPath '{self.website_info.website_navigation.SUBMIT_BUTTON}'"
                )
                logger.error(error_msg, exc_info=True)
                raise UnableToOpenSearchResultsException(error_msg) from e

    @retry_on_timeout()
    @retry_on_stale_element()
    def _search_results_get_products_urls(self, n: int) -> List[str]:
        """
        Retrieve URLs of the first n products from search results.

        Extracts product URLs from elements identified by the XPath template in
        `website_info.website_navigation.SEARCH_RESULT_PRODUCTS_XPATH_TEMPLATES`.
        Uses the specified link attribute to get each URL.

        Args:
            n (int): Number of product URLs to retrieve

        Returns:
            List[str]: List of up to n product URLs found in search results

        Raises:
            UnableToGetNProductUrls: If product URLs cannot be retrieved
            TimeoutException: If elements aren't found within timeout (after retries)
            StaleElementReferenceException: If elements become stale (after retries)
        """
        logger.debug(f"Retrieving up to {n} product URLs from search results")

        product_urls = []
        try:
            logger.debug(
                f"Parsing product URL elements with XPath: '{self.website_info.website_navigation.SEARCH_RESULT_PRODUCTS_XPATH_TEMPLATES}'")
            product_url_elements = self._parse_elements(
                xpath=self.website_info.website_navigation.SEARCH_RESULT_PRODUCTS_XPATH_TEMPLATES,
                multiple=True
            )[:n]
            logger.debug(
                f"Found {len(product_url_elements)} product URL elements (limited to {n})")

            for url_element in product_url_elements:
                attribute = self.website_info.website_navigation.SEARCH_RESULT_LINK_ATTRIBUTE
                product_url = url_element.get_attribute(attribute)
                if product_url:
                    product_urls.append(product_url)
                    logger.debug(
                        f"Extracted URL: '{product_url}' using attribute '{attribute}'")
                else:
                    logger.warning(
                        f"No URL found for element using attribute '{attribute}'")

        except (StaleElementReferenceException, TimeoutException) as e:
            error_msg = (
                f"Failed to get product URLs for {self.website_info} using XPath "
                f"'{self.website_info.website_navigation.SEARCH_RESULT_PRODUCTS_XPATH_TEMPLATES}' "
                "due to timeout or staleness"
            )
            logger.error(error_msg, exc_info=True)
            raise

        except Exception as e:
            error_msg = (
                f"Unable to get {n} product URLs for {self.website_info} using XPath "
                f"'{self.website_info.website_navigation.SEARCH_RESULT_PRODUCTS_XPATH_TEMPLATES}'"
            )
            logger.error(error_msg, exc_info=True)
            raise UnableToGetNProductUrls(error_msg) from e

        logger.debug(
            f"Retrieved {len(product_urls)} product URLs: {product_urls}")
        return product_urls

    def _get_product_urls(self, product: str, n: int) -> List[str]:
        try:
            logger.debug(f"Opening search results for '{product}'")
            self._open_search_results(product)
            logger.debug("Search results opened successfully")
        except Exception as e:
            logger.error(
                f"Failed to open search results for '{product}'", exc_info=True)
            raise

        try:
            logger.debug(f"Retrieving {n} product URLs")
            product_urls = self._search_results_get_products_urls(n)
            logger.debug(
                f"Retrieved {len(product_urls)} product URLs: {product_urls}")
        except Exception as e:
            logger.error(
                f"Failed to retrieve product URLs for '{product}'", exc_info=True)
            raise

        return product_urls

    def _find_n_products(self, product: str, n: int, fast_parse: bool = True, ignore_price_format: bool = True,
                         raise_exception: bool = False) -> List[ProductInfo]:
        """
        Search for and retrieve information on up to `n` products.

        Performs a search for the given product name, retrieves URLs for up to `n` products from the
        search results, and collects detailed information for each. If fewer than `n` products are
        found or parsed, logs a warning and raises an exception if `raise_exception` is True.

        Args:
            product (str): Product name to search for
            n (int): Maximum number of products to retrieve
            fast_parse (bool): If True, retrieves only price (faster); if False, gets full details. Defaults to True
            ignore_price_format (bool): If True, returns raw price strings; if False, parses to floats. Defaults to True
            raise_exception (bool): If True, raises exceptions on failure; if False, returns partial results. Defaults to False

        Returns:
            List[ProductInfo]: List of ProductInfo objects for found products (may be fewer than n)

        Raises:
            UnableToGetNProductUrls: If fewer than `n` products are found and raise_exception is True
            UnableToOpenSearchResultsException: If search results cannot be opened
            Exception: If product info parsing fails and raise_exception is True
        """
        for i in range(3):
            product_urls = self._get_product_urls(product=product, n=n)
            if len(product_urls) == 0:
                warning_msg = f"No product URLs found for '{product}'"
                logger.warning(warning_msg)
            else:
                break

        products = []
        for product_url in product_urls:
            try:
                logger.debug(f"Parsing product info for URL: '{product_url}'")
                product_info = self.info_about_product(
                    product_url,
                    fast_parse=fast_parse,
                    ignore_price_format=ignore_price_format,
                    raise_exception=raise_exception
                )
                products.append(product_info)
                logger.debug(f"Product info parsed")
            except Exception as e:
                error_msg = f"Failed to parse product info for '{product_url}'"
                logger.error(error_msg, exc_info=True)
                if raise_exception:
                    raise

        if len(products) < n:
            warning_msg = f"Only {len(products)} products found for '{product}', expected {n}"
            logger.warning(warning_msg)
            if raise_exception:
                raise UnableToGetNProductUrls(warning_msg)

        logger.debug(f"Returning {len(products)} products")
        return products

    def find_n_products(self, product: str, n: int, fast_parse: bool = True, ignore_price_format: bool = True,
                        raise_exception: bool = False) -> List[ProductInfo]:
        """
        Abstract method to find and retrieve information on up to `n` products.

        This method must be implemented by subclasses to search for a product and return a list of
        ProductInfo objects. It defines the interface for product search functionality, with options
        for parsing speed, price formatting, and exception handling.

        Args:
            product (str): Product name to search for
            n (int): Maximum number of products to retrieve
            fast_parse (bool): If True, performs faster parsing (e.g., price only). Defaults to True
            ignore_price_format (bool): If True, returns raw price strings instead of normalized floats. Defaults to True
            raise_exception (bool): If True, raises exceptions on failure; if False, may return partial results. Defaults to False

        Returns:
            List[ProductInfo]: List of ProductInfo objects containing product details (in subclasses)

        Raises:
            NotImplementedError: Always raised in this base implementation, as it must be overridden
        """
        logger.debug(f"Called abstract method find_n_products with product='{product}', n={n}, "
                     f"fast_parse={fast_parse}, ignore_price_format={ignore_price_format}, "
                     f"raise_exception={raise_exception}")
        raise NotImplementedError("Subclasses must implement find_n_products")
