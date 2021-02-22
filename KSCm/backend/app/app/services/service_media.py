from app.schemas.media import MediaCreate
from app.utils.app_exceptions import AppException
from app.utils.service_result import ServiceResult
from app.services.main import AppService

from app.utils.core import generate_fixed_filename
from app import crud


class MediaService(AppService):
    def create_media(
            self, *, media_in: MediaCreate, auto_save: bool = False
    ) -> ServiceResult:
        exist_in_db = crud.media.get_by_kwargs(self.db,
                                               filename=media_in.filename).first()
        if exist_in_db:
            # IF FILENAME EXIST IN DB AND AUTO SAVE IS FALSE
            if not auto_save:
                return ServiceResult(AppException.MediaCreate(
                    {"message": f"{media_in.filename} already exists "
                                + f"[in db: {exist_in_db.id}]"}
                ))
            # OTHERWISE WE GENERATE A NEW FILENAME
            new_filename = generate_fixed_filename(media_in.filename)
            # AND OVERWRITE THE MEDIA_IN FILENAME
            media_in.filename = new_filename

        media = crud.media.create(self.db, obj_in=media_in)
        if not media:
            return ServiceResult(AppException.MediaCreate())
        return ServiceResult(media)

    def get_media(self, media_id: int) -> ServiceResult:
        media = crud.media.get(self.db, id=media_id)
        if not media:
            return ServiceResult(AppException.MediaGet({"media_id": media_id}))
        return ServiceResult(media)
