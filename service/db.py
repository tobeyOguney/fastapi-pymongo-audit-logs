from pymongo import MongoClient
from pymongo.database import Database

from service.core.config import settings


def get_client() -> Database:
    client = MongoClient(settings.MONGODB_URL)
    return client
