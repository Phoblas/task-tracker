from celery import Celery

from app.core.config import settings

# Создаём экземпляр Celery
celery_app = Celery(
    "task_tracker",
    broker=settings.REDIS_BROKER_URL,  # брокер (очередь)
    backend=settings.REDIS_BACKEND_URL,  # (необязательно) — для хранения результатов
)


# Автоматически искать задачи в этом модуле
celery_app.autodiscover_tasks(["app.tasks"])

# # ✅ 👇 Явно импортируем задачу, чтобы Celery её увидел
# from app.tasks.example import send_email_task  # <-- вот это критично

@celery_app.task(name="test_hello")
def hello():
    print("HELLO FROM CELERY")