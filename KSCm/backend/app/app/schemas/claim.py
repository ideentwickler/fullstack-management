from typing import Optional, Any
from datetime import datetime
from pydantic import BaseModel

from app.models.claim import ClaimKind


# Shared properties
class ClaimBase(BaseModel):
    contract_nr: Optional[int] = None
    bill: Optional[float] = None
    discharge: Optional[float] = None
    kind: Optional[ClaimKind] = None
    ticket_id: Optional[int] = None
    owner_id: Optional[int] = None
    store_internal_id: Optional[int] = None
    created_at: Optional[datetime] = None


# Properties to receive on item creation
class ClaimCreate(ClaimBase):
    contract_nr: int
    bill: float
    discharge: Optional[float]
    kind: Any
    ticket_id: int
    owner_id: int
    store_internal_id: int
    created_at: datetime


# Properties to receive on item update
class ClaimUpdate(ClaimBase):
    bill: float
    discharge: Optional[float]


# Properties shared by models stored in DB
class ClaimInDBBase(ClaimBase):
    id: int
    owner_id: int
    store_internal_id: int
    ticket_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Claim(ClaimInDBBase):
    pass


# Properties properties stored in DB
class ClaimInDB(ClaimInDBBase):
    pass
