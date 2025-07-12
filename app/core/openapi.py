from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

def custom_openapi(app: FastAPI) -> None:
    """
    Генерация кастомной схемы OpenAPI с поддержкой авторизации через JWT (Bearer).
    Это позволяет отображать кнопку Authorize в Swagger UI и использовать токен.
    
    Args:
        app (FastAPI): Экземпляр приложения FastAPI
    """

    if app.openapi_schema:
        return
    
    openapi_schema = get_openapi(
        title="FastAPI Task Tracker",
        version="1.0.0",
        description="Документация API с авторизацией через JWT",
        routes=app.routes,
    )

    # 🛠 Создаём ключ components, если его нет
    openapi_schema.setdefault("components", {})

    # 🔐 Добавляем схему авторизации (JWT через Bearer)
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    # Добавляем авторизацию по умолчанию ко всем эндпоинтам
    openapi_schema["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    app.openapi = lambda: app.openapi_schema