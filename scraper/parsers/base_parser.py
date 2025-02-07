from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from scraper.utils.config import SELENIUM_OPTIONS, EXCPLICIT_TIMEOUT, IMPLICIT_TIMEOUT

class BaseParser:
    def __init__(self):
        self.options = Options()
        for option in SELENIUM_OPTIONS:
            self.options.add_argument(option)
        
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)
        self.driver.implicitly_wait(IMPLICIT_TIMEOUT)
        
        self.wait = WebDriverWait(self.driver, EXCPLICIT_TIMEOUT)

    def _parse_price_and_sale_price(self, price_on_sale_XPATH, price_without_sale_XPATH):
        price_on_sale_element = self.wait.until(EC.presence_of_element_located((By.XPATH, price_on_sale_XPATH)))
        price_element = self.wait.until(EC.presence_of_element_located((By.XPATH, price_without_sale_XPATH)))
        return { 'price_element' : price_element, 'price_on_sale_element' : price_on_sale_element }
    
    def _parse_price(self, price_XPATH): 
        price_element = self.wait.until(EC.presence_of_element_located((By.XPATH, price_XPATH)))
        return price_element
    
    def _parse_title(self, title_XPATH):
        title_element = self.wait.until(EC.presence_of_element_located((By.XPATH, title_XPATH)))
        return title_element
    
    def _parse_availability(self, info_about_availability_XPATH, predicate):
        is_available = self.wait.until(EC.presence_of_element_located((By.XPATH, info_about_availability_XPATH)))
        response = False
        if predicate(is_available):
            response = True
        return response

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

    def info(self, url):
        raise NotImplementedError()