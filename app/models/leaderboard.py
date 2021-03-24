from typing import Optional, List
from .rwmodel import RWModel
from enum import Enum
from .dbmodel import DBModelMixin
from .profile import ProfileInLeaderboard


class Leaderboard(RWModel):
    leaderboard_list: List[ProfileInLeaderboard]
