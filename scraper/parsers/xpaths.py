class ProductXpaths:
    def __init__(self, price_on_sale, price_without_sale, price, availability, title, available_text):
        self.PRICE_ON_SALE = price_on_sale
        self.PRICE_WITHOUT_SALE = price_without_sale
        self.PRICE = price
        self.AVAILABILITY = availability
        self.TITLE = title
        self.AVAILABLE_TEXT = available_text

class RozetkaProductXPaths(ProductXpaths):
    # ROZETKA_PRICE_WITHOUT_SALE vs ROZETKA_PRICE:
    # some products on rozetka are on sales, in such case ROZETKA_PRICE_WITHOUT_SALE is the price without sale for product which is on sale
    # ROZETKA_PRICE is price of product which is not on sale
    def __init__(self):
        super().__init__(price_on_sale='//*[@id="#scrollArea"]/div[1]/div[2]/div/rz-product-main-info/div/div[2]/div/div[1]/p[2]', 
                         price_without_sale='//*[@id="#scrollArea"]/div[1]/div[2]/div/rz-product-main-info/div/div[2]/div/div[1]/p[1]', 
                         price='//*[@id="#scrollArea"]/div[1]/div[2]/div/rz-product-main-info/div/div[2]/div/div[1]/p', 
                         availability='//*[@id="#scrollArea"]/div[1]/div[2]/div/rz-product-main-info/div/div[2]/div/div[1]/rz-status-label/p', 
                         title='//*[@id="#scrollArea"]/div[1]/div[2]/div/rz-title-block/div/div[1]/div/h1', 
                         available_text='Є в наявності', 
                         url='https://rozetka.com.ua/ua')
        
class SilpoProductXPaths(ProductXpaths):
    def __init__(self):
        super().__init__(price_on_sale='/html/body/sf-shop-silpo-root/shop-silpo-root-shell/silpo-shell-main/div/div[3]/silpo-product-product-page/div/div/div/div[2]/div/div[1]/div[1]', 
                         price_without_sale='/html/body/sf-shop-silpo-root/shop-silpo-root-shell/silpo-shell-main/div/div[3]/silpo-product-product-page/div/div/div/div[2]/div/div[1]/div[2]/div[1]', 
                         price='/html/body/sf-shop-silpo-root/shop-silpo-root-shell/silpo-shell-main/div/div[3]/silpo-product-product-page/div/div/div/div[2]/div/div[1]/div[1]', 
                         availability='/html/body/sf-shop-silpo-root/shop-silpo-root-shell/silpo-shell-main/div/div[3]/silpo-product-product-page/div/div/div/div[2]/div/div[2]/shop-silpo-common-page-add-to-basket/div/div/button', 
                         title='/html/body/sf-shop-silpo-root/shop-silpo-root-shell/silpo-shell-main/div/div[3]/silpo-product-product-page/div/div/div/div[2]/h1', 
                         available_text='У кошик', 
                         url='https://silpo.ua/')
    
class EpicentrProductXPaths(ProductXpaths):
    def __init__(self):
        super().__init__(price_on_sale='//*[@id="main"]/div[2]/div[4]/div/div[1]/div[2]/data/data[1]', 
                         price_without_sale='//*[@id="main"]/div[2]/div[4]/div/div[1]/div[1]/s/data', 
                         price='//*[@id="main"]/div[2]/div[4]/div/div[1]/div/data/data[1]', 
                         availability='//*[@id="main"]/div[2]/div[1]/div/div/div[1]/span', 
                         title='//*[@id="__template"]/main/div[1]/div/div/div/header/div/div[1]/h1', 
                         available_text='Готовий до відправки', 
                         url='https://epicentrk.ua/')

class CitadelProductXPaths(ProductXpaths):
    def __init__(self):
        super().__init__(price_on_sale='//*[@id="content"]/div/div[1]/div[2]/div[2]/div/div[1]', 
                         price_without_sale='//*[@id="content"]/div/div[1]/div[2]/div[2]/div/div[2]', 
                         price='//*[@id="content"]/div/div[1]/div[2]/div[2]/div/div', 
                         availability='//*[@id="content"]/div/div[1]/div[2]/div[2]/ul/li[3]/span', 
                         title='//*[@id="product-product"]/main/div[1]/div/h1', 
                         available_text='В наявності', 
                         url='https://citadelbuddekor.com.ua/')
        
class CustomProductXPaths(ProductXpaths):
    def __init__(self, price_on_sale, price_without_sale, price, availability, title, available_text, url, *args, **kwargs):
        super().__init__(price_on_sale, price_without_sale, price, availability, title, available_text, url)
        self.kwargs = dict(kwargs.values())


class WebsiteNavigationXPaths:
    def __init__(self, search_field : str, submit_button : str, search_result_products_xpath_templates : str, search_result_link_attribute : str):
        self.SEARCH_FIELD = search_field
        self.SUBMIT_BUTTON = submit_button
        self.SEARCH_RESULT_PRODUCTS_XPATH_TEMPLATES = search_result_products_xpath_templates
        self.SEARCH_RESULT_LINK_ATTRIBUTE = search_result_link_attribute