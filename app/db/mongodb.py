from pymongo import MongoClient
from typing import Optional
import os

MONGO_URI = os.getenv("MONGODB_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")  # choose a DB name

client: Optional[MongoClient] = None
db = None

def get_mongo_db():
    global client, db
    if client is None:
        client = MongoClient(MONGO_URI)
        db = client[MONGO_DB_NAME]
    return db