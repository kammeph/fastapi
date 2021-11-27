
from uuid import UUID
from passlib.context import CryptContext
from pythondi import inject
from core.service import Service
from user.mapper import UserMapper
from user.models import User, UserCreate, UserInDb
from user.dao import UserDao

class UserService(Service):
    __pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")
    
    @inject()
    def __init__(self, dao: UserDao, mapper: UserMapper) -> None:
        super().__init__(dao, mapper)
        self.dao = dao

    async def get_by_name(self, name: str):
        getResult = await self.dao.get_user_by_name(name)
        if getResult is not None:
            user = User(**getResult)
            return user
        return None

    async def authenticate_user(self, name: str, password: str) -> User:
        getResult = await self.dao.get_user_by_name(name)
        if getResult is not None:
            user = UserInDb.parse_obj(getResult)
            if await self.__verify_password(password, user.password_hash):
                authenticated_user = User.parse_obj(user)
                await self.dao.cache_entity(user.id)
                return authenticated_user
        return None

    async def create(self, request: UserCreate) -> User:
        password_hash = await self.__get_password_hash(request.password)
        entity = UserInDb(password_hash=password_hash, **request.dict())
        return await super().create(entity)

    async def clear_from_cache(self, id: UUID):
        await self.dao.cache_clear_entity(id)

    async def patch_password(self, id: UUID, password: str):
        password_hash = await self.__get_password_hash(password)
        return await self.dao.update(id, { "password_hash": password_hash })

    async def __verify_password(self, plain_password, hashed_password):
        return self.__pwd_context.verify(plain_password, hashed_password)

    async def __get_password_hash(self, password):
        return self.__pwd_context.hash(password)
