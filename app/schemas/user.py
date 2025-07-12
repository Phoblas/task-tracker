from pydantic import BaseModel, EmailStr, ConfigDict, field_validator

from app.schemas.task import TaskRead

# Базовая схема: общие поля, не передаётся напрямую
class UserBase(BaseModel):
    username: str
    email: EmailStr

    @field_validator("username")
    @classmethod
    def strip_username(cls, v: str) -> str:
        return v.strip()


# Схема для создания пользователя
class UserCreate(UserBase):
    pass


# Схема для чтения (ответа): добавляется id
class UserRead(UserBase):
    id: int
    tasks: list[TaskRead] = []  # 👈 Вложенные задачи

    model_config = ConfigDict(from_attributes=True)  # позволяет FastAPI автоматически преобразовывать SQLAlchemy-модель в Pydantic-схему
