from scraper.parsers.base_parser import BaseParser
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import re

SILPO_URL = 'https://silpo.ua/'
SILPO_PRICE_ON_SALE_XPATH = '/html/body/sf-shop-silpo-root/shop-silpo-root-shell/silpo-shell-main/div/div[3]/silpo-product-product-page/div/div/div/div[2]/div/div[1]/div[1]'
SILPO_PRICE_WITHOUT_SALE_XPATH = '/html/body/sf-shop-silpo-root/shop-silpo-root-shell/silpo-shell-main/div/div[3]/silpo-product-product-page/div/div/div/div[2]/div/div[1]/div[2]/div[1]'
SILPO_PRICE_XPATH = '/html/body/sf-shop-silpo-root/shop-silpo-root-shell/silpo-shell-main/div/div[3]/silpo-product-product-page/div/div/div/div[2]/div/div[1]/div[1]'
SILPO_INFO_ABOUT_AVAILABILITY_XPATH = '/html/body/sf-shop-silpo-root/shop-silpo-root-shell/silpo-shell-main/div/div[3]/silpo-product-product-page/div/div/div/div[2]/div/div[2]/shop-silpo-common-page-add-to-basket/div/div/button'
SILPO_IS_NOT_AVAILABLE_MESSAGE = 'Товар закінчився'
SILPO_IS_AVAILABLE_MESSAGE = 'У кошик'
SILPO_TITLE_XPATH = '/html/body/sf-shop-silpo-root/shop-silpo-root-shell/silpo-shell-main/div/div[3]/silpo-product-product-page/div/div/div/div[2]/h1'

class SilpoParser(BaseParser):
    def init(self):
        super().__init__()
    
    def info(self, url):
        '''method returns a dictionary is the following format:
        data = {
            'url': url,
            'price': None,
            'price_on_sale': None,
            'is_available': False,
            'title': None,
        }
        '''

        self.driver.get(url)

        data = {
            'url': url,
            'price': None,
            'price_on_sale': None,
            'is_available': False,
            'title': None,
        }

        # if on sale
        try:
            d = self._parse_price_and_sale_price(SILPO_PRICE_ON_SALE_XPATH, SILPO_PRICE_WITHOUT_SALE_XPATH)
            data['price_on_sale'] = d['price_on_sale_element'].text
            data['price'] = d['price_element'].text
        except Exception as e:
            # product is not on sale
            try:
                price_element = self._parse_price(SILPO_PRICE_XPATH)
                data['price'] = price_element.text
            except Exception as e:
                print('Unable to parse price')
        
        # if is available
        try:
            data['is_available'] = self._parse_availability(SILPO_INFO_ABOUT_AVAILABILITY_XPATH,
                                                            lambda info: SILPO_IS_AVAILABLE_MESSAGE in info.text)
        except:
            pass

        # title
        try:
            title_element = self._parse_title(SILPO_TITLE_XPATH)
            data['title'] = title_element.text
        except:
            pass
        return data