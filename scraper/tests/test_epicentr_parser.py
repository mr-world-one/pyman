import unittest
from scraper.parsers.epicentr_parser import EpicentrParser

class TestRozetkaParser(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        self.parser = EpicentrParser()

    def test_info_product_on_sale(self):
        url = 'https://epicentrk.ua/ua/shop/smartfon-apple-iphone-16-pro-max-1000gb-white-titanium-myx53sx-a.html'

        info = self.parser.info(url)

        self.assertEqual(info['price'], 88499)
        self.assertEqual(info['price_on_sale'], 83999)
    
    def test_info_product_not_on_sale(self):
        url = 'https://epicentrk.ua/ua/shop/smartfon-samsung-galaxy-fold6-5g-12-512gb-silver-shadow-sm-f956bzscsek.html'

        info = self.parser.info(url)

        self.assertEqual(info['price'], 84999)
        self.assertIsNone(info['price_on_sale'])

    def test_info_product_is_not_available(self):
        url = 'https://epicentrk.ua/ua/shop/apple-iphone-15-pro-512gb-space-black.html'

        info = self.parser.info(url)

        self.assertEqual(info['is_available'], False)

    def test_info_product_is_available(self):
        url = 'https://epicentrk.ua/ua/shop/smartfon-apple-iphone-16-pro-max-1000gb-white-titanium-myx53sx-a.html'

        info = self.parser.info(url)

        self.assertEqual(info['is_available'], True)

    def test_info_title(self):
        url = 'https://epicentrk.ua/ua/shop/apple-iphone-15-pro-512gb-space-black.html'

        info = self.parser.info(url)

        self.assertEqual(info['title'], 'Смартфон Apple iPhone 15 Pro 512GB Black Titanium (MTV73RX/A)')

    @classmethod
    def tearDownClass(self):
        self.parser.close()

def run_tests():
    unittest.main(exit=False)

if __name__ == '__main__':
    run_tests()
