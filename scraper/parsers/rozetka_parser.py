from scraper.parsers.base_parser import BaseParser
import re

ROZETKA_URL = 'https://rozetka.com.ua/ua'
ROZETKA_PRICE_ON_SALE_XPATH = '//*[@id="#scrollArea"]/div[1]/div[2]/div/rz-product-main-info/div/div[2]/div/div[1]/p[2]'
ROZETKA_PRICE_WITHOUT_SALE_XPATH = '//*[@id="#scrollArea"]/div[1]/div[2]/div/rz-product-main-info/div/div[2]/div/div[1]/p[1]'
ROZETKA_PRICE_XPATH = '//*[@id="#scrollArea"]/div[1]/div[2]/div/rz-product-main-info/div/div[2]/div/div[1]/p'
# ROZETKA_PRICE_WITHOUT_SALE vs ROZETKA_PRICE:
# some products on rozetka are on sales, in such case ROZETKA_PRICE_WITHOUT_SALE is the price without sale for product which is on sale
# ROZETKA_PRICE is price of product which is not on sale
ROZETKA_INFO_ABOUT_AVAILABILITY_XPATH = '//*[@id="#scrollArea"]/div[1]/div[2]/div/rz-product-main-info/div/div[2]/div/div[1]/rz-status-label/p'
ROZETKA_IS_AVAILABLE_MESSAGE = 'Є в наявності'
ROZETKA_IS_NOT_AVAILABLE_MESSAGE = 'Немає в наявності'
ROZETKA_TITLE_XPATH = '//*[@id="#scrollArea"]/div[1]/div[2]/div/rz-title-block/div/div[1]/div/h1'


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
        data = { 'url' : url, 'price' : price, 'price_on_sale' : price_on_sale, 'is_available' : is_available, 'title': title }'''
        self.open_page(url)

        data = {
            'url': url,
            'price': None,
            'price_on_sale': None,
            'is_available': False,
            'title': None,
        }

        # if product is on sale
        try:
            d = self._parse_price_and_sale_price(ROZETKA_PRICE_ON_SALE_XPATH, ROZETKA_PRICE_WITHOUT_SALE_XPATH)
            data['price'] = self.parse_price(d['price_element'].text)
            data['price_on_sale'] = self.parse_price(d['price_on_sale_element'].text)
        except Exception as e: 
            # if product is not on sale
            try:
                price_element = self._parse_price(ROZETKA_PRICE_XPATH)
                data['price'] = self.parse_price(price_element.text)
            except Exception as e:
                print('Unable to get price')
        
        # if product is available
        try:
            data['is_available'] = self._parse_availability(ROZETKA_INFO_ABOUT_AVAILABILITY_XPATH, 
                                                            lambda info: info.text == ROZETKA_IS_AVAILABLE_MESSAGE)
        except Exception as e:
            print('Unable to get info about availability')
        
        # trying to get title
        try:
            title_element = self._parse_title(ROZETKA_TITLE_XPATH)
            data['title'] = title_element.text
        except Exception as e:
            print('Unable to get title')

        return data
