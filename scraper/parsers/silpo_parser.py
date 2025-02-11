from scraper.parsers.base_parser import BaseParser
from scraper.parsers.xpaths import SilpoXPaths
import re

class SilpoParser(BaseParser):

    xpaths = SilpoXPaths()

    def init(self):
        super().__init__()

    def normalize_price(self, price):
        # silpo provides price in the following format: *** грн
        match = re.search(r"\d+\.\d+|\d+", price)
        if match:
            price = float(match.group())
            return price
        
    def info(self, url):
        data = super().info(url, self.xpaths)
        if data['price_on_sale'] == data['price']:
            data['price_on_sale'] = None
        return data