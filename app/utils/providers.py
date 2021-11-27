from pythondi import Provider
from db.database import Cache, DatabaseContext
from user.dao import UserDao
from user.mapper import UserMapper

provider = Provider()
provider.bind(DatabaseContext, DatabaseContext)
provider.bind(Cache, Cache)
provider.bind(UserDao, UserDao)
provider.bind(UserMapper, UserMapper)