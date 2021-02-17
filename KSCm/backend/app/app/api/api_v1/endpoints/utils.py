from typing import Any

from fastapi import APIRouter, Depends, BackgroundTasks
from pydantic.networks import EmailStr

from app import models, schemas
from app.api import deps
from app.core.celery_app import celery_app, background_on_message
from app.utils import send_test_email

router = APIRouter()


@router.post("/test-celery/", response_model=schemas.Msg, status_code=201)
def test_celery(
    msg: schemas.Msg,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Test Celery worker.
    """
    celery_app.send_task("app.worker.test_celery", args=[msg.msg])
    return {"msg": "Word received"}


@router.get("/test-import/")
def test_progress_ticket_data(background_task: BackgroundTasks) -> Any:
    task = celery_app.send_task("app.worker.progress_ticket_data")
    background_task.add_task(background_on_message, task)
    return {
        'msg': 'processing...'
    }


@router.post("/test-email/", response_model=schemas.Msg, status_code=201)
def test_email(
    email_to: EmailStr,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Test emails.
    """
    send_test_email(email_to=email_to)
    return {"msg": "Test email sent"}
