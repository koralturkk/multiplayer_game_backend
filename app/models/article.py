from mongoengine import Document, StringField
from bson import ObjectId
from typing import Optional
from pydantic import BaseModel, Field


class PyObjectId(ObjectId):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')


class Article(Document):
    id: Optional[PyObjectId] = Field(alias='_id')
    text = StringField(required=True, max_length=100)
    label = StringField(max_length=20)
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }

        schema_extra = {
            "example": {
                "id": "00010203-0405-0607-0809-0a0b0c0d0e0f",
                "text": "The name Google is derived from the term 'googol'. A googol is a 1 with 100 zeroes behind it!",
                "label": "facts",
            }
        }