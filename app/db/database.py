import os
from pymongo.database import Database
from pymongo.mongo_client import MongoClient
from redis import Redis

class DatabaseContext(Database):
    def __init__(self):
        client = MongoClient(
            host=os.environ.get('MONGO_HOST'), 
            port=int(os.environ.get('MONGO_PORT')),
            username=os.environ.get('MONGO_INITDB_ROOT_USERNAME'),
            password=os.environ.get('MONGO_INITDB_ROOT_PASSWORD'))
        super().__init__(client, os.environ.get('MONGO_INITDB_DATABASE'))

class Cache(Redis):
    def __init__(self):
        super().__init__(
            host=os.environ.get('REDIS_HOST'), 
            port=int(os.environ.get('REDIS_PORT')),
            db=0)
