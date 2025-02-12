from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    Username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username:str
    email: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    username: str | None = None
