import logging


logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()
    ],
    encoding='utf-8'
)

logger = logging.getLogger(__name__)


class ProductInfo:
    def __init__(self, url, price, is_on_sale, price_on_sale, is_available, title):
        self.url = url
        self.price = price
        self.is_on_sale = is_on_sale
        self.price_on_sale = price_on_sale
        self.is_available = is_available
        self.title = title

    def to_dict(self):
        return {
            "url": self.url,
            "price": self.price,
            "is_on_sale": self.is_on_sale,
            "price_on_sale": self.price_on_sale,
            "is_available": self.is_available,
            "title": self.title
        }

    def __str__(self):
        return str(self.to_dict())
