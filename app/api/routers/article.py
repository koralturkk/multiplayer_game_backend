# from typing import Optional
# from ...core.jwt import get_current_user_authorizer

# from fastapi import APIRouter, Body, Depends, Path, Query
# from slugify import slugify
# from starlette.exceptions import HTTPException
# from ...crud.article import (
#     get_articles_with_filters,
# )

# from ...db.mongodb import AsyncIOMotorClient, get_database
# from ...models.article import (
#     ArticleFilterParams,
#     ArticleInCreate,
#     ArticleInResponse,
#     ArticleInUpdate,
#     ManyArticlesInResponse,
# )
# from ...models.user import User

# router = APIRouter()


# @router.get("/articles", response_model=ManyArticlesInResponse, tags=["articles"])
# async def get_articles(
#         tag: str = "",
#         author: str = "",
#         favorited: str = "",
#         limit: int = Query(20, gt=0),
#         offset: int = Query(0, ge=0),
#         user: User = Depends(get_current_user_authorizer(required=False)),
#         db: AsyncIOMotorClient = Depends(get_database),
# ):
#     filters = ArticleFilterParams(
#         tag=tag, author=author, favorited=favorited, limit=limit, offset=offset
#     )
#     dbarticles = await get_articles_with_filters(
#         db, filters, user.username if user else None
#     )
#     return create_aliased_response(
#         ManyArticlesInResponse(articles=dbarticles, articles_count=len(dbarticles))
#     )