from models.profile import ProfileInDB
from typing import Optional, List

from starlette.exceptions import HTTPException
from starlette.status import (
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)
from crud.user import get_user
from db.mongodb import AsyncIOMotorClient
from core.config import database_name, followers_collection_name, users_collection_name, profiles_collection_name
from models.profile import Profile, Country
import datetime


async def create_profile_for_user(conn: AsyncIOMotorClient, username: str, country : Country) -> ProfileInDB:

    row = await conn[database_name][profiles_collection_name].find_one({"username": username})
    if not row:
        raise HTTPException(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Username already has a profile",
        )

    dbprofile = ProfileInDB(
        username = username,
        points = 0,
        country = country
        )
    dbprofile.created_at = datetime.now()
    dbprofile.updated_at = datetime.now()

    row = await conn[database_name][profiles_collection_name].insert_one(dbprofile.dict())

    dbprofile.id = row.inserted_id

    return dbprofile


async def get_profile_for_user(conn: AsyncIOMotorClient, username: str) -> ProfileInDB:
    
    row = await conn[database_name][profiles_collection_name].find_one({"username": username})
    if not row:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Profile does not exist",
        )

    return ProfileInDB(**row)


# async def is_following_for_user(
#     conn: AsyncIOMotorClient, current_username: str, target_username: str
# ) -> bool:
#     count = await conn[database_name][followers_collection_name].count_documents({"follower": current_username,
#                                                                                   "following": target_username})
#     return count > 0

# async def follow_for_user(
#     conn: AsyncIOMotorClient, current_username: str, target_username: str
# ):
#     target_user = await get_user(conn, target_username)

#     if target_user:
#         await conn[database_name][followers_collection_name].insert_one({"follower": current_username,
#                                                                          "following": target_user.username})
#     else:
#         raise HTTPException(
#             status_code=HTTP_404_NOT_FOUND, detail=f"User {target_username} not found"
#         )


# async def unfollow_user(conn: AsyncIOMotorClient, current_username: str, target_username: str):
#     await conn[database_name][followers_collection_name].delete_many({"follower": current_username,
#                                                                      "following": target_username})

