from typing import TypeVar

from app.utils.app_exceptions import AppException
from app.utils.service_result import ServiceResult
from app.services.main import AppService
from pydantic import BaseModel

from app import crud, models

RequestType = TypeVar("RequestParameter", bound=BaseModel)


class ClaimService(AppService):
    """
    SERVICE object to handle all kind business logic stuff.

    """
    def get_paginate_query(self, *, request: RequestType):
        query = crud.claim.get_query(self.db)
        if request.order_by:
            get_attr = getattr(models.Claim, request.order_by, None)
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

    def get(self, *, id: int):
        query = crud.claim.get_by_kwargs(self.db, id=id).first()
        if not query:
            return ServiceResult(AppException.MediaGet())
        return ServiceResult(query)

