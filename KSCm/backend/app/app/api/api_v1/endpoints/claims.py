import typing as t

from pydantic import BaseModel
from fastapi import APIRouter, Depends
from fastapi_pagination import Page, pagination_params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from app.utils.service_result import handle_result
from app.services.service_claim import ClaimService
from app.api import deps
from app import schemas


router = APIRouter()


class ReadClaimsGetParams(BaseModel):
    desc: t.Optional[str] = None
    order_by: t.Optional[str] = None


@router.get("/", response_model=Page[schemas.Claim],
            dependencies=[Depends(pagination_params)])
def read_claims(
    db: Session = Depends(deps.get_db),
    request: ReadClaimsGetParams = Depends()
) -> t.Any:
    """
    Retrieve claims.
    """
    service = ClaimService(db).get_paginate_query(request=request)
    result = handle_result(service)
    return paginate(result)


@router.get("/{id}", response_model=schemas.Claim)
def read_claim(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> t.Any:
    """
    Get claim by ID.
    """
    service = ClaimService(db).get(id=id)
    return handle_result(service)
