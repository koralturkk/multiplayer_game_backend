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
    following: Optional[List[str]] = []#
    country: Optional[Country] = None

class ProfileInDB(Profile, DBModelMixin):
    pass
    
class ProfileInResponse(RWModel):
    profile: Profile