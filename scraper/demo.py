from scraper.parsers.rozetka_parser import RozetkaParser
from scraper.parsers.silpo_parser import SilpoParser
from scraper.parsers.website_info import * 
from scraper.parsers.epicentr_parser import EpicentrParser
from scraper.parsers.citadel_parser import CitadelParser

def rozetka_demo(parser : RozetkaParser):
    product_info = parser.find_n_products('iphone 16', n=2, fast_parse=False)
    print(*product_info)

    product_info = parser.find_n_products('сік садочок', n=2, fast_parse=False)
    print(*product_info)

def silpo_demo(parser : SilpoParser):
    product_info = parser.find_n_products('iphone 16', n=2, fast_parse=False)
    print(*product_info)

    product_info = parser.find_n_products('сік садочок', n=2, fast_parse=False)
    print(*product_info)

def epicenter_demo(parser : EpicentrParser):
    product_info = parser.find_n_products('iphone 16', n=2, fast_parse=False)
    print(*product_info)

    product_info = parser.find_n_products('сік садочок', n=2, fast_parse=False)
    print(*product_info)

def citadel_demo(parser : CitadelParser):
    product_info = parser.find_n_products('цемент', n=2, fast_parse=False)
    print(*product_info)

    product_info = parser.find_n_products('бруківка', n=2, fast_parse=False)
    print(*product_info)

if __name__ == '__main__':
    successfull = 0
    try:
        while True:
            rozetka_demo(parser=RozetkaParser())
            successfull += 1
    except Exception as e:
        print(e)
        print('\n\n\n', successfull)