from core.jwt import get_current_active_user
from fastapi import APIRouter, Body, Depends, Path, Query
from db.mongodb import AsyncIOMotorClient, get_database
from models.profile import (
    Country,
)
from models.user import User
from models.leaderboard import (
    Leaderboard
)
from crud.leaderboard import (
    get_leaderboard
)

router= APIRouter(prefix= "/leaderboard")


@router.get("/",response_model=Leaderboard, tags=["leaderboard"])
async def retrieve_leaderboard(
    by_country: Country = Query(None, description= "Retrieves the leaderboard by country. If None, all players are ranked"),
    length: int = Query(10, description= "Number of profiles to retrieve in leaderboard"),
    db: AsyncIOMotorClient=Depends(get_database),
    current_user: User=Depends(get_current_active_user)):

    leaderboard_list = await get_leaderboard(by_country= by_country, length = length, conn = db)
    leaderboard = Leaderboard(leaderboard_list=leaderboard_list)
    return leaderboard


