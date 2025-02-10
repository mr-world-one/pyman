import unittest
from scraper.parsers.silpo_parser import SilpoParser

class TestRozetkaParser(unittest.TestCase):
    
    def setUp(self):
        self.parser = SilpoParser()

    def test_info_product_on_sale(self):
        url = 'https://silpo.ua/product/ridkyi-zasib-frosch-dlia-prannia-kolorovykh-rechei-134375'

        info = self.parser.info(url)

        self.assertEqual(info['price'], 579)
        self.assertEqual(info['price_on_sale'], 349)
    
    def test_info_product_not_on_sale(self):
        url = 'https://silpo.ua/product/korm-dlia-kotiv-sheba-black-gold-z-indychkoiu-v-zhele-712556'

        info = self.parser.info(url)

        self.assertEqual(info['price'], 29.19)
        self.assertIsNone(info['price_on_sale'])

    def test_info_product_is_not_available(self):
        url = 'https://silpo.ua/product/ridkyi-zasib-frosch-dlia-prannia-kolorovykh-rechei-134375'

        info = self.parser.info(url)

        self.assertEqual(info['is_available'], False)

    def test_info_product_is_available(self):
        url = 'https://silpo.ua/product/korm-dlia-kotiv-sheba-black-gold-z-indychkoiu-v-zhele-712556'

        info = self.parser.info(url)

        self.assertEqual(info['is_available'], True)

    def test_info_title(self):
        url = 'https://silpo.ua/product/korm-dlia-kotiv-sheba-black-gold-z-indychkoiu-v-zhele-712556'

        info = self.parser.info(url)

        self.assertEqual(info['title'], 'Корм для котів Sheba Black&Gold з індичкою в желе, 85г')

    def tearDown(self):
        self.parser.close()

def run_tests():
    unittest.main(exit=False)

if __name__ == '__main__':
    run_tests()
