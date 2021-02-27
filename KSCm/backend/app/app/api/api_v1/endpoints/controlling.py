import typing as t
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from app.utils.service_result import handle_result
from app import crud, models, schemas, services
from app.api import deps

router = APIRouter()


class CreateReporting(BaseModel):
    title: str
    year: int
    month_start: int
    month_end: int
    stores: t.List[int]
    email_reciepent: t.Optional[EmailStr] = None
    filename: t.Optional[str] = None


@router.post("/media", summary="Create Media", response_model=schemas.Media)
def media_test(
        media_in: schemas.MediaCreate,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user),
):
    #  media_in.owner_id = current_user.id
    result = services.MediaService(db).create_media(media_in=media_in,
                                                    owner_id=current_user.id,
                                                    auto_save=False)
    return handle_result(result)


@router.post("/create")
def create_reporting(
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
    controlling_context['subtitle'] = 'Gesamtübersicht'.upper()

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

    save_as_filename = pdf.save_as(filename=create_in.filename)

    if save_as_filename:
        db_obj = schemas.MediaCreate(
            type=models.MediaType.REPORTING,
            filename=f'{save_as_filename}.pdf',
        )
        media = crud.media.create_with_owner(
            db, obj_in=db_obj, owner_id=_current_user.id
        )
        return {
            'file': f'{media.id}',
        }

    return {
        'msg': 'success',
    }


