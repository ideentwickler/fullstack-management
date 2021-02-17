from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Ticket])
def read_tickets(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 999,
    _current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve stores.
    """
    tickets = crud.store.get_multi(db, skip=skip, limit=limit)
    return tickets


@router.put("/{ticket_id}", response_model=schemas.Ticket)
def update_ticket(
    *,
    db: Session = Depends(deps.get_db),
    ticket_id: int,
    ticket_in: schemas.TicketUpdate,
    _current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an ticket.
    """
    ticket = crud.ticket.get_by_kwargs(db, ticket_id=ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    store = crud.store.update(db, db_obj=ticket, obj_in=ticket_in)
    return store


@router.get("/{ticket_id}", response_model=schemas.Store)
def read_ticket(
    *,
    db: Session = Depends(deps.get_db),
    ticket_id: int,
    _current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get ticket by ID.
    """
    ticket = crud.ticket.get_by_kwargs(db, ticket_id=ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

