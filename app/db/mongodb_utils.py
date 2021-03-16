  
import logging
from motor.motor_asyncio import AsyncIOMotorClient
from core.config import DB_URL, MAX_CONNECTIONS_COUNT, MIN_CONNECTIONS_COUNT
from db.mongodb import db
import certifi

async def connect_to_mongo():
    logging.info("Starting MongoDB connection")
    db.client = AsyncIOMotorClient(str(DB_URL), tlsCAFile=certifi.where())
    logging.info("MongoDB connection completed!")

async def close_mongo_connection():
    logging.info("Closing MongoDB connection")
    db.client.close()
    logging.info("MongoDB connection closed!")
