import json
import typing as t

from fastapi import APIRouter, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from fastapi_cache.backends.redis import RedisCacheBackend

from app import crud, models, schemas, services
from app.api import deps
from app.core.redis import redis_cache
from app.utils.service_result import handle_result


router = APIRouter()


@router.get("/static")
async def get_static(db: Session = Depends(deps.get_db), cache: RedisCacheBackend = Depends(redis_cache)):
    in_cache = await cache.get('some_cached_key7')
    if not in_cache:
        result = services.StaticDataService(db).get()
        json_dump = json.dumps(result.value)
        await cache.set('some_cached_key7', json_dump)
        await cache.expire('some_cached_key7', 50000)
        return result.value

    return json.loads(in_cache)


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
    media_in.owner_id = current_user.id
    result = services.MediaService(db).create_media(media_in=media_in, auto_save=False)
    return handle_result(result)


@router.post("/create")
def create_reporting(
    *,
    db: Session = Depends(deps.get_db),
    create_in: CreateReporting,
    _current_user: models.User = Depends(deps.get_current_active_user),
) -> t.Any:
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
            owner_id=_current_user.id,
        )
        media = crud.media.create(db, obj_in=db_obj)
        return {
            'file': f'{media.id}',
        }

    return {
        'msg': 'success',
    }


