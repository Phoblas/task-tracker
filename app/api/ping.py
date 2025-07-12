from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from celery.result import AsyncResult
from pydantic import BaseModel

from app.tasks.example import send_email_task
from app.db.deps import get_db
from app.celery_worker import celery_app

router = APIRouter(prefix="/ping", tags=["ping"])


class PingResponse(BaseModel):
    message: str


@router.get("/ping", response_model=PingResponse, summary="Healthcheck")
async def ping(_: AsyncSession = Depends(get_db)) -> PingResponse:
    """
    Проверка доступности сервиса и базы данных.

    Returns:
        JSON сообщение { "message": "pong" }
    """
    return PingResponse(message="pong")


@router.get("/send-test-email")
def send_fake_email():
    """
    Запускает фоновую задачу и возвращает её ID.
    """

    task = send_email_task.delay(
        "test@example.com",
        "Hello",
        "This is a test"
    )
    return {"task_id": task.id}


@router.get("task-status/{task_id}")
def get_task_status(task_id: str):
    """
    Проверяет статус выполнения Celery-задачи.
    """

    result = AsyncResult(task_id, app=celery_app)

    match result.state:
        case "PENDING":
            return {"status": "pending"}
        case "STARTED":
            return {"status": "in progress"}
        case "SUCCESS":
            return {"status": "success", "result": result.result}
        case "FAILURE":
            return {
                "status": "failure",
                "error": str(result.result)
            }
        case _:
            raise HTTPException(status_code=500, detail="Unknown task state")