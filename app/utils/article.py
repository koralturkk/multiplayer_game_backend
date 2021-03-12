from typing import List, Optional
from bson import ObjectId
from slugify import slugify
from datetime import datetime
from ..db.mongodb import AsyncIOMotorClient
from ..settings.config import COLLECTION_NAME, DB_NAME
from ..models.article import ArticleInDB,Article


async def get_article_by_slug(
    conn: AsyncIOMotorClient, slug: str, username: Optional[str] = None
) -> ArticleInDB:
    article_doc = await conn[DB_NAME][COLLECTION_NAME].find_one({"slug": slug})
    if article_doc:
        article_doc["author"] = await get_profile_for_user(conn, article_doc["author_id"])

        return ArticleInDB(
            **article_doc,
            created_at=ObjectId(article_doc["_id"]).generation_time
        )


async def create_article_by_slug(
    conn: AsyncIOMotorClient, article: ArticleInCreate, username: str
) -> ArticleInDB:
    slug = slugify(article.title)
    article_doc = article.dict()
    article_doc["slug"] = slug
    article_doc["author_id"] = username
    article_doc["updated_at"] = datetime.now()
    await conn[database_name][article_collection_name].insert_one(article_doc)

    if article.tag_list:
        await create_tags_that_not_exist(conn, article.tag_list)

    author = await get_profile_for_user(conn, username, "")
    return ArticleInDB(
        **article_doc,
        created_at=ObjectId(article_doc["_id"]).generation_time,
        author=author,
        favorites_count=1,
        favorited=True,
    )


async def update_article_by_slug(
    conn: AsyncIOMotorClient, slug: str, article: ArticleInUpdate, username: str
) -> ArticleInDB:
    dbarticle = await get_article_by_slug(conn, slug, username)

    if article.title:
        dbarticle.slug = slugify(article.title)
        dbarticle.title = article.title
    dbarticle.body = article.body if article.body else dbarticle.body
    dbarticle.description = (
        article.description if article.description else dbarticle.description
    )
    if article.tag_list:
        await create_tags_that_not_exist(conn, article.tag_list)
        dbarticle.tag_list = article.tag_list

    dbarticle.updated_at = datetime.now()
    await conn[database_name][article_collection_name].replace_one({"slug": slug, "author_id": username}, dbarticle.dict())

    dbarticle.created_at = ObjectId(dbarticle.id).generation_time
    return dbarticle


async def delete_article_by_slug(conn: AsyncIOMotorClient, slug: str, username: str):
    await conn[database_name][article_collection_name].delete_many({"author_id": username,
                                                                    "slug": slug})


async def get_user_articles(
    conn: AsyncIOMotorClient, username: str, limit=20, offset=0
) -> List[ArticleInDB]:
    articles: List[ArticleInDB] = []
    article_docs = conn[database_name][article_collection_name].find({"author_id": username},
                                                                       limit=limit, skip=offset)
    async for row in article_docs:
        slug = row["slug"]
        author = await get_profile_for_user(conn, row["author_id"], username)
        tags = await get_tags_for_article(conn, slug)
        favorites_count = await get_favorites_count_for_article(conn, slug)
        favorited_by_user = await is_article_favorited_by_user(conn, slug, username)
        articles.append(
            ArticleInDB(
                **row,
                author=author,
                created_at=ObjectId(row["_id"]).generation_time,
                favorites_count=favorites_count,
                favorited=favorited_by_user,
            )
        )
    return articles


async def get_articles_with_filters(
    conn: AsyncIOMotorClient, filters: ArticleFilterParams, username: Optional[str] = None
) -> List[ArticleInDB]:
    articles: List[ArticleInDB] = []
    base_query = {}

    if filters.tag:
        base_query["tag_list"] = f"$all: [\"{filters.tag}\"]"

    if filters.favorited:
        base_query["slug"] = f"$in: [\"{filters.favorited}\"]"

    if filters.author:
        base_query["author"] = f"$in: [\"{filters.author}]\""

    rows = conn[database_name][article_collection_name].find({"author_id": username},
                                                             limit=filters.limit,
                                                             skip=filters.offset)

    async for row in rows:
        slug = row["slug"]
        author = await get_profile_for_user(conn, row["author_id"], username)
        tags = await get_tags_for_article(conn, slug)
        favorites_count = await get_favorites_count_for_article(conn, slug)
        favorited_by_user = await is_article_favorited_by_user(conn, slug, username)
        articles.append(
            ArticleInDB(
                **row,
                author=author,
                created_at=ObjectId(row["_id"]).generation_time,
                favorites_count=favorites_count,
                favorited=favorited_by_user,
            )
        )
    return articles