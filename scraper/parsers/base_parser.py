from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from scraper.utils.config import SELENIUM_OPTIONS, EXCPLICIT_TIMEOUT, IMPLICIT_TIMEOUT

class BaseParser:
    def __init__(self):
        self.options = Options()
        for option in SELENIUM_OPTIONS:
            self.options.add_argument(option)
        
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)
        self.driver.implicitly_wait(IMPLICIT_TIMEOUT)
        
        self.wait = WebDriverWait(self.driver, EXCPLICIT_TIMEOUT)

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