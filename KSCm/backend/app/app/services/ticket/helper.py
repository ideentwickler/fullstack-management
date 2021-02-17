from datetime import datetime
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app import crud, models

db = SessionLocal()


def get_tickets_count(
        _db: Session = db, *, start: datetime = None, end: datetime = None,
        store_internal_id: int = None, owner_id: int = None,
        kind: models.TicketKind = None, status: models.TicketStatus = None
):
    query = crud.ticket.get_query(_db)
    if start and end:
        query = query.filter(models.Ticket.created_at.between(start, end))
    if store_internal_id:
        query = query.filter(models.Ticket.store_internal_id == store_internal_id)
    if owner_id:
        query = query.filter(models.Ticket.owner_id == owner_id)
    if kind:
        query = query.filter(models.Ticket.kind == kind)
    if status:
        query = query.filter(models.Ticket.status == status)
    return query.count()


