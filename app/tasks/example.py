from time import sleep
from celery import Task

from app.celery_worker import celery_app


@celery_app.task(
        name="send_email_task",
        bind=True,  # 📌 bind=True нужно, чтобы внутри метода был доступ к self (Celery Task instance)
        max_retries=3,  # 📌 max_retries — сколько всего попыток (включая первую)
        default_retry_delay=60,  # 📌 default_retry_delay — задержка (в секундах) перед повторной попыткой
        acks_late=True,  # подтверджать задание после успешного выполнения
        reject_on_worker_lost=True  # Если воркер закрашится/упадёт — задача перейдёт обратно в очередь, а не будет считаться выполненной.
)
def send_email_task(self: Task, to: str, subject: str, body: str) -> str:
    """
    Фоновая задача отправки письма с retry и countdown.
    
    Аргументы:
      to (str)        — адрес получателя
      subject (str)   — тема письма
      body (str)      — содержимое письма
    
    Поведение:
      - При любой исключительной ситуации задача выбрасывает self.retry()
      - retry() автоматически подставляет countdown и увеличивает retry count
      - После превышения max_retries — инициируется FAILURE
    """

    try:
        print(f"[send_email_task] Sending email to {to} with subject: '{subject}'")
        sleep(2)  # эмуляция долгой работы

        # Имитация случайной ошибки (пример для теста retry)
        import random
        if random.choice([True, False]):
            raise ConnectionError("Simulated SMTP connection drop")

        print(f"[send_email_task] Email successfully sent to {to}")
        return f"Email sent to {to}"
    
    except Exception as exc:
        # 📌 self.request.retries — текущее число попыток (0 на первой итерации)
        retries = self.request.retries
        print(f"[send_email_task] Exception: {exc!r}; retry {retries + 1}/{self.max_retries}")

        # Повторяем задачу через default_retry_delay (или свой countdown)
        # Можно передать countdown=int, чтобы переопределить delay
        raise self.retry(exc=exc, countdown=self.default_retry_delay)