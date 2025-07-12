from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError

from app.models.task import Task
from app.schemas.task import TaskCreate

class TaskRepository:
    """
    Репозиторий для работы с задачами (Task).
    Обёртка над SQLAlchemy для изоляции доступа к данным.
    """

    def __init__(self, session: AsyncSession):
        """
        Конструктор: принимает асинхронную сессию SQLAlchemy.
        Это позволяет использовать session в методах create, get и т.д.
        """

        self.session = session

    async def create(self, task_in: TaskCreate, user_id: int) -> Task:
        """
        Создание задачи, принадлежащей пользователю.
        :param task_in: данные задачи (без user_id)
        :param user_id: ID пользователя (из токена)
        :return: созданный объект Task
        """

        # Добавляем user_id вручную (в Pydantic-модели его нет)
        task_data = task_in.model_dump()
        task_data["user_id"] = user_id
        task = Task(**task_data)
        self.session.add(task)

        try:
            # Применяем изменения и обновляем объект task (чтобы получить id)
            await self.session.commit()
            await self.session.refresh(task)
            return task
        except IntegrityError:
            # Например, если user_id ссылается на несуществующего пользователя
            await self.session.rollback()
            raise ValueError("Invalid user_id or duplicate task")

    async def get_all_by_user(self, user_id: int) -> list[Task]:
        """
        Получение всех задач из базы.
        :return: список Task-объектов
        """

        result = await self.session.execute(
            select(Task).where(Task.user_id == user_id)
        )
        return result.scalars().all()  # scalars() → только объекты Task, без "сырых" строк

    async def get_by_id_by_user(self, task_id: int, user_id: int) -> Task | None:
        """
        Получение одной задачи по её ID.
        :param task_id: идентификатор задачи
        :param user_id: идентификатор пользователя
        :return: Task или None
        """

        result = await self.session.execute(
            select(Task).where(Task.id == task_id, Task.user_id == user_id)
        )
        return result.scalar_one_or_none()  # либо Task, либо None

    async def delete(self, task_id: int, user_id: int) -> bool:
        """
        Удаление задачи по ID.
        :param task_id: идентификатор задачи
        :param user_id: идентификатор пользователя
        :return: True если удалено, False если задача не найдена или чужая
        """
        result = await self.session.execute(
            delete(Task).where(Task.id == task_id, Task.user_id == user_id)
        )
        deleted = result.rowcount  # сколько строк было удалено
        await self.session.commit()
        return bool(deleted)
