from typing import List, Union, Optional
import datetime

from pydantic import BaseModel, EmailStr


class UserLogin(BaseModel):
    username: str
    password: str


class UserCreate(UserLogin):
    email: EmailStr
    

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username: str
    role: str
    created_at: datetime.datetime

    class Config:
        orm_mode = True


class ItemBase(BaseModel):
    name: str
    description: str
    element: str
    
    
class ItemResponse(ItemBase):
    created_at: datetime.datetime

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str
    

class TokenData(BaseModel):
    id: Optional[str] = None