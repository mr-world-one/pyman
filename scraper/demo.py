from scraper.parsers.rozetka_parser import RozetkaParser
from scraper.parsers.silpo_parser import SilpoParser
from scraper.parsers.epicentr_parser import EpicentrParser
from scraper.parsers.citadel_parser import CitadelParser

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

def epicenter_demo():
    product_on_sale = 'https://epicentrk.ua/ua/shop/smartfon-apple-iphone-16-pro-max-1000gb-white-titanium-myx53sx-a.html'
    product_not_on_sale = 'https://epicentrk.ua/ua/shop/smartfon-samsung-galaxy-fold6-5g-12-512gb-silver-shadow-sm-f956bzscsek.html'
    product_is_not_availible = 'https://epicentrk.ua/ua/shop/apple-iphone-15-pro-512gb-space-black.html'

    urls = [ product_on_sale, product_not_on_sale, product_is_not_availible ]

    epicentr = EpicentrParser()
    for url in urls:
        print(epicentr.info(url))
    print('Success')

def citadel_demo():
    product_on_sale = 'https://citadelbuddekor.com.ua/products/klej-dlja-plitki-atlas-geoflex-5kg-000104500'
    product_not_on_sale = 'https://citadelbuddekor.com.ua/products/klej-dlja-plitki-elastichnij-atlas-plus-bilij-5kg-000008497'

    urls = [ product_on_sale, product_not_on_sale ]

    epicentr = CitadelParser()
    for url in urls:
        print(epicentr.info(url))
    print('Success')


if __name__ == '__main__':
    citadel_demo()