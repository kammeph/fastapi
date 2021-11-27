from core.dao import Dao

class UserDao(Dao):
    def __init__(self) -> None:
        super().__init__(collection='users', use_cache=True)
        self.db[self.collection].create_index(keys=[("username", 1)], unique=True)
        
    async def get_user_by_name(self, name: str):
        return self.db[self.collection].find_one({"username": name})