from scraper.parsers.base_parser import BaseParser
from scraper.parsers.xpaths import EpicentrXPaths
import re

class EpicentrParser(BaseParser):
    
    # if product from epicentr is not availible, then there's no opportunity to get price

    xpaths = EpicentrXPaths()

    def __init__(self):
        super().__init__()

    def normalize_price(self, price : str):
        # epicentr provides price in the following format: ** ***$
        match = re.search(r'\d+', price.replace(' ', ''))
        return float(match.group()) if match else None
    
    def info(self, url):
        return super().info(url, self.xpaths)