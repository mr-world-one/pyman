from scraper.parsers.base_parser import BaseParser
from scraper.parsers.website_info import WebsiteInfo
from scraper.parsers.xpaths import ProductXpaths, WebsiteNavigationXPaths
import re

class SilpoParser(BaseParser):

    def __init__(self):
        super().__init__(
            WebsiteInfo(
                url = 'https://silpo.ua',
                price_format=r'\d+',
                product_xpaths=ProductXpaths(price_on_sale='/html/body/sf-shop-silpo-root/shop-silpo-root-shell/silpo-shell-main/div/div[3]/silpo-product-product-page/div/div/div/div/div[2]/div/div/div[1]/div[1]', 
                                price_without_sale='/html/body/sf-shop-silpo-root/shop-silpo-root-shell/silpo-shell-main/div/div[3]/silpo-product-product-page/div/div/div/div/div[2]/div/div/div[1]/div[2]/div[1]', 
                                price='/html/body/sf-shop-silpo-root/shop-silpo-root-shell/silpo-shell-main/div/div[3]/silpo-product-product-page/div/div/div/div/div[2]/div/div/div[1]/div', 
                                availability='/html/body/sf-shop-silpo-root/shop-silpo-root-shell/silpo-shell-main/div/div[3]/silpo-product-product-page/div/div/div/div/div[2]/div/div/div[2]/shop-silpo-common-page-add-to-basket/div/div/button', 
                                title='/html/body/sf-shop-silpo-root/shop-silpo-root-shell/silpo-shell-main/div/div[3]/silpo-product-product-page/div/div/div/div/div[2]/div/h1', 
                                available_text='У кошик', 
                ),
                website_navigation=WebsiteNavigationXPaths(search_field='/html/body/sf-shop-silpo-root/shop-silpo-root-shell/silpo-shell-main/div/div[1]/silpo-shell-header/silpo-shell-desktop-header/div/div/div[1]/div[3]/silpo-search-suggestion/silpo-search-input/div/input',
                                submit_button=None,
                                search_result_products_xpath_templates='//shop-silpo-common-product-card/div/a',
                                search_result_link_attribute='href',
                )
    ))
        
    def info_about_product(self, url, fast_parse=True, raise_exception=False, ignore_price_format=True):
        data = super().info_about_product(url=url, fast_parse=fast_parse, raise_exception=raise_exception, ignore_price_format=ignore_price_format)
        if data.price_on_sale == data.price:
            data.price_on_sale = None
            data.is_on_sale = False
        return data
    
    def find_n_products(self, product, n, fast_parse=True, raise_exception=False, ignore_price_format=True):
        return super()._find_n_products(product, n, fast_parse=fast_parse, raise_exception=raise_exception, ignore_price_format=ignore_price_format)
    