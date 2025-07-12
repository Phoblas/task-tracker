"""
Зависимости FastAPI для авторизованных роутов.
Содержит функцию get_current_user, которая извлекает пользователя из JWT-токена.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError

from app.core.security import decode_access_token  # Расшифровка токена
from app.db.deps import get_db                     # Асинхронная сессия БД
from app.crud.user import UserRepository           # Репозиторий пользователей
from app.models.user import User                   # SQLAlchemy модель

# Стандартный способ указать, где брать токен авторизации
# FastAPI будет искать заголовок Authorization: Bearer <token>
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login",  # важно: URL должен существовать!
    scheme_name="BearerAuth",  # <--- ВАЖНО: это имя будет использовано в OpenAPI
    description="Введите токен (без 'Bearer ') из /auth/login"
)


async def get_current_user(
    token: str = Depends(oauth2_scheme),            # Извлекаем токен из запроса
    db: AsyncSession = Depends(get_db),             # Получаем сессию БД
) -> User:
    print("TOKEN:", token)
    """
    Зависимость FastAPI, которая:
    1. Извлекает JWT из заголовка Authorization
    2. Расшифровывает токен и достаёт user_id из `sub`
    3. Загружает пользователя из БД
    4. Бросает исключение, если токен недействителен или пользователь не найден

    Returns:
        User: объект пользователя из базы данных
    """
    # Исключение, которое бросим, если токен невалиден
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Пытаемся расшифровать токен и извлечь user_id
    payload = decode_access_token(token)
    
    if payload is None or "sub" not in payload:
        raise credentials_exception

    try:
        user_id = int(payload["sub"])
    except (TypeError, ValueError):
        raise credentials_exception

    # Получаем пользователя из БД
    repo = UserRepository(db)
    user = await repo.get_by_id(user_id)
    if user is None:
        raise credentials_exception

    return user
