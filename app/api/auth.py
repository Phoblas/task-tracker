from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.deps import get_current_user
from app.crud.user import UserRepository
from app.db.deps import get_db

from app.schemas.auth import UserRegister, UserLogin
from app.schemas.token import Token
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token

from sqlalchemy import select

from app.schemas.user import UserRead

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", status_code=201)
async def register(user_in: UserRegister, db: AsyncSession = Depends(get_db)):
    """Регистрация пользователя"""

    repo = UserRepository(db)

    try:
        user = await repo.register(user_in)
        return {"message": f"User {user.email} created successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=Token)
async def login(user_in: UserLogin, db: AsyncSession = Depends(get_db)):
    """Логин и получение токена"""

    repo = UserRepository(db)
    try:
        user = await repo.authenticate_user(user_in)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    
    # Генерируем токен с user.id как subject (sub)
    token = create_access_token(data={"sub": str(user.id)})
    return Token(access_token=token)


@router.get("/me", response_model=UserRead)
async def read_current_user(current_user: User = Depends(get_current_user)):
    """
    Получение текущего авторизованного пользователя по токену.
    """
    return current_user