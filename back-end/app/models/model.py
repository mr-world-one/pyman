from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)


class Store(Base):
    __tablename__ = "stores"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    url = Column(String, unique=True, nullable=False)
    title_xpath = Column(String, nullable=False)
    available_xpath = Column(String, nullable=False)
    price_xpath = Column(String, nullable=False)
    price_without_sale_xpath = Column(String, nullable=False)
    price_on_sale_xpath = Column(String, nullable=False)


# ── Scraper tables (unified into the same DB) ──


class ProductXpath(Base):
    """XPath selectors for product data extraction."""
    __tablename__ = "product_xpaths"

    id = Column(Integer, primary_key=True, index=True)
    price_on_sale = Column(Text)
    price_without_sale = Column(Text)
    price = Column(Text)
    availability = Column(Text)
    title = Column(Text)
    available_text = Column(Text)

    websites = relationship("WebsiteConfig", back_populates="product_xpaths_rel")


class NavigationXpath(Base):
    """XPath selectors for website navigation (search)."""
    __tablename__ = "navigation_xpaths"

    id = Column(Integer, primary_key=True, index=True)
    search_field = Column(Text)
    submit_button = Column(Text)
    search_result_products_xpath_templates = Column(Text)
    search_result_link_attribute = Column(Text)

    websites = relationship("WebsiteConfig", back_populates="navigation_xpaths_rel")


class WebsiteConfig(Base):
    """Website configuration for the scraper."""
    __tablename__ = "websites"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(255), unique=True, nullable=False)
    price_format = Column(String(50), nullable=False)
    product_xpaths_id = Column(Integer, ForeignKey("product_xpaths.id", ondelete="CASCADE"), nullable=False)
    navigation_xpaths_id = Column(Integer, ForeignKey("navigation_xpaths.id", ondelete="CASCADE"), nullable=False)

    product_xpaths_rel = relationship("ProductXpath", back_populates="websites")
    navigation_xpaths_rel = relationship("NavigationXpath", back_populates="websites")