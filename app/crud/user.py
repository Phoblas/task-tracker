from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

from app.core.security import hash_password, verify_password
from app.models.user import User
from app.schemas.auth import UserLogin, UserRegister
from app.schemas.user import UserCreate

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_in: UserCreate) -> User:
        user = User(**user_in.model_dump())
        self.session.add(user)
        try:
            await self.session.commit()
            await self.session.refresh(user)
            return user
        except IntegrityError:
            await self.session.rollback()
            raise ValueError("User with this email or username already exists")

    async def get_all(self) -> list[User]:
        result = await self.session.execute(select(User))
        return result.scalars().all()

    async def get_by_id(self, user_id: int) -> User | None:
        result = await self.session.execute(
            select(User)
            .options(joinedload(User.tasks))  # Она загружает связанные задачи (User.tasks) в один SQL-запрос
            .where(User.id == user_id)
        )
        return result.unique().scalar_one_or_none()

    async def delete(self, user_id: int) -> bool:
        result = await self.session.execute(delete(User).where(User.id == user_id))
        deleted = result.rowcount
        await self.session.commit()
        return bool(deleted)
    
    async def register(self, user_in: UserRegister) -> User:
        """
        Регистрирует нового пользователя (если email уникален).
        :raises ValueError: если пользователь с таким email уже есть
        """

        # Проверяем, есть ли уже пользователь с таким email
        result = await self.session.execute(select(User).where(User.email == user_in.email))
        existing = result.scalar_one_or_none()
        if existing:
            raise ValueError("User with this email already exists")

        # Создаём нового пользователя и хешируем пароль
        user = User(
            username=user_in.username,
            email=user_in.email,
            hashed_password=hash_password(user_in.password)
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
    
    async def authenticate_user(self, user_in: UserLogin) -> User:
        """
        Проверка email и пароля. Если всё ок — возвращает пользователя.
        :raises ValueError: если неверный email или пароль
        """
        
        result = await self.session.execute(
            select(User).where(User.email == user_in.email)
        )
        user = result.scalar_one_or_none()

        if not user or not verify_password(user_in.password, user.hashed_password):
            raise ValueError("Invalid credentials")

        return user