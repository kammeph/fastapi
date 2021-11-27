from typing import Any, List
from uuid import UUID
from pydantic.main import BaseModel
from core.dao import Dao
from core.mapper import Mapper

class Service:

    def __init__(self, dao: Dao, mapper: Mapper) -> None:
        self.dao = dao
        self.mapper = mapper

    async def get_all(self) -> List[BaseModel]:
        rows = await self.dao.get_all()
        entities = []
        for row in rows:
            entities.append(await self.mapper.to_dto(row))
        return entities

    async def get(self, id: UUID) -> BaseModel:
        getResult = await self.dao.get(id)
        if getResult is not None:
            return await self.mapper.to_dto(getResult)
        return None

    async def create(self, request: Any) -> BaseModel:
        entity = await self.mapper.to_entity(request)
        insertResult = await self.dao.create(entity.dict())
        if insertResult.inserted_id is not None:
            return await self.mapper.to_dto(entity)
        return None

    async def delete(self, id: UUID) -> bool:
        return await self.dao.delete(id)

    async def update(self, id: UUID, update: Any) -> bool:
        updateRequest = await self.mapper.to_update(update)
        return await self.dao.update(id, updateRequest)