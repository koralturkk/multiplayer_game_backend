from core.jwt import get_current_active_user
from fastapi import APIRouter, Body, Depends, Path, Query
from starlette.exceptions import HTTPException
from crud.profile import (
    create_profile_for_username,
    get_profile_for_username,
    update_profile_for_username,
    delete_profile_for_username
)
from crud.user import verify_user
from db.mongodb import AsyncIOMotorClient, get_database
from models.profile import (
    Profile,
    ProfileInDB,
    ProfileInResponse,
    ProfileInUpdate,
    Country
)
from models.user import User, UserInLogin, UserInDB


router = APIRouter(prefix = "/profile")


@router.get("", response_model=ProfileInDB, tags=["profiles"])
async def retrieve_user_profile(
    db: AsyncIOMotorClient = Depends(get_database),
    current_user: User = Depends(get_current_active_user)):
    dbprofile = await get_profile_for_username(conn = db, username = current_user.username)
    return dbprofile

@router.post("", response_model=ProfileInDB, tags=["profiles"])
async def create_user_profile(
    country: Country, 
    current_user: User = Depends(get_current_active_user),
    db: AsyncIOMotorClient = Depends(get_database),
):
    #Checks for existing profile are made in CRUD
    dbprofile = await create_profile_for_username(
        country = country, 
        username=current_user.username, 
        conn=db)

    return dbprofile


@router.put("", response_model=ProfileInUpdate, tags=["profiles"])
async def update_user_profile(
    user : UserInLogin,
    country: Country, 
    current_user: User = Depends(get_current_active_user),
    db: AsyncIOMotorClient = Depends(get_database),
):
    dbuser = await verify_user(conn= db, user= user, current_user= current_user)
    #Checks for existing profile are made in CRUD
    profileInUpdate = await update_profile_for_username(
        country = country, 
        username=dbuser.username, 
        conn=db)

    return profileInUpdate


@router.delete("", response_model=ProfileInDB, tags=["profiles"])
async def delete_user_profile(
    user : UserInLogin,
    current_user: User = Depends(get_current_active_user),
    db: AsyncIOMotorClient = Depends(get_database),
):
    #Checks for existing profile are made in CRUD
    dbuser = await verify_user(conn= db, user= user, current_user= current_user)
    dbprofile = await delete_profile_for_username(
        username=dbuser.username, 
        conn=db)

    return dbprofile
