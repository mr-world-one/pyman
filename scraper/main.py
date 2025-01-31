from scraper.parsers.rozetka_parser import RozetkaParser
from scraper.tests.test_rozetka_parser import run_tests

if __name__ == '__main__':
    url = 'https://rozetka.com.ua/ua/348712653/p348712653/'
    rozetka = RozetkaParser()
    print(rozetka.info(url))
    print('Success')