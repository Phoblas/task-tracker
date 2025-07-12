from fastapi import FastAPI

from app.api import ping, user, task, auth
from app.core.openapi import custom_openapi  # импорт кастомизации

app = FastAPI()

app.include_router(ping.router)
app.include_router(user.router)
app.include_router(task.router)
app.include_router(auth.router)

# кастомизируем openapi схему (Swagger UI с кнопкой Authorize)
custom_openapi(app)


@app.get("/")
def read_root():
    return {"message": "Task Tracker API is up!"}

