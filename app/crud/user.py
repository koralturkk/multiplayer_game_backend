from db.mongodb import AsyncIOMotorClient
from pydantic import EmailStr
from bson.objectid import ObjectId
from core.config import database_name, users_collection_name
from models.user import UserInCreate, UserInDB, UserInUpdate, UserInLogin
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from starlette.exceptions import HTTPException
import datetime



async def get_user(conn: AsyncIOMotorClient, username: str) -> UserInDB:
    row = await conn[database_name][users_collection_name].find_one({"username": username})
    if row:
        return UserInDB(**row)

async def get_user_by_email(conn: AsyncIOMotorClient, email: EmailStr) -> UserInDB:
    row = await conn[database_name][users_collection_name].find_one({"email": email})
    if row:
        return UserInDB(**row)

async def create_user(conn: AsyncIOMotorClient, user: UserInCreate) -> UserInDB:
    dbuser = UserInDB(**user.dict())
    dbuser.change_password(user.password)
    dbuser.created_at = datetime.now()
    dbuser.updated_at = datetime.now()

    row = await conn[database_name][users_collection_name].insert_one(dbuser.dict())
    dbuser.id = row.inserted_id

    return dbuser

async def update_user(conn: AsyncIOMotorClient, username: str, user: UserInUpdate) -> UserInDB:
    dbuser = await get_user(conn, username)

    dbuser.username = user.username or dbuser.username
    dbuser.email = user.email or dbuser.email
    dbuser.bio = user.bio or dbuser.bio
    dbuser.image = user.image or dbuser.image
    if user.password:
        dbuser.change_password(user.password)

    dbuser.updated_at = datetime.now()
    await conn[database_name][users_collection_name].update_one({"username": dbuser.username}, {'$set': dbuser.dict()})
    return dbuser


async def delete_user(conn: AsyncIOMotorClient, user : UserInLogin) -> UserInDB:
    dbuser = await get_user_by_email(conn, user.email)
    if not dbuser or not dbuser.check_password(user.password):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Incorrect username or password"
        )
    try:
        await conn[database_name][users_collection_name].delete_one({"email": user.email})
    except Exception as e:
        print(e)

    return dbuser