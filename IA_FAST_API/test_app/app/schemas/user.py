from pydantic import BaseModel
from typing import Literal


class UserBase(BaseModel):
    username: str
    full_name: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    role: Literal["user", "admin"] = "user"

    class Config:
        from_attributes = True

class UserOut(BaseModel):
    id: int
    username: str
    full_name: str
    role: str

class Login(BaseModel):
    username: str
    password: str  

class LoginOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
