from .rwmodel import RWModel
from typing import Optional


class TokenData(RWModel):
    username: str = ""

class Token(RWModel):
    access_token: str
    token_type: str
