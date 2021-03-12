from typing import List, Optional
from pydantic import Field, Schema
from .mongo_model import MongoModel, OID
from .profile import Profile


class ArticleBase(MongoModel):
    id: OID = Field()
    title: str
    body: str
    tag_list: List[str] = Schema([], alias="tagList")
    

class Article(ArticleBase):
    slug: str
    author: Profile


class ArticleInDB(Article):
    pass


class ArticleInResponse(MongoModel):
    article: Article


class ManyArticlesInResponse(MongoModel):
    articles: List[Article]
    articles_count: int = Schema(..., alias="articlesCount")


class ArticleInCreate(ArticleBase):
    pass


class ArticleInUpdate(MongoModel):
    title: Optional[str] = None
    body: Optional[str] = None
    tag_list: List[str] = Schema([], alias="tagList")


# @app.post('/me', response_model=User)
# def save_me(body: User):
#   assert isinstance(body.id, ObjectId)
#   res = db.insert_one(body.mongo())
#   assert res.inserted_id == body.id

#   found = col.find_one({'_id': res.inserted_id})
#   return User.from_mongo(found)


