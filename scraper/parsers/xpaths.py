class BaseXPaths:
    PRICE_ON_SALE = None
    PRICE_WITHOUT_SALE = None
    PRICE = None
    AVAILABILITY = None
    TITLE = None
    AVAILABLE_TEXT = None
    URL = None


class RozetkaXPaths(BaseXPaths):
    # ROZETKA_PRICE_WITHOUT_SALE vs ROZETKA_PRICE:
    # some products on rozetka are on sales, in such case ROZETKA_PRICE_WITHOUT_SALE is the price without sale for product which is on sale
    # ROZETKA_PRICE is price of product which is not on sale

    PRICE_ON_SALE = '//*[@id="#scrollArea"]/div[1]/div[2]/div/rz-product-main-info/div/div[2]/div/div[1]/p[2]'
    PRICE_WITHOUT_SALE = '//*[@id="#scrollArea"]/div[1]/div[2]/div/rz-product-main-info/div/div[2]/div/div[1]/p[1]'
    PRICE = '//*[@id="#scrollArea"]/div[1]/div[2]/div/rz-product-main-info/div/div[2]/div/div[1]/p'
    AVAILABILITY = '//*[@id="#scrollArea"]/div[1]/div[2]/div/rz-product-main-info/div/div[2]/div/div[1]/rz-status-label/p'
    TITLE = '//*[@id="#scrollArea"]/div[1]/div[2]/div/rz-title-block/div/div[1]/div/h1'
    AVAILABLE_TEXT = 'Є в наявності'
    URL = 'https://rozetka.com.ua/ua'

class SilpoXPaths(BaseXPaths):
    PRICE_ON_SALE = '/html/body/sf-shop-silpo-root/shop-silpo-root-shell/silpo-shell-main/div/div[3]/silpo-product-product-page/div/div/div/div[2]/div/div[1]/div[1]'
    PRICE_WITHOUT_SALE = '/html/body/sf-shop-silpo-root/shop-silpo-root-shell/silpo-shell-main/div/div[3]/silpo-product-product-page/div/div/div/div[2]/div/div[1]/div[2]/div[1]'
    PRICE = '/html/body/sf-shop-silpo-root/shop-silpo-root-shell/silpo-shell-main/div/div[3]/silpo-product-product-page/div/div/div/div[2]/div/div[1]/div[1]'
    AVAILABILITY = '/html/body/sf-shop-silpo-root/shop-silpo-root-shell/silpo-shell-main/div/div[3]/silpo-product-product-page/div/div/div/div[2]/div/div[2]/shop-silpo-common-page-add-to-basket/div/div/button'
    TITLE = '/html/body/sf-shop-silpo-root/shop-silpo-root-shell/silpo-shell-main/div/div[3]/silpo-product-product-page/div/div/div/div[2]/h1'
    AVAILABLE_TEXT = 'У кошик'
    URL = 'https://silpo.ua/'
    
class EpicentrXPaths(BaseXPaths):
    PRICE_ON_SALE = '//*[@id="main"]/div[2]/div[4]/div/div[1]/div[2]/data/data[1]'
    PRICE_WITHOUT_SALE = '//*[@id="main"]/div[2]/div[4]/div/div[1]/div[1]/s/data'
    PRICE = '//*[@id="main"]/div[2]/div[4]/div/div[1]/div/data/data[1]'
    AVAILABILITY = '//*[@id="main"]/div[2]/div[1]/div/div/div[1]/span'
    TITLE = '//*[@id="__template"]/main/div[1]/div/div/div/header/div/div[1]/h1'
    AVAILABLE_TEXT = 'Готовий до відправки'
    URL = 'https://epicentrk.ua/'

class CitadelXPaths(BaseXPaths):
    PRICE_ON_SALE = '//*[@id="content"]/div/div[1]/div[2]/div[2]/div/div[1]'
    PRICE_WITHOUT_SALE = '//*[@id="content"]/div/div[1]/div[2]/div[2]/div/div[2]'
    PRICE = '//*[@id="content"]/div/div[1]/div[2]/div[2]/div/div'
    AVAILABILITY = '//*[@id="content"]/div/div[1]/div[2]/div[2]/ul/li[3]/span'
    TITLE = '//*[@id="product-product"]/main/div[1]/div/h1'
    AVAILABLE_TEXT = 'В наявності'
    URL = 'https://citadelbuddekor.com.ua/'
