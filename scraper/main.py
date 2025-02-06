from scraper.parsers.rozetka_parser import RozetkaParser

product_on_sale = 'https://rozetka.com.ua/ua/348712653/p348712653/'
product_not_on_sale = 'https://rozetka.com.ua/ua/folio-9786175516683/p450358784/'
product_is_not_availible = 'https://rozetka.com.ua/ua/389118078/p389118078/'

urls = [ product_on_sale, product_not_on_sale, product_is_not_availible ]

if __name__ == '__main__':
    rozetka = RozetkaParser()
    for url in urls:
        print(rozetka.info(url))
    print('Success')