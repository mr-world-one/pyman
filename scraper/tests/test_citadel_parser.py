import unittest
from scraper.parsers.citadel_parser import CitadelParser

class TestRozetkaParser(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        self.parser = CitadelParser()

    def test_info_product_on_sale(self):
        url = 'https://citadelbuddekor.com.ua/products/klej-dlja-plitki-atlas-geoflex-5kg-000104500'

        product_info = self.parser.info_about_product(url, fast_parse=False)

        self.assertEqual(product_info.url, url)
        self.assertTrue(200 < product_info.price < 300 and product_info.price > product_info.price_on_sale)
        self.assertTrue(product_info.is_on_sale)
        self.assertTrue(200 < product_info.price_on_sale < 300)
        self.assertTrue(product_info.is_available)
        self.assertIsNotNone(product_info.title)

    
    def test_info_product_not_on_sale(self):
        url = 'https://citadelbuddekor.com.ua/products/klej-dlja-plitki-elastichnij-atlas-plus-bilij-5kg-000008497'

        product_info = self.parser.info_about_product(url, fast_parse=False)

        self.assertEqual(product_info.url, url)
        self.assertTrue(300 < product_info.price < 400)
        self.assertFalse(product_info.is_on_sale)
        self.assertIsNone(product_info.price_on_sale)
        self.assertTrue(product_info.is_available)
        self.assertIsNotNone(product_info.title)

    def is_not_empty(self, product):
        result = (product.title is not None) and (product.price is not None)
        return result

    def test_search_1(self):
        result = self.parser.find_n_products('клей', 2)
        self.assertTrue(len(result) != 0)
        for product in result:
            self.assertTrue(self.is_not_empty(product))
        
    def test_search_2(self):
        result = self.parser.find_n_products('цемент', 2)
        self.assertTrue(len(result) != 0)
        for product in result:
            self.assertTrue(self.is_not_empty(product))

    @classmethod
    def tearDownClass(self):
        self.parser._close()

def run_tests():
    unittest.main(exit=False)

if __name__ == '__main__':
    run_tests()
