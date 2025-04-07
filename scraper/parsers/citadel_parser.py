from scraper.parsers.base_parser import BaseParser, logger, PriceIsNotNormalizedException, PriceNotFoundException
from scraper.parsers.website import Website, ProductXpaths, NavigationXPaths
from scraper.utils.database import Database

class CitadelParser(BaseParser):
    def __init__(self):
        self.db = Database()
        
        website_info = self.db.get_website_info('https://citadelbuddekor.com.ua/')
        
        if not website_info:
            print("Дані для Epicentr не знайдено в базі, додаємо...")
            website_info = self._create_default_website()
            self.db.add_website(website_info)
        
        super().__init__(website_info)

    def _create_default_website(self):
        return Website(
            url='https://citadelbuddekor.com.ua/',
            price_format=r'\d+',
            product_xpaths=ProductXpaths(
                price_on_sale='//*[@id="content"]/div/div[1]/div[2]/div[2]/div/div[1]',
                price_without_sale='//*[@id="content"]/div/div[1]/div[2]/div[2]/div/div[2]',
                price='//*[@id="content"]/div/div[1]/div[2]/div[2]/div/div[1]',
                availability='//*[@id="content"]/div/div[1]/div[2]/div[2]/ul/li[3]/span',
                title='//*[@id="product-product"]/main/div[1]/div/h1',
                available_text='В наявності',
            ),
            website_navigation=NavigationXPaths(
                search_field='//*[@id="input_search"]',
                submit_button='//*[@id="oct-search-button"]',
                search_result_products_xpath_templates='//div/div[3]/div[1]/a',
                search_result_link_attribute='href'
            )
        )

    def get_price(self, url, ignore_price_format, open_page=True):
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

    def get_price_on_sale(self, url, ignore_price_format, open_page=True):
        if open_page:
            self.open_page(url)

        try:
            price_on_sale = self._parse_price(
                xpath=self.website_info.product_xpaths.PRICE_ON_SALE, ignore_price_format=ignore_price_format)
            if self.get_price(url=url, ignore_price_format=ignore_price_format, open_page=False) == price_on_sale:
                raise PriceNotFoundException
            return price_on_sale
        except PriceIsNotNormalizedException:
            raise
        except Exception as e:
            message = f'{self.website_info}: Unable to get price on sale with {self.website_info.product_xpaths.PRICE_ON_SALE}, maybe product is not on sale.'
            logger.exception(message)
            raise PriceNotFoundException from e

    def find_n_products(self, product, n, fast_parse=True, ignore_price_format=True, raise_exception=False):
        return super()._find_n_products(product, n, fast_parse, ignore_price_format, raise_exception)
