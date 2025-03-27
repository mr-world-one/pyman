from scraper.parsers.base_parser import BaseParser
from scraper.parsers.website_info import WebsiteInfo
from scraper.parsers.xpaths import ProductXpaths, WebsiteNavigationXPaths
from scraper.parsers.base_parser import PriceIsNotNormalizedException, logger, PriceNotFoundException
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
        
    def get_price(self, url, ignore_price_format, open_page = True):
        if open_page:
            self.open_page(url)

        try:
            return self._parse_price(xpath=self.website_info.product_xpaths.PRICE_WITHOUT_SALE, ignore_price_format=ignore_price_format)
        except PriceIsNotNormalizedException:
            raise
        except Exception:
            message = f"{self.website_info}: Couldn't get price with {self.website_info.product_xpaths.PRICE}, maybe product is not on sale."
            logger.error(message)
            try:
                return self._parse_price(xpath=self.website_info.product_xpaths.PRICE, ignore_price_format=ignore_price_format)
            except Exception as e:
                message = f"{self.website_info}: Couldn't get price with {self.website_info.product_xpaths.PRICE_WITHOUT_SALE}, unknown reason"
                logger.exception(message)
                raise PriceNotFoundException from e
            
    def get_price_on_sale(self, url, ignore_price_format, open_page = True):
        if open_page:
            self.open_page(url)

        try:
            price_on_sale = self._parse_price(xpath=self.website_info.product_xpaths.PRICE_ON_SALE, ignore_price_format=ignore_price_format)
            if self.get_price(url=url, ignore_price_format=ignore_price_format, open_page=False) == price_on_sale:
                raise PriceNotFoundException
            return price_on_sale
        except PriceIsNotNormalizedException:
            raise
        except Exception as e:
            message = f'{self.website_info}: Unable to get price on sale with {self.website_info.product_xpaths.PRICE_ON_SALE}, maybe product is not on sale.'
            logger.exception(message)
            raise PriceNotFoundException from e
    
    def find_n_products(self, product, n, fast_parse=True, raise_exception=False, ignore_price_format=True):
        return super()._find_n_products(product, n, fast_parse=fast_parse, raise_exception=raise_exception, ignore_price_format=ignore_price_format)
    