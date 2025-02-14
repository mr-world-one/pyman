from pydantic import BaseModel, EmailStr, AnyUrl

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    name:str
    email: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    name: str | None = None


class StoreCreate(BaseModel):
    name: str
    url: AnyUrl
    title_xpath: str
    available_xpath: str
    price_xpath: str
    price_without_sale_xpath: str
    price_on_sale_xpath: str


class StoreResponse(StoreCreate):
    id: int

    class Config:
        from_attributes = True

class StoreEditRequest(BaseModel):
    url: AnyUrl | None = None
    title_xpath: str | None = None
    available_xpath: str | None = None
    price_xpath: str | None = None
    price_without_sale_xpath: str | None = None
    price_on_sale_xpath: str | None = None