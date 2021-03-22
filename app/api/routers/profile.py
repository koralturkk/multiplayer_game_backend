from core.jwt import get_current_active_user
from fastapi import APIRouter, Body, Depends, Path, Query
from starlette.exceptions import HTTPException
from crud.profile import (
    create_profile_for_user,
    get_profile_for_user
)
from models.profile import Profile, Country

from db.mongodb import AsyncIOMotorClient, get_database
from models.profile import (
    Profile,
    ProfileInDB,
    ProfileInResponse
)
from models.user import User

router = APIRouter(prefix = "/profile")


@router.get("", response_model=ProfileInDB, tags=["profiles"])
async def retrieve_current_profile(user: User = Depends(get_current_active_user)):
    return


@router.post("", response_model=ProfileInDB, tags=["profiles"])
async def create_profile(
    country: Country, 
    current_user: User = Depends(get_current_active_user),
    db: AsyncIOMotorClient = Depends(get_database),
):

    dbprofile = await create_profile(country = country, username=current_user.username, conn=db)

    return dbprofile