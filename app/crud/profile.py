
from typing import Optional, List
from fastapi.param_functions import Query
from starlette.exceptions import HTTPException
from starlette.status import (
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)
from db.mongodb import AsyncIOMotorClient
from core.config import (
    database_name, 
    followers_collection_name, 
    users_collection_name, 
    profiles_collection_name)
from models.profile import( 
    Profile, 
    Country, 
    ProfileInUpdate, 
    ProfileInFollow,
    ProfileInDB)
from datetime import datetime


async def create_profile_for_username(
    conn: AsyncIOMotorClient, 
    username: str, 
    country : Country,
    bio : str,
    image : str
    ) -> ProfileInDB:

    row = await conn[database_name][profiles_collection_name].find_one({"username": username})
    if row:
        raise HTTPException(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Username already has a profile",
        )

    dbprofile = ProfileInDB(
        username = username,
        points = 0,
        country = country,
        bio = bio,
        image = image
        )

    dbprofile.created_at = datetime.now()
    dbprofile.updated_at = datetime.now()

    inserted_row = await conn[database_name][profiles_collection_name].insert_one(dbprofile.dict())
    dbprofile.id = str(inserted_row.inserted_id)

    return dbprofile


async def get_profile_for_username(conn: AsyncIOMotorClient, username: str) -> ProfileInDB:
    
    row = await conn[database_name][profiles_collection_name].find_one({"username": username})
    if not row:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Profile does not exist",
        )
    
    dbprofile = ProfileInDB(**row)
    dbprofile.id = str(row["_id"])

    return dbprofile


async def update_profile_for_username(
        conn: AsyncIOMotorClient, 
        username: str, 
        country : Country,
        bio : str,
        image : str
        ) -> ProfileInDB:

    old_profile = await get_profile_for_username(conn, username)
    new_profile = ProfileInDB(**old_profile.dict())

    new_profile.updated_at = datetime.now()
    new_profile.country = country or old_profile.country
    new_profile.bio = bio or old_profile.bio
    new_profile.image = image or old_profile.image

    await conn[database_name][profiles_collection_name].update_one({"username": old_profile.username}, {'$set': new_profile.dict()})
    return ProfileInUpdate(old_profile = old_profile, new_profile = new_profile)

async def delete_profile_for_username(conn: AsyncIOMotorClient, username: str) -> ProfileInDB:
    dbprofile = await get_profile_for_username(conn, username)
    try:
        await conn[database_name][profiles_collection_name].delete_one({"username": dbprofile.username})
    except Exception as e:
        print(e)
    return dbprofile

async def follow_profile(
    conn: AsyncIOMotorClient, 
    current_username: str, 
    target_username: str
) -> ProfileInFollow:
    target_profile = await get_profile_for_username(conn, target_username)

    if target_profile:
        await conn[database_name][followers_collection_name].insert_one({"follower": current_username,
                                                                          "following": target_profile.username})
    else:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail=f"User {target_username} not found"
        )

    return ProfileInFollow(username= target_profile.username, points = target_profile.points)
    


async def get_follower_list(conn: AsyncIOMotorClient, current_username: str) -> List[str]:
    cursor = conn[database_name][followers_collection_name].find({"following": current_username})

    if not cursor:
        followers = []
    else:
        followers = await cursor.distinct(key = "follower")

    return followers


async def get_following_list(conn: AsyncIOMotorClient, current_username: str) -> List[str]:
    cursor = conn[database_name][followers_collection_name].find({"follower": current_username})

    if not cursor:
        following = []
    else:
        following = await cursor.distinct(key = "following")

    return following


async def get_followers_count(conn: AsyncIOMotorClient, current_username: str) -> int:
    follower_count = await conn[database_name][followers_collection_name].count_documents({"following": current_username})
    return follower_count


async def get_following_count(conn: AsyncIOMotorClient, current_username: str) -> int:
    following_count = await conn[database_name][followers_collection_name].count_documents({"follower": current_username})
    return following_count


async def unfollow_profile(conn: AsyncIOMotorClient, current_username: str, target_username: str) -> ProfileInFollow:
    await conn[database_name][followers_collection_name].delete_many({"follower": current_username,
                                                                     "following": target_username})


async def is_following_profile(conn: AsyncIOMotorClient, current_username: str, target_username: str) -> bool:
    row = await conn[database_name][followers_collection_name].find_one({
                                                                        "follower": current_username,
                                                                        "following": target_username
                                                                        })
    if row:
        return True
    else:
        return False
# async def is_following_for_user(
#     conn: AsyncIOMotorClient, current_username: str, target_username: str
# ) -> bool:
#     count = await conn[database_name][followers_collection_name].count_documents({"follower": current_username,
#                                                                                   "following": target_username})
#     return count > 0