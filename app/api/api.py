from fastapi import APIRouter

from api.routers.user import router as user_router
from api.routers.authentication import router as authentication_router
from api.routers.profile import router as profile_router
from api.routers.follow import router as follow_router
from api.routers.leaderboard import router as leaderboard_router

router = APIRouter()
router.include_router(authentication_router)
router.include_router(user_router)
router.include_router(profile_router)
router.include_router(follow_router)
router.include_router(leaderboard_router)
