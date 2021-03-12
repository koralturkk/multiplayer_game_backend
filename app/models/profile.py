from typing import Optional

from pydantic import UrlStr
from .mongo_model import MongoModel


class Profile(MongoModel):
    username: str
    bio: Optional[str] = ""
    image: Optional[UrlStr] = None


class ProfileInResponse(MongoModel):
    profile: Profile