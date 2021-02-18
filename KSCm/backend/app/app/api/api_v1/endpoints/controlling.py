import typing as t
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app import crud, models, schemas, services
from app.api import deps

router = APIRouter()


class CreateReporting(BaseModel):
    title: str
    year: int
    month_start: int
    month_end: int
    stores: t.List[int]
    email_reciepent: t.Optional[str] = None


@router.post("/create")
def read_items(
    *,
    db: Session = Depends(deps.get_db),
    create_in: CreateReporting,
    _current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    controlling_data = services.ControllingData(year=create_in.year,
                                                monthrange=[create_in.month_start,
                                                            create_in.month_end])
    controlling_context = controlling_data.get_context().dict()
    controlling_context['headline'] = create_in.title
    controlling_context['subtitle'] = 'Gesamtübersicht'

    pdf = services.PDFGenerator(save_as='ksc-attachment.pdf', view='inline')
    pdf.new_document(template="pdf/reporting/stores.html", **controlling_context)

    for store_in in create_in.stores:
        store = crud.store.get_by_kwargs(db, internal_id=store_in).first()
        store_controlling_data = services.ControllingData(
            year=create_in.year,
            monthrange=[create_in.month_start, create_in.month_end],
            store_internal_id=store.internal_id
        )
        store_controlling_context = store_controlling_data.get_context().dict()
        store_controlling_context['headline'] = create_in.title
        store_controlling_context['subtitle'] = store.name.upper()
        pdf.new_document(
            template='pdf/reporting/stores.html', **store_controlling_context
        )

    pdf.save_as()

    return {
        'msg': 'success'
    }


