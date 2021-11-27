from abc import ABC, abstractclassmethod
from pydantic.main import BaseModel

class Mapper(ABC):
    @abstractclassmethod
    async def to_entity(self, obj) -> BaseModel:
        pass

    @abstractclassmethod
    async def to_dto(self, obj) -> BaseModel:
        pass

    @abstractclassmethod
    async def to_update(self, obj) -> BaseModel:
        pass