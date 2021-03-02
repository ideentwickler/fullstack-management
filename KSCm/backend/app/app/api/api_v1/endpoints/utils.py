from typing import Any

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from pydantic.networks import EmailStr

from app import models, schemas
from app.api import deps
from app.core.celery_app import celery_app
from app.utils import send_test_email

router = APIRouter()

RUNNING_TASKS = []


@router.post("/test-celery/")
async def test_celery(
    *,
    msg: schemas.Msg,
) -> Any:
    """
    Test Celery worker.
    """
    task = celery_app.send_task("app.worker.test_celery", args=[msg.msg])
    print("task", task, "status", task.status)

    task_two = celery_app.send_task("app.worker.test_test")
    RUNNING_TASKS.append(task_two)
    print("task_two", task_two, "status", task_two.status)

    return {
        "task_id": task_two.id,
    }


class TaskStatusResponse(BaseModel):
    result: str


@router.get("/task-status/")
async def test_task_status(task_id: str = None):
    for task in RUNNING_TASKS:
        if task == task_id:
            return {
                'result': task.status
            }
    return 'failed'


@router.get("/test-import/")
async def test_progress_ticket_data() -> Any:
    task = celery_app.send_task("app.worker.progress_ticket_data")
    RUNNING_TASKS.append(task)
    if task:
        return {
            'task_id': task.id,
        }

@router.get("/test-claim-import/")



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
