from core.jwt import get_current_active_user
from fastapi import APIRouter, Body, Depends, Path, Query
from starlette.exceptions import HTTPException
from crud.profile import (
    create_profile_for_username,
    get_profile_for_username,
    update_profile_for_username,
    delete_profile_for_username,
    add_points_to_profile
)
from crud.follow import (
    follow_profile,
    unfollow_profile,
    is_following_profile,
    get_followers_count,
    get_follower_list,
    get_following_list,
    get_following_count
)

from crud.user import verify_user
from db.mongodb import AsyncIOMotorClient, get_database
from models.profile import (
    Profile,
    ProfileInDB,
    ProfileInResponse,
    ProfileInUpdate,
    Country,
    ProfileInFollow,
    ProfileInDisplay
)
from models.user import User, UserInLogin, UserInDB
from fastapi.responses import JSONResponse


router= APIRouter(prefix= "/profile")


@router.get("", response_model= ProfileInDisplay, tags=["profiles"])
async def retrieve_user_profile(
    db: AsyncIOMotorClient=Depends(get_database),
    current_user: User=Depends(get_current_active_user)):
    db_profile = await get_profile_for_username(conn=db, username=current_user.username)
    follower_list = await get_follower_list(conn = db, current_username=current_user.username)
    follower_count = await get_followers_count(conn = db, current_username=current_user.username)
    following_count = await get_following_count(conn = db, current_username=current_user.username)
    follower_list = await get_following_list(conn = db, current_username=current_user.username)

    profile_in_display = ProfileInDisplay(
        **db_profile.dict(), 
        follower_count = follower_count, 
        follower_list = follower_list,
        following_count = following_count, 
        following_list = follower_list, 
        )
    return profile_in_display


@router.post("", response_model=ProfileInDB, tags=["profiles"])
async def create_user_profile(
    country: Country=Query(...), 
    bio: str= Query(None), 
    image: str= Query(None), 
    current_user: User=Depends(get_current_active_user),
    db: AsyncIOMotorClient=Depends(get_database),

):
    #Checks for existing profile are made in CRUD
    db_profile= await create_profile_for_username(
        country= country, 
        username= current_user.username, 
        conn= db,
        bio = bio,
        image = image)

    return db_profile

@router.put("", response_model= ProfileInUpdate, tags= ["profiles"])
async def update_user_profile(
    user : UserInLogin,
    country: Country= Query(None), 
    bio: str= Query(None), 
    image: str= Query(None), 
    current_user: User= Depends(get_current_active_user),
    db: AsyncIOMotorClient= Depends(get_database),
):
    db_user= await verify_user(conn= db, user= user, current_user= current_user)
    #Checks for existing profile are made in CRUD
    profileInUpdate= await update_profile_for_username(
        country= country, 
        username= db_user.username, 
        conn= db,
        bio= bio,
        image= image)

    return profileInUpdate



@router.put("/{points}", response_model= ProfileInDB, tags= ["profiles"])
async def add_points_to_user_profile(
    points: int = Query(...),
    current_user: User= Depends(get_current_active_user),
    db: AsyncIOMotorClient= Depends(get_database),
):
    db_profile = await get_profile_for_username(conn=db, username=current_user.username)
    await add_points_to_profile(points = points, conn= db, current_username= db_profile.username)
    updated_profile = await get_profile_for_username(conn=db, username=db_profile.username)
    return updated_profile


@router.delete("", response_model= ProfileInDB, tags= ["profiles"])
async def delete_user_profile(
    user : UserInLogin,
    current_user: User= Depends(get_current_active_user),
    db: AsyncIOMotorClient= Depends(get_database),
):
    #Checks for existing profile are made in CRUD
    db_user= await verify_user(conn= db, user= user, current_user= current_user)
    db_profile= await delete_profile_for_username(
        username= db_user.username, 
        conn= db)

    return db_profile