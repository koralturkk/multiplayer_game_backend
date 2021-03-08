from fastapi import FastAPI
from ml import nlp
from models import Article

app = FastAPI()


from pydantic import BaseModel
from typing import List

class Article(BaseModel):
    content: str
    comments : List[str] = []


@app.get("/")
def read_main():
    return {"message": "Hello World"}

@app.post("/article/")
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