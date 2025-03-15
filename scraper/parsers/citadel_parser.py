from scraper.parsers.base_parser import BaseParser
from scraper.parsers.xpaths import CitadelProductXPaths
import re


class CitadelParser(BaseParser):

    xpaths = CitadelProductXPaths()

    def __init__(self):
        super().__init__()

    def normalize_price(self, price: str):
        # citadel provides price in the following format: *** грн.
        match = re.search(r'\d+', price)
        return float(match.group()) if match else None

    def info_about_product(self, url):
        data = super().info_about_product(url, self.xpaths)
        if data['price'] == data['price_on_sale']:
            data['price_on_sale'] = None
        return data
