from typing import Any, List, Optional, Union, TypeVar

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination import Page, pagination_params

from app.utils.service_result import handle_result
from app.services.service_ticket import TicketService
from app import crud, schemas
from app.api import deps

router = APIRouter()


class ReadTicketsGetParams(BaseModel):
    desc: Optional[str] = None
    order_by: Optional[str] = None


@router.get("/", response_model=Page[schemas.Ticket],
            dependencies=[Depends(pagination_params)])
def read_tickets(db: Session = Depends(deps.get_db),
                 request: ReadTicketsGetParams = Depends()) -> Any:
    """
    Retrieve tickets.
    """
    service = TicketService(db).get_paginate_query(request=request)
    result = handle_result(service)
    return paginate(result)


@router.get("/{ticket_id}", response_model=schemas.Ticket)
def read_ticket(*, ticket_id: int, db: Session = Depends(deps.get_db)) -> Any:
    """
    Get ticket by ticket_id.
    """
    service = TicketService(db).get(ticket_id=ticket_id)
    result = handle_result(service)
    return result

