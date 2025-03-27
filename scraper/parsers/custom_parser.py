from scraper.parsers.base_parser import BaseParser
from scraper.parsers.xpaths import CustomProductXPaths
import re

class CustomParser(BaseParser):
    def __init__(self, xpaths, price_format):
        super().__init__()
        self.xpaths = xpaths
        self.price_format = price_format

    def find_n_products(self, product, n, fast_parse=True, ignore_price_format=True, raise_exception=False):
        return super()._find_n_products(product, n, fast_parse, ignore_price_format, raise_exception)