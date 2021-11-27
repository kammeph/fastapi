from json import dumps, loads
from uuid import UUID
from pythondi import inject
from pydantic.main import BaseModel
from pymongo.cursor import Cursor
from pymongo.results import InsertOneResult
from db.database import Cache, DatabaseContext

class Dao():
    @inject(db=DatabaseContext, cache=Cache)
    def __init__(self, db: DatabaseContext, cache: Cache, collection: str, use_cache: bool = False) -> None:
        self.db = db
        self.cache = cache
        self.use_cache = use_cache
        self.collection = collection
        self.db[self.collection].create_index(keys=[("id", 1)], unique=True)

    async def get_all(self) -> Cursor:
        return self.db[self.collection].find()

    async def get(self, id: UUID):
        if self.use_cache and self.cache.exists(str(id)):
            return loads(self.cache.get(str(id)))
        return self.db[self.collection].find_one({"id": id})

    async def create(self, requestDict: dict) -> InsertOneResult:
        return self.db[self.collection].insert_one(requestDict)

    async def delete(self, id: UUID) -> bool:
        delete_result = self.db[self.collection].delete_one({"id": id})
        await self.cache_clear_entity(id)
        return delete_result.deleted_count > 0

    async def update(self, id: UUID, update: BaseModel) -> bool:
        update_result = self.db[self.collection].update_one({"id": id}, { "$set": update.dict() })
        await self.cache_entity(id)
        return update_result.matched_count > 0

    async def cache_entity(self, id: UUID):
        entity = self.db[self.collection].find_one({"id": id})
        if self.use_cache and entity is not None:
            self.cache.set(str(id), dumps(entity, default=str))
            
    async def cache_clear_entity(self, id: UUID):
        if self.use_cache and self.cache.exists(str(id)):
            self.cache.delete(str(id))