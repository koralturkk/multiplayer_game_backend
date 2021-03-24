from core.jwt import get_current_active_user
from fastapi import APIRouter, Body, Depends, Path, Query
from crud.profile import (
    get_profile_for_username,
)
from crud.follow import (
    follow_profile,
    unfollow_profile,
    is_following_profile,
    get_follower_list,
    get_following_list,
)

from db.mongodb import AsyncIOMotorClient, get_database
from models.profile import (

    ProfileInFollow,
)
from models.user import User
from fastapi.responses import JSONResponse

router= APIRouter(prefix= "/profile")

@router.get("/followers", tags=["follow"])
async def retrieve_profile_followers(
    db: AsyncIOMotorClient=Depends(get_database),
    current_user: User=Depends(get_current_active_user)):
    db_profile=await get_profile_for_username(conn=db, username=current_user.username)
    follower_list = await get_follower_list(conn = db, current_username=db_profile.username)
    return {"followers": follower_list}

@router.get("/following", tags=["follow"])
async def retrieve_profile_following(
    db: AsyncIOMotorClient=Depends(get_database),
    current_user: User=Depends(get_current_active_user)):
    db_profile=await get_profile_for_username(conn=db, username=current_user.username)
    following_list = await get_following_list(conn = db, current_username=db_profile.username)
    return {"following": following_list}


@router.put("/{follow_username}", response_model= ProfileInFollow, tags= ["follow"])
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



@router.put("/{unfollow_username}", response_model= ProfileInFollow, tags= ["follow"])
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


