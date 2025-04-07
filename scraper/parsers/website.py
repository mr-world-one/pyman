class Website:
    def __init__(self, url: str, price_format: str, product_xpaths: 'ProductXpaths', website_navigation: 'NavigationXPaths'):
        self.url = url
        self.price_format = price_format
        self.product_xpaths = product_xpaths
        self.website_navigation = website_navigation

    def __str__(self):
        return f'{self.url}'


class ProductXpaths:
    def __init__(self, price_on_sale, price_without_sale, price, availability, title, available_text):
        self.PRICE_ON_SALE = price_on_sale
        self.PRICE_WITHOUT_SALE = price_without_sale
        self.PRICE = price
        self.AVAILABILITY = availability
        self.TITLE = title
        self.AVAILABLE_TEXT = available_text


class NavigationXPaths:
    def __init__(self, search_field: str, submit_button: str, search_result_products_xpath_templates: str, search_result_link_attribute: str):
        self.SEARCH_FIELD = search_field
        self.SUBMIT_BUTTON = submit_button
        self.SEARCH_RESULT_PRODUCTS_XPATH_TEMPLATES = search_result_products_xpath_templates
        self.SEARCH_RESULT_LINK_ATTRIBUTE = search_result_link_attribute
