from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from scraper.utils.config import SELENIUM_OPTIONS, EXCPLICIT_TIMEOUT, IMPLICIT_TIMEOUT
from scraper.parsers.xpaths import BaseXPaths

class BaseParser:
    def __init__(self):
        self.options = Options()
        for option in SELENIUM_OPTIONS:
            self.options.add_argument(option)
        
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)
        self.driver.implicitly_wait(IMPLICIT_TIMEOUT)
        
        self.wait = WebDriverWait(self.driver, EXCPLICIT_TIMEOUT)

    def normalize_price(*args):
        raise NotImplementedError()

    def parse_element(self, xpath, multiple = False):
        try:
            elements = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
            return elements if multiple else elements[0]
        except:
            return [] if multiple else None
    
    def parse_price(self, xpath): 
        price_element = self.parse_element(xpath)
        return self.normalize_price(price_element.text) if price_element else None
    
    def parse_availability(self, xpath, available_text):
        element = self.parse_element(xpath)
        return available_text in element.text if element else False

    def open_page(self, url):
        try:
            self.driver.get(url)
        except:
            print('Unable to open page')

    def close(self):
        self.driver.quit()

    def __del__(self):
        try:
            self.driver.quit()
        except Exception as e:
            print(e)

    def info(self, url, xpaths : BaseXPaths):
        self.open_page(url)
        price_without_sale = self.parse_price(xpaths.PRICE_WITHOUT_SALE)
        price = price_without_sale if price_without_sale else self.parse_price(xpaths.PRICE)
        return {
            'url': url,
            'price': price,
            'price_on_sale': self.parse_price(xpaths.PRICE_ON_SALE),
            'is_available': self.parse_availability(xpaths.AVAILABILITY, xpaths.AVAILABLE_TEXT),
            'title': self.parse_element(xpaths.TITLE).text,
        }