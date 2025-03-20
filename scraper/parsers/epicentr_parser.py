from scraper.parsers.base_parser import BaseParser, PriceIsNotNormalizedException, logger, PriceNotFoundException
from scraper.parsers.website_info import WebsiteInfo
from scraper.parsers.xpaths import ProductXpaths, WebsiteNavigationXPaths


class EpicentrParser(BaseParser):

    # if product from epicentr is not availible, then there's no opportunity to get price

    def __init__(self):
        super().__init__(
            WebsiteInfo(
                url='https://epicentrk.ua/',
                price_format=r'\d+',
                product_xpaths=ProductXpaths(price_on_sale='//div/div[1]/div[2]/data/data[1]',
                                             price_without_sale='//div/div[1]/div[1]/s/data',
                                             price='//div/div[1]/div[1]/data/data[1]',
                                             availability='//*[@id="main"]/div[2]/div/div/button',
                                             title='//*[@id="__template"]/main/div[1]/div/div/div/header/div/div[1]/h1',
                                             available_text='КУПИТИ'),
                website_navigation=WebsiteNavigationXPaths(
                    search_field='//*[@id="global-site-header"]/header/div/div[3]/form/input',
                    submit_button='//*[@id="global-site-header"]/header/div/div[3]/form/button[2]',
                    search_result_products_xpath_templates='//div[3]/div/h2/a',
                    search_result_link_attribute='href',
                ))
        )

    def find_n_products(self, product: str, n: int, fast_parse=True, ignore_price_format=True, raise_exception=False):
        return super()._find_n_products(product=product, n=n, fast_parse=fast_parse, ignore_price_format=ignore_price_format, raise_exception=raise_exception)
