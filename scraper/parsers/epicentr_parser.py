from scraper.parsers import Website, ProductXpaths, NavigationXPaths
from scraper.parsers.base_parser import BaseParser
from scraper.utils.database import Database

class EpicentrParser(BaseParser):
    def __init__(self):
        self.db = Database()

        website_info = self.db.get_website_info('https://epicentrk.ua/')

        if not website_info:
            print("Дані для Epicentr не знайдено в базі, додаємо...")
            website_info = self._create_default_website()
            self.db.add_website(website_info)

        super().__init__(website_info)

    def _create_default_website(self):
        return Website(
            url='https://epicentrk.ua/',
            price_format=r'\d+',
            product_xpaths=ProductXpaths(
                price_on_sale='//div/div[1]/div[2]/data/data[1]',
                price_without_sale='//div/div[1]/div[1]/s/data',
                price='//div/div[1]/div[1]/data/data[1]',
                availability='//*[@id="main"]/div[2]/div/div/button',
                title='//*[@id="__template"]/main/div[1]/div/div/div/header/div/div[1]/h1',
                available_text='КУПИТИ'
            ),
            website_navigation=NavigationXPaths(
                search_field='//*[@id="global-site-header"]/header/div/div[3]/form/input',
                submit_button='//*[@id="global-site-header"]/header/div/div[3]/form/button[2]',
                search_result_products_xpath_templates='//div[3]/div/h2/a',
                search_result_link_attribute='href'
            )
        )

    def find_n_products(self, product: str, n: int, fast_parse=True, ignore_price_format=True, raise_exception=False):
        return super()._find_n_products(
            product=product,
            n=n,
            fast_parse=fast_parse,
            ignore_price_format=ignore_price_format,
            raise_exception=raise_exception
        )
