from core.mapper import Mapper
from user.models import User, UserInDb, UserUpdate

class UserMapper(Mapper):
    async def to_entity(self, obj) -> UserInDb:
        return UserInDb.parse_obj(obj)

    async def to_dto(self, obj) -> User:
        return User.parse_obj(obj)

    async def to_update(self, obj) -> UserUpdate:
        return UserUpdate.parse_obj(obj)