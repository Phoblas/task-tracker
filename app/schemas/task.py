"""
Pydantic-схемы (валидация и сериализация) для задач (Task).
"""

from pydantic import BaseModel, ConfigDict, field_validator

class TaskBase(BaseModel):
    '''Базовая схема, из которой будем наследовать другие схемы'''

    # Заголовок задачи: обязательное строковое поле (с автоматическим .strip())
    title: str
    
    # Описание задачи: опциональное поле, может быть None
    description: str | None = None

    @field_validator("title")
    @classmethod
    def strip_title(cls, v: str) -> str:
        return v.strip()


class TaskCreate(TaskBase):
    '''Схема, которую мы получаем от клиента при создании задачи'''
    pass  # user_id больше не требуется в теле запроса (берём из JWT)


class TaskRead(TaskBase):
    '''Схема ответа пользователю (например, из GET/POST)'''

    id: int  # уникальный ID задачи
    user_id: int  # ID пользователя-владельца

    # Позволяет Pydantic брать данные напрямую из SQLAlchemy-модели
    model_config = ConfigDict(from_attributes=True)