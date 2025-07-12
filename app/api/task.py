from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.deps import get_db  # Зависимость, возвращающая асинхронную сессию
from app.schemas.task import TaskCreate, TaskRead  # Схемы запроса и ответа
from app.crud.task import TaskRepository  # Репозиторий для работы с задачами

from app.core.deps import get_current_user  # 🔐 наша зависимость авторизации
from app.models.user import User

# Создаём роутер FastAPI с префиксом /tasks
router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_in: TaskCreate,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),  # 🔐 только авторизованный пользователь
):
    """
    Создаёт новую задачу, связанную с текущим пользователем.
    """

    repo = TaskRepository(session)  # Создаём репозиторий с текущей сессией

    try:
        task = await repo.create(task_in, user_id=current_user.id)  # Вызываем метод создания
        return task  # Возвращаем задачу → автоматически преобразуется в TaskRead
    except ValueError as e:
        # Ошибка может быть, если user_id не существует
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[TaskRead])
async def get_tasks(
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Получение списка всех задач.
    """

    repo = TaskRepository(session)
    return await repo.get_all_by_user(user_id=current_user.id)


@router.get("/{task_id}", response_model=TaskRead)
async def get_task_by_id(
    task_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db)
):
    """
    Получение одной задачи по её ID.
    """

    repo = TaskRepository(session)
    task = await repo.get_by_id_by_user(task_id=task_id, user_id=current_user.id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Удаление задачи по её ID.
    """
    
    repo = TaskRepository(session)
    deleted = await repo.delete(task_id=task_id, user_id=current_user.id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
