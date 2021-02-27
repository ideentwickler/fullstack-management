import typing as t
from uuid import UUID
from typing import Any, List

from fastapi import APIRouter, File, UploadFile, Depends
from sqlalchemy.orm import Session

from app.utils.service_result import handle_result
from app import crud, models, schemas
from app.services import MediaService
from app.api import deps

router = APIRouter()


@router.post("/", response_model=schemas.Media)
async def create_upload_media(
        *,
        db: Session = Depends(deps.get_db),
        file: UploadFile = File(...),
        progress: str = None,
) -> Any:
    content = await file.read()
    media_in = schemas.MediaCreate(type=models.MediaType.IMPORT, filename=file.filename, owner_id=1)

    upload_and_create = await MediaService(db).\
        create_media(media_in=media_in, auto_save=True,
                     upload=True, file_content=content)
    return handle_result(upload_and_create)


@router.get("/", response_model=t.List[schemas.Media])
async def get_media(*, db: Session = Depends(deps.get_db)) -> Any:
    media = crud.media.get_multi(db)
    return media


@router.get("/{id}")
def get_media_one(*, db: Session = Depends(deps.get_db), id: UUID, task: bool = False):
    media = MediaService(db).get_media(media_id=id)
    if task:
        media = MediaService(db).start_celery_task(media_id=id)
    return handle_result(media)
