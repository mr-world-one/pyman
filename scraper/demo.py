from scraper.parsers.rozetka_parser import RozetkaParser
from scraper.parsers.silpo_parser import SilpoParser

def rozetka_demo():
    product_on_sale = 'https://rozetka.com.ua/ua/348712653/p348712653/'
    product_not_on_sale = 'https://rozetka.com.ua/ua/folio-9786175516683/p450358784/'
    product_is_not_availible = 'https://rozetka.com.ua/ua/389118078/p389118078/'

    urls = [ product_on_sale, product_not_on_sale, product_is_not_availible ]

    rozetka = RozetkaParser()
    for url in urls:
        print(rozetka.info(url))
    print('Success')

def silpo_demo():
    product_on_sale = 'https://silpo.ua/product/ridkyi-zasib-frosch-dlia-prannia-kolorovykh-rechei-134375'
    product_not_on_sale = 'https://silpo.ua/product/korm-dlia-kotiv-sheba-black-gold-z-indychkoiu-v-zhele-712556'
    product_is_not_availible = 'https://silpo.ua/product/syr-domashnii-vagovyi-412736'

    urls = [ product_on_sale, product_not_on_sale, product_is_not_availible ]

    silpo = SilpoParser()
    for url in urls:
        print(silpo.info(url))
    print('Success')


if __name__ == '__main__':
    silpo_demo()