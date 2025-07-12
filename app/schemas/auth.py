from pydantic import BaseModel, EmailStr, Field

class UserRegister(BaseModel):
    """Схема для регистрации пользователя"""

    username: str = Field(..., min_length=3)
    email: EmailStr
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    """Схема для логина (email + password)"""

    email: EmailStr
    password: str
