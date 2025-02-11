from scraper.parsers.base_parser import BaseParser
from scraper.parsers.xpaths import RozetkaXPaths
import re

class RozetkaParser(BaseParser):

    xpaths = RozetkaXPaths()

    def __init__(self):
        super().__init__()

    def normalize_price(self, price):
        # rozetka provides price in the following format: ***$
        match = re.search(r'\d+', price)
        return float(match.group()) if match else None
    
    def info(self, url):
        return super().info(url, self.xpaths)