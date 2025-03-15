from pydantic import BaseModel, EmailStr, AnyUrl
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    name: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):  
    email: EmailStr
    password: str

class User(UserBase):
    id: int
    is_active: bool = True

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "name": "John Doe",
                "id": 1,
                "is_active": True
            }
        }

class UserResponse(UserBase):
    id: int
    is_active: bool = True

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }

class StoreBase(BaseModel):
    name: str
    url: AnyUrl
    title_xpath: str
    available_xpath: str
    price_xpath: str
    price_without_sale_xpath: str
    price_on_sale_xpath: str

class StoreCreate(StoreBase):
    pass

class StoreResponse(StoreBase):
    id: int

    class Config:
        from_attributes = True

class StoreEditRequest(BaseModel):
    url: Optional[AnyUrl] = None
    title_xpath: Optional[str] = None
    available_xpath: Optional[str] = None
    price_xpath: Optional[str] = None
    price_without_sale_xpath: Optional[str] = None
    price_on_sale_xpath: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "url": "https://example.com",
                "title_xpath": "//h1",
                "price_xpath": "//span[@class='price']"
            }
        }