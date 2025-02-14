import unittest
from scraper.parsers.rozetka_parser import RozetkaParser

class TestRozetkaParser(unittest.TestCase):
    
    def setUp(self):
        self.parser = RozetkaParser()

    def test_info_product_on_sale(self):
        url = 'https://rozetka.com.ua/348712653/p348712653/'

        info = self.parser.info(url)

        self.assertEqual(info['price'], 360)
        self.assertEqual(info['sale_price'], 319)
    
    def test_info_product_not_on_sale(self):
        url = 'https://rozetka.com.ua/412737279/p412737279/'

        info = self.parser.info(url)

        self.assertEqual(info['price'], 277)
        self.assertIsNone(info['sale_price'])

    def test_info_product_is_not_available(self):
        url = 'https://rozetka.com.ua/452784485/p452784485/'

        info = self.parser.info(url)

        self.assertEqual(info['is_available'], False)

    def test_info_product_is_available(self):
        url = 'https://rozetka.com.ua/412737279/p412737279/'

        info = self.parser.info(url)

        self.assertEqual(info['is_available'], True)

    def test_info_title(self):
        url = 'https://rozetka.com.ua/412737279/p412737279/'

        info = self.parser.info(url)

        self.assertIsNotNone(info['title'])

    def tearDown(self):
        self.parser.close()

def run_tests():
    unittest.main(exit=False)

if __name__ == '__main__':
    run_tests()
