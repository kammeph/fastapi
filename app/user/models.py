from typing import List, Optional
from pydantic import BaseModel
from enum import Enum
from pydantic.fields import Field
from core.models import DbModel, DbCreated, DbUpdated
from utils.security import Role

class Gender(str, Enum):
    male = "male"
    female = "female"

class UserBase(BaseModel):
    username: str
    gender: Gender
    active: bool = Field(default_factory=lambda: True)
    roles: Optional[List[Role]] = Field(default_factory=lambda: ["users"])

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase, DbUpdated):
    pass

class User(UserBase, DbUpdated, DbCreated, DbModel):
    pass

class UserInDb(User):
    password_hash: str