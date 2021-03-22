from typing import Optional

from pydantic import EmailStr

from .dbmodel import DBModelMixin
from .rwmodel import RWModel
from core.security import generate_salt, get_password_hash, verify_password

from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from passlib.context import CryptContext
from .token import Token

class UserBase(RWModel):
    username: str
    email: EmailStr
    bio: Optional[str] = ""
    image: Optional[str] = None

class UserInDB(DBModelMixin, UserBase):
    salt: str = ""
    hashed_password: str = ""

    def check_password(self, password: str):
        return verify_password(self.salt + password, self.hashed_password)

    def change_password(self, password: str):
        self.salt = generate_salt()
        self.hashed_password = get_password_hash(self.salt + password)

class User(UserBase):
    access_token: str
    
class UserInResponse(RWModel):
    user: User
    
class UserInLogin(RWModel):
    email: EmailStr
    password: str

class UserInCreate(UserInLogin):
    username: str

class UserInUpdate(RWModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    bio: Optional[str] = None
    image: Optional[str] = None