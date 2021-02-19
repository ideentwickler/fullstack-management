from typing import Optional
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel

from app.models.media import MediaType


# Shared properties
class MediaBase(BaseModel):
    type: Optional[MediaType] = None
    filename: Optional[str] = None
    created_at: Optional[datetime] = None


# Properties to receive on item creation
class MediaCreate(MediaBase):
    title: str


# Properties to receive on item update
class MediaUpdate(MediaBase):
    pass


# Properties shared by models stored in DB
class MediaInDBBase(MediaBase):
    id: UUID
    title: str
    owner_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Media(MediaInDBBase):
    pass


# Properties properties stored in DB
class MediaInDB(MediaInDBBase):
    pass