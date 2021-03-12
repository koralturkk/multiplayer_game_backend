from app.models.article import Article
from typing import List
from fastapi import APIRouter
from motor.motor_asyncio import AsyncIOMotorClient
from app.settings.config import DB_NAME, DB_URL
from app.core.ml import nlp


router = APIRouter(
    prefix="/articles",
    tags=["articles"],
    responses={404: {"description": "Not found"}},
)





@router.post("/")
def analyze_article(articles: List[Article]):
    ents = []
    comments = []
    for article in articles:
        for comment in article.comments:
            comments.append(comment.upper())
        doc = nlp(article.content)
        for ent in doc.ents:
            ents.append({"text": ent.text, "label": ent.label})
    return {"ents": ents, "comments": comments}


@router.get('/articles')
async def list_articles():
    articles = []
    for article in router.mongodb.find():
        articles.append(Article(**article))
    return {'articles': articles}

@router.post('/articles')
async def add_text(article: Article):
    if hasattr(article, 'id'):
        delattr(article, 'id')
    ret = router.mongodb.insert_one(article.dict(by_alias=True))
    article.id = ret.inserted_id
    return {'text_input': article}