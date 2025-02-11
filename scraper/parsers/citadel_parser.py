from scraper.parsers.base_parser import BaseParser
from scraper.parsers.xpaths import CitadelXPaths
import re

class CitadelParser(BaseParser):
    
    # if product from epicentr is not availible, then there's no opportunity to get price

    xpaths = CitadelXPaths()

    def __init__(self):
        super().__init__()

    def normalize_price(self, price : str):
        # citadel provides price in the following format: *** грн.
        match = re.search(r'\d+', price)
        return float(match.group()) if match else None
    
    def info(self, url):
        data = super().info(url, self.xpaths)
        if data['price'] == data['price_on_sale']:
            data['price_on_sale'] = None
        return data