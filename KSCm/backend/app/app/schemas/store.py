from typing import Optional, Any

from pydantic import BaseModel, ValidationError, validator

from app.models.store import StoreSupport


# Shared properties
class StoreBase(BaseModel):
    internal_id: Optional[int] = None
    name: Optional[str] = None
    support: Optional[StoreSupport] = None


# Properties to receive on item creation
class StoreCreate(StoreBase):
    internal_id: int
    name: str
    support: Any

    @validator('name')
    def name_must_be_upper(cls, v):
        return v.upper()


# Properties to receive on item update
class StoreUpdate(StoreBase):
    @validator('name')
    def name_must_be_upper(cls, v):
        return v.upper()


# Properties shared by models stored in DB
class StoreInDBBase(StoreBase):
    id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Store(StoreInDBBase):
    pass


# Properties properties stored in DB
class StoreInDB(StoreInDBBase):
    pass
