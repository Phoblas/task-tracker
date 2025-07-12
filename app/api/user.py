from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import UserCreate, UserRead
from app.db.deps import get_db
from app.crud.user import UserRepository

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_in: UserCreate,
    session: AsyncSession = Depends(get_db)
):
    repo = UserRepository(session)
    try:
        user = await repo.create(user_in)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/", response_model=list[UserRead])
async def get_users(
    session: AsyncSession = Depends(get_db)
):
    repo = UserRepository(session)
    return await repo.get_all()


@router.get("/{user_id}", response_model=UserRead)
async def get_user_by_id(
    user_id: int,
    session: AsyncSession = Depends(get_db)
):
    repo = UserRepository(session)
    user = await repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    session: AsyncSession = Depends(get_db)
):
    repo = UserRepository(session)
    deleted = await repo.delete(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
