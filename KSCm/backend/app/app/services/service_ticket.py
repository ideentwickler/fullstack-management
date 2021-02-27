from typing import TypeVar

from app.schemas.media import MediaCreate
from app.utils.app_exceptions import AppException
from app.utils.service_result import ServiceResult
from app.services.main import AppService
from pydantic import BaseModel

from app.utils.core import generate_fixed_filename, check_valid_filename
from app import crud, models

RequestType = TypeVar("RequestParameter", bound=BaseModel)


class TicketService(AppService):
    """
    SERVICE object to handle all kind business logic stuff.

    """
    def get_paginate_query(self, *, request: RequestType):
        query = crud.ticket.get_query(self.db)
        if request.order_by:
            get_attr = getattr(models.Ticket, request.order_by, None)
            if get_attr is None:
                return ServiceResult(
                    AppException.MediaGet({"error": "invalid attribute"}))

            if request.desc is None\
                    or request.desc == 'null'\
                    or request.desc == 'false':
                get_attr = get_attr.desc()
            else:
                get_attr = get_attr.asc()
            query = query.order_by(get_attr)
        return ServiceResult(query)

    def get(self, *, ticket_id: int):
        query = crud.ticket.get_by_kwargs(self.db, ticket_id=ticket_id).first()
        if not query:
            return ServiceResult(AppException.MediaGet())
        return ServiceResult(query)

