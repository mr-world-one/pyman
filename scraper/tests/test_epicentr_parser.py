import unittest
from scraper.parsers.epicentr_parser import EpicentrParser

class TestEpicentrParser(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.parser = EpicentrParser()

    def test_info_product_on_sale_fast_parse_false(self):
        url = 'https://epicentrk.ua/ua/shop/bezalkogolnyy-napitok-coca-cola-24-sht-0-5-l-0000054491472-.html'

        product_info = self.parser.info_about_product(url, fast_parse=False)

        self.assertEqual(product_info.url, url)
        self.assertTrue(20 < product_info.price < 35 and product_info.price > product_info.price_on_sale)
        self.assertTrue(product_info.is_on_sale)
        self.assertTrue(20 < product_info.price_on_sale < 30)
        self.assertTrue(product_info.is_available)
        self.assertIsNotNone(product_info.title)

    def test_info_product_on_sale_fast_parse_true(self):
        url = 'https://epicentrk.ua/ua/shop/bezalkogolnyy-napitok-coca-cola-24-sht-0-5-l-0000054491472-.html'

        product_info = self.parser.info_about_product(url, fast_parse=True)

        self.assertEqual(product_info.url, url)
        self.assertTrue(30 < product_info.price < 35)
        self.assertIsNone(product_info.is_on_sale)
        self.assertIsNone(product_info.price_on_sale)
        self.assertIsNone(product_info.is_available)
        self.assertIsNotNone(product_info.title)

    def test_info_product_is_not_available_fast_parse_false(self):
        url = 'https://epicentrk.ua/ua/shop/mplc-upakovka-napoyu-coca-cola-0-33-l-kh-12-banok-ma001235-1ecd5081-60a9-6aba-9e56-1bc064dedece.html'

        product_info = self.parser.info_about_product(url, fast_parse=False)

        self.assertEqual(product_info.url, url)
        self.assertIsNone(product_info.price)
        self.assertIsNone(product_info.is_on_sale)
        self.assertIsNone(product_info.price_on_sale)
        self.assertFalse(product_info.is_available)
        self.assertIsNotNone(product_info.title)

    def is_not_empty(self, product):
        result = (product.title is not None) and (product.price is not None)
        return result

    def test_category_search(self):
        result = self.parser.find_n_products('iphone 15', 2)
        self.assertTrue(len(result) != 0)
        for product in result:
            self.assertTrue(self.is_not_empty(product))

    def test_basic_search(self):
        result = self.parser.find_n_products('сік яблучний', 2)
        self.assertTrue(len(result) != 0)
        for product in result:
            self.assertTrue(self.is_not_empty(product))

    @classmethod
    def tearDownClass(cls):
        cls.parser._close()

def run_tests():
    unittest.main(exit=False)

if __name__ == '__main__':
    run_tests()