from core.jwt import get_current_active_user
from fastapi import APIRouter, Body, Depends, Path, Query
from starlette.exceptions import HTTPException
from crud.profile import (
    create_profile_for_username,
    get_profile_for_username,
    update_profile_for_username,
    delete_profile_for_username,
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


# @router.get("/followers", response_model= ProfileInDB, tags=["profiles"])
# async def retrieve_profile_followers(
#     db: AsyncIOMotorClient=Depends(get_database),
#     current_user: User=Depends(get_current_active_user)):
#     db_profile=await get_profile_for_username(conn=db, username=current_user.username)
#     return db_profile

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


@router.put("/{follow_username}", response_model= ProfileInFollow, tags= ["profiles"])
async def follow_user_profile(
    follow_username: str= Query(...), 
    current_user: User= Depends(get_current_active_user),
    db: AsyncIOMotorClient= Depends(get_database),
):
    is_following= await is_following_profile(conn= db, target_username= follow_username, current_username= current_user.username)
    #Checks for existing profile are made in CRUD
    if is_following:
        return JSONResponse(status_code= 200, content= {"message": "Profile is already being followed"})

    followed_profile= await follow_profile(conn= db, target_username= follow_username, current_username= current_user.username)
    return followed_profile



@router.put("/{unfollow_username}", response_model= ProfileInFollow, tags= ["profiles"])
async def unfollow_user_profile(
    unfollow_username: str= Query(...), 
    current_user: User= Depends(get_current_active_user),
    db: AsyncIOMotorClient= Depends(get_database),
):
    is_following= await is_following_profile(conn= db, target_username= unfollow_username, current_username= current_user.username)
    #Checks for existing profile are made in CRUD
    if not is_following:
        return JSONResponse(status_code= 404, content= {"message": "Profile is not being followed"})

    unfollowed_profile= await unfollow_profile(conn= db, target_username= unfollow_username, current_username= current_user.username)
    return unfollowed_profile
