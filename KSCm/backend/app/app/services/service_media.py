import os
from uuid import UUID

import aiofiles
import typing as t
from app.schemas.media import MediaCreate
from app.utils.app_exceptions import AppException
from app.utils.service_result import ServiceResult
from app.services.main import AppService
from app.core.config import settings
from app.models.media import MediaType
from app.utils.core import generate_fixed_filename, check_valid_filename
from app import crud


class MediaService(AppService):
    """
    SERVICE object to handle all kind business logic stuff.

    """

    async def create_media(
            self, *, media_in: MediaCreate, auto_save: bool = False,
            upload: bool = False, file_content: t.Any = None,
    ) -> ServiceResult:
        if not check_valid_filename(filename=media_in.filename):
            return ServiceResult(
                AppException.MediaCreate({"message": f"file extension not allowed"}))

        if not getattr(MediaType, media_in.type, None):
            return ServiceResult(
                AppException.MediaCreate({"message": f"Unexpected Mediatype"}))

        exist_in_db = crud.media.get_by_kwargs(self.db,
                                               filename=media_in.filename).first()
        if exist_in_db:
            if not auto_save:
                return ServiceResult(AppException.MediaCreate({
                    "message": f"{media_in.filename} "
                               f"already exists [in db: {exist_in_db.id}]"}))

            fixed_filename = generate_fixed_filename(media_in.filename)
            setattr(media_in, 'filename', fixed_filename)

        if upload and file_content:
            _path = os.path.join(f'{settings.SERVER_BASE_DIR}/'
                                 + f'{settings.SERVER_MEDIA_DIR}/'
                                 + f'{media_in.filename}')
            async with aiofiles.open(_path, 'wb') as f:
                await f.write(file_content)

        media = crud.media.create(self.db, obj_in=media_in)

        if not media:
            return ServiceResult(AppException.MediaCreate())
        return ServiceResult(media)

    def get_media(self, media_id: UUID) -> ServiceResult:
        media = crud.media.get(self.db, id=media_id)
        if not media:
            return ServiceResult(AppException.MediaGet({"media_id": media_id}))
        return ServiceResult(media)

    def start_celery_task(self, media_id: UUID) -> ServiceResult:
        media = crud.media.get(self.db, id=media_id)
        if not media:
            return ServiceResult(AppException.MediaGet({"media_id": media_id}))

        from app.core.celery_app import celery_app
        from app.api.api_v1.endpoints.utils import RUNNING_TASKS

        if media.type == MediaType.IMPORT:
            task = celery_app.\
                send_task("app.worker.progress_ticket_data", args=[media.filepath])
        elif media.type == MediaType.CLAIMS:
            print("?")
            task = celery_app.\
                send_task("app.worker.progress_claim_data", args=[media.filepath])
        else:
            task = celery_app.send_task("app.worker.test_test")

        RUNNING_TASKS.append(task)
        result = {
            'task_id': task.id,
            'media_id': media.id,
        }
        return ServiceResult(result)

