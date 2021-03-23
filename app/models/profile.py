from typing import Optional, List
from .rwmodel import RWModel
from enum import Enum
from .dbmodel import DBModelMixin

class Country(str, Enum):
    Germany = 'DE'
    Turkey = 'TR'
    UnitedStates = 'US'

class Profile(RWModel):
    username: str
    points: int = 0
    country: Optional[Country] = None
    bio: Optional[str] = ""
    image: Optional[str] = None

class ProfileInDB(Profile, DBModelMixin):
    pass 

class ProfileInResponse(RWModel):
    profile: Profile

class ProfileInUpdate(RWModel):
    old_profile: Profile
    new_profile: Profile

class ProfileInFollow(RWModel):
    username: str
    points: int

class ProfileInDisplay(ProfileInDB):
    follower_count: int
    follower_list: List[str]
    following_count: int
    following_list: List[str]
