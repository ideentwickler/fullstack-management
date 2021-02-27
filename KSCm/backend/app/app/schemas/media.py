from typing import Optional, Any
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel

from app.models.media import MediaType


# Shared properties
class MediaBase(BaseModel):
    type: Optional[MediaType] = None
    filename: Optional[str] = None
    owner_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


# Properties to receive on item creation
class MediaCreate(MediaBase):
    type: Optional[Any] = MediaType.OTHER.name
    filename: str

    class Config:
        schema_extra = {
            "example": {
                "filename": "filename with allowed extension",
                "type": "every kind of MediaType"
            }
        }


# Properties to receive on item update
class MediaUpdate(MediaBase):
    pass


# Properties shared by models stored in DB
class MediaInDBBase(MediaBase):
    id: UUID

    class Config:
        orm_mode = True


# Properties to return to client
class Media(MediaInDBBase):
    pass


# Properties properties stored in DB
class MediaInDB(MediaInDBBase):
    pass
