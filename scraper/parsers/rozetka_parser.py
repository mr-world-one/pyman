from scraper.parsers import Website, ProductXpaths, NavigationXPaths, logger
from scraper.parsers.base_parser import BaseParser
from scraper.parsers.exceptions import UnableToGetNProductUrls

class RozetkaParser(BaseParser):

    def __init__(self):
        website_info = self._create_default_website()

        super().__init__(website_info)

    def _create_default_website(self):
        return Website(
            url='https://rozetka.com.ua/ua/',
            price_format=r'\d+',
            product_xpaths=ProductXpaths(
                price_on_sale='//*[@id="#scrollArea"]/div[1]/div[2]/div/rz-product-main-info/div/div[2]/div/div[1]/p[2]',
                price_without_sale='//*[@id="#scrollArea"]/div[1]/div[2]/div/rz-product-main-info/div/div[2]/div/div[1]/p[1]',
                price='//*[@id="#scrollArea"]/div[1]/div[2]/div/rz-product-main-info/div/div[2]/div/div[1]/p',
                availability='//*[@id="#scrollArea"]/div[1]/div[2]/div/rz-product-main-info/div/div[2]/div/div[1]/rz-status-label/p',
                title='//*[@id="#scrollArea"]/div[1]/div[2]/div/rz-title-block/div/div[1]/div/h1',
                available_text='Є в наявності'),
            website_navigation=NavigationXPaths(
                search_field='/html/body/rz-app-root/div/div[1]/rz-main-header/header/div/div/div/rz-search-suggest/form/div[1]/div/div/input',
                submit_button='/html/body/rz-app-root/div/div[1]/rz-main-header/header/div/div/div/rz-search-suggest/form/div[1]/button',
                search_result_products_xpath_templates="""/html/body/rz-app-root/div/div[1]/rz-category/div/main/rz-catalog-layout/div[2]/section/rz-category-goods//rz-product-tile/div/a[2] | /html/body/rz-app-root/div/div[1]/rz-search/rz-catalog/div/div[2]/section//rz-button-product-page[2]/rz-indexed-link/a""",                    
                search_result_link_attribute='href'))

    def find_n_products(self, product, n, fast_parse=True, raise_exception=False, ignore_price_format=True):
        result = []
        try:
            result = super()._find_n_products(product, n, fast_parse=fast_parse, raise_exception=raise_exception,ignore_price_format=ignore_price_format)
            logger.info(f'Managed to parse {len(result)} products')

        except Exception as e:
            if raise_exception or len(result) == 0:
                raise UnableToGetNProductUrls(
                    f'Unable to find products ({len(result)} found)') from e

        return result
