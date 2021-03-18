from datetime import datetime, timedelta
from typing import Optional
import jwt
from fastapi import Depends, HTTPException, status
from jwt import PyJWTError
from starlette.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND
from jose import JWTError, jwt
from crud.user import get_user
from db.mongodb import AsyncIOMotorClient, get_database
from models.token import TokenData
from models.user import User
from .config import JWT_TOKEN_PREFIX, SECRET_KEY
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

ALGORITHM = "HS256"
access_token_jwt_subject = "access"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# def _get_authorization_token(authorization: str = Header(...)):
#     token_prefix, token = authorization.split(" ")
#     if token_prefix != JWT_TOKEN_PREFIX:
#         raise HTTPException(
#             status_code=HTTP_403_FORBIDDEN, detail="Invalid authorization type"
#         )
#     return token

async def get_current_user(db: AsyncIOMotorClient = Depends(get_database), access_token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(access_token, str(SECRET_KEY), algorithms=[ALGORITHM])
        username: str = payload.get("username")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    dbuser = await get_user(db, token_data.username)
    if not dbuser:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")

    user = User(**dbuser.dict(), access_token=access_token)
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    return current_user

def create_access_token(*, data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire, "sub": access_token_jwt_subject})
    encoded_jwt = jwt.encode(to_encode, str(SECRET_KEY), algorithm=ALGORITHM)
    return encoded_jwt




# from fastapi import Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer
# from blog import token

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# def get_current_user(data: str = Depends(oauth2_scheme)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )

#     return token.verify_token(data, credentials_exception)


# def verify_token(token: str, credentials_exception):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         email: str = payload.get("sub")
#         if email is None:
#             raise credentials_exception
#         token_data = schemas.TokenData(email=email)
#     except JWTError:
#         raise credentials_exception