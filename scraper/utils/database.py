import psycopg2
from psycopg2 import Error
from dotenv import load_dotenv
import os

from scraper.parsers.website import ProductXpaths, NavigationXPaths, Website

load_dotenv()

class Database:
    def __init__(self):
        self.connection = None
        try:
            self.connection = psycopg2.connect(
                database=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT")
            )
        except Error as e:
            print(f"Помилка при підключенні: {e}")

    def init_db(self):
        try:
            cursor = self.connection.cursor()
            with open('sql/init_db.sql', 'r') as f:
                cursor.execute(f.read())
            self.connection.commit()
        except Error as e:
            print(f"Помилка при ініціалізації: {e}")
        finally:
            cursor.close()

    def add_product_xpaths(self, product_xpaths : ProductXpaths):
        try:
            cursor = self.connection.cursor()
            query = """
                INSERT INTO product_xpaths (
                    price_on_sale, price_without_sale, price, 
                    availability, title, available_text
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id
            """
            cursor.execute(query, (
                product_xpaths.PRICE_ON_SALE,
                product_xpaths.PRICE_WITHOUT_SALE,
                product_xpaths.PRICE,
                product_xpaths.AVAILABILITY,
                product_xpaths.TITLE,
                product_xpaths.AVAILABLE_TEXT
            ))
            self.connection.commit()
            return cursor.fetchone()[0]
        except Error as e:
            print(f"Помилка при додаванні product_xpaths: {e}")
            return None
        finally:
            cursor.close()

    def add_navigation_xpaths(self, navigation_xpaths : NavigationXPaths):
        try:
            cursor = self.connection.cursor()
            query = """
                INSERT INTO navigation_xpaths (
                    search_field, submit_button, 
                    search_result_products_xpath_templates, search_result_link_attribute
                )
                VALUES (%s, %s, %s, %s)
                RETURNING id
            """
            cursor.execute(query, (
                navigation_xpaths.SEARCH_FIELD,
                navigation_xpaths.SUBMIT_BUTTON,
                navigation_xpaths.SEARCH_RESULT_PRODUCTS_XPATH_TEMPLATES,
                navigation_xpaths.SEARCH_RESULT_LINK_ATTRIBUTE
            ))
            self.connection.commit()
            return cursor.fetchone()[0]
        except Error as e:
            print(f"Помилка при додаванні navigation_xpaths: {e}")
            return None
        finally:
            cursor.close()

    def add_website(self, website : Website):
        try:
            cursor = self.connection.cursor()
            product_xpaths_id = self.add_product_xpaths(website.product_xpaths)
            if not product_xpaths_id:
                return None

            navigation_xpaths_id = self.add_navigation_xpaths(website.website_navigation)
            if not navigation_xpaths_id:
                return None
            
            query = """
                INSERT INTO websites (
                    url, price_format, product_xpaths_id, navigation_xpaths_id
                )
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (url) DO UPDATE 
                SET price_format = EXCLUDED.price_format,
                    product_xpaths_id = EXCLUDED.product_xpaths_id,
                    navigation_xpaths_id = EXCLUDED.navigation_xpaths_id
                RETURNING id
            """
            cursor.execute(query, (
                website.url,
                website.price_format,
                product_xpaths_id,
                navigation_xpaths_id
            ))
            self.connection.commit()
            return cursor.fetchone()[0]
        except Error as e:
            print(f"Помилка при додаванні сайту: {e}")
            return None
        finally:
            cursor.close()

    def get_website_info(self, url):
        try:
            cursor = self.connection.cursor()
            query = """
                SELECT 
                    w.url, w.price_format,
                    p.price_on_sale, p.price_without_sale, p.price, p.availability, p.title, p.available_text,
                    n.search_field, n.submit_button, n.search_result_products_xpath_templates, n.search_result_link_attribute
                FROM websites w
                LEFT JOIN product_xpaths p ON w.product_xpaths_id = p.id
                LEFT JOIN navigation_xpaths n ON w.navigation_xpaths_id = n.id
                WHERE w.url = %s
            """
            cursor.execute(query, (url,))
            data = cursor.fetchone()
            if data:
                url, price_format, *rest = data 
                product_data = rest[:6]
                navigation_data = rest[6:]
                product_xpaths = ProductXpaths(*product_data)
                navigation_xpaths = NavigationXPaths(*navigation_data)
                return Website(url, price_format, product_xpaths, navigation_xpaths)
            return None
        except Error as e:
            print(f"Помилка при отриманні Website: {e}")
            return None
        finally:
            cursor.close()

    def __del__(self):
        if self.connection:
            self.connection.close()