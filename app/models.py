from typing import List
from pydantic import BaseModel
from typing import List


class Article(BaseModel):
    content: str
    comments : List[str] = []

