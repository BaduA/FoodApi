from datetime import datetime
from typing import List, Optional
from fastapi import Form, UploadFile
from pydantic import BaseModel, EmailStr

# USER
class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    username: str


class TokenData(BaseModel):
    id: Optional[str] = None


class UserOut(BaseModel):
    email: str
    username: str

    class Config:
        orm_mode = True


class ChangePsw(BaseModel):
    new_psw: str
    old_psw: str

