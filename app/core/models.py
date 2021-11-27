from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import datetime

class DbModel(BaseModel):
    id: UUID = Field(default_factory=lambda: uuid4())

class DbCreated(BaseModel):
    created_at: datetime = Field(default_factory=lambda: datetime.now())

class DbUpdated(BaseModel):
    updated_at: datetime = Field(default_factory=lambda: datetime.now())