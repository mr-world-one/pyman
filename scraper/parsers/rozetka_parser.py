from scraper.parsers.base_parser import BaseParser
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re

class RozetkaParser(BaseParser):
    def __init__(self):
        super().__init__()

    @staticmethod
    def parse_price(price):
        # rozetka provides price in the following format: ***$
        match = re.search(r'\d+', price)
        return int(match.group()) if match else None

    def info(self, url):
        '''returns information about specific product 
        format of data:
        data = { 'url' : url, 'price' : price, 'sale_price' : sale_price, 'is_available' : is_available, 'title': title }'''
        self.open_page(url)

        data = {
            'url': url,
            'price': None,
            'sale_price': None,
            'is_available': False,
            'title': None,
        }

        # if product is on sale
        try:
            sale_price_element = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'product-price__big.product-price__big-color-red')))
            price_element = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'product-price__small.ng-star-inserted')))
            data['sale_price'] = RozetkaParser.parse_price(sale_price_element.text)
            data['price'] = RozetkaParser.parse_price(price_element.text)
        except: 
            # if product is not on sale
            print('Product is not on sale')
            try:
                price_element = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'product-price__big')))
                data['price'] = RozetkaParser.parse_price(price_element.text)
            except:
                print('Unable to get price')
        
        # if product is available
        try:
            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'status-label.status-label--green.ng-star-inserted')))
            data['is_available'] = True
        except:
            # product is not available that's OK
            pass
        
        # trying to get title
        try:
            title_element = self.wait.until(EC.presence_of_element_located((By.XPATH, '/html[1]/body[1]/rz-app-root[1]/div[1]/div[1]/rz-product[1]/div[1]/rz-product-tab-main[1]/div[1]/div[1]/div[2]/div[1]/rz-title-block[1]/div[1]/div[1]/div[1]/h1[1]')))
            data['title'] = title_element.text
        except Exception as e:
            print('Unable to get title')
            print(e)

        return data
