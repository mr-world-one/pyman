from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String)

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