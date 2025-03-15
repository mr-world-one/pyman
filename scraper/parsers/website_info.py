from scraper.parsers.xpaths import ProductXpaths, WebsiteNavigationXPaths


class WebsiteInfo:
    def __init__(self, url: str, price_format: str, product_xpaths: ProductXpaths, website_navigation: WebsiteNavigationXPaths):
        self.url = url
        self.price_format = price_format
        self.product_xpaths = product_xpaths
        self.website_navigation = website_navigation

    def __str__(self):
        return f'{self.url}'
