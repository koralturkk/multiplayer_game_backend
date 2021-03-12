  
import logging
from motor.motor_asyncio import AsyncIOMotorClient
from app.settings.config import DB_URL
from .mongodb import db


async def connect_to_mongo():
    logging.info("Starting MongoDB connection")
    db.client = AsyncIOMotorClient(DB_URL)
    logging.info("MongoDB connection completed!")


async def close_mongo_connection():
    logging.info("Closing MongoDB connection")
    db.client.close()
    logging.info("MongoDB connection closed!")

