from typing import Optional, Any
from datetime import datetime
from pydantic import BaseModel

from app.models.ticket import TicketStatus, TicketKind


# Shared properties
class TicketBase(BaseModel):
    ticket_id: Optional[int] = None
    contract_nr: Optional[int] = None
    customer_name: Optional[str] = None
    status: Optional[TicketStatus] = None
    kind: Optional[TicketKind] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    store_internal_id: Optional[int] = None
    owner_id: Optional[int] = None


# Properties to receive on item creation
class TicketCreate(TicketBase):
    ticket_id: int
    contract_nr: int
    customer_name: str
    status: Any
    kind: Any
    owner_id: int
    store_internal_id: int


# Properties to receive on item update
class TicketUpdate(TicketBase):
    status: Any
    owner_id: Optional[int]
    updated_at: datetime


# Properties shared by models stored in DB
class TicketInDBBase(TicketBase):
    id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Ticket(TicketInDBBase):
    pass


# Properties properties stored in DB
class TicketInDB(TicketInDBBase):
    pass
