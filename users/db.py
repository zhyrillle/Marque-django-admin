from pymongo import MongoClient
from django.conf import settings
import os

_client = None


def get_db():
    global _client
    if _client is None:
        _client = MongoClient(os.getenv('MONGO_URI'))
    return _client[os.getenv('MONGO_DB_NAME', 'marque_db')]


def get_users_collection():
    return get_db()['users']
