from fastapi import APIRouter

from .routers.article import router as article_router

router = APIRouter()
router.include_router(article_router)

# @router.get("/")
# async def root():
#     return {"message": "Hello Bigger Applications!"}

