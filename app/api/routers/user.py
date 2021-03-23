from fastapi import APIRouter, Body, Depends

from core.jwt import get_current_active_user
from crud.shortcuts import check_free_username_and_email
from crud.user import update_user, delete_user
from db.mongodb import AsyncIOMotorClient, get_database
from models.user import User, UserInResponse, UserInUpdate, UserInLogin
from crud.profile import delete_profile_for_username

router = APIRouter(prefix="/user")

@router.get("", response_model=UserInResponse, tags=["users"])
async def retrieve_current_user(user: User = Depends(get_current_active_user)):
    return UserInResponse(user=user)

@router.put("", response_model=UserInResponse, tags=["users"])
async def update_current_user(
    user: UserInUpdate = Body(..., embed=True),
    current_user: User = Depends(get_current_active_user),
    db: AsyncIOMotorClient = Depends(get_database)
):
    if user.username == current_user.username:
        user.username = None
    if user.email == current_user.email:
        user.email = None

    await check_free_username_and_email(db, user.username, user.email)

    dbuser = await update_user(db, current_user.username, user)
    return UserInResponse(user=User(**dbuser.dict(), access_token=current_user.access_token))

@router.delete("", response_model=UserInResponse, tags=["users"])
async def delete_current_user(
    user: UserInLogin = Body(..., embed=True),
    current_user: User = Depends(get_current_active_user),
    db: AsyncIOMotorClient = Depends(get_database),
):

    if user.username != current_user.username:
        user.username = None

    dbuser = await delete_user(db, user)
    await delete_profile_for_username(conn = db, username = dbuser.username)
    return UserInResponse(user=User(**dbuser.dict(), access_token=current_user.access_token))