from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.ticket import Ticket
from app.schemas.ticket import TicketCreate, TicketUpdate


class CRUDTicket(CRUDBase[Ticket, TicketCreate, TicketUpdate]):
    def create(self, db: Session, *, obj_in: TicketCreate) -> Ticket:
        db_obj = Ticket(
            ticket_id=obj_in.ticket_id,
            contract_nr=obj_in.contract_nr,
            customer_name=obj_in.customer_name,
            status=obj_in.status,
            kind=obj_in.kind,
            owner_id=obj_in.owner_id,
            store_internal_id=obj_in.store_internal_id,
            created_at=obj_in.created_at,
            updated_at=obj_in.updated_at,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


ticket = CRUDTicket(Ticket)
