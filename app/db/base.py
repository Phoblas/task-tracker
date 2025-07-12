from app.db.base_class import Base

# Импортируем все модели, чтобы Alembic "увидел" их
from app.models.user import User  # noqa
from app.models.task import Task  # noqa
