from celery import Celery

celery_app = Celery(
    "worker",
    backend="redis://:password123@redis:6379/0",
    broker="amqp://user:bitnami@rabbitmq:5672//",
)

celery_app.conf.task_routes = {
    "app.worker.test_celery": "main-queue",
    "app.worker.progress_ticket_data": "main-queue",
}

celery_app.conf.beat_schedule = {
    "run-every-ten-seconds": {
        "task": "app.worker.checker",
        "schedule": 10.0,
    }
}

celery_app.conf.update(task_track_started=True)


def celery_on_message(body):
    print(body)


def background_on_message(task):
    print(task.get(on_message=celery_on_message, propagate=False))

