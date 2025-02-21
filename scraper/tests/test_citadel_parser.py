import unittest
from scraper.parsers.citadel_parser import CitadelParser

class TestRozetkaParser(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        self.parser = CitadelParser()

    def test_info_product_on_sale(self):
        url = 'https://citadelbuddekor.com.ua/products/klej-dlja-plitki-atlas-geoflex-5kg-000104500'

        info = self.parser.info(url)

        self.assertEqual(info['price'], 281.00)
        self.assertEqual(info['price_on_sale'], 245.00)
    
    def test_info_product_not_on_sale(self):
        url = 'https://citadelbuddekor.com.ua/products/klej-dlja-plitki-elastichnij-atlas-plus-bilij-5kg-000008497'

        info = self.parser.info(url)

        self.assertEqual(info['price'], 399.00)
        self.assertIsNone(info['price_on_sale'])

    def test_info_product_is_not_available(self):
        pass

    def test_info_product_is_available(self):
        url = 'https://citadelbuddekor.com.ua/products/klej-dlja-plitki-elastichnij-atlas-plus-bilij-5kg-000008497'

        info = self.parser.info(url)

        self.assertEqual(info['is_available'], True)

    def test_info_title(self):
        url = 'https://citadelbuddekor.com.ua/products/klej-dlja-plitki-elastichnij-atlas-plus-bilij-5kg-000008497'

        info = self.parser.info(url)

        self.assertEqual(info['title'], 'КЛЕЙ ДЛЯ ПЛИТКИ ЕЛАСТИЧНИЙ АТЛАС PLUS БІЛИЙ 5КГ')

    @classmethod
    def tearDownClass(self):
        self.parser.close()

def run_tests():
    unittest.main(exit=False)

if __name__ == '__main__':
    run_tests()
